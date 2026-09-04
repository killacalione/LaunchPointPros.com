#!/usr/bin/env python3
"""Small repository safety checks, not a full secret scanner or HTML validator."""

import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote


REQUIRED = ('index.html', 'styles.css', 'script.js')
PATTERNS = {
    'private-key': re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'github-token': re.compile(r'\b(?:gh[pousr]_[A-Za-z0-9]{36,}|github_pat_[A-Za-z0-9_]{40,})\b'),
    'aws-access-key': re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'service-secret-key': re.compile(r'\bsk-(?:proj-|live-)?[A-Za-z0-9_-]{32,}\b'),
    'local-filesystem-path': re.compile(
        r'(?:/(?:Users|home)/[A-Za-z0-9_.-]+/[^\s\"\'<>]*'
        r'|[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/][^\s\"\'<>]+'
        r'|file:' r'//[^\s\"\'<>]+)'
    ),
}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())


class Report:
    def __init__(self):
        self.errors = 0
        self.warnings = 0

    def emit(self, level, location, rule):
        # Never include matched content: it could contain credentials or personal data.
        if level == 'ERROR':
            self.errors += 1
        else:
            self.warnings += 1
        print(f'{level} {location}: {rule}')


class PageChecks(HTMLParser):
    """Target explicit markup used here; optional HTML end tags may warn."""

    def __init__(self, name, report):
        super().__init__(convert_charrefs=True)
        self.name = name
        self.report = report
        self.ids = set()
        self.anchors = []
        self.stack = []

    def warn(self, line, rule):
        self.report.emit('WARN', f'{self.name}:{line}', rule)

    def handle_starttag(self, tag, attrs):
        line = self.getpos()[0]
        attrs = dict(attrs)
        element_id = attrs.get('id')
        if element_id:
            if element_id in self.ids:
                self.warn(line, 'duplicate-id')
            self.ids.add(element_id)
        href = (attrs.get('href') or '').strip()
        if href == '#' or href.lower().startswith('javascript:'):
            self.warn(line, 'placeholder-link')
        elif href.startswith('#'):
            self.anchors.append((unquote(href[1:]), line))
        if tag not in VOID:
            self.stack.append((tag, line))

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        line = self.getpos()[0]
        if not any(open_tag == tag for open_tag, _ in self.stack):
            self.warn(line, 'unmatched-closing-tag')
            return
        if self.stack[-1][0] != tag:
            self.warn(line, 'misnested-or-implicitly-closed-tag')
        while self.stack:
            open_tag, _ = self.stack.pop()
            if open_tag == tag:
                break

    def finish(self):
        self.close()
        for _, line in self.stack:
            self.warn(line, 'unclosed-tag')
        for target, line in self.anchors:
            if target not in self.ids:
                self.warn(line, 'missing-fragment-target')


def git(root, *args):
    return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)


def main():
    report = Report()
    try:
        root = Path(git(Path.cwd(), 'rev-parse', '--show-toplevel').decode().strip())
        tracked = set(git(root, 'ls-files', '-z').decode().split('\0')) - {''}
        untracked = set(git(root, 'ls-files', '--others', '--exclude-standard', '-z').decode().split('\0')) - {''}
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        print('ERROR repository: Git repository inventory unavailable')
        return 1

    for name in REQUIRED:
        if not (root / name).is_file():
            report.emit('ERROR', name, 'missing-required-source')

    for name in sorted(tracked | untracked):
        path = root / name
        parts = Path(name).parts
        environment_file = any(
            part == '.env' or (part.startswith('.env.') and part != '.env.example')
            for part in parts
        )
        if '.DS_Store' in parts or environment_file:
            report.emit('ERROR', name, 'tracked-or-committable-local-file')
        if path.is_symlink():
            report.emit('ERROR', name, 'symlink-requires-manual-safety-review')
            continue
        try:
            data = path.read_bytes()
        except OSError:
            report.emit('ERROR', name, 'file-unreadable-or-missing')
            continue
        if b'\0' in data:
            continue  # Binary assets are not rewritten or interpreted as text.
        try:
            source = data.decode('utf-8')
        except UnicodeError:
            report.emit('WARN', name, 'non-utf8-content-not-scanned')
            continue
        for rule, pattern in PATTERNS.items():
            for match in pattern.finditer(source):
                line = source.count('\n', 0, match.start()) + 1
                report.emit('ERROR', f'{name}:{line}', rule)
        if path.suffix.lower() == '.html':
            parser = PageChecks(name, report)
            try:
                parser.feed(source)
                parser.finish()
            except (ValueError, AssertionError):
                report.emit('WARN', name, 'markup-check-incomplete')
        if path.suffix.lower() == '.js':
            for line_number, line in enumerate(source.splitlines(), 1):
                if re.search(r'\.textContent\s*=\s*[\"\']Email sent!', line):
                    report.emit('WARN', f'{name}:{line_number}', 'success-message-requires-real-backend-verification')
                if re.search(r'console\.log\s*\(.*emailInput\.value', line):
                    report.emit('WARN', f'{name}:{line_number}', 'contact-email-console-logging')

    print(f'Validation: {report.errors} error(s), {report.warnings} warning(s); '
          f'{len(tracked | untracked)} file(s) inspected.')
    return 1 if report.errors else 0


if __name__ == '__main__':
    sys.exit(main())
