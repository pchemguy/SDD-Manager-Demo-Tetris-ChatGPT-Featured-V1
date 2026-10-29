# Main documentation preparation record

## Current control

- Mode: autodoc/onepass, selected by the user's project request on 2026-10-29.
- Scope: classic browser-based Tetris; Electron delivery remains future scope.
- Approval basis: PROJECT requires human approval. ARCHITECTURE through TASKS checkpoints are preapproved by autodoc selection. Product clarifications do not approve an unseen document.
- Tracking: enabled for preparation and implementation by root AGENTS.md. All nine standard issues and their sdd-docs-main milestone associations were verified before repository writes.
- Publication: push and exact-ref readback after every owned commit.
- Next boundary: publish PROJECT for human review, then stop. After approval, continue through DOCS-008 and stop before DOCS-009 package QC or implementation.
- Reporting: concise Standard reporting; consequential choices and checkpoints remain visible.

## Scope and decisions

The user requested a browser classic Tetris game and future platform reuse, then confirmed:

- Modern extensions are outside scope.
- Share TypeScript game logic and UI; separate browser integration for future Electron reuse. Electron delivery is outside the current scope.
- Lock when a gravity or soft-drop attempt cannot move a piece downward; there is no separate lock timer.

The remaining baseline particulars will be presented in PROJECT as proposals: 10 by 20 board, seven tetrominoes, independent random selection, rotation without wall kicks, next-piece preview, scoring/levels, pause/restart and game over. These have not been separately confirmed by the human. Precise contracts belong in SPEC after brief approval.

## Decisions and document evidence

| Task | Evidence and decision basis |
| --- | --- |
| DOCS-001 | All four root files retained byte for byte against initial commit 1d93908b57fcf935f09a5b7446c090b9fdf54f5b; none copied. Manual provenance scaffold and merge verified as below. This commit includes the checked initialization task and HANDOFF; its push/readback and issue closure follow. |
| DOCS-002 | PROJECT not yet authored or approved. |
| DOCS-003 through DOCS-008 | Pending; document checkpoints preapproved by autodoc selection, dependent on PROJECT approval and required technical QC. |
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

Publish/read back this initialization commit, then close/read back DOCS-001. Prepare and publish PROJECT as an unapproved proposal. Later documentation integration and milestone closure require DOCS-009 and remain outside the current autodoc stop.
