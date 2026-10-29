# Browser delivery plan

## Delivery objective

Deliver the [specified classic game](SPEC.md) as a static browser build and deployable release archive, preserving the [engine/UI/platform boundaries](ARCHITECTURE.md). Phase 1 produces v0.1.0. Modern gameplay and additional delivery platforms have no planned phase in this scope.

One phase is proportionate to this small, complete classic baseline. Its milestones expose live play early and then close the remaining accepted experience and delivery qualities; they are not separate technical-layer phases. Removing score/progression, basic pause or the delivery artifact from the phase would leave the accepted browser baseline incomplete. No independent enhancement backlog is bundled into this phase.

## Phase 1 - Classic browser baseline

Outcome: a usable, verified classic browser game that can be deployed from its release archive. Entry requires accepted and technically reviewed preparation, its verified published integration into the actual default branch, and eligible Phase 1 tracking activation before task execution. Implementation uses a phase branch created from that baseline.

| Milestone | Integrated outcome | Scope and dependency | Exit evidence |
| --- | --- | --- | --- |
| 1.1 Playable falling-piece loop | Start/restart a browser game, move/rotate/drop pieces, observe failed-down locking, row clearing and top-out | Establish pinned tooling and isolated browser readiness; implement shared model/geometry and core session transitions; compose the first board view and browser input/clock host. Covers S-01 to S-04, row/spawn resolution in S-05 and the basic keyboard/render path. Statistics/progression and pause/presentation completion belong to 1.2. | Deterministic geometry/session tests plus actual browser play in Chromium and Firefox. Show a real board and demonstrate support contact versus failed downward locking, row clearing and restart. Review the whole delivered capability, repair blockers and retain a milestone report/HANDOFF. |
| 1.2 Complete classic experience | Complete the accepted scoring, speed, preview, status and pause/resume experience | Depends on 1.1. Complete S-05 progression and S-06 to S-08, including preserved countdown, exact input ordering, page focus/visibility, error containment, accessible buttons and responsive presentation. Preserve the usable loop. | Level-crossing and clock/lifecycle tests, real UI/keyboard checks, screenshots at both specified viewports and a complete playable demonstration. Review the entire milestone and regressions; repair blockers and retain its report/HANDOFF. |
| 1.3 Deployable browser delivery | Deploy the same verified application from a reproducible browser archive | Depends on 1.2. Close S-09 and the complete S-10 matrix: static subpath hosting, production build, package allowlist/hash/version metadata, deployment instructions, clean/extracted-byte acceptance and release notes. | Clean build/type check, full feasible test matrix, visual inspection, reproducible archive bytes, verified manifest/checksum and smoke tests against extracted files in both selected engines. Review whole delivery/packaging scope and relevant regressions, repair blockers and retain its report/HANDOFF. |
| 1.4 Phase review | Establish cross-milestone acceptance and integration readiness | A dedicated final milestone containing exactly one phase code-review/testing/report task. Starts only after all three delivery milestones and their required tracked closures. | Independent assessment of code structure and contracts in addition to test execution, complete phase exits, findings/TODO aggregation, phase report, final implementation report and refreshed HANDOFF. |

At the 1.1 demonstration, evidence informs whether the basic controls, falling cadence and no-kick rotation should continue as specified or need human steering. At 1.2, screenshots and lifecycle behavior inform whether the complete experience is usable. These are useful review points, not extra mandatory approval pauses or authority for the agent to change scope. Honor any implementation range the human selects.

## Review and integration gates

Every delivery milestone requires whole-capability code review, relevant tests/regressions, blocker repair, a committed milestone report and HANDOFF update. TASKS assigns a standalone review task only when that milestone contains at least four delivery tasks and the phase has at least two delivery milestones; otherwise its final delivery task owns these obligations before its completion commit. The special phase review milestone always retains exactly one review task.

Milestone review reports use `docs/dev/reports/phases/1/<milestone-id>.md`; phase and final reports use `docs/dev/reports/phases/1/PHASE-REPORT.md` and `docs/dev/reports/IMPLEMENTATION-REPORT.md`. Each report retains findings, checks, limitations and a TODO section, with None when empty. The final report aggregates unresolved/deferred items and their provenance. Contract/exit violations cannot be deferred to claim completion.

After complete phase acceptance and tracked milestone closures, explicitly integrate the verified phase branch into its recorded default-branch target, recheck the merged state, publish and confirm containment. Partial implementation ranges remain on the phase branch without integrating unfinished scope. The coordinator then creates the release commit/tag and publishes v0.1.0 with finalized notes, archive and checksum from that verified source. The user's release instruction authorizes this post-phase publication; preparation alone does not create a release.

## Verification strategy and environment

Use pytest for deterministic compiled-engine scenarios, cooperating UI/host checks, browser acceptance and archive checks. TypeScript checking and production build are separate required checks. Control time/RNG in test harnesses, and inspect visible screenshots rather than treating DOM labels as proof of rendered cells. Tests exercise the actual built HTTP app, including extracted archive bytes and nested deployment paths.

Establish pinned development dependencies and representative Chromium headless-shell/managed Firefox execution during the first toolchain unit, before dependent browser work. Follow the repository browser and Playwright environment policies, preserve isolated profiles/caches and verify managed build/runner compatibility. Exact versions, setup commands and observed capabilities are implementation evidence, not assumptions supplied by this plan.

Headless modes suffice for the specified gameplay/rendering checks. Unavailable full-browser/native-window behavior is excluded and reported as unverified under the browser policy; it is not a reason to omit feasible selected-engine coverage. Provisioning/launch evidence, modeled focus handlers, native focus events, screenshots and application acceptance remain distinct. No Windows-native or Electron execution gate is imposed on this browser release.

## Risks and completion criteria

- Timing errors can alter locking. Protect expiry ordering, no-reset cadence, lag overflow and pause remainder with controlled-clock scenarios and browser-host integration.
- UI reuse can erode if rules leak into adapters. Review dependency direction and canonical geometry/state ownership at milestone and phase boundaries.
- Browser provisioning may fail independently of application behavior. Diagnose the exact stage with bounded recovery under project policy, preserving verified results and reporting any remaining required capability blocker.
- A source build can differ from packaged bytes. Verify the extracted archive, its manifest, absence of development/secret content and nested HTTP hosting before delivery claims.

Phase completion requires the complete accepted classic behavior, all feasible required evidence, documentation, reproducible deployable artifact, code reviews, reports and applicable tracked closures. Published integration and the subsequent verified GitHub release are reported separately. There are no unresolved product decisions or planned later phases in the current scope.
