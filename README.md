# Browser-based classic Tetris

A classic single-player browser game under development. Shared TypeScript logic and UI are intended for future platform reuse; Electron delivery is outside the current scope.

The [project brief](docs/dev/PROJECT.md) defines the accepted project scope. The gameplay application is under development; no software release is published yet.

Development uses [SDD Manager](SDD-MANAGER.md). See the [AI-assisted development disclosure](AI_DISCLOSURE.md).

## Development

Use the project-local pinned tools:

```text
python tools/setup.py
npm run build
python tools/check.py environment
```

See [environment evidence and bounded recovery](docs/dev/ENVIRONMENT.md) for observed modes, the process-local Firefox remedy and official download fallback. A production browser player needs no Node.js installation.
