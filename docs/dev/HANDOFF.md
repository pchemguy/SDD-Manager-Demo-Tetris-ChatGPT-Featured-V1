# Project handoff

Checkpoint: main preparation initialization, before the PROJECT proposal.

The repository is initialized for documentation preparation. No application is implemented and no release is published. Recover later state from Git and the linked owning records.

## Workflow and sources

- Stage and owner: main development, autodoc/onepass preparation, sdd-manage; sdd-design owns the next project brief.
- Tasks: [DOCS_TASKS](DOCS_TASKS.md). Decisions, evidence and current control: [DOCS_PREPARATION](DOCS_PREPARATION.md).
- SDD Manager v0.15.4 is installed and also available under [.agents/plugins/sdd-manager](../../.agents/plugins/sdd-manager/PLUGIN.md).

## Scope and human decisions

- Prepare classic browser Tetris with shared TypeScript game logic/UI and separate browser integration. Modern extensions and Electron delivery are outside current scope.
- Failed gravity or soft-drop movement locks the piece immediately; no separate lock timer.
- Stop for human PROJECT approval. Autodoc then preapproves subsequent document checkpoints through TASKS and stops before package QC and implementation.
- GitHub tracking is enabled by AGENTS.md; publish every owned commit. Keep reports concise while preserving consequential decisions.

## Branches and return

- Working branch: design-docs/main.
- Creation parent and integration target: main.
- Branch-off commit: a60bc0644a4cae7ffa736f1433c154c8cf0f3a0f.
- Preliminary manual provenance seed c7fce835bdf1477968dcaa52cb4f891fafef96a6 was integrated into main and published; retain design-docs/ai-logs. Do not select manual logs as unfinished product work.
- No suspended implementation workflow exists.

## Pending work and next action

- This checkpoint's initialization commit requires push/readback and DOCS-001 issue closure before PROJECT authoring.
- Next eligible action: publish initialization, close its issue with evidence, then prepare/publish PROJECT for human review.
- Later documentation integration and milestone closure remain pending; no implementation range is selected.
