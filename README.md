# Classic Tetris

A single-player classic Tetris browser app with seven independent random pieces, one next-piece preview, scoring, level progression and pause/resume. A piece locks when a gravity or soft-drop attempt cannot move it down; there is no separate lock timer. Modern extensions and Electron delivery are outside this scope.

## Play and deploy

Use the deployable browser ZIP attached to a GitHub release. Follow [installation, controls and static hosting instructions](docs/INSTALL.md). Players need no Node.js installation. Copy the built files to an ordinary HTTP(S) host, at its root or a nested path. Direct file-URL loading is unsupported.

## Development

Shared TypeScript rules are in src/core; the DOM UI is in src/shared. Browser clocks, lifecycle, keyboard mapping and entry are isolated in src/platform/browser for future platform reuse.

```text
python tools/setup.py
npm run build
python tools/check.py all
python tools/serve.py --root dist --port 4173
```

Open http://127.0.0.1:4173/ and select Start. See [environment evidence](docs/dev/ENVIRONMENT.md) for pinned versions, the official download fallback and the process-local Firefox remedy required on the recorded Linux host. Provisioning evidence and application acceptance are separate. The build includes only local modules/styles/assets and the license notice.

Prepare a candidate archive and checksum under artifacts/:

```text
python tools/package.py
```

The command rebuilds first. Metadata identifies the current commit and whether source changes are present. Final release preparation uses python tools/package.py --require-clean from the pinned release commit. The ZIP contains only web/, INSTALL.md, release.json and SHA256SUMS. Stable asset names are classic-tetris-browser.zip and classic-tetris-browser.zip.sha256.

Browser acceptance can target another built or extracted web directory without changing the app:

```text
python tools/check.py browser --web-root path/to/web --web-prefix games/classic
```

The [project brief](docs/dev/PROJECT.md), [specification](docs/dev/SPEC.md) and [tasks](docs/dev/TASKS.md) define scope and evidence. Development uses [SDD Manager](SDD-MANAGER.md); see the [AI-assisted development disclosure](AI_DISCLOSURE.md).
