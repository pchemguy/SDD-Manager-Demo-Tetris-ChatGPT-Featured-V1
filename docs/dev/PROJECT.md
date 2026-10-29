# Browser-based classic Tetris

## Purpose and outcome

Build a single-player classic Tetris game that people can play in a desktop browser using a keyboard. Deliver a complete playable browser application as a static build, with clear controls, visible game status and reproducible verification.

## Gameplay scope

- A board with 10 columns and 20 visible rows and the seven tetromino shapes.
- Independently and uniformly selected pieces, movement left/right, clockwise and counterclockwise rotation, gravity and soft drop. Rotation attempts that collide with the board or occupied cells fail without a wall kick.
- A piece locks immediately when a gravity or soft-drop attempt cannot move it downward. Contact alone does not lock it. There is no separate lock-delay timer. Movement, rotation and soft drop do not postpone the gravity schedule; pause freezes its remaining countdown and resume restores it.
- Complete rows clear together. Score, total cleared lines and level are visible; gravity becomes faster as the level increases.
- One next-piece preview, start, pause/resume, restart and game over when the next piece cannot spawn legally.
- Clear keyboard-control instructions and readable game state. Pause preserves the game; leaving the active page pauses play to avoid an unattended running game.

The application runs entirely in the browser, with no application server, account or Node.js installation needed by a player. Development tools may use Node.js. Precise scoring, speed progression, spawn/rotation geometry, input repeat, focus handling and event ordering are defined in SPEC.

## Reuse and platform boundary

Use TypeScript for shared game logic and UI. Keep game rules independent of browser APIs, rendering, timers and input devices. Keep the UI reusable in a future Electron renderer, with browser startup, scheduling, input/focus integration and any platform services behind explicit boundaries. Prefer small cohesive modules and a lightweight browser UI over speculative platform frameworks.

Electron delivery is future scope. The current project establishes reusable boundaries without creating an Electron shell, native integration, installer or desktop compatibility claim.

## Exclusions

Modern gameplay extensions are outside scope: hold, ghost piece, seven-bag randomization, wall kicks/SRS, hard drop, timed lock delay and its resets, and special piece modes. Online services, multiplayer, persistent high scores/settings, browser-extension delivery and native desktop packaging are also outside the proposed browser baseline.

## Delivery and verification

Deliver the simplest complete classic browser game before considering any new feature scope. The first verified browser release is planned as v0.1.0. Subsequent versions reflect delivered changes, with a tagged GitHub release and release notes after each completed, verified and integrated implementation phase. Preparation documents alone do not constitute a software release.

Verify deterministic game rules independently of the UI, then exercise the actual built browser app in isolated Chromium and Firefox environments under the repository browser policy. Check rendered output, keyboard interaction, lifecycle transitions and deployable build contents. Report unavailable checks and unverified behavior explicitly; passing headless checks does not establish native window behavior.
