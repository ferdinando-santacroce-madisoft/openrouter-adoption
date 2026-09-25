#!/usr/bin/env node
/**
 * gen-md-gdrive.mjs — prepara i markdown da caricare sui Google Docs
 * (workflow governato dal manifest-gdrive.yaml).
 *
 * Perche' esiste: l'aggiornamento di un Google Doc da markdown sostituisce
 * l'intero corpo del documento. Il markdown va quindi preparato in modo
 * riproducibile, con le stesse regole di trasformazione dichiarate nel manifest.
 *
 * Regole implementate:
 *  - l'H1 iniziale e' rimosso: il titolo e' il nome del file Google Doc, non un
 *    heading del corpo;
 *  - le sezioni fra `CONFLUENCE-LOCAL-ONLY` e `/CONFLUENCE-LOCAL-ONLY` non si
 *    pubblicano (stessa convenzione del target Confluence);
 *  - i link relativi fra i documenti sono riscritti con l'URL Google Docs
 *    assoluto registrato nel manifest (file_id); se il target non e' nel
 *    manifest il link resta invariato con un warning;
 *  - i link esterni e assoluti non sono toccati.
 *
 * Uso:
 *   node gen-md-gdrive.mjs --source contenuti/ssr-adozione-openrouter.md [--out file.md]
 *   node gen-md-gdrive.mjs --all --out-dir /tmp/openrouter-gdrive
 *   node gen-md-gdrive.mjs --verify ssr_adozione_openrouter
 *
 * Il tool NON scrive su Google Drive: produce markdown e verifica. Le scritture
 * passano da `gws-account` e richiedono autorizzazione esplicita di Nando.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { load as yamlLoad } from 'js-yaml';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_DOCS_ROOT = path.resolve(HERE, '../../../../');
const DEFAULT_MANIFEST = 'manifest-gdrive.yaml';
const DEFAULT_SNAPSHOT_DIR = 'snapshots-gdrive';
const DISPOSITIONS_PUSHABLE = new Set(['push', 'publish_page']);

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

if (!fs.existsSync(DOCS_ROOT)) { console.error(`docs-root non trovata: ${DOCS_ROOT}`); process.exit(2); }
if (!fs.existsSync(MANIFEST)) { console.error(`manifest non trovato: ${MANIFEST}`); process.exit(2); }

const manifest = yamlLoad(fs.readFileSync(MANIFEST, 'utf8'));
const artifacts = Array.isArray(manifest?.artifacts) ? manifest.artifacts : [];

const DOC_URL = (fileId) => `https://docs.google.com/document/d/${fileId}/edit`;

/** source (relativo alla docs root) -> { url, title } della pagina Google Docs */
const PAGES = {};
const BY_KEY = {};
for (const a of artifacts) {
  const src = (a.source || '').replace(/^\.\//, '');
  const fileId = a.file_id || a.targets?.[0]?.file_id;
  if (src && fileId) PAGES[src] = { url: a.url || DOC_URL(fileId), title: a.title || path.posix.basename(src, '.md') };
  if (a.target_key) BY_KEY[a.target_key] = a;
}

function stripInline(s) {
  return s.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_`]/g, '').trim();
}

/**
 * Risolve un href relativo rispetto al file sorgente e restituisce il path
 * relativo alla docs root. null se l'href non e' locale.
 */
function localRelOf(href, sourceRel) {
  if (/^(https?:|mailto:|\/|#)/i.test(href)) return null;
  let decoded = href;
  try { decoded = decodeURIComponent(href); } catch { /* keep */ }
  const [p] = decoded.split('#');
  if (!p) return null;
  return path.posix.normalize(path.posix.join(path.posix.dirname(sourceRel), p)).replace(/^\.\//, '');
}

function generate(sourceRel) {
  const warnings = [];
  const src = fs.readFileSync(path.join(DOCS_ROOT, sourceRel), 'utf8');

  // sezioni CONFLUENCE-LOCAL-ONLY non pubblicate
  let clean = src.replace(/<!--\s*CONFLUENCE-LOCAL-ONLY[\s\S]*?<!--\s*\/CONFLUENCE-LOCAL-ONLY\s*-->/g, '');
  if (clean.includes('CONFLUENCE-LOCAL-ONLY')) {
    warnings.push(`marker CONFLUENCE-LOCAL-ONLY non chiuso: la sezione residua viene esclusa (${sourceRel})`);
    clean = clean.replace(/<!--\s*CONFLUENCE-LOCAL-ONLY[\s\S]*$/, '');
  }

  // rimuove l'H1 iniziale (il titolo e' il nome del Google Doc)
  clean = clean.replace(/^\s*#\s+.*\n+/, '');

  // riscrive i link relativi fra documenti con l'URL Google Docs assoluto
  clean = clean.replace(/\[([^\]]*)\]\(([^)\s]+)(\s+"[^"]*")?\)/g, (all, label, href, title) => {
    const rel = localRelOf(href, sourceRel);
    if (!rel) return all;
    const page = PAGES[rel];
    if (!page) {
      warnings.push(`target senza Google Doc nel manifest, link invariato: ${rel} (${sourceRel})`);
      return all;
    }
    return `[${label}](${page.url}${title || ''})`;
  });

  return { markdown: clean, warnings };
}

function hrefsOf(md) {
  return [...new Set([...md.matchAll(/\]\(([^)\s]+)/g)].map((m) => m[1]))].sort();
}

let exitCode = 0;
const emit = (msg) => { if (!QUIET) console.error(msg); };

// --- modalita' --verify ------------------------------------------------------
if (flag('--verify')) {
  const key = opt('--verify');
  if (!key) { console.error('--verify richiede un target_key'); process.exit(2); }
  const a = BY_KEY[key];
  if (!a) { console.error(`target_key non nel manifest: ${key}`); process.exit(2); }
  const snap = path.join(SNAPSHOT_DIR, `${key}.md`);
  if (!fs.existsSync(snap)) { console.error(`baseline non trovata: ${snap}`); process.exit(2); }
  const { markdown, warnings } = generate(a.source);
  warnings.forEach((w) => emit('WARN ' + w));
  const gen = hrefsOf(markdown);
  const base = hrefsOf(fs.readFileSync(snap, 'utf8'));
  const onlyBase = base.filter((x) => !gen.includes(x));
  const onlyGen = gen.filter((x) => !base.includes(x));
  console.log(`# verify ${key} (${a.source})`);
  if (!onlyBase.length && !onlyGen.length) {
    console.log('href identici alla baseline esportata dal Google Doc');
  } else {
    onlyBase.forEach((x) => console.log(`  SOLO nella baseline (link esterno da recepire): ${x}`));
    onlyGen.forEach((x) => console.log(`  SOLO nel generato (link nuovo dal sorgente): ${x}`));
    if (onlyBase.length) exitCode = 1;
  }
  process.exit(exitCode);
}

// --- modalita' --all o --source ---------------------------------------------
const jobs = artifacts.filter((a) =>
  a.source && String(a.source).endsWith('.md') &&
  DISPOSITIONS_PUSHABLE.has(a.disposition) &&
  fs.existsSync(path.join(DOCS_ROOT, a.source)));

if (flag('--all')) {
  const outDir = opt('--out-dir', '/tmp/openrouter-gdrive');
  fs.mkdirSync(outDir, { recursive: true });
  let n = 0;
  for (const a of jobs) {
    const key = a.target_key || path.posix.basename(a.source, '.md');
    const { markdown, warnings } = generate(a.source);
    const out = path.join(outDir, `${key}.md`);
    fs.writeFileSync(out, markdown);
    warnings.forEach((w) => emit('WARN ' + w));
    console.log(`${key}\t${out}\t${markdown.length} bytes`);
    n++;
  }
  console.log(`generati ${n} markdown in ${outDir}`);
  process.exit(exitCode);
}

const source = opt('--source');
if (!source) {
  console.error('serve --source <file.md>, oppure --all, oppure --verify <target_key>');
  process.exit(2);
}
const { markdown, warnings } = generate(source);
warnings.forEach((w) => emit('WARN ' + w));
const out = opt('--out');
if (out) { fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true }); fs.writeFileSync(out, markdown); console.log(`${out}\t${markdown.length} bytes`); }
else process.stdout.write(markdown);
process.exit(exitCode);
