# Classic Tetris specification

[PROJECT](PROJECT.md) owns scope. [ARCHITECTURE](ARCHITECTURE.md) and [DECOMPOSITION](DECOMPOSITION.md) identify the engine, shared view and browser-host owners. This document defines observable contracts for that design. Modern extensions and Electron delivery are excluded.

## S-01 State and boundaries

The engine exposes immutable snapshots containing a 20-row by 10-column settled board, an optional active piece, an optional queued piece, phase, score, cleared-line total, level and remaining gravity duration. Board cells are empty or one of I, J, L, O, S, T, Z. Coordinates are zero-based, x rightward and y downward. The settled board excludes the active piece.

Phases are ready, running, paused and game-over. A fresh ready snapshot has an empty board, no pieces, score/lines zero and level one. Start is effective only in ready; restart is effective in every phase. Either begins a fresh running game with two independent piece draws and a full initial gravity interval. Restart resets board, statistics, pause status and countdown; it does not reload the page. It continues using the supplied RNG rather than promising a reproducible player seed.

Move, rotate, soft drop and time advancement affect only running games. Pause affects only running; resume affects only paused. Other phase-inapplicable valid commands are harmless no-ops. A blocked new-piece spawn enters game-over; gameplay commands cannot resume that game. Start/restart/resume are explicit user actions; loading the application does not start play automatically.

## S-02 Geometry, collision and spawn

Matrices below use dots for empty cells. Rows separated by slashes form square matrices. A clockwise turn maps matrix cell (x,y) to (N-1-y,x); counterclockwise is the inverse. The active origin stays fixed during rotation. O rotation is a no-op with rotation state zero. Four quarter turns restore every other piece's original occupied coordinates.

| Piece | Spawn matrix | Size |
| --- | --- | --- |
| I | `..../IIII/..../....` | 4 |
| J | `J../JJJ/...` | 3 |
| L | `..L/LLL/...` | 3 |
| O | `OO/OO` | 2 |
| S | `.SS/SS./...` | 3 |
| T | `.T./TTT/...` | 3 |
| Z | `ZZ./.ZZ/...` | 3 |

Each piece has four occupied cells. Spawn uses rotation zero, origin x=floor((10-N)/2), y=0. There are no hidden rows. A placement is legal only when every occupied cell is within x=0..9, y=0..19 and overlaps no settled cell. Empty matrix padding is not a collision cell; the matrix origin itself may lie outside the board when all occupied cells fit. A rejected move/rotation leaves origin, rotation, board, statistics and gravity countdown unchanged. There are no wall kicks or automatic position corrections.

## S-03 Randomness and queue

Each draw maps a fresh supplied value u in [0,1) to floor(7*u), in the order I, J, L, O, S, T, Z. Repeats are legal; no bag, drought prevention or hold exists. Production supplies the random function at browser composition, while tests supply controlled sequences.

The first draw is active and the second queued. After locking and row resolution, the queued kind is promoted at its canonical spawn. If it fits, draw exactly one replacement queued kind. If it cannot spawn, enter game-over, set active to null and retain the offending queued kind in the preview without consuming another random value. Movement, rotation, pause, rejected input and rendering consume no random values.

## S-04 Gravity and failed downward attempts

At level L, the gravity interval is max(100, 1000-75*(L-1)) milliseconds. Each spawned piece starts with a full interval at its current level. The engine accepts finite nonnegative elapsed durations. While running, elapsed time below the remaining duration subtracts from it; reaching or exceeding it makes one gravity attempt. Overflow beyond that attempt is discarded rather than producing a burst of catch-up moves. A successful gravity step moves one row and starts a full interval. A callback therefore causes at most one gravity attempt.

Soft drop attempts one downward row immediately and awards no drop points. A successful soft drop preserves the remaining gravity duration. Movement and rotation also preserve it. A failed gravity or soft-drop attempt locks the active piece immediately. Merely moving into a position that touches support does not lock it. There is no lock timer, grace period or movement-reset count.

The browser host advances time to an event's monotonic timestamp before applying its command. A gravity attempt due at exactly that timestamp therefore runs first, including any lock/spawn; the command then applies to the resulting game. The host updates its time baseline after synchronization so the next callback cannot count elapsed time twice. New-piece countdowns do not inherit expired time from the locked piece.

Pause synchronizes time first, then freezes the current countdown and game snapshot. Resume preserves the remaining duration, establishes a fresh host clock baseline and restarts one loop. Time spent paused is never charged to the game. Pausing does not itself grant a new full gravity interval.

## S-05 Locking, clearing and progression

Locking atomically writes the four active cells, finds every full settled row, removes those rows together and inserts the same number of empty rows at the top. Non-cleared rows retain order. No intermediate unresolved board is exposed to the view. Apply scoring/progression, then attempt the queued spawn as defined in S-03.

| Rows cleared by one lock | Base points |
| --- | --- |
| 0 | 0 |
| 1 | 40 |
| 2 | 100 |
| 3 | 300 |
| 4 | 1200 |

Award base points multiplied by the level immediately before this clear. Increase the line total, then set level to floor(total lines/10)+1. The next spawned piece receives the interval for that resulting level. Multi-row clears crossing a level boundary use the old level for all points from that lock. Clearing before spawn can avoid an otherwise blocked spawn. The locked board and final statistics remain visible on game-over.

## S-06 Keyboard and control commands

Game shortcuts operate only while the focusable game surface has keyboard focus and no Ctrl, Alt or Meta modifier is active. Shift does not change the physical-key mapping. Use KeyboardEvent.code. Prevent browser defaults only for recognized game shortcuts in that focus context. Native button Enter/Space activation and navigation outside the game surface remain available.

| Physical key | Command | Repeated keydown |
| --- | --- | --- |
| ArrowLeft / ArrowRight | Attempt one cell left / right | Accepted |
| ArrowDown | One soft-drop attempt | Accepted |
| ArrowUp or KeyX | Clockwise quarter turn | Ignored |
| KeyZ | Counterclockwise quarter turn | Ignored |
| KeyP or Escape | Pause running / resume paused | Ignored |
| KeyR | Restart | Ignored |

Browser-native key repeat supplies repeated movement/down commands; the application adds no repeat timer or held-key acceleration. Each delivered recognized keydown is handled once, in arrival order. Simultaneous opposite keys are therefore ordered events, not a special chord. Space is not a drop/rotation shortcut.

Shared UI provides Start, Pause/Resume and Restart buttons. Start is available in ready; Pause/Resume labels and availability reflect running/paused; Restart is available in all phases. Start, resume and restart focus the game surface. Visible instructions describe the actual controls. Invalid gameplay moves do not show an error dialog.

## S-07 View and accessibility

Render all settled cells and active occupied cells consistently with engine geometry, plus exactly one next-piece preview when a queue exists. Show score, total lines, level and clear ready/paused/game-over status. Ready has no invented preview piece. Paused and game-over overlays do not erase board/statistics. Render no hold area, ghost, hard-drop control or modern mode indicator.

Use distinguishable piece classes and visible cell boundaries, a visible focus indicator, labeled semantic buttons and a concise accessible board description. Game status must not depend on color alone. Announce major phase changes without making every falling-cell update a live announcement. All controls are reachable by keyboard. At 640x480 and 1280x720 viewports, board, status and controls remain usable without clipping; smaller layouts may scroll. Touch controls, audio and mobile-specific behavior are not required.

The shared view accepts snapshots and callbacks, performs no game-state mutation and owns no global clock or window/page listeners. Disposal detaches its owned handlers/nodes. Browser host disposal cancels its animation callback, removes its listeners and prevents any subsequent transition or render.

## S-08 Page lifecycle and errors

When the document becomes hidden or the browser window loses focus, synchronize elapsed time and pause a running game. Repeated hide/blur events are idempotent. Visibility/focus restoration leaves it paused; explicit resume is required and cannot resume a hidden document. Ready and game-over remain in their phases. Page hiding does not destroy the board or create another session.

All engine operations preserve prior snapshots. Malformed internal action data, negative/nonfinite elapsed time or nonfinite/out-of-range RNG values reject the transition with a descriptive Error; callers do not replace the previous snapshot. This is an internal API failure, distinct from an illegal player move. No public save/load API or untrusted game-state import is provided.

An unexpected transition/render/host failure stops the loop and disables game actions, showing a readable message such as "Game unavailable. Reload to retry." No automatic error-retry loop, alert storm or partially applied snapshot is permitted. A fresh page load can create a new ready game. Application operation uses no persistence, telemetry, network game services or credentials.

## S-09 Static build and release artifact

The production build consists of local HTML, external CSS and compiled ES modules with relative URLs. It runs over static HTTP(S), including a nested deployment path; file-URL loading is not supported. After loading those local assets, play needs no external service or runtime download. A player needs no Node.js installation. Default content policy permits only the local scripts/styles/assets needed by this build; there are no inline scripts or dynamic code execution requirements.

Release v0.1.0 supplies a deployable ZIP containing the browser build under `web/`, installation/deployment instructions, version/source-commit metadata and a payload hash manifest. Publish a SHA-256 checksum beside the archive. Packaging uses an explicit allowlist, stable entry ordering/timestamps and rejects traversal/symlink entries. Credentials, source test fixtures, browser binaries/caches, dependencies, AI logs and development documents are excluded. Repeated packaging from identical inputs produces identical archive bytes. Instructions identify the artifact as a static browser build and give an ordinary static-server example; they must not imply a native installer, signed Electron package or store distribution.

## S-10 Acceptance evidence

| Contract group | Required evidence and responsible boundary |
| --- | --- |
| S-01 through S-05 | Pytest-driven engine cases with independent cell/score fixtures: four-turn geometry cycles, padding/bounds/collisions, repeat RNG values and boundary draws, legal/rejected moves, initial/later top-out, successful contact versus failed-down lock, exact gravity expiry, overflow discard, unchanged cadence, pause remainder, 1-4 simultaneous clears and level-crossing scores |
| S-06 through S-08 | Real cooperating engine/view/host tests, plus built-app Chromium and Firefox checks: keyboard/button behavior, discrete-key repeat filtering, phase/focus lifecycle, restart, visible board/preview/overlays, screenshot inspection, repeated isolated page/context teardown and error containment |
| S-09 | Clean pinned build/type check, safe archive inventory and manifests/checksum, repeat-build/package comparison, extraction and HTTP serving under a nested path, and smoke checks against extracted bytes in both selected browser engines |

Provision isolated browsers proactively under the repository browser policy before dependent checks. Prioritize the matching managed Chromium headless shell and include managed Firefox. Headless execution is sufficient for rendering/gameplay checks. Record effective runner/browser versions and modes; model-only lifecycle checks do not prove native window focus delivery. Unavailable full-browser/native-window checks are excluded by default under that policy and reported as unverified; feasible required checks remain mandatory. Runtime/browser provisioning success alone does not establish application acceptance. No software acceptance test is claimed by this specification.
