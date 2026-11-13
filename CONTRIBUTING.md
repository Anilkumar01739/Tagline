# Contributing to TagLine

Thanks for being here. TagLine is a video editor that runs entirely on the
user's machine, and it gets better mostly through people using it hard and
reporting what broke.

## The most valuable thing you can do

Install an APK from [Releases](https://github.com/Anilkumar01739/Tagline/releases)
or build locally (`scripts/build-android-windows.ps1`), then edit real footage on
Android. A good bug report (device model, Android version, steps, media type) helps
more than most drive-by patches.

## Before you write code

Open a [GitHub issue](https://github.com/Anilkumar01739/Tagline/issues) first for anything beyond a small fix. Large
areas are already in progress or intentionally deferred, and it is
no fun to review a big PR that has to be turned down for reasons that were
invisible from outside.

## Setting up

You will need Rust (see `rust-version` in `src/Cargo.toml`), the FFmpeg
7+ development libraries (`brew install ffmpeg`; see `src/README.md` for
Windows and Linux), cmake and a C++ compiler. Then:

```sh
cd src && cargo run -p tagline
```

That is the editor window. Everything - the engine, the host layer and the
Slint UI - is one Cargo workspace under `src/`.

## Layout

| Path | What lives there |
|---|---|
| `src/crates/` | The engine (core, media, render, effects, export, project), the host layer (`tagline-host`, `tagline-speech`), the API (`tagline-api`, `tagline-server`), the CLI, and `tagline`, the Slint editor window |

[`src/README.md`](src/README.md) explains how the crates fit together and
where the sharp edges are. Read it before touching the engine.

## Checks

Run these before opening a PR:

```sh
cd src && cargo fmt --check && cargo clippy --all-targets -- -D warnings && cargo test
```

If you added or changed text the interface shows, also run
`python3 scripts/locales.py` so the string inventory follows; CI checks it.
Translations live in one JSON file per language; see
[`TRANSLATING.md`](TRANSLATING.md).

If you added or changed a downloadable model, put it in
[`models/manifest.toml`](models/manifest.toml) as well as the engine table it
belongs to, and run `python3 scripts/models.py --check`; CI checks that too.
A maintainer then runs the *Mirror models* workflow, which fetches the model,
records its digest in both places and publishes it to the mirror the app
downloads from.

Write what happens through the `log` facade (`log::info!`, `log::warn!`,
`log::error!`) rather than to standard output or standard error. Every run
writes `<app data>/logs/concat-<when>.log`, and a packaged build has no
terminal for anything that goes anywhere else; `TAGLINE_LOG=debug` turns the
level up. See `src/crates/tagline-host/src/logs.rs`.

New source files need a licence header (see below). Match the style of the code
around you; the engine avoids cleverness on purpose.

## Licensing your contribution

Concat is published under **AGPL-3.0-or-later** ([`LICENSE`](LICENSE)) and
also licensed on commercial terms by its owner ([`LICENSING.md`](LICENSING.md)).

Contributions come in under the terms in [`CLA.md`](CLA.md): **you license
your contribution under the MIT No Attribution licence (MIT-0)**. You keep
your copyright and can use your own work for anything; TagLine's owner, and
anyone else, can use it for anything too, commercial terms included, with no
credit owed.

Two things are needed before a pull request can be merged:

1. Every commit is signed off, with your real name and a working email:

   ```sh
   git commit -s -m "your message"
   ```

2. On your first pull request, a comment from you confirming you have read the
   terms and agree to them. The pull request asks for it.

### File headers

Every source file starts with:

```rust
// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Jareer Abdullah
```

Use this header as it is, and don't add a copyright line of your own.

### Third-party code

If your patch brings in code you did not write, say so in the PR: what it is,
where it came from, and its licence. It has to be under a permissive licence
(MIT, BSD, Apache-2.0, zlib, ISC or similar), because TagLine's commercial
builds must be able to carry it too; GPL, AGPL, LGPL and other copyleft code
cannot be merged. Licence problems are much cheaper to catch before a merge
than after a release.

## Trademarks

The code is free to fork. The TagLine name and logo are not covered by the AGPL
grant; see [`TRADEMARK.md`](TRADEMARK.md). Forks are welcome; please ship them
under your own name.

## Conduct

[`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) applies to the repo, the Discussions
and Discord.
