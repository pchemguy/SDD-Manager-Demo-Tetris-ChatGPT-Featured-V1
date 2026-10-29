# Project handoff

Checkpoint: autodoc/onepass completion through DOCS-008, before whole-package QC.

Outcome: PROJECT was explicitly approved, and ARCHITECTURE, DECOMPOSITION, SPEC, PLAN, layout and TASKS were prepared under autodoc preapproval. Required scoped SPEC/design, PLAN/layout and TASKS/PLAN review reports are Ready. This is not a DOCS-009 whole-package QC result, integrated preparation or implemented software.

## Workflow and sources

- Workflow/stage/owner: main development, autodoc/onepass preparation, sdd-manage at the DOCS-008 stop.
- Governing documents: [PROJECT](PROJECT.md), [ARCHITECTURE](ARCHITECTURE.md), [DECOMPOSITION](DECOMPOSITION.md), [SPEC](SPEC.md), [PLAN](PLAN.md), [layout](layout.md) and [TASKS](TASKS.md).
- Preparation owners: [DOCS_TASKS](DOCS_TASKS.md) for task checkoffs and [DOCS_PREPARATION](DOCS_PREPARATION.md) for control/decisions/exact document identities.
- Technical gates: [SPEC review](SPEC-REVIEW-REPORT.md), [PLAN/layout review](PLAN-REVIEW-REPORT.md) and [TASKS review](TASKS-REVIEW-REPORT.md). These do not substitute for whole-package QC.
- SDD Manager v0.15.4 is available through the installed package and the repository's [.agents/plugins/sdd-manager](../../.agents/plugins/sdd-manager/PLUGIN.md). No application toolchain or browser acceptance environment is claimed provisioned.

## Scope and human decisions

- Deliver the classic browser game; modern extensions and Electron delivery are excluded. Share TypeScript game logic/UI and isolate browser integration for future reuse.
- Lock immediately on failed gravity/soft-drop movement, with no separate lock timer. PROJECT also establishes independent random draws, no-kick rotation, next-piece preview, scoring/levels and pause/lifecycle behavior.
- The user's "k" on 2026-10-29 approved the published PROJECT proposal at 95e60a638d1dbd33de68b52cc7286d5409f7342f. ARCHITECTURE through TASKS use the existing autodoc document preapproval.
- Exact stop: after DOCS-008 publication and issue closure, before DOCS-009 package QC, documentation integration and implementation. No implementation range is selected.
- Tracking is enabled for preparation/implementation by AGENTS.md; publish/read back every owned commit. Keep Standard reports concise while surfacing consequential choices and limitations.

## Branches and return

- Working branch: design-docs/main.
- Creation parent and eventual integration target: main.
- Branch-off commit: a60bc0644a4cae7ffa736f1433c154c8cf0f3a0f, the published two-parent manual-provenance scaffold merge.
- Main contains only the initial repository and that preliminary scaffold merge; product preparation has not been integrated.
- Retain design-docs/ai-logs as the manual provenance branch; no transcript was created or selected for current authority.
- No implementation/phase branch or suspended implementation exists.

## Pending work and next action

- The DOCS-008 completion commit still requires push/readback and issue #8 closure as of this snapshot. Reconcile actual later effects rather than repeating completed operations.
- DOCS-001 through DOCS-007 were published/read back and their issues closed/read back. DOCS-009 and milestone sdd-docs-main remain open; no implementation phase objects are activated.
- After the DOCS-008 effects settle, wait for human direction. The next preparation operation is whole-package QC, not a repeat of already accepted document checkpoints. Passing package QC must precede verified published documentation integration and preparation milestone closure.
- TASKS contains one phase, three delivery milestones and a final review milestone, with 12 tasks. Source/test/tool paths and commands remain planned. v0.1.0 is the intended first software release, not a published release.
