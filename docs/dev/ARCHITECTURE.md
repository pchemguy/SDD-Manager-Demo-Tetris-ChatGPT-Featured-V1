# Application architecture

The [accepted brief](PROJECT.md) defines a classic browser game and a shared TypeScript boundary for future Electron reuse. The application is a static web build with three cooperating blocks.

## Blocks and dependencies

| Block | Owns | Depends on |
| --- | --- | --- |
| Game engine | Board and active piece, piece geometry, legal transitions, gravity countdown, random-piece selection, row resolution and game statistics | TypeScript types and an injected random-number function |
| Shared UI | DOM board rendering, preview, status, instructions and semantic control buttons | Read-only engine snapshots and command callbacks |
| Browser host | Startup, keyboard mapping, monotonic time, animation scheduling, page visibility/focus, error presentation and disposal | Engine and shared UI |

Dependencies point inward: the browser host composes engine and UI; neither imports the browser host. The UI consumes engine types but cannot mutate engine state. The engine imports no DOM, browser, storage, filesystem or Electron API.

## State and event flow

The host holds the current immutable engine snapshot. An input or scheduled callback first advances elapsed game time, then dispatches its command, replaces the snapshot and asks the view to render. All transitions are synchronous and serialized on the JavaScript event loop. The engine receives elapsed durations rather than reading a clock. Random values are injected at piece-draw boundaries so tests can reproduce sequences without adding production debug controls.

The UI owns DOM nodes, accessible labels and button callbacks, not game decisions. It renders a snapshot without timers or global listeners. Standard DOM is a deliberate shared renderer boundary: it works in a browser and can be hosted in an Electron renderer. Reuse does not imply a native widget UI.

Browser integration owns keyboard and page lifecycle effects. Pause freezes game time; resume establishes a fresh clock baseline. Input cannot reset the gravity cadence. A failed downward attempt resolves locking, row clearing and spawning within one engine transition; intermediate invalid boards are not rendered. SPEC owns exact ordering and timing.

## Technology and delivery

Use TypeScript compiled to browser ES modules, external CSS and standard HTML/DOM. A framework and bundler are unnecessary for a fixed 200-cell board and small control surface. Relative module and asset URLs support ordinary static hosting under a subpath. TypeScript checking and build tools run during development; the deployed game needs no Node.js runtime or application backend.

Use pytest as the test runner. Core tests drive compiled engine modules through a small Node subprocess bridge; browser checks use Playwright's Python API against the actual HTTP-served build. Keep clocks/randomness controlled in tests and keep fixtures outside production assets. Project-local, pinned development dependencies and isolated managed browser binaries support reproducibility; exact package versions are established and locked during toolchain implementation.

## Invariants and failure boundaries

- Rules are authoritative in one engine; UI and platform code do not reproduce collision, scoring or locking rules.
- Each transition leaves a valid snapshot or rejects invalid internal input without replacing the previous snapshot.
- One host owns one loop and listener set. Disposal cancels owned callbacks/listeners and prevents later state changes.
- No game state is persisted or sent over the network. No remote runtime dependency is fetched by the game.
- Unexpected application errors stop the loop and present a readable reload instruction rather than continuing with uncertain state.
- Tests and release packages exclude credentials, browser caches, development dependencies and manual conversation records.

Detailed component responsibilities belong in `DECOMPOSITION.md`; [PROJECT](PROJECT.md) remains the scope authority. Electron processes, IPC, installers and platform service abstractions without a current consumer are outside this design.
