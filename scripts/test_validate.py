"""Exercise safety rules in disposable Git repositories without touching this index."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name('validate.py').resolve()


class ValidatorTests(unittest.TestCase):
    def run_case(self, files=None, tracked=(), missing=()):
        with tempfile.TemporaryDirectory(prefix='launchpoint-validation-') as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', directory], check=True)
            content = {'index.html': '<!doctype html><html><body></body></html>',
                       'styles.css': '', 'script.js': ''}
            content.update(files or {})
            for name in missing:
                content.pop(name)
            for name, value in content.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(value, encoding='utf-8')
            if tracked:
                subprocess.run(['git', '-C', directory, 'add', '-f', '--', *tracked], check=True)
            return subprocess.run([sys.executable, str(VALIDATOR)], cwd=root,
                                  capture_output=True, text=True)

    def test_clean_untracked_repository(self):
        result = self.run_case()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn('0 warning(s)', result.stdout)

    def test_warning_rules_do_not_fail(self):
        result = self.run_case({'index.html': '<html><body><a href="#">x</a>'
                                '<a href="javascript:void(0)">x</a><a href="#missing">x</a>'
                                '<div id="same"></div><div id="same"></div></section></body></html>',
                                'script.js': "button.textContent = 'Email sent!';\n"
                                "console.log('Email submitted:', emailInput.value);"})
        self.assertEqual(result.returncode, 0, result.stdout)
        for rule in ('placeholder-link', 'missing-fragment-target', 'duplicate-id',
                     'unmatched-closing-tag', 'success-message-requires-real-backend-verification',
                     'contact-email-console-logging'):
            self.assertIn(rule, result.stdout)

    def test_missing_source(self):
        self.assertEqual(self.run_case(missing=('script.js',)).returncode, 1)

    def test_tracked_ignored_files(self):
        for name in ('.env', '.env.local', 'nested/.env.production', '.DS_Store'):
            with self.subTest(name=name):
                result = self.run_case({name: 'local', '.gitignore': '.env*\n.DS_Store\n'}, (name,))
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn('tracked-or-committable-local-file', result.stdout)

    def test_ignored_local_files_are_excluded(self):
        result = self.run_case({'.env': 'private', '.gitignore': '.env\n'})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_safe_template(self):
        result = self.run_case({'.env.example': 'API_KEY=replace-me\n'})
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_credentials_are_blocked_and_redacted(self):
        samples = ['ghp_' + 'A' * 36, 'AKIA' + 'A' * 16,
                   'sk-' + 'A' * 40, '-----BEGIN ' + 'PRIVATE KEY-----']
        for value in samples:
            with self.subTest(prefix=value[:4]):
                result = self.run_case({'.env.example': value})
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertNotIn(value, result.stdout)

    def test_local_paths_are_blocked_and_redacted(self):
        for value in ('/' + 'Users/example/project', '/' + 'home/example/project',
                      'C:' + '\\Users\\example\\project', 'file:' + '///example/project'):
            result = self.run_case({'notes.md': value})
            self.assertEqual(result.returncode, 1, result.stdout)
            self.assertNotIn(value, result.stdout)

    def test_validator_source_does_not_match_itself(self):
        result = self.run_case({'scripts/validate.py': VALIDATOR.read_text(),
                               'scripts/test_validate.py': Path(__file__).read_text()})
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
