# Classic browser implementation report

## Delivered capability

Phase 1 implements the accepted classic browser game: seven independently drawn pieces, fixed-origin no-kick rotation, immediate locking on a failed gravity/soft-drop attempt, atomic row clearing/spawning, next preview, scoring and level-dependent gravity. Pause/resume retains the countdown. Keyboard-accessible controls, responsive layouts, automatic page-lifecycle pause and contained runtime errors complete the experience. Shared TypeScript rules and DOM UI remain separate from browser integration for future host reuse.

The deployable artifact is a deterministic static browser ZIP plus external SHA-256. It includes web assets/license, deployment instructions, version/source metadata and payload hashes. Players need an HTTP(S) host and browser, with no Node runtime. Modern extensions and Electron delivery are excluded.

## Verification and review

The final [phase report](phases/1/PHASE-REPORT.md) records independent code assessment, contract coverage, exact input source and the navigation correction. npm run build passed; complete pytest suite: 106 passed, no warnings or skips, including all 30 browser checks against verified extracted files under a nested URL. Both managed headless engines exercised the specified viewports, native controls and real gravity. Timing/RNG/error boundaries are controlled independently. See [environment evidence](../ENVIRONMENT.md) for pinned identities and the process-local Firefox remedy.

[Milestone 1.1](phases/1/1.1.md) resolved detached-child cleanup; [1.2](phases/1/1.2.md) completed gameplay/presentation; [1.3](phases/1/1.3.md) completed static deployment and package acceptance. Each executable task owns one result/evidence/initial-checkbox commit and is published before advancement. GitHub tracking is enabled; issue/milestone closure follows verified publication.

## Scope limits and workflow state

Native OS-window lifecycle delivery, headed/full-browser modes, Windows-native and Electron execution are unverified/excluded under the declared policy. Visibility/blur handler checks are modeled. No CI, signing, store package or live hosted game is claimed.

This report is the implementation checkpoint. Main integration and v0.1.0 release publication follow the complete phase and hosted closure. The release coordinator rebuilds from the exact clean default-branch release commit and verifies tag/body/assets/downloaded bytes/latest separately. Candidate archives with source_dirty=true are not final release artifacts.

## TODO aggregation

None. Milestone R1 and phase P1 are corrected and rechecked; all accepted behavior and feasible required checks are fulfilled. Policy-excluded native modes are evidence limits, not unresolved product defects. Integration/release effects remain the coordinator's required next boundary at this checkpoint.
