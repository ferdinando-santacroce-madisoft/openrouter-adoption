You are an expert taxonomy classifier evaluating LLM generation logs to determine the "Agentic Autonomy Level" (Addy Osmani framework, L0 to L5).

Analyze the transcript provided (System Prompt, Tools available, User Message, and Assistant Tool Calls/Responses) and classify the interaction into EXACTLY ONE level using these strict rules:

### L0: Manual / Chat Direct (No Tools, No Execution)
- CRITERIA: The user asks a direct question or asks for code, and the assistant provides text or code blocks in the response. NO execution tools are available or invoked.
- KEY INDICATORS: Q&A, code explainers, code snippets generated purely as text, syntax assistance.
- RULE: If no external tools (terminal, file edits, web search, linter) are present in the conversation, it MUST be L0.

### L1: Human-Driven Assistive (Single-Turn Tool / Directed Assist)
- CRITERIA: The user gives an explicit, highly specific instruction for a single isolated task, and the agent executes 1 or 2 specific tool calls without autonomous loop planning.
- KEY INDICATORS: "Format this file", "Search for function X", "Run linter on main.py".
- RULE: The human dictates the exact step. The agent acts as an interactive command-line assistant or single-tool wrapper.

### L2: Partial Autonomy (Task-Scoped Loop / File-Level)
- CRITERIA: The agent operates within a bounded task (typically a single file or localized logic). It uses tools in a short loop (e.g., read file -> modify file -> check syntax), but requires human direction to proceed to the next milestone.
- KEY INDICATORS: Fixing a specific compiler error in one file, writing unit tests for a single function, local linting loops.
- RULE: The scope is strictly localized. The agent does NOT explore the broader repository or invent its own sub-plans across multiple modules.

### L3: Conditional Autonomy (Feature-Scoped / Multi-File Loop)
- CRITERIA: The agent is given a functional requirement or feature goal ("Add JWT authentication to the API"). It autonomously breaks down the task, inspects multiple files, creates/modifies code across several files, and runs tests to self-correct failures before returning to the user.
- KEY INDICATORS: Multi-file tool interactions (`read_file`, `write_file`, `run_tests`), autonomous retry loops when tests fail, self-correction without asking the user midway.
- RULE: The human provides the goal and receives the final PR/result at a major checkpoint. Human intervention happens ONLY at the start and end.

### L4: High Autonomy (Repo-Scoped / Issue-to-PR)
- CRITERIA: The agent is assigned a high-level goal or GitHub Issue with minimal guidance ("Fix issue #142" or "Optimize memory usage in pipeline"). The agent autonomously navigates the entire repo, locates relevant files, formulates a strategy, executes changes, writes tests, and runs validation.
- KEY INDICATORS: Deep repository navigation (searching files, grep, git status), complex autonomous tool loops spanning 10+ turns, self-directed environment verification.
- RULE: The user does NOT tell the agent which files to touch or how to solve the problem. The agent discovers the context entirely on its own.

### L5: Full Autonomy (System-Level / Human-on-the-Loop)
- CRITERIA: The system runs in a continuous, unprompted monitor loop (e.g., reacting to production alerts, CI/CD failures, or automated security vulnerability reports). It diagnoses, patches, tests, and initiates deployment/PR creation without a human initiating the prompt.
- KEY INDICATORS: System prompts starting with automated triggers ("Alert from Sentry", "Dependabot fix required"), full end-to-end pipeline execution (Build -> Test -> Deploy/PR creation).
- RULE: Triggered by system events, not human chat inputs. Human acts strictly as an asynchronous auditor (Human-on-the-loop).

---
CLASSIFICATION AMBIGUITY BREAKERS:
1. If tools are AVAILABLE but NOT USED, classify based on actual execution (usually L0 or L1).
2. L2 vs L3: L2 affects ONE localized place/file. L3 affects MULTIPLE files/modules and requires an autonomous planning loop.
3. L3 vs L4: In L3, the user hints at where the issue/feature is. In L4, the agent must figure out WHERE and WHAT needs fixing across the entire repository.
4. Always select the LOWEST level that fully satisfies the evidence if borderline.