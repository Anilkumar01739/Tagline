# TagLine rebrand (fork)

User-facing branding is **TagLine** only. Repository links default to **`anilk/TagLine`** (edit `tagline-host::brand` if your fork differs).

## Central links

- `src/crates/tagline-host/src/brand.rs` — `GITHUB_URL`, `SITE_URL`, `RELEASES_API_URL`, `RELEASE_FILE_PREFIX`, `PRODUCT`
- `start.rs`, `updates.rs`, `models.rs` read from `brand`

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/rebrand-locales-tagline.py` | Locale values (Concat → TagLine) |
| `scripts/rebrand-phase2-env.py` | `CONCAT_*` → `TAGLINE_*` env names |
| `scripts/rebrand-locale-keys-tagline.py` | Keys like `settings.concat` → `settings.tagline` |
| `scripts/rebrand-urls-fast.py` | GitHub/site URLs, `TagLine-*` bundles, SPDX line |
| `scripts/rebrand-readme-tagline.py` | README product name |

## Shipped identity

- Android `app.tagline.editor`, desktop data `app.tagline.editor`, binary **`tagline`** (Cargo bin name; crate package still `tagline`)
- Release artifacts: `TagLine-<version>-…`
- Linux: `/opt/tagline`, `tagline.desktop`, `StartupWMClass=tagline`
- Windows installers: `assets/windows/tagline.iss`, `tagline.wxs` (CI: `build-app.yml`)
- Legacy adopt: `app.concat.editor`, `org.standalones.concat` (data dirs only; see `dirs.rs` `LEGACY_IDENTIFIERS`)

## Rust workspace (`tagline-*`)

Crates live under `src/crates/tagline-*` (main window crate: `tagline`). Re-run `scripts/rebrand-crates-tagline.py` only if a checkout still has `concat-*` folders.

Projects and effects from before the rename: `concat.json`, ids `concat.*`, locks `concat.lock` (new saves use `tagline.json` / `tagline.lock`).

## Fonts

Subset font **files** on disk still use `*-Concat.otf` in the filename; only the binary embed path, not user-visible branding.

## Rebrand audit (2026-11-13)

Grep scope: tracked tree, excluding `target/`, `vendor/`, `.git/`, local build logs.

| Pattern | Before (approx.) | After (approx.) | Notes |
|---------|------------------|---------------|-------|
| `\bConcat\b` (files) | 28 files / ~98 matches | 15 files / ~78 matches | Fixed CI, iOS bundle, docs quick wins below |
| `Concat-` bundles | 2 (mobile CI) | 0 | → `TagLine-android-arm64`, `TagLine-ios-arm64` |
| `tagline.iss` / `tagline.wxs` in CI | 4 refs | 0 | → `tagline.iss`, `tagline.wxs` |
| `tagline.standalones` | 0 in product | 0 | Only in rebrand helper scripts |
| `github.com/jub0t` | 4 product files | 4 | `TRADEMARK.md`, `CLA.md` (upstream attribution); rebrand scripts |

### Fixed this pass (user-visible / CI)

- `src/scripts/ios-app.sh` — iOS display name, executable `TagLine`, privacy strings
- `scripts/ci/smoke-ios.sh` — expects `TagLine … · ios` log line
- `.github/workflows/build-app.yml` — Inno/WiX paths
- `.github/workflows/mobile.yml` — artifact names, keystore org
- `.github/workflows/models.yml`, `.github/release-notes.sh` — release titles
- `docs/MCP.md`, `docs/LOGGING.md`, `docs/AUDIO_LIBRARY.md`
- `android-native/.../AndroidManifest.xml` — launcher label
- `scripts/models.py`, README lang snippets (`docs/README.*`, `scripts/readme/lang_*.py`)

### Still intentionally `Concat` / upstream

| Item | Reason |
|------|--------|
| `concat-*` in old projects / locks / temp names | Legacy compat; see catalogue + `projects.rs` |
| `TRADEMARK.md`, `LICENSING.md`, legal headers | Upstream copyright / mark (Jareer Abdullah) |
| `THIRD_PARTY_NOTICES.md`, `SECURITY.md`, etc. | Legal / historical product name in notices |
| `README.md` Trendshift badge `jub0t%2FTagLine`, `jub0trd@gmail.com` | Upstream repo analytics & DMCA contact until fork replaces |
| `.github/workflows/terms.yml` `jub0t` allowlist | Upstream maintainer on shared workflow |
| `assets/icons/tagline_logo_512.png` filename | Asset path only; optional rename |
| `*-Concat.otf` font filenames | Embed paths only |
| `tagline.lock`, MCP tool `tagline_version` | On-disk / API identifiers |
| `scripts/rebrand-*.py` | Migration tooling |
| `.claude/skills/run-tagline-android/SKILL.md` | Claude skill: build/install Android APK |
| `ffmpeg-mobile.log`, `android-libs.log` | Local build artifacts (gitignored ideally) |

### Locales

`src/crates/tagline/locales/*.json` — no remaining `Concat` product strings in `en.json` (verified). No unused social keys found.

## Windows folder rename (`Concat` → `TagLine`)

Build scripts no longer hard-code `Projects\Concat`; they resolve paths from the repo root.

While **Cursor** (or any terminal) has the repo open, Windows blocks renaming `C:\Users\anilk\Projects\Concat`.

1. Save work, **close this Cursor window** (and any shells whose cwd is under `Concat`).
2. In a new PowerShell (cwd **not** under `Concat`):

   ```powershell
   & "C:\Users\anilk\Projects\Concat\scripts\rename-root-to-tagline.ps1"
   ```

   Or: `Rename-Item -LiteralPath C:\Users\anilk\Projects\Concat -NewName TagLine`

3. Reopen **`C:\Users\anilk\Projects\TagLine\src`** in Cursor.

Local logs under `vendor/` may still mention the old path until you rebuild FFmpeg/Android deps.

## Before you publish

1. Create **`github.com/anilk/TagLine`** (or change `brand.rs` to your repo).
2. Publish releases named `TagLine-*` with `manifest.json` so in-app updates match.
3. Push `origin` away from `jub0t/Concat` when you are ready.
