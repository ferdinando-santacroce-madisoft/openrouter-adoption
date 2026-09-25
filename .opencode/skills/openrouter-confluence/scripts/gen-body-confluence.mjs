#!/usr/bin/env node
/**
 * gen-body-confluence.mjs — generatore dei body HTML per le pagine OpenRouter
 * della selezione software (workflow di pubblicazione governato dal manifest).
 *
 * Perche' esiste: `twg confluence content update` sovrascrive l'intero corpo
 * della pagina. Il body va quindi rigenerato dal sorgente markdown con le
 * stesse regole di trasformazione dichiarate nel manifest, ogni volta e in modo
 * riproducibile. Questo tool e' quella trasformazione, versionata.
 *
 * Regole implementate (dal manifest, sezione transformation_rules):
 *  - l'H1 iniziale e' rimosso: il titolo e' un attributo della pagina (title nel
 *    manifest), non un heading del body;
 *  - i link relativi sono risolti rispetto al file sorgente e riscritti con
 *    l'URL Confluence assoluto degli artifact pubblicati (content_id del
 *    manifest, anche per le pagine derivate da split_pages);
 *  - un link locale il cui target non ha una pagina Confluence diventa testo: se
 *    il manifest dichiara un titolo (vale anche per i documenti local_only) si usa
 *    quello, altrimenti il testo del link. Nel body pubblicato non restano mai
 *    href relativi;
 *  - le chiavi Jira diventano link stabili `.../browse/<KEY>` a ogni occorrenza,
 *    anche quando il sorgente le scrive in inline code (`PLAT-796`): uno span
 *    fatto di sole chiavi linkificabili viene srotolato. Restano codice i prefissi
 *    senza registro pubblicato (DEC-, ADR-, INIT-) e le chiavi gia' dentro un link;
 *  - gli anchor interni `#slug` diventano `#Heading-Git`, con l'algoritmo di
 *    Confluence: punteggiatura rimossa, spazi -> `-`, case conservato,
 *    caratteri non ASCII URL-encoded;
 *  - i link cross-pagina con fragment sono risolti sull'indice degli heading del
 *    file target (fragment non risolto -> link senza anchor, mai anchor rotti);
 *  - le sezioni fra `<!-- CONFLUENCE-LOCAL-ONLY -->` e `<!-- /CONFLUENCE-LOCAL-ONLY -->` non si
 *    pubblicano;
 *  - nessun `id` sugli heading: il formato di storage Confluence (HTML_PLUS) non
 *    li accetta;
 *  - il contenuto dentro <pre> e dentro <code> (tranne gli span di sole chiavi)
 *    non viene toccato.
 *
 * Uso:
 *   node gen-body-confluence.mjs --source contenuti/ssr-adozione-openrouter.md [--out file.html]
 *   node gen-body-confluence.mjs --all --out-dir /tmp/openrouter-bodies
 *   node gen-body-confluence.mjs --verify ssr_adozione_openrouter   # confronta gli href col snapshot pubblicato
 *
 * Opzioni:
 *   --docs-root <dir>   radice dei documenti (default: dedotta dal path dello script)
 *   --manifest <file>   manifest di migrazione (default: manifest-confluence.yaml)
 *   --snapshot-dir <d>  snapshot pubblicati (default: snapshots-confluence)
 *   --quiet             non stampare i warning (restano su stderr)
 *
 * Il tool NON pubblica nulla: produce body e verifica. Le scritture su Confluence
 * passano da `twg` e richiedono autorizzazione esplicita preventiva di Nando.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import MarkdownIt from 'markdown-it';
import { load as yamlLoad } from 'js-yaml';

const HERE = path.dirname(fileURLToPath(import.meta.url));
// <repo>/.opencode/skills/openrouter-confluence/scripts -> <repo>
const DEFAULT_DOCS_ROOT = path.resolve(HERE, '../../../../');
const DEFAULT_MANIFEST = 'manifest-confluence.yaml';
const DEFAULT_SNAPSHOT_DIR = 'snapshots-confluence';
const SPACE_BASE = 'https://madisoft.atlassian.net/wiki/spaces/TIS/pages';

const args = process.argv.slice(2);
function opt(name, def = null) {
  const i = args.indexOf(name);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : def;
}
function flag(name) { return args.includes(name); }

const DOCS_ROOT = path.resolve(opt('--docs-root', DEFAULT_DOCS_ROOT));
const MANIFEST = path.resolve(DOCS_ROOT, opt('--manifest', DEFAULT_MANIFEST));
const SNAPSHOT_DIR = path.resolve(DOCS_ROOT, opt('--snapshot-dir', DEFAULT_SNAPSHOT_DIR));
const QUIET = flag('--quiet');

if (!fs.existsSync(DOCS_ROOT)) {
  console.error(`docs-root non trovata: ${DOCS_ROOT}`);
  process.exit(2);
}
if (!fs.existsSync(MANIFEST)) {
  console.error(`manifest non trovato: ${MANIFEST}`);
  process.exit(2);
}

const manifest = yamlLoad(fs.readFileSync(MANIFEST, 'utf8'));
const artifacts = Array.isArray(manifest?.artifacts) ? manifest.artifacts : [];

/** source (relativo alla docs root) -> URL Confluence assoluto della pagina pubblicata */
const PAGES = {};
/** source (relativo alla docs root) -> titolo di pagina, anche per i target non ancora pubblicati */
const TITLES = {};
/** target_key -> artifact, per la modalita' --verify */
const BY_KEY = {};
for (const a of artifacts) {
  const src = (a.source || '').replace(/^\.\//, '');
  if (src && a.content_id) PAGES[src] = `${SPACE_BASE}/${a.content_id}`;
  // split_pages (es. il Piano): il sorgente cita la prima pagina del gruppo con un content_id
  if (src && !PAGES[src] && Array.isArray(a.targets)) {
    const main = a.targets.find((t) => t && t.content_id);
    if (main) PAGES[src] = `${SPACE_BASE}/${main.content_id}`;
  }
  if (src && a.title) TITLES[src] = String(a.title).trim();
  for (const t of (Array.isArray(a.targets) ? a.targets : [])) {
    if (t && t.target_key) BY_KEY[t.target_key] = { ...t, source: a.source, disposition: a.disposition };
  }
  if (a.target_key) BY_KEY[a.target_key] = a;
}

const md = new MarkdownIt({ html: false, linkify: true, breaks: false, typographer: false });

function stripInline(s) {
  return s.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_`]/g, '').trim();
}

/** slug in stile GitHub, usato per interpretare gli anchor `#slug` nei sorgenti */
function gitSlug(text) {
  return stripInline(text).toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu, '').trim().replace(/\s+/g, '-');
}

/** slug in stile Confluence, usato negli href pubblicati */
function confSlug(text) {
  const s = stripInline(text).replace(/[^\p{L}\p{N}\s_-]/gu, '').trim().replace(/\s+/g, '-');
  return encodeURIComponent(s);
}

const headingCache = new Map();
function headingsOf(relPath) {
  if (headingCache.has(relPath)) return headingCache.get(relPath);
  const map = { git: new Map(), conf: new Set() };
  const abs = path.join(DOCS_ROOT, relPath);
  if (fs.existsSync(abs)) {
    let inFence = false;
    for (const line of fs.readFileSync(abs, 'utf8').split('\n')) {
      if (/^\s*```/.test(line)) { inFence = !inFence; continue; }
      if (inFence) continue;
      const m = line.match(/^(#{1,6})\s+(.+?)\s*$/);
      if (m) { map.git.set(gitSlug(m[2]), confSlug(m[2])); map.conf.add(confSlug(m[2])); }
    }
  }
  headingCache.set(relPath, map);
  return map;
}

/**
 * Risolve un href locale rispetto al file sorgente e restituisce il path relativo alla docs root.
 * null se l'href non e' locale (http, mailto, assoluto, anchor).
 */
function localRelOf(href, sourceRel) {
  if (/^(https?:|mailto:|\/|#)/i.test(href)) return null;
  let decoded = href;
  try { decoded = decodeURIComponent(href); } catch { /* keep */ }
  const [p] = decoded.split('#');
  if (!p) return null;
  return path.posix.normalize(path.posix.join(path.posix.dirname(sourceRel), p)).replace(/^\.\//, '');
}

/**
 * Chiave Jira "nuda": mai preceduta o seguita da lettera, cifra, "_" o "-".
 * Il lookbehind/esclusione evita di linkificare `INIT-HER-01` (codice filo) e
 * `ADR-20260805-01` (decisione architetturale).
 */
const KEY_RE = /(?<![\p{L}\p{N}_-])([A-Z][A-Z0-9]{1,9}-[0-9]+)(?![\p{L}\p{N}_-])/gu;
const KEY_EXCLUDE = /^(DEC|ADR|INIT)-/;
/** separatori ammessi dentro uno span di sole chiavi Jira */
const KEY_ONLY_REST = /^[\s,;/·+–—]*$/u;

function linkifyKeys(segment) {
  const chunks = segment.split(/(<a\b[^>]*>[\s\S]*?<\/a>)/g);
  for (let i = 0; i < chunks.length; i++) {
    if (i % 2 === 1) continue;
    chunks[i] = chunks[i].replace(/(<[^>]+>|[^<]+)/g, (piece) => {
      if (piece.startsWith('<')) return piece;
      return piece.replace(KEY_RE, (all, key) =>
        KEY_EXCLUDE.test(key) ? all : `<a href="https://madisoft.atlassian.net/browse/${key}">${key}</a>`);
    });
  }
  return chunks.join('');
}

/** Decodifica le entita' che markdown-it produce nel testo. */
function decodeEntities(s) {
  return String(s)
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&amp;/g, '&');
}

function stripTags(s) {
  return String(s).replace(/<[^>]*>/g, '');
}

/** Testo piano di un frammento HTML. */
function plainTextOf(html) {
  return stripTags(decodeEntities(html));
}

/**
 * Ritaglio del sorgente per una pagina derivata (disposition split_pages).
 * slice = { heading, part } con part "before" | "from", riferito a una intestazione.
 */
function sliceMarkdown(src, slice) {
  if (!slice) return src;
  const lines = src.split('\n');
  const idx = lines.findIndex(
    (l) => /^#{1,6}\s+/.test(l) && stripInline(l.replace(/^#{1,6}\s+/, '')) === slice.heading,
  );
  if (idx < 0) return null;
  return (slice.part === 'from' ? lines.slice(idx) : lines.slice(0, idx)).join('\n');
}

/** regola di split dichiarata su un target del manifest (o null) */
const sliceOf = (a) => (a && a.split_heading ? { heading: String(a.split_heading), part: String(a.split_part || 'before') } : null);

function generate(sourceRel, slice = null) {
  const warnings = [];
  const src = fs.readFileSync(path.join(DOCS_ROOT, sourceRel), 'utf8');
  const body0 = sliceMarkdown(src, slice);
  if (body0 === null) {
    warnings.push(`intestazione non trovata per lo split: "${slice.heading}" (${sourceRel})`);
    return { html: '', warnings };
  }
  // le sezioni marcate CONFLUENCE-LOCAL-ONLY non si pubblicano (transformation_rules.markdown)
  let clean = body0.replace(/<!--\s*CONFLUENCE-LOCAL-ONLY[\s\S]*?<!--\s*\/CONFLUENCE-LOCAL-ONLY\s*-->/g, '');
  if (clean.includes('CONFLUENCE-LOCAL-ONLY')) {
    warnings.push(`marker CONFLUENCE-LOCAL-ONLY non chiuso: la sezione residua viene esclusa (${sourceRel})`);
    clean = clean.replace(/<!--\s*CONFLUENCE-LOCAL-ONLY[\s\S]*$/, '');
  }
  const text = clean.replace(/^#\s+.*\n+/, '');
  const html = md.render(text);

  // --- protezione del codice -------------------------------------------------
  // Il codice non va toccato (fence e inline), con una eccezione: uno span inline
  // fatto di sole chiavi Jira viene srotolato, cosi' le chiavi ricevono il link.
  const chunks = [];
  const protect = (raw) => { chunks.push(raw); return `\u0000${chunks.length - 1}\u0000`; };
  const PH_RE = /\u0000(\d+)\u0000/g;
  /**
   * Uno span inline e' una "lista di chiavi" se contiene solo chiavi Jira e
   * separatori e ogni chiave e' linkificabile (DEC-/ADR-/INIT- restano codice,
   * perche' non hanno un registro pubblicato a cui puntare).
   */
  const keyListOf = (plain) => {
    const keys = [...plain.matchAll(KEY_RE)].map((m) => m[1]);
    if (!keys.length) return false;
    if (!KEY_ONLY_REST.test(plain.replace(KEY_RE, ''))) return false;
    return keys.every((k) => !KEY_EXCLUDE.test(k));
  };

  let body = html.replace(/<pre[\s\S]*?<\/pre>/g, (m) => protect(m));
  body = body.replace(/<code>([\s\S]*?)<\/code>/g, (all, inner) => {
    const plain = plainTextOf(inner).replace(/\s+/g, ' ').trim();
    return keyListOf(plain) ? plain : protect(all);
  });

  /** testo visibile di un frammento, con il codice protetto ripristinato come testo */
  const visibleText = (fragment) => plainTextOf(fragment)
    .replace(PH_RE, (_, i) => ` ${plainTextOf(chunks[Number(i)])} `)
    .replace(/\s+/g, ' ')
    .trim();

  const rewriteHref = (raw) => {
    let href = raw.replace(/&amp;/g, '&');
    if (/^(https?:|mailto:|\/)/i.test(href)) return raw;
    let decoded = href;
    try { decoded = decodeURIComponent(href); } catch { /* keep */ }

    if (decoded.startsWith('#')) {
      const conf = headingsOf(sourceRel).git.get(gitSlug(decoded.slice(1)));
      if (conf) return '#' + conf;
      warnings.push(`anchor interno non risolto: ${decoded} (${sourceRel})`);
      return raw;
    }

    const [p, frag] = decoded.split('#');
    if (!p) return raw;
    const rel = path.posix.normalize(path.posix.join(path.posix.dirname(sourceRel), p)).replace(/^\.\//, '');
    const url = PAGES[rel];
    if (!url) return raw; // target senza pagina Confluence: lo gestisce il passo 1
    if (!frag) return url;
    const tm = headingsOf(rel);
    const conf = tm.git.get(gitSlug(frag)) || (tm.conf.has(encodeURIComponent(frag)) ? encodeURIComponent(frag) : null);
    if (conf) return url + '#' + conf;
    warnings.push(`fragment cross-pagina non risolto: ${rel}#${frag} (${sourceRel})`);
    return url;
  };

  // 1. link locali senza pagina Confluence: diventano testo (titolo del target), mai href relativi
  body = body.replace(/<a\s+[^>]*href="([^"]*)"[^>]*>([\s\S]*?)<\/a>/g, (all, h, label) => {
    const rel = localRelOf(decodeEntities(h), sourceRel);
    if (!rel || PAGES[rel]) return all;
    const title = TITLES[rel] || visibleText(label) || path.posix.basename(rel);
    warnings.push(`target senza pagina Confluence, reso come testo: ${rel} -> "${title}" (${sourceRel})`);
    return title;
  });
  // 2. href rimasti: pagine pubblicate (URL Confluence), anchor interni, fragment
  // un solo livello di escaping: markdown-it ha gia' convertito "&" in "&amp;"
  const escapeHref = (u) => u.replace(/&amp;/g, '&').replace(/&/g, '&amp;');
  body = body.replace(/href="([^"]*)"/g, (all, h) => {
    const r = rewriteHref(h);
    return `href="${escapeHref(typeof r === 'string' ? r : h)}"`;
  });
  // 3. chiavi Jira: ogni occorrenza diventa un link stabile
  body = linkifyKeys(body);
  // 4. ripristino del codice protetto
  body = body.replace(PH_RE, (_, i) => chunks[Number(i)]);

  return { html: body, warnings };
}

function hrefsOf(html) {
  return [...new Set([...html.matchAll(/href="([^"]*)"/g)].map((m) => m[1].replace(/&amp;/g, '&')))].sort();
}

/** artifact con sorgente markdown esistente, espansi in una pagina per target */
const jobs = [];
for (const a of artifacts) {
  if (!a.source || !String(a.source).endsWith('.md') || !fs.existsSync(path.join(DOCS_ROOT, a.source))) continue;
  if (a.disposition === 'publish_page') {
    jobs.push({ key: a.target_key || path.basename(a.source, '.md'), source: a.source, slice: null, artifact: a });
  } else if (a.disposition === 'split_pages') {
    for (const t of (Array.isArray(a.targets) ? a.targets : [])) {
      jobs.push({ key: t.target_key, source: a.source, slice: sliceOf(t), artifact: { ...t, source: a.source } });
    }
  }
}

let exitCode = 0;
const emit = (msg) => { if (!QUIET) console.error(msg); };

// --- modalita' --verify ------------------------------------------------------
if (flag('--verify')) {
  const key = opt('--verify');
  if (!key) { console.error('--verify richiede un target_key'); process.exit(2); }
  const a = BY_KEY[key];
  if (!a) { console.error(`target_key non nel manifest: ${key}`); process.exit(2); }
  const snap = path.join(SNAPSHOT_DIR, path.basename(a.published_body_path || `${key}.html`));
  if (!fs.existsSync(snap)) { console.error(`snapshot non trovato: ${snap}`); process.exit(2); }
  const { html, warnings } = generate(a.source, sliceOf(a));
  warnings.forEach((w) => emit('WARN ' + w));
  const gen = hrefsOf(html);
  const pub = hrefsOf(fs.readFileSync(snap, 'utf8'));
  const onlyPub = pub.filter((x) => !gen.includes(x));
  const onlyGen = gen.filter((x) => !pub.includes(x));
  console.log(`# verify ${key} (${a.source})`);
  if (!onlyPub.length && !onlyGen.length) {
    console.log('href identici allo snapshot pubblicato');
  } else {
    onlyPub.forEach((x) => console.log(`  SOLO nello snapshot (link esterno da recepire): ${x}`));
    onlyGen.forEach((x) => console.log(`  SOLO nel generato (link nuovo dal sorgente): ${x}`));
    if (onlyPub.length) exitCode = 1;
  }
  process.exit(exitCode);
}

// --- modalita' --all o --source ---------------------------------------------
if (flag('--all')) {
  const outDir = opt('--out-dir', '/tmp/openrouter-bodies');
  fs.mkdirSync(outDir, { recursive: true });
  let n = 0;
  for (const job of jobs) {
    const key = job.key;
    const { html, warnings } = generate(job.source, job.slice);
    const out = path.join(outDir, `${key}.html`);
    fs.writeFileSync(out, html);
    warnings.forEach((w) => emit('WARN ' + w));
    console.log(`${key}\t${out}\t${html.length} bytes`);
    n++;
  }
  console.log(`generati ${n} body in ${outDir}`);
  process.exit(exitCode);
}

const source = opt('--source');
if (!source) {
  console.error('serve --source <file.md>, oppure --all, oppure --verify <target_key>');
  process.exit(2);
}
const { html, warnings } = generate(source);
warnings.forEach((w) => emit('WARN ' + w));
const out = opt('--out');
if (out) { fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true }); fs.writeFileSync(out, html); console.log(`${out}\t${html.length} bytes`); }
else process.stdout.write(html);
process.exit(exitCode);
