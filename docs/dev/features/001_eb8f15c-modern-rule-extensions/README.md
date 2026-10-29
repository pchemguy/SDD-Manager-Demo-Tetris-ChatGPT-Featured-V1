# Modern rule extensions

## Campaign identity

Feature campaign 001_eb8f15c, opened at eb8f15c418f8f4462815e8771429fea7be37c135 from main. Package: docs/dev/features/001_eb8f15c-modern-rule-extensions/. Preparation branch: design-docs/001_eb8f15c-modern-rule-extensions. Preparation integration target: main. Intended implementation branch: feature/001_eb8f15c-modern-rule-extensions, created only after accepted preparation is explicitly integrated, verified and published on main. Implementation creation parent/branch-off will be recorded at that later boundary; no implementation branch exists yet.

## Requested capability

The user requested opening this feature campaign with hold, next-piece preview, ghost, 7-bag randomization, wall kicks, hard drop and a full gravity-interval grounded lock delay. The delay is the default; hard drop follows that same policy unless immediate hard-drop locking is selected. This supersedes the classic release's immediate failed-down lock contract for the new capability. The user has not supplied movement/rotation reset semantics.

The released baseline already provides one next-piece preview. Retain and verify that capability with hold, bag refill, promotion and top-out rather than add a second preview. Preserve shared TypeScript game logic/DOM UI and separate browser integration. Electron delivery remains future scope.

## Existing sources

Current accepted main [PROJECT](../../PROJECT.md), [ARCHITECTURE](../../ARCHITECTURE.md), [DECOMPOSITION](../../DECOMPOSITION.md), [SPEC](../../SPEC.md), [PLAN](../../PLAN.md), [layout](../../layout.md) and [TASKS](../../TASKS.md) describe the released classic baseline. v0.1.0 source: 1d84b4e22934eafa68fa80cd52bf490b73520cee; this campaign starts from its published post-release evidence checkpoint. Closed phase records and the v0.1.0 tag remain unchanged.

## Preparation and navigation

Stage: feature exploration/preparation, coordinated through sdd-manage and sdd-design. Necessary active FEATURE documents and adjacent QC reports will live in docs/dev and be linked here as actually authored. No FEATURE-SPEC, FEATURE-PLAN or FEATURE-TASKS is claimed to exist or be accepted yet. Main-preparation DOCS_TASKS is completed historical scope and is not reopened by this feature.

GitHub tracking remains enabled under AGENTS. Project eligible feature task/milestone objects after the feature hierarchy is defined and reviewed; this opening does not fabricate executable tasks or project a future phase. The project's release-after-delivery instruction remains applicable. Propose v0.2.0 for the complete verified feature release; no version bump or release is performed at campaign opening.

## Material proposals requiring resolution

These are agent proposals, not user decisions or implementation contracts:

- Preserve the current architecture and add modern state/actions to the shared engine and rendering to the shared UI.
- Use one held piece, at most one hold action per active-piece cycle until a board lock. Held pieces return in canonical spawn orientation; an occupied spawn ends the game.
- Retain one next-piece preview, show the active piece's lowest legal ghost landing, and obtain pieces from shuffled bags containing each kind once.
- Use SRS wall-kick behavior with explicit rotation tables/coordinate and top-boundary contracts in the specification. Preserve the 10x20 visible board unless a necessary change is explicitly accepted.
- Use C for hold and Space for hard drop; retain current movement, rotation and pause bindings. Provide a session-only immediate-hard-drop-lock option, off by default. Persistent settings and a general mode selector are not requested.
- Start a separate full current-level gravity-interval lock countdown when the active piece becomes grounded, independently of the remaining fall countdown. Freeze both clocks on pause. Failed down attempts do not bypass that delay.
- Recommended reset rule: grounded movement/rotation does not restart the lock countdown; becoming airborne cancels it and landing again starts a full interval. A delayed hard drop that leaves an already grounded piece in place preserves its existing countdown. Immediate hard-drop mode locks on the command, including zero-distance drops.

Before a dependent specification, resolve whether successful grounded movement/rotation resets the delay. Then finalize hold/queue/bag ordering, ghost/kick/top-out boundaries, drop-option semantics and exact elapsed-time event ordering in the feature design/specification. No product code or tests were changed at this opening.

## Opening evidence and next boundary

Inspected clean Git/main state, current handoff/instructions and engine/model; read back actual default main and all remote branches. No prior campaign reservation or active FEATURE package was found in local paths/refs or remote branches. Main checkpoint matched eb8f15c418f8f4462815e8771429fea7be37c135. Allocated sequence 001 once across feature/review/steering identities. New branch and opening record must be published/read back before progression. Next human checkpoint: resolve the material gameplay choice and review necessary feature design proposals. Previous full implementation authority applied to the completed classic scope; it does not constitute acceptance of unwritten feature documents.
