# Development environment evidence

## Observed host and tools

Verified on 2026-10-29: Linux x86_64, Ubuntu 24.04, Python 3.12.14 and Node 24.22.1. TypeScript 7.0.2 is pinned by package-lock.json. Pytest 9.2.0, Playwright Python 1.64.1 and transitive packages are pinned with official PyPI distribution hashes in requirements.lock. Dependencies remain in node_modules and .tools/python; global packages were not modified.

## Provisioning and recovery

The normal installer returned HTTP 200 text/html (a 195-byte Site Unavailable page) for the Chromium CDN URL, causing ZIP extraction failure. Firefox's independent installation succeeded from the runner-declared Microsoft fallback; the subsequent FFmpeg CDN/lock step failed. After the owning installer exited, its known empty stale __dirlock was removed; no unrelated lock was removed.

The contained fallback derives the exact Chromium revision/version from the installed runner and its URL from Google's documented Chrome-for-Testing version metadata. Firefox/FFmpeg use the runner-declared official Microsoft fallback. Downloads are bounded, ZIP CRC/path/type checked and extracted only into the owned browser root with executable modes preserved. The helper refuses an installer lock and reuses sound contained installations. Microsoft's version-matched image manifest was reachable but no image files were used.

The initial fallback completed archive validation and extraction. A later check of the retained temporary Chromium ZIP found an invalid central directory; that temporary archive was discarded rather than assigned a current-valid archive hash. Installed executable identities and working-runner evidence are retained below; no publisher-supplied binary hash is claimed.

- `chrome-headless-shell` installed executable SHA-256 `4fa61f0ba0b4f89b7bec242c32ca16d3bccf69dbfef0651924a9ba8fede5f9d6`.
- `firefox` installed executable SHA-256 `1f637a7cfe8f1a3ec814a7da7e38c360a3e3c39553b8c7245ac5d6643fd495eb`.

## Execution evidence

- Chromium 156.0.8078.4, managed headless shell revision 1248. Effective launch logs identify .tools/browsers/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell with no channel override and the runner's default --no-sandbox argument.
- Firefox 157.0, managed patched revision 1555. Default launch succeeds but page creation crashes; browser logs identify Sandbox: writing /proc/self/uid_map: EPERM.
- For trusted local checks on this host only, TETRIS_FIREFOX_CONTENT_SANDBOX=1 makes the test-only launcher pass MOZ_DISABLE_CONTENT_SANDBOX=1 to the Firefox child. This reduces its internal content sandbox; host restrictions remain unchanged. Re-evaluate on another host and do not use it for arbitrary remote content.
- Both engines passed two fresh context/page input, rendering/screenshot and teardown cycles. Inspected screenshots show readable READY glyphs, the colored rectangle and entered input text in both engines.
- npm run build passes. Final environment suite: six passed cases (two browser probes plus four hostile ZIP cases). Missing binaries, invalid CDN archives and the default Firefox content crash were environment failures, not gameplay RED tests.

## Reproduction

Run at the repository root:

```text
python tools/setup.py
npm run build
python tools/check.py environment
```

If the diagnosed CDN failure occurs on Linux x86_64 after dependencies install, settle the installer and lock ownership before using:

```text
python tools/setup.py --official-fallback
```

For this diagnosed host's trusted local suites:

```text
TETRIS_FIREFOX_CONTENT_SANDBOX=1 python tools/check.py environment
```

Setup/check scripts consistently set an absolute project-owned PLAYWRIGHT_BROWSERS_PATH. Full Chrome/headed/native-window focus, Windows-native development and Electron execution are unverified. These synthetic capability probes establish no application acceptance.

## Milestone 1.1 supervision recheck

The Linux check runner also verifies owned detached-child timeout cleanup and normal adopted-child reaping. The actual host omits the task/children procfs interface; PPid verification and NSpid translation identify only the owner's children. Both controlled regression cases pass, and the complete implemented suite exits successfully after cleanup. Windows-native supervision remains unverified.
