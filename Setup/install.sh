#!/usr/bin/env bash
# Public entrypoint: always delegate to the latest Admin and Web installers.
set -euo pipefail

PRODUCT='product-reels-fayreel'
readonly ADMIN_URL='https://github.com/ceenreels/product-reels-fayreel/releases/download/product-reels-fayreel-admin/install.sh'
readonly WEB_URL='https://github.com/ceenreels/product-reels-fayreel/releases/download/product-reels-fayreel-web/install.sh'
WORK_DIR=''

say() { printf '%s\n' "$*"; }
die() { printf '错误：%s\n' "$*" >&2; exit 1; }
cleanup() {
  if [ -n "$WORK_DIR" ]; then rm -rf -- "$WORK_DIR"; fi
}
usage() {
  cat <<'USAGE'
Fayreel 统一安装入口
用法：sudo bash install.sh [--update]

默认：依次运行最新版 Admin 和 Web 安装器；首次安装需要交互终端。
--update：依次更新已经安装的 Admin 和 Web。
--help / -h：显示帮助，不下载或安装任何内容。

需要 Linux、root 权限和 curl；系统版本要求沿用 Admin 安装器。
私有镜像需要 GitHub 账号及 read:packages 权限，复用 /root/.docker 登录信息。
安装目录和代理配置通过原有环境变量传递：
  FAYREEL_INSTALL_DIR      Admin 目录，默认 /opt/fayreel
  FAYREEL_PROXY_MODE       caddy 或 external-nginx（默认由 Admin 询问）
  FAYREEL_NGINX_NETWORK    已有 Docker Nginx 网络
  FAYREEL_WEB_INSTALL_DIR  Web 目录，默认 /opt/fayreel-web
  FAYREEL_WEB_ROOT         Web 静态文件目录，默认 Web 目录下的 site

Web 安装后仍需配置站点域名、证书及 Nginx 静态目录和 API 路由。
各组件保留自己的自动更新定时器。安装中断后可重新执行本入口；
若 Web 失败，已成功安装的 Admin 会保留。
USAGE
}
download() {
  local name="$1" url="$2" target="$3" identity="$4"
  say "获取 $name 最新安装器…"
  curl --fail --show-error --silent --location \
    --proto '=https' --proto-redir '=https' \
    --retry 3 --retry-max-time 300 --connect-timeout 20 --max-time 120 \
    "$url" --output "$target" || die "$name 安装器下载失败，尚未执行任何安装。"
  bash -n "$target" || die "$name 安装器语法无效，尚未执行任何安装。"
  grep -Fxq "$identity" "$target" &&
    grep -Eq "^RELEASE_VERSION='[0-9]+\.[0-9]+\.[0-9]+'$" "$target" &&
    grep -Eq "^RELEASE_COMMIT='[a-f0-9]{40}'$" "$target" ||
    die "$name 安装器不是预期的已发布文件，尚未执行任何安装。"
}
main() {
  [ "$#" -le 1 ] || die '只接受 --update、--help 或不带参数。'
  case "${1:-}" in
    --help|-h) usage; return ;;
    --update|'') ;;
    *) die "未知参数：$1" ;;
  esac
  [ "$(uname -s)" = Linux ] || die '安装器仅支持 Linux。'
  [ "$(id -u)" = 0 ] || die '请使用 sudo bash install.sh。'
  command -v curl >/dev/null || die '请先安装 curl 和系统 CA 证书。'

  umask 077
  WORK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/fayreel-install.XXXXXXXX")"
  trap cleanup EXIT
  trap 'exit 130' INT
  trap 'exit 143' TERM

  # Fetch and check both files before either installer changes the server.
  download Admin "$ADMIN_URL" "$WORK_DIR/admin.sh" "INSTALL_URL='$ADMIN_URL'"
  download Web "$WEB_URL" "$WORK_DIR/web.sh" "PRODUCT='product-reels-fayreel-web'"

  # Admin already uses this root-owned config; Web must reuse the same login.
  export DOCKER_CONFIG=/root/.docker
  local status
  say '[1/2] 运行 Admin 安装器…'
  bash "$WORK_DIR/admin.sh" "$@" || {
    status=$?
    printf 'Admin 执行失败（退出码 %s），未运行 Web 安装器。\n' "$status" >&2
    return "$status"
  }
  say '[2/2] 运行 Web 安装器…'
  bash "$WORK_DIR/web.sh" "$@" || {
    status=$?
    printf 'Web 执行失败（退出码 %s）；Admin 已完成，解决问题后可重新执行本入口。\n' "$status" >&2
    return "$status"
  }
  say 'Admin 和 Web 安装器均已成功完成。'
  say 'Web 站点域名、证书与 Nginx 路由请按部署配置接入。'
}

main "$@"
