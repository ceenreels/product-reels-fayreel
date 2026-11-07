# Fayreel

Public documentation, release downloads, and references to the private Fayreel projects. Each project has its own fixed Release tag. Application source remains in the private submodule repositories.

## Documentation

- [Documentation home](https://ceenreels.github.io/product-reels-fayreel/)
- [Setup documentation](https://ceenreels.github.io/product-reels-fayreel/Docs/Setup/)
- [Admin user guide](https://ceenreels.github.io/product-reels-fayreel/Docs/Guide/)

Open the root `index.html` locally to browse both guides with their accompanying assets.

## Repository layout

```text
index.html
Docs/
  Setup/
  Guide/
Src/
  Admin/  private Git submodule
  App/    private Git submodule
  Web/    private Git submodule
```

| Submodule | Private repository | Tracking branch |
| --- | --- | --- |
| `Src/Admin` | [`ceenreels/product-reels-fayreel-admin`](https://github.com/ceenreels/product-reels-fayreel-admin) | `ceen` |
| `Src/App` | [`ceenreels/product-reels-fayreel-app`](https://github.com/ceenreels/product-reels-fayreel-app) | `ceen` |
| `Src/Web` | [`ceenreels/product-reels-fayreel-web`](https://github.com/ceenreels/product-reels-fayreel-web) | `ceen` |

Anyone can clone this public repository to read the documentation. Developers with access to the private repositories can initialize the pinned submodule commits:

```bash
git clone --branch ceen https://github.com/ceenreels/product-reels-fayreel.git
cd product-reels-fayreel
git submodule update --init --recursive
```

Authenticate with an account that has access to the private repositories. The public repository stores only their URLs, paths, and commit references; credentials must never be added to `.gitmodules`.

To advance a submodule to the latest `ceen` commit, run `git submodule update --remote Src/Admin` (or `Src/App` / `Src/Web`), review the change, and commit the updated reference in this repository. Private source changes are committed and pushed in their respective repositories first.

## Publishing

GitHub Pages uses **GitHub Actions**. The workflow in `.github/workflows/pages.yml` deploys changes to the homepage, documentation, or workflow pushed to `ceen`; it can also be run manually on `ceen`.

The workflow explicitly disables submodule checkout. It exports only the committed `index.html`, `.nojekyll`, and `Docs/` paths into `_site/`, rejects symbolic links, and uploads only that directory. Private source directories and repository metadata are excluded from the website. No private-repository token is required for Pages.

## Downloads and repository rename

The public repository was renamed from `ceenreels/product-reels-fayreel-release` to `ceenreels/product-reels-fayreel`. Existing Releases and their project-specific tags are retained:

- [`product-reels-fayreel-admin`](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel-admin)
- [`product-reels-fayreel-app`](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel-app)
- [`product-reels-fayreel-web`](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel-web)

GitHub redirects the old repository and download URLs, allowing existing published installers to keep working. Use the new name in new integrations and do not recreate a repository under the old name, which would take over those URLs. GitHub Pages uses the new documentation URLs listed above.
