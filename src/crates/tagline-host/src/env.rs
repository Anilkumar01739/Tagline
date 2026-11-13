// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Jareer Abdullah

//! Environment variables for TagLine, with Concat-era names as fallback.

use std::ffi::OsString;

/// Reads `TAGLINE_{name}` or legacy `CONCAT_{name}`.
pub fn var(name: &str) -> Option<OsString> {
    std::env::var_os(format!("TAGLINE_{name}"))
        .or_else(|| std::env::var_os(format!("CONCAT_{name}")))
}

/// Same as [`var`], as UTF-8 lossy text.
pub fn var_lossy(name: &str) -> Option<String> {
    var(name).map(|value| value.to_string_lossy().into_owned())
}
