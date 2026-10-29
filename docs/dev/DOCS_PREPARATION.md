# Main documentation preparation record

## Current control

- Mode: autodoc/onepass, selected by the user's project request on 2026-10-29.
- Scope: classic browser-based Tetris; Electron delivery remains future scope.
- Approval basis: PROJECT was explicitly approved on 2026-10-29. ARCHITECTURE through TASKS checkpoints are preapproved by autodoc selection. Product clarifications do not approve an unseen document.
- Tracking: enabled for preparation and implementation by root AGENTS.md. All nine standard issues and their sdd-docs-main milestone associations were verified before repository writes.
- Publication: push and exact-ref readback after every owned commit.
- Next boundary: package QC and verified preparation integration, then the full T-001 through T-012 range and post-phase v0.1.0 release, authorized by "Do QC and full implement" on 2026-10-29.
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
| DOCS-005 | Autodoc preapproval applies. [SPEC](SPEC.md) SHA-256 `91dc68e3dc49391df3559901bb4b922aa8c2aeb1c6ed421fd6f1b5e4309ec9f0`; author scope/consistency review and Markdown/local-link checks passed. Required technical gate: [SPEC-REVIEW-REPORT.md](SPEC-REVIEW-REPORT.md), Ready for its stated scope. |
| DOCS-006 | Autodoc preapproval applies. [PLAN](PLAN.md) SHA-256 `cb466bf4148d5a654766b8288f6462e5d1185c55b0ea21529822f517fe11b17d`; author scope/consistency review and Markdown/local-link checks passed. Required technical gate: [PLAN-REVIEW-REPORT.md](PLAN-REVIEW-REPORT.md), Ready for its stated scope. |
| DOCS-007 | Autodoc preapproval applies. [layout](layout.md) SHA-256 `c4ca6fd5077ec0a8ce6a552968de21946b208b4bb5410bb0f5e43e9ca9340481`; author scope/consistency review and Markdown/local-link checks passed. Required technical gate: [PLAN-REVIEW-REPORT.md](PLAN-REVIEW-REPORT.md), Ready for its stated scope. |
| DOCS-008 | Autodoc preapproval applies. [TASKS](TASKS.md) SHA-256 `654cbbf1260933d4f8acc684c9fb48fb76b6ebf2e625e5d9538fd261d6b38b02`; author scope/consistency review and Markdown/local-link checks passed. Required technical gate: [TASKS-REVIEW-REPORT.md](TASKS-REVIEW-REPORT.md), Ready for its stated scope. |
| DOCS-009 | Whole-package assessment [DOCS-QC-REPORT](DOCS-QC-REPORT.md), Ready against baseline 7cb0860ec3571859db7ab160d5929ce83c5095e9. Explicit user authorization advances beyond the autodoc stop. |

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

Publish/read back DOCS-009 and close issue #9; explicitly integrate/verify/publish design-docs/main into main; then close sdd-docs-main. After that, activate the Phase 1 objects and execute T-001 through T-012, with the user's requested verified integrated v0.1.0 release. These later effects require actual readback and are not certified by a checked task.
