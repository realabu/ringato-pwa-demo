#!/usr/bin/env python3
"""Evidence-only, two-repository status. Never executes development repo code."""
import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = 'docs/implementation-plan/10-inkrementalis-merfoldkovek.md'
DEV = 'nmarton/ringato-dev'
DEMO = 'realabu/ringato-pwa-demo'
LABELS = ['PWA projektalap', 'Arculat és közös UI', 'WordPress Core és session',
          'Fiók és belépés', 'Valós katalógus és programok', 'Médialejátszó alap',
          'Jegyek, bérletek és beléptetés', 'Programfoglalás', 'Havi prémium',
          'Védett Bunny médiatár', 'Virág kérdezi', 'Szülő–Virág üzenetek',
          'Push és értesítések', 'Pilot és éles átadás']
EXTS = {'.php', '.ts', '.tsx', '.js', '.jsx', '.mjs', '.css', '.scss', '.html'}
GENERATED = {'ringato-pwa/src/shared/api/contracts.ts', 'ringato-pwa/src/features/content/schema.ts'}


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root, text=True).strip()


def tracked(root):
    return git(root, 'ls-files', '-z').strip('\0').split('\0')


def is_source(p):
    return (p.startswith(('ringato-pwa/src/', 'wordpress-plugins/', 'wordpress-local/mu-plugins/'))
            or p in {'ringato-pwa/index.html', 'ringato-pwa/public/offline.html'}) and pathlib.Path(p).suffix in EXTS and not is_test(p) and p not in GENERATED


def is_test(p):
    return '.test.' in p or '/tests/' in p or p.startswith('tests/')


def measure(root, paths):
    rows = []
    for p in sorted(paths):
        lines = (root / p).read_text(encoding='utf-8').splitlines()
        rows.append({'path': p, 'lines': len(lines), 'nonblank': sum(bool(s.strip()) for s in lines)})
    return {'files': len(rows), 'lines': sum(r['lines'] for r in rows),
            'nonblank': sum(r['nonblank'] for r in rows), 'inventory': rows}


def link(repo, sha, path):
    return f'https://github.com/{repo}/blob/{sha}/{path}'


def plan_ready_ids():
    """Read the plan's explicitly declared local handoff range, not the release evidence."""
    text = (ROOT / PLAN).read_text(encoding='utf-8')
    match = re.search(
        r'\*\*Állapot:\*\*\s*MF01[–-]MF(\d{2})\s+implementálva,\s*lokális ellenőrzésre kész',
        text, re.I)
    if not match:
        # Backward compatibility with the earlier wording of the plan.
        match = re.search(r'MF01[–-]MF(\d{2}) állapota \*\*ellenőrzésre kész', text)
    if not match:
        return []
    last = int(match[1])
    return [f'MF{i:02d}' for i in range(1, min(last, len(LABELS)) + 1)]


def plan_ready_count():
    return len(plan_ready_ids())


def release_states(root):
    """Explicit handoff text AND release/test/source evidence; no commit-title inference."""
    paths = set(tracked(root))
    result = {}
    for n in range(1, 15):
        folder = 'mf01-mf03' if n <= 3 else f'mf{n:02d}'
        release = f'docs/releases/{folder}/RELEASE.md'
        tests = f'docs/releases/{folder}/local-test-results.md'
        if release not in paths or tests not in paths:
            continue
        text = (root / release).read_text() + '\n' + (root / tests).read_text()
        if re.search(r'implementált|implementálva|ellenőrzésre kész|elkészült', text, re.I):
            result[f'MF{n:02d}'] = {'release': release, 'tests': tests}
    return result


def source_events(root):
    events = []
    # Full history, first-parent order, including deleted/renamed source paths.
    for sha in git(root, 'rev-list', '--first-parent', 'HEAD').splitlines():
        changes = git(root, 'diff-tree', '--root', '--no-commit-id', '--name-only', '-r', sha).splitlines()
        sources = [p for p in changes if is_source(p)]
        if not sources:
            continue
        patch = git(root, 'show', '--format=', '--no-ext-diff', '--ignore-all-space', sha, '--', *sources)
        if not patch:
            continue
        date, title = git(root, 'show', '-s', '--format=%cI%n%s', sha).split('\n', 1)
        events.append({'sha': sha, 'at': date, 'title': title, 'type': 'code',
                       'repository': DEV, 'url': f'https://github.com/{DEV}/commit/{sha}',
                       'changed_source_files': len(sources)})
    return events


def generate(dev):
    paths = tracked(dev)
    dev_sha = git(dev, 'rev-parse', 'HEAD')
    demo_sha = git(ROOT, 'rev-parse', 'HEAD')
    sources = [p for p in paths if is_source(p)]
    if not sources:
        raise ValueError('Missing implementation source: refusing an empty snapshot')
    groups = {
        'frontend': [p for p in sources if p.startswith('ringato-pwa/')],
        'wordpress_plugins': [p for p in sources if p.startswith('wordpress-plugins/')],
        'local_mu_plugins': [p for p in sources if p.startswith('wordpress-local/')],
        'tests': [p for p in paths if is_test(p) and pathlib.Path(p).suffix in EXTS | {'.py'}],
        'generated': [p for p in paths if p in GENERATED],
        'tooling': [p for p in paths if (p.startswith(('scripts/', 'ringato-pwa/scripts/')) or p in {'compose.sh', 'clone-wordpress.sh'}) and pathlib.Path(p).suffix in EXTS | {'.py', '.sh'}],
    }
    breakdown = {key: measure(dev, items) for key, items in groups.items()}
    totals = measure(dev, sources)
    features = sorted({p.split('/')[3] for p in sources if p.startswith('ringato-pwa/src/features/')})
    layers = sorted({p.split('/')[3] for p in sources if p.startswith('wordpress-plugins/ringato-core/src/')})
    plugins = []
    option_keys = {}
    for p in sources:
        if not p.endswith('.php'):
            continue
        content = (dev / p).read_text()
        header = re.search(r'^\s*\*?\s*Plugin Name:\s*(.+)$', content[:8192], re.M)
        if header:
            version = re.search(r'^\s*\*?\s*Version:\s*(.+)$', content[:8192], re.M)
            plugins.append({'name': header[1].strip(), 'version': version[1].strip() if version else None,
                            'path': p, 'url': link(DEV, dev_sha, p)})
        if p.startswith('wordpress-plugins/'):
            for key in re.findall(r"\b(?:add|update)_option\(\s*['\"]([^'\"]+)['\"]", content):
                option_keys.setdefault(key, []).append(link(DEV, dev_sha, p))
    states = release_states(dev)
    plan_ids = plan_ready_ids()
    events = source_events(dev)
    if not events:
        raise ValueError('No source history: fetch complete history')
    milestones = []
    for i, label in enumerate(LABELS, 1):
        mid = f'MF{i:02d}'
        evidence = states.get(mid)
        milestones.append({'id': mid, 'name': label,
                           'state': 'Ellenőrzésre kész' if evidence else 'Tervezett',
                           'evidence': {k: link(DEV, dev_sha, p) for k, p in evidence.items()} if evidence else {}})
    demo = measure(ROOT, [p for p in tracked(ROOT) if p in {'app.html', 'index.html', 'app.js', 'v13.js', 'sw.js'}])
    fingerprint = hashlib.sha256()
    for p in sorted(sources):
        # Whitespace-only rewrites and generated files do not change the progress key.
        fingerprint.update(p.encode() + b'\0' + re.sub(rb'\s+', b'', (dev / p).read_bytes()) + b'\0')
    fingerprint.update(json.dumps(sorted(states)).encode())
    return {
        'schema': 2, 'refresh': {'source_access': True}, 'generated_at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
        'completed': len(states), 'total': 14, 'milestones': milestones,
        'repositories': [
            {'name': DEV, 'role': 'primary', 'sha': dev_sha, 'branch': git(dev, 'branch', '--show-current'), 'url': f'https://github.com/{DEV}/commit/{dev_sha}'},
            {'name': DEMO, 'role': 'plan_and_prototype', 'sha': demo_sha, 'branch': git(ROOT, 'branch', '--show-current'), 'url': f'https://github.com/{DEMO}/commit/{demo_sha}'}],
        'metrics': {'implementation_file_count': totals['files'], 'implementation_lines': totals['lines'],
                    'implementation_nonblank_lines': totals['nonblank'], 'feature_modules': len(features),
                    'core_layers': len(layers), 'source_wp_plugins': len(plugins),
                    'verified_installed_wp_plugins': None, 'verified_wp_setting_changes': None,
                    'implemented_wp_option_keys': len(option_keys),
                    'prototype_lines': demo['lines'], 'prototype_file_count': demo['files']},
        'breakdown': breakdown, 'features': features, 'core_layers': layers, 'plugins': plugins,
        'wp_option_keys': option_keys,
        'local_installation_report': {'scope': 'Kiadási dokumentáció szerinti helyi WP-klón; most nem újramért állapot',
                                      'url': link(DEV, dev_sha, 'docs/releases/mf06/local-test-results.md')},
        'plan_completed': len(plan_ids), 'plan_ready_milestone_ids': plan_ids,
        'plan_status_source': 'A mérföldkőterv deklarált lokális készültsége; nem önálló kód-, teszt- vagy éles bizonyíték.',
        'last_observable_progress_at': events[0]['at'], 'progress_events': events[:20],
        'progress_fingerprint': fingerprint.hexdigest(),
        'source_commit': dev_sha,
        'notes': ['A mérföldkő helyi implementációs átadás, nem éles elfogadás. A terv és a kiadások eltérését külön jelezzük.',
                  'Kódsor = UTF-8 fizikai sor, kommentekkel és üres sorokkal. A nem üres sorok külön látszanak.',
                  'Teszt, generált kód, eszközök, függőségek, lockfile, média és dokumentáció nincs a fő kódsorszámban.',
                  'Modul = forrást tartalmazó features alkönyvtár; réteg = Core src alkönyvtár; nem önállóan kész üzleti funkció.',
                  'WP opciókulcs = a saját plugin kódjában literállal add_option/update_option hívásnak átadott különböző kulcs; nem végrehajtott beállításváltozás.',
                  'Éles pluginleltár és WP-audit nem érhető el; ezek értéke ismeretlen, nem nulla.',
                  'A forrásváltozás megfigyelt kódaktivitás; önmagában nem bizonyít kész funkciót vagy működést.'],
        'links': {'repo': f'https://github.com/{DEV}', 'plan': link(DEMO, demo_sha, PLAN),
                  'decisions': link(DEMO, demo_sha, 'docs/implementation-plan/09-nyitott-kerdesek-es-dontesek.md')}
    }


def preserved_snapshot():
    """Keep original measurement date; never turn a failed read into fresh numbers."""
    baseline = json.loads((ROOT / 'docs/dev-status/baseline.json').read_text())
    candidates = [baseline]
    try:
        with urllib.request.urlopen('https://realabu.github.io/ringato-pwa-demo/dev-status/status.json', timeout=15) as response:
            previous = json.load(response)
        if previous.get('schema') == 2 and previous.get('source_commit') and previous.get('metrics', {}).get('implementation_lines') is not None:
            candidates.append(previous)
    except (OSError, ValueError):
        pass
    snapshot = max(candidates, key=lambda s: dt.datetime.fromisoformat(s['generated_at']))
    snapshot['refresh'] = {'source_access': False,
                           'attempted_at': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
                           'message': 'A privát fejlesztési repó nem olvasható a frissítőből. Az utolsó igazolt mérés látható; ez nem inaktivitási bizonyíték. RINGATO_DEV_READ_TOKEN hozzáférés szükséges.'}
    return snapshot


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev-repo', type=pathlib.Path)
    parser.add_argument('--fallback', action='store_true')
    parser.add_argument('--output', default='docs/dev-status/status.json')
    args = parser.parse_args()
    if not args.fallback and not args.dev_repo:
        parser.error('--dev-repo is required unless --fallback is used')
    result = preserved_snapshot() if args.fallback else generate(args.dev_repo.resolve())
    target = ROOT / args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'completed': result['completed'], **result['metrics'], 'source_commit': result['source_commit']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
