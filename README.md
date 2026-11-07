# Fayreel

Public documentation, release downloads, and references to the private Fayreel projects. Each project has its own fixed Release tag. Application source remains in the private submodule repositories.

## Server installation

The [`product-reels-fayreel` Release](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel) is the main entrypoint for a new server. It contains a single uploaded asset, `install.sh`, maintained in [`Setup/install.sh`](Setup/install.sh).

Run on the target Linux server with `curl` and CA certificates installed:

```bash
curl -fL --retry 3 https://github.com/ceenreels/product-reels-fayreel/releases/download/product-reels-fayreel/install.sh -o install.sh
sudo bash install.sh
```

The entrypoint downloads and checks the latest installers from the fixed Admin and Web release tags, then runs **Admin first, Web second**. Initial installation is interactive and requires a GitHub account with access to the private GHCR packages and a classic PAT with `read:packages`. Both installers share Docker credentials in `/root/.docker`. Supported operating systems and architectures follow the Admin installer.

Admin installs its services and prerequisites. Web installs its static files; configure the Web domain, TLS certificate, Nginx static root and API routes according to the deployment setup. The wrapper does not configure those Web routes. Admin's default Caddy mode serves Admin and the API, so exposing the public Web still requires the appropriate proxy configuration.

For existing deployments, run `sudo bash install.sh --update` to update both components in order. Each component keeps its own automatic update timer. Admin failure stops the wrapper before Web runs; if Web fails, the completed Admin installation remains. Resolve the reported issue and rerun the same command. This is sequential installation, without a combined rollback of both components.

Custom deployment settings use the child installers' existing environment variables. Pass them through `sudo env` when using non-default paths:

```bash
sudo env \
  FAYREEL_INSTALL_DIR=/srv/fayreel-admin \
  FAYREEL_WEB_INSTALL_DIR=/srv/fayreel-web \
  FAYREEL_WEB_ROOT=/srv/nginx/fayreel-web \
  bash install.sh
```

`FAYREEL_PROXY_MODE` (`caddy` or `external-nginx`) and `FAYREEL_NGINX_NETWORK` are also passed through to Admin. Use the same custom paths for later manual updates. Run `bash install.sh --help` for defaults; help does not download or install anything.

## Documentation

- [Documentation home](https://ceenreels.github.io/product-reels-fayreel/)
- [Setup documentation](https://ceenreels.github.io/product-reels-fayreel/Docs/Setup/)
- [Admin user guide](https://ceenreels.github.io/product-reels-fayreel/Docs/Guide/)

Open the root `index.html` locally to browse both guides with their accompanying assets.

## Repository layout

```text
index.html
Setup/
  install.sh  unified server installation entrypoint
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

The separate `.github/workflows/release.yml` workflow checks the installer on pull requests and publishes changes to `Setup/` or the workflow pushed to `ceen`; it also supports manual runs on `ceen`. It updates the fixed `product-reels-fayreel` tag and Release, marks it **Latest**, and uploads only `Setup/install.sh`. Publication verifies the downloaded asset matches the source file. Submodules are not checked out, and other projects' releases are left intact. Admin and Web releases remain independent; the unified installer fetches their latest published installers each time it runs, without needing its own release to change.

To check the entrypoint locally without installing software:

```bash
bash -n Setup/install.sh
python3 -B -m unittest discover -s Setup/tests -v
```

## Downloads and repository rename

The public repository was renamed from `ceenreels/product-reels-fayreel-release` to `ceenreels/product-reels-fayreel`. Releases use fixed project-specific tags:

- [`product-reels-fayreel`](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel) — unified Admin + Web installer (Latest)
- [`product-reels-fayreel-admin`](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel-admin)
- [`product-reels-fayreel-app`](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel-app)
- [`product-reels-fayreel-web`](https://github.com/ceenreels/product-reels-fayreel/releases/tag/product-reels-fayreel-web)

GitHub redirects the old repository and download URLs, allowing existing published installers to keep working. Use the new name in new integrations and do not recreate a repository under the old name, which would take over those URLs. GitHub Pages uses the new documentation URLs listed above.
