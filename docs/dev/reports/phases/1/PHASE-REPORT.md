# Phase 1 code review and acceptance

## Scope and identity

Reviewed the complete classic browser capability at delivery tip b6add9c2f4169eac1cb138619f9cc4a81cba3839, with the documentation/JSDoc correction included in this T-012 checkpoint. Delivery milestones 1.1, 1.2 and 1.3 and their issues were closed/read back before this review began. This is the dedicated cross-milestone review, distinct from their earlier assessments. Preparation baseline: fae386357a66d931b476ef66e3788b893a48a2c1; branch phase/1-classic-browser-baseline; creation parent/integration target main.

## Code assessment

Inspected the coherent core, shared UI, browser integration, static assets and development/build/package/test boundaries separately from execution. Cross-checked SPEC S-01 through S-10 and PLAN exits, including atomic clear/spawn/score/top-out ordering; immutable prior snapshots; independent RNG and draw counts; occupied-cell geometry/no kicks; immediate failed-down locking; overflow discard and no-reset countdown; synchronized input, pause remainder and due-gravity ordering; phase-only announcements and focus ownership; error containment and teardown; root/subpath deployment; package/source identities and exact payload boundaries.

Core has no platform dependency. The view consumes canonical geometry and authoritative snapshots; clocks/global events remain in browser composition. Shared TypeScript rules/UI can be reused by a future host without adding Electron code now. Reviewed locked development tools and official browser recovery/owned-process cleanup. Browser binaries, dependencies, credentials and provenance records are excluded from production. Static assets require no remote runtime. No scope extension, contradictory rule authority, dependency cycle or remaining contract blocker was found.

## Finding and recheck

P1, low, AGENTS.md current project navigation: it still described core/browser/package suites as future work after their delivery. Corrected navigation to the validated commands, selected-root acceptance, installation guide and clean-source release procedure. Added a concise mountView ownership/API comment. Rechecked 37 local links across ten current navigation/governing documents and staged whitespace. No behavior change or test-first gameplay claim is associated with this documentation repair.

## Acceptance evidence

| Contracts | Evidence |
| --- | --- |
| S-01 state/session | Ready/start/restart, phase no-ops, immutable prior snapshots and game-over recovery |
| S-02 geometry | Seven literal shapes/spawns, hand-checked rotations, cycles, O no-op, padding/bounds and settled collision |
| S-03 RNG/queue | Range boundaries/repeats, exact draw counts, promotion/preview and blocked-spawn retention |
| S-04 timing/locking | Support contact versus failed down, exact expiry, no-reset cadence, discarded overflow, due-before-command and pause remainder |
| S-05 progression | Independent 0/1/2/3/4-row score fixtures, nonadjacent compaction, pre-clear multiplier, ten-line crossings and minimum interval |
| S-06 controls | Actual keyboard/button play, repeat/modifier filtering, shortcut focus ownership and native activation |
| S-07 presentation | Board/preview/stats/overlays and individually inspected two-engine screenshots at 640x480 and 1280x720 |
| S-08 lifecycle/errors | Modeled visibility/blur/hidden-resume, explicit resume, injected transition/render faults, one-loop disposal and stale callback rejection after disposal |
| S-09 deployment/package | Strict local-only assets/CSP, root/nested hosting, actual Python server, deterministic archive, metadata/license/manifest/checksum and hostile-input rejection |
| S-10 acceptance | Full actual-build matrix and all browser flows against verified extracted nested-path bytes |

Final npm run build passed. Final complete implemented pytest suite: 106 passed in 49.90s, with no warnings or skips. Counts: 11 environment, 55 core, 30 browser and 10 package; the extracted-byte package test additionally ran the complete 30-case browser suite in an isolated nested deployment. Both selected managed headless engines ran with the documented process-local Firefox remedy. Initial eleven closing commits were audited for exactly one owning task, initial checkbox, result/evidence and boundary report/HANDOFF composition. T-012 composition and remote containment are checked after its commit, before integration.

## Findings aggregation and limits

Milestone 1.1 R1 (owned detached-child cleanup) was repaired and remains covered by two process regressions. Milestones 1.2 and 1.3 retain no unresolved findings; planned later-stage deferrals are now fulfilled. P1 is corrected. No accepted product behavior was deferred.

Native OS-window lifecycle delivery, headed/full-browser modes, Windows-native execution and Electron remain unverified/excluded by the declared environment policy. Visibility/blur tests model event delivery; native keyboard/button/render/gravity checks are separate. No CI execution, native installer, signing or store distribution is claimed. Modern extensions remain outside scope.

## Exit and next boundary

Phase implementation/QC exits are satisfied, subject to publication and task/review-milestone readback of this checkpoint. Audit all twelve closing commits, then explicitly merge the complete phase into main, recheck the merged state and publish/read back main. Release coordination then pins an eligible default-branch release commit, refreshes notes, rebuilds/rechecks exact clean source and publishes/readbacks tag, body, two assets, downloaded bytes and latest. No release publication is claimed by this phase report.

## TODO

None. Remaining integration/release operations are mandatory workflow effects, not deferred implementation findings.
