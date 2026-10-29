# Browser-based classic Tetris

A classic single-player browser game under development. Shared TypeScript logic and UI are intended for future platform reuse; Electron delivery is outside the current scope.

The [project brief](docs/dev/PROJECT.md) defines the accepted project scope. The live browser loop supports movement, rotation, soft drop, failed-downward locking, row clearing and restart. The complete classic experience and release packaging are under development.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md).

## Development

Use the project-local pinned tools:

```text
python tools/setup.py
npm run build
python tools/check.py environment
```

See [environment evidence and bounded recovery](docs/dev/ENVIRONMENT.md) for observed modes, the process-local Firefox remedy and official download fallback. A production browser player needs no Node.js installation.

## Play from a build

```text
npm run build
python tools/serve.py --root dist --port 4173
```

Open http://127.0.0.1:4173 and select Start. Use Left/Right to move, Down to soft drop, Up or X to rotate clockwise, Z to rotate counterclockwise and R to restart. Contact alone leaves a piece active; a failed gravity or soft-drop attempt locks it.
