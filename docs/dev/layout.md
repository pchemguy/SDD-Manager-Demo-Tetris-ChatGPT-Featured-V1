# Repository layout

This is the intended physical allocation for [ARCHITECTURE](ARCHITECTURE.md), [DECOMPOSITION](DECOMPOSITION.md) and [PLAN](PLAN.md). Application, test and tool paths below are planned; this document does not claim that they exist or that their commands have run.

## Source and assets

| Location | Owner and contents | Dependency constraint |
| --- | --- | --- |
| `src/core/model.ts` | Immutable snapshot, piece and action types | No DOM/platform imports |
| `src/core/geometry.ts` | Canonical matrices, rotations, occupied cells and placement legality | Core model only; shared canonical geometry |
| `src/core/engine.ts` | Session transitions, countdown, lock/clear/spawn, RNG use and statistics | Model/geometry and supplied RNG; no platform APIs |
| `src/shared/game-view.ts` | Shared DOM board, preview, status, instructions, controls and view disposal | Read-only core types/geometry and callbacks; no platform-host imports or global listeners |
| `src/platform/browser/input.ts` | Keyboard-to-command translation and repeat/default filtering | Core action types and explicit event context |
| `src/platform/browser/host.ts` | Clock, scheduling, page lifecycle, current snapshot, composition and fatal-error containment | Core/shared and browser facilities; exports a disposal boundary |
| `src/platform/browser/main.ts` | Browser entry and root mounting | Browser host; contains no rules |
| `web/index.html`, `web/styles.css` | Static page, external styling/CSP, cells/piece classes, layout and focus indication | Relative links to compiled browser entry and CSS; no duplicated geometry/rules |

Keep imports within core, from shared to core, and from browser composition toward shared/core. Do not add Electron directories, IPC interfaces or native packaging for this scope. Standard DOM rendering is shared code; window focus, clocks and browser startup remain platform code.

## Tests and fixtures

| Location | Responsibility |
| --- | --- |
| `tests/core/` | Pytest geometry, session, randomness, clock, lock/clear, progression and state invariants |
| `tests/support/engine_driver.mjs` | Narrow JSON/stdin bridge to compiled TypeScript modules; returns snapshots/errors for pytest assertions, without owning expected game rules |
| `tests/support/` | Controlled-time/RNG fixtures and local integration harnesses using production modules |
| `tests/environment/` | Runner/browser provisioning, repeated isolated context/page lifecycle and teardown evidence, distinguished from app acceptance |
| `tests/browser/` | Playwright Python tests against HTTP-served production/extracted builds, including real keyboard/rendering and scoped lifecycle/error checks |
| `tests/package/` | Archive inventory, metadata/checksums, determinism, safe extraction and deployment-path checks |
| `tests/conftest.py`, `pytest.ini` | Session fixtures, isolated server/browser management and suite selection |

Tests remain outside source/static production assets. A test harness may supply valid board fixtures and controlled RNG/time through production boundaries; it must not require a fixture endpoint or debug global in the released app. Pytest owns assertions; the Node bridge only executes compiled modules and transports results.

## Tooling and configuration

| Location | Responsibility |
| --- | --- |
| `package.json`, `package-lock.json`, `tsconfig.json` | Application version, pinned TypeScript development toolchain, build script and ES-module type-check/emit configuration |
| `requirements.lock` | Exact project-local pytest/Playwright Python dependency resolution with reproducible install inputs |
| `tools/setup.py` | Explicit project-local dependency/browser provisioning using trusted distributions; preserves host installations and follows project policies |
| `tools/build.py` | Type-check/compile into generated output and copy allowlisted static assets; reject unsafe output destinations |
| `tools/serve.py` | Local static HTTP server for development and test/build paths; no game backend or production runtime dependency |
| `tools/check.py` | Bounded suite dispatcher for `environment`, `core`, `browser`, `package` and `all`; invokes pytest and needed build checks |
| `tools/package.py` | Deterministic allowlisted archive, source/version metadata, payload manifest and external checksum; no uploading |

Planned command interfaces are `python tools/setup.py`, `npm run build`, `python tools/check.py <suite>` and `python tools/package.py`. TASKS establishes each interface before dependent use. Do not describe them as validated until actual execution. Native Windows command invocation follows the existing CMD-only policy; no PowerShell script is required.

## Generated files and release contents

Use ignored `.tools/` for project-local development dependencies and managed browsers, with a consistent absolute `PLAYWRIGHT_BROWSERS_PATH`. Use ignored `.work/` for isolated profiles, servers, screenshots, test outputs and temporary extraction. Never search personal/system browser profiles.

Use ignored `dist/` for the clean compiled web tree, preserving module paths beneath `src/` and copying the contents of `web/` to its root. The page uses the relative entry `./platform/browser/main.js`. Use ignored `artifacts/` for candidate/release archives and external SHA-256 files. Generated cleanup is limited to owned paths and rejects symlink/external destinations.

The deployable archive contains only `web/` build contents, `INSTALL.md`, `release.json` source/version metadata and a payload hash manifest. Packaging code owns that exact allowlist. Test fixtures, source dependencies, credentials, caches, manual AI logs and development records are not deployable assets. Production content contains no remote runtime fetch or Node dependency.

## Documentation and existing content

Keep user setup, play and deployment instructions in root `README.md` and `docs/INSTALL.md`; package the installation instructions as `INSTALL.md`. Keep browser/environment setup evidence in `docs/dev/ENVIRONMENT.md` and actual milestone/task evidence, not in product SPEC. Keep finalized release text at root `RELEASE-NOTES.md`.

Main governing documents and their adjacent QC reports live in `docs/dev/`. Phase reports use `docs/dev/reports/phases/1/`; the final report uses `docs/dev/reports/IMPLEMENTATION-REPORT.md`, as assigned by PLAN. `DOCS_TASKS.md` owns preparation checkoffs, `DOCS_PREPARATION.md` owns control/decisions/evidence, and `TASKS.md` owns implementation work.

Preserve `.agents/`, existing instruction/disclosure/usage files, LICENSE and the manual `docs/ai-logs/` scaffold. Root AGENTS supplies current navigation and only genuinely validated command evidence; it is not another task checklist. Repository-local credentials retain their existing effective ignore rule and remain outside tracked/generated deliverables.
