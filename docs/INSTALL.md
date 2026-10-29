# Install and play Classic Tetris v0.1.0

This archive is a deployable static browser build. It contains no native installer, Electron application, signed executable or store package. Players need a JavaScript-enabled browser and an HTTP(S) server. Node.js and Python are not game runtime dependencies. Python below is only an optional local static-server example.

## Verify and extract

Download classic-tetris-browser.zip and classic-tetris-browser.zip.sha256 from the same GitHub release. Compare the ZIP's SHA-256 with the checksum file before extracting. Use your operating system's SHA-256 utility. On Windows CMD, certutil is an ordinary alternative:

```text
certutil -hashfile classic-tetris-browser.zip SHA256
```

Extract to an ordinary directory. release.json records version and source commit. SHA256SUMS records hashes of every payload file except the manifest itself. web/LICENSE.txt retains the project license.

## Serve locally

From the extracted directory, with Python 3 installed:

```text
python -m http.server 4173 --bind 127.0.0.1 --directory web
```

Open http://127.0.0.1:4173/ and select Start. Opening index.html directly with a file URL is unsupported because the build uses ES modules.

## Deploy

Copy the contents of web/ to any static HTTP(S) host. Keep all paths and filenames together; no compilation is needed. Deployment at a nested path such as /games/classic/ is supported. Use that path with a trailing slash. The host must serve .js files with a JavaScript MIME type and .css files as CSS, and must not rewrite module requests to an HTML fallback. HTTPS is recommended for public hosting. No external game service, remote script, account or credential is required. Refreshing the page clears the session.

## Controls and behavior

| Control | Action |
| --- | --- |
| Left / Right | Move one column; held-key repeat is accepted |
| Down | Soft drop one row; held-key repeat is accepted |
| Up / X | Rotate clockwise |
| Z | Rotate counterclockwise |
| P / Escape | Pause or resume |
| R | Restart from any game phase |

Start, Pause/Resume and Restart are native keyboard-accessible buttons. Starting, restarting and resuming focuses the board. Shortcuts apply while the board has focus; use Tab to reach buttons. Ctrl/Alt/Meta shortcuts are ignored. Space activates a focused button and has no board action. Merely touching support leaves a piece active; the first failed gravity or soft-drop downward attempt locks it. There is no separate lock timer. Rotations have no wall kicks. Pieces are drawn independently, so repeats are expected. One next piece is shown.

Clear 1/2/3/4 rows for 40/100/300/1200 points times the current level. Every ten cleared lines raises the level; gravity becomes faster. Soft drop awards no points. Losing browser focus or hiding the page pauses play; returning requires explicit Resume. A blocked spawn ends the game. Restart resets the board and score. There is no saved session, sound, hold, ghost, hard drop or modern mode.

## Verified scope and troubleshooting

The release is checked using isolated managed Chromium headless shell and Firefox on Linux, including both 640x480 and 1280x720 layouts and nested-path static hosting. Native OS-window focus delivery, headed/full-browser modes, Windows-native execution and Electron are not verified. Modeled visibility/blur handlers are distinguished from native keyboard/focus checks in the development reports. No native compatibility is claimed by this browser archive.

If the page fails to load, confirm HTTP hosting, MIME types, correct paths and permitted local assets. If a runtime failure displays "Game unavailable. Reload to retry.", reload to start a fresh session. Server error logs and the browser console can help diagnose deployment errors. Do not put GitHub tokens or development directories on the static host.
