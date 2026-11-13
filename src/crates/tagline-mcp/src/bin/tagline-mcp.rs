// SPDX-License-Identifier: AGPL-3.0-or-later
// SPDX-FileCopyrightText: 2026 Jareer Abdullah

//! The MCP server on its own, for development and the end-to-end test.
//! What ships is the same server inside the app: `tagline --mcp`.
//!
//! usage: tagline-mcp [auto|window|headless]   (or TAGLINE_MCP_MODE)

use std::process::ExitCode;

fn main() -> ExitCode {
    let word = std::env::args()
        .nth(1)
        .or_else(|| std::env::var("TAGLINE_MCP_MODE").ok())
        .unwrap_or_default();
    let Some(mode) = tagline_mcp::Mode::parse(&word) else {
        eprintln!("usage: tagline-mcp [auto|window|headless]");
        return ExitCode::from(2);
    };
    match tagline_mcp::run(mode) {
        Ok(()) => ExitCode::SUCCESS,
        Err(error) => {
            eprintln!("tagline mcp: {error}");
            ExitCode::FAILURE
        }
    }
}
