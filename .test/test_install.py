"""Exercise orchestration with fake downloads; never install software or use root."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


INSTALLER = Path(__file__).resolve().parents[1] / 'Setup' / 'install.sh'
BASE_URL = 'https://github.com/ceenreels/product-reels-fayreel/releases/download'


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        self.downloads = self.root / 'tmp'
        self.downloads.mkdir()
        self.events = self.root / 'events'
        self.events.touch()
        self.env = {
            **os.environ,
            'PATH': str(self.bin) + os.pathsep + os.environ['PATH'],
            'TMPDIR': str(self.downloads),
            'FIXTURES': str(self.root),
            'EVENTS': str(self.events),
            'FAKE_UID': '0',
            'FAKE_SYSTEM': 'Linux',
            'DOCKER_CONFIG': '/unused-user-config',
        }
        self.tool('uname', 'printf "%s\\n" "$FAKE_SYSTEM"')
        self.tool('id', 'printf "%s\\n" "$FAKE_UID"')
        self.tool('curl', '''
case "$*" in
  *releases/download/product-reels-fayreel-admin/install.sh*) name=admin ;;
  *releases/download/product-reels-fayreel-web/install.sh*) name=web ;;
  *) exit 98 ;;
esac
while [ "$#" -gt 0 ]; do
  if [ "$1" = --output ]; then target="$2"; break; fi
  shift
done
printf 'download:%s\\n' "$name" >> "$EVENTS"
if [ "${FAIL_DOWNLOAD:-}" = "$name" ]; then exit 22; fi
cp "$FIXTURES/$name.sh" "$target"
''')
        self.fixture('admin')
        self.fixture('web')

    def tool(self, name, script):
        executable = self.bin / name
        executable.write_text('#!/usr/bin/env bash\nset -eu\n' + script + '\n')
        executable.chmod(0o755)

    def fixture(self, name, status=0):
        identity = (f"INSTALL_URL='{BASE_URL}/product-reels-fayreel-admin/install.sh'"
                    if name == 'admin' else "PRODUCT='product-reels-fayreel-web'")
        (self.root / f'{name}.sh').write_text(
            f"#!/usr/bin/env bash\nset -eu\n{identity}\n"
            "RELEASE_VERSION='1.0.29'\n"
            f"RELEASE_COMMIT='{'a' * 40}'\n"
            f"printf 'run:{name}:%s\\n' \"$*\" >> \"$EVENTS\"\n"
            f"env > \"$FIXTURES/{name}.env\"\n"
            f"exit {status}\n"
        )

    def run_installer(self, *args, **env):
        result = subprocess.run(
            ['bash', str(INSTALLER), *args], env={**self.env, **env},
            capture_output=True, text=True, timeout=10,
        )
        self.assertEqual(list(self.downloads.iterdir()), [], 'Temporary files leaked')
        return result

    def log(self):
        return self.events.read_text().splitlines()

    def test_install_downloads_both_before_running_admin_then_web(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.log(), ['download:admin', 'download:web', 'run:admin:', 'run:web:'])

    def test_update_flag_reaches_both_installers(self):
        result = self.run_installer('--update')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.log()[-2:], ['run:admin:--update', 'run:web:--update'])

    def test_paths_and_proxy_settings_preserved_and_docker_login_shared(self):
        settings = {
            'FAYREEL_INSTALL_DIR': '/srv/admin',
            'FAYREEL_PROXY_MODE': 'external-nginx',
            'FAYREEL_NGINX_NETWORK': 'existing-proxy',
            'FAYREEL_WEB_INSTALL_DIR': '/srv/web',
            'FAYREEL_WEB_ROOT': '/srv/nginx/web',
        }
        result = self.run_installer(**settings)
        self.assertEqual(result.returncode, 0, result.stderr)
        for name in ('admin', 'web'):
            actual = dict(line.split('=', 1) for line in
                          (self.root / f'{name}.env').read_text().splitlines() if '=' in line)
            for key, value in settings.items():
                self.assertEqual(actual[key], value)
            self.assertEqual(actual['DOCKER_CONFIG'], '/root/.docker')

    def test_admin_failure_stops_web_and_preserves_exit_code(self):
        self.fixture('admin', status=42)
        result = self.run_installer()
        self.assertEqual(result.returncode, 42)
        self.assertEqual(self.log(), ['download:admin', 'download:web', 'run:admin:'])

    def test_web_failure_preserves_exit_code_and_explains_partial_install(self):
        self.fixture('web', status=43)
        result = self.run_installer()
        self.assertEqual(result.returncode, 43)
        self.assertIn('Admin 已完成', result.stderr)
        self.assertEqual(self.log()[-2:], ['run:admin:', 'run:web:'])

    def test_download_failure_never_runs_either_installer(self):
        for name in ('admin', 'web'):
            with self.subTest(component=name):
                self.events.write_text('')
                result = self.run_installer(FAIL_DOWNLOAD=name)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse(any(line.startswith('run:') for line in self.log()))

    def test_malformed_or_wrong_release_never_runs_either_installer(self):
        for name in ('admin', 'web'):
            for invalid in ('syntax', 'identity', 'version', 'commit', 'html', 'empty'):
                with self.subTest(component=name, invalid=invalid):
                    self.fixture(name)
                    fixture = self.root / f'{name}.sh'
                    source = fixture.read_text()
                    if invalid == 'syntax':
                        source += '\nif then\n'
                    elif invalid == 'identity':
                        source = source.replace('product-reels-fayreel-', 'wrong-project-')
                    elif invalid == 'version':
                        source = source.replace('1.0.29', '__RELEASE_VERSION__')
                    elif invalid == 'commit':
                        source = source.replace('a' * 40, '__RELEASE_COMMIT__')
                    elif invalid == 'html':
                        source = '<html>Service unavailable</html>\n'
                    else:
                        source = ''
                    fixture.write_text(source)
                    self.events.write_text('')
                    result = self.run_installer()
                    self.assertNotEqual(result.returncode, 0)
                    self.assertFalse(any(line.startswith('run:') for line in self.log()))
                    self.fixture(name)

    def test_help_works_without_root_or_linux_or_downloads(self):
        for arg in ('--help', '-h'):
            result = self.run_installer(arg, FAKE_UID='1000', FAKE_SYSTEM='Darwin')
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('Fayreel', result.stdout)
        self.assertEqual(self.log(), [])

    def test_invalid_arguments_never_download(self):
        for args in (('--unknown',), ('--update', '--extra'), ('--help', '--extra')):
            with self.subTest(args=args):
                self.assertNotEqual(self.run_installer(*args).returncode, 0)
        self.assertEqual(self.log(), [])

    def test_root_and_linux_required_before_download(self):
        self.assertNotEqual(self.run_installer(FAKE_UID='1000').returncode, 0)
        self.assertNotEqual(self.run_installer(FAKE_SYSTEM='Darwin').returncode, 0)
        self.assertEqual(self.log(), [])

    def test_missing_curl_fails_before_download(self):
        # Use only the commands required before the curl preflight.
        (self.bin / 'curl').unlink()
        (self.bin / 'bash').symlink_to(shutil.which('bash'))
        result = self.run_installer(PATH=str(self.bin))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('curl', result.stderr)
        self.assertEqual(self.log(), [])


if __name__ == '__main__':
    unittest.main()
