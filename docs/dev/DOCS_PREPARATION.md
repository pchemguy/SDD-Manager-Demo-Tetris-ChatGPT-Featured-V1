# Main documentation preparation record

## Current control

- Mode: autodoc/onepass, selected by the user's project request on 2026-10-29.
- Scope: classic browser-based Tetris; Electron delivery remains future scope.
- Approval basis: PROJECT was explicitly approved on 2026-10-29. ARCHITECTURE through TASKS checkpoints are preapproved by autodoc selection. Product clarifications do not approve an unseen document.
- Tracking: enabled for preparation and implementation by root AGENTS.md. All nine standard issues and their sdd-docs-main milestone associations were verified before repository writes.
- Publication: push and exact-ref readback after every owned commit.
- Next boundary: continue through DOCS-008 and stop before DOCS-009 package QC or implementation.
- Reporting: concise Standard reporting; consequential choices and checkpoints remain visible.

## Scope and decisions

The user requested a browser classic Tetris game and future platform reuse, then confirmed:

- Modern extensions are outside scope.
- Share TypeScript game logic and UI; separate browser integration for future Electron reuse. Electron delivery is outside the current scope.
- Lock when a gravity or soft-drop attempt cannot move a piece downward; there is no separate lock timer.

The approved PROJECT also establishes: 10 by 20 board, seven tetrominoes, independent random selection, rotation without wall kicks, next-piece preview, scoring/levels, pause/restart and game over. These particulars are accepted through approval of the published brief. Precise contracts belong in SPEC after brief approval.

## Decisions and document evidence

| Task | Evidence and decision basis |
| --- | --- |
| DOCS-001 | All four root files retained byte for byte against initial commit 1d93908b57fcf935f09a5b7446c090b9fdf54f5b; none copied. Manual provenance scaffold and merge verified as below. This commit includes the checked initialization task and HANDOFF; its push/readback and issue closure follow. |
| DOCS-002 | PROJECT approved by the user's "k" on 2026-10-29, referring to published proposal 95e60a638d1dbd33de68b52cc7286d5409f7342f. Accepted SHA-256 `87f006ee0894cc98cfee305aa9e926231c0a9aab79211afb46d18e3501dd1bcf`; document bytes unchanged. |
| DOCS-003 | Autodoc preapproval applies. [ARCHITECTURE](ARCHITECTURE.md) SHA-256 `b8073650a2f260a759f8d7b2c67949458ab41b515a91790c2ced0e2bc6a4743d`; author scope/consistency review and Markdown/local-link checks passed. |
| DOCS-004 | Autodoc preapproval applies. [DECOMPOSITION](DECOMPOSITION.md) SHA-256 `c4539e9930a0c626e36abfc9be1ca5a40bd883e8aacd76ea92b3e46fb51fe5b6`; author scope/consistency review and Markdown/local-link checks passed. |
| DOCS-005 | Pending under autodoc preapproval; required technical QC remains applicable. |
| DOCS-006 | Pending under autodoc preapproval; required technical QC remains applicable. |
| DOCS-007 | Pending under autodoc preapproval; required technical QC remains applicable. |
| DOCS-008 | Pending under autodoc preapproval; required technical QC remains applicable. |
| DOCS-009 | Not selected; autodoc stops before package QC. |

## Initialization

- Root files preserved: AI_DISCLOSURE.md, SDD-MANAGER.md, AGENTS.md and SKILL_DISCOVERY_PROTOCOL.md. All existed; no mixed-presence continuation pause applies.
- Preservation checks: direct byte comparisons against the initial committed versions passed for all four files.
- Manual provenance: enabled by default; no transcript created. Both scaffold files match the running package assets.
- Provenance parent: main at 1d93908b57fcf935f09a5b7446c090b9fdf54f5b.
- Provenance seed: c7fce835bdf1477968dcaa52cb4f891fafef96a6, on retained design-docs/ai-logs.
- Verified published two-parent merge into main: a60bc0644a4cae7ffa736f1433c154c8cf0f3a0f.
- Preparation branch: design-docs/main, created from main at a60bc0644a4cae7ffa736f1433c154c8cf0f3a0f; integration target remains main.
- Discovery: repository standalone Technical Writing Assistant and SDD Manager v0.15.4 entries inspected and reported in chat. Actual host is Linux; Windows-only shell rules do not apply here.
- Credential handling: repository token excluded by *.tkn and verified untracked. No credential value belongs in development evidence.
- Reset: none; one documentation pass.

## Pending transitions

Publish/read back this DOCS-004 completion and close/read back issue #4 before dependent preparation. Then continue under existing autodoc preapproval, stopping after DOCS-008. DOCS-009, documentation integration and implementation remain outside that stop.
