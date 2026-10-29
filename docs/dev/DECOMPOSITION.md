# Logical component decomposition

[ARCHITECTURE](ARCHITECTURE.md) owns the three-block arrangement. Components below refine those blocks without prescribing file placement or delivery order.

## Engine components

| Component | Responsibility and provided boundary | Dependencies and exclusions |
| --- | --- | --- |
| Model | Immutable game snapshot and discriminated action types; identifies ready, running, paused and game-over states | TypeScript only; contains no clock, renderer or mutable singleton |
| Piece geometry | Canonical spawn matrices, rotated occupied-cell coordinates and board-fit queries | Model; exports the same geometry used by rules and preview rendering, with no duplicated shape definitions |
| Session transitions | Create/start/restart, legal moves/rotations, soft drop, gravity advancement, locking, simultaneous row clearing, score/level updates, queued-piece promotion and top-out | Model, geometry and caller-supplied RNG; returns a complete snapshot, never edits the input snapshot |

The session owns gameplay state and transition ordering. Gravity countdown is game data; the monotonic clock and callback schedule are browser concerns. Illegal player moves return an unchanged game state. Invalid internal inputs are rejected; SPEC owns the exact preconditions and error contract. Injected RNG values are consumed only when pieces are drawn, which gives deterministic test seams without exposing a player seed setting.

## Shared UI

The game view mounts into a caller-supplied DOM element, renders a read-only snapshot, reports user button commands through callbacks and disposes its own listeners/nodes. It owns the board, active-piece appearance, next-piece preview, statistics, status/overlays, keyboard instructions and semantic buttons. Canonical geometry determines occupied cells; the view does not calculate legal moves or award points.

The view uses its root's standard DOM document and external CSS classes. It does not access window focus, animation scheduling, persistence, network, Electron APIs or production randomness. An explicit error-rendering operation supports a stopped host without changing the engine's game-over semantics. Accessibility labels and status announcements are presentation responsibilities.

## Browser host

The input adapter translates allowed keydown events into commands, filters key repeats for discrete controls and leaves native button activation intact. Browser-native repeat supplies repeated lateral/soft-drop commands; there is no extra game input-repeat timer.

The clock/lifecycle adapter measures elapsed monotonic time and schedules rendering callbacks, including time synchronization before commands. It pauses on document hiding or window blur, preserves the remaining countdown and requires explicit resume. It prevents overlapping loops and updates the clock baseline on resume.

The composition root creates the RNG source, session, view and adapters; holds the latest snapshot; serializes transitions; and contains unexpected failures. It owns one complete host lifecycle. Disposal cancels pending callbacks, removes global listeners and disposes the view. A disposed host cannot resume. Neither engine nor view imports these adapters.

## Collaboration and verification seams

| Boundary | Producer and consumer | Independent evidence |
| --- | --- | --- |
| Action to snapshot | Browser host invokes session transitions | Deterministic pytest scenarios through a compiled-module driver with explicit actions, elapsed durations and RNG values |
| Geometry to occupied cells | Geometry serves session and view | Hand-checked cell fixtures, rotation cycles, occupied-cell counts and collision boundaries |
| Snapshot to rendered UI | Host gives snapshot to shared view | Isolated DOM integration and screenshot inspection, including overlays and preview |
| Browser events to actions | Keyboard/lifecycle adapters feed composition root | Real browser keyboard/focus/visibility evidence where supported; modeled handler checks identified separately |
| Application to deployable files | Build/package tools consume source and static assets | Clean build, safe archive inventory, hashes, subpath serving and tests against extracted package bytes |

Tests control clock/RNG through their own harnesses or trusted local browser initialization; no fixture endpoint, debug global or test-only control is shipped in production. Tooling owns build/provision/package operations, not gameplay decisions. SPEC defines precise public behavior and acceptance; `layout.md` assigns physical paths.
