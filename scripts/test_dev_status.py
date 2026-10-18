import pathlib
import subprocess
import tempfile
import unittest
from dev_status import is_source, measure, source_events, generate, preserved_snapshot
from unittest.mock import patch


class MetricsTests(unittest.TestCase):
    def test_source_boundary(self):
        for path in ['ringato-pwa/src/pages/HomePage.tsx', 'wordpress-plugins/core/foo.php', 'wordpress-local/mu-plugins/dev.php']:
            self.assertTrue(is_source(path), path)
        for path in ['ringato-pwa/src/sw.test.ts', 'ringato-pwa/src/features/content/schema.ts', 'ringato-pwa/src/shared/api/contracts.ts', 'ringato-pwa/package-lock.json', 'docs/dev-status/index.html', 'ringato-pwa/public/demo-media/tone.wav']:
            self.assertFalse(is_source(path), path)

    def test_physical_lines(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            (root / 'a.ts').write_text('// comment\n\nconst a = 1;\n')
            result = measure(root, ['a.ts'])
            self.assertEqual((result['files'], result['lines'], result['nonblank']), (1, 3, 2))

    def test_documentation_and_whitespace_are_not_code_activity_but_deletion_is(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            def run(*args):
                return subprocess.check_output(['git', *args], cwd=root, text=True).strip()
            run('init', '-q')
            run('config', 'user.name', 'Fixture')
            run('config', 'user.email', 'fixture@example.test')
            path = root / 'ringato-pwa/src/main.ts'
            path.parent.mkdir(parents=True)
            path.write_text('const a = 1;\n')
            def commit(message):
                run('add', '-A')
                run('commit', '-qm', message)
            commit('source')
            (root / 'README.md').write_text('New plans')
            commit('docs only')
            path.write_text('const   a = 1;\n')
            commit('format only')
            self.assertEqual([e['title'] for e in source_events(root)], ['source'])
            path.unlink()
            commit('remove code')
            self.assertEqual([e['title'] for e in source_events(root)], ['remove code', 'source'])

    def test_failed_refresh_preserves_verified_time_and_numbers(self):
        with patch('dev_status.urllib.request.urlopen', side_effect=OSError('offline')):
            result = preserved_snapshot()
        self.assertFalse(result['refresh']['source_access'])
        self.assertEqual(result['metrics']['implementation_lines'], 4464)
        self.assertEqual(result['source_commit'], '960319f6c0e66836068cd12cec20023f15a69a20')
        self.assertNotEqual(result['generated_at'], result['refresh']['attempted_at'])

    def test_missing_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            root = pathlib.Path(folder)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            with self.assertRaises((ValueError, subprocess.CalledProcessError)):
                generate(root)


if __name__ == '__main__':
    unittest.main()
