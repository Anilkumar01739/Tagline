// SPDX-License-Identifier: AGPL-3.0-or-later

//! TagLine fork: one place for repository and site URLs (change here when the fork moves).

/// GitHub `owner/repo` for releases, models, and in-app links.
pub const GITHUB_OWNER_REPO: &str = "anilk/TagLine";

/// Repository page.
pub const GITHUB_URL: &str = "https://github.com/anilk/TagLine";

/// Guides and docs (no upstream TagLine site).
pub const SITE_URL: &str = "https://github.com/anilk/TagLine/tree/main/docs";

/// GitHub Releases API.
pub const RELEASES_API_URL: &str =
    "https://api.github.com/repos/anilk/TagLine/releases?per_page=100";

/// Shipped release file prefix (`TagLine-0.2.10-…`).
pub const RELEASE_FILE_PREFIX: &str = "TagLine";

/// Product name in prose.
pub const PRODUCT: &str = "TagLine";
