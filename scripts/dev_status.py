#!/usr/bin/env python3
"""Generate a read-only GitHub Pages snapshot from tracked repository facts.

No WordPress production connection, credentials or guessed operational metrics.
Run from repo root with a complete git history (checkout fetch-depth: 0).
"""
import argparse
import datetime as dt
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLAN = "docs/implementation-plan/10-inkrementalis-merfoldkovek.md"
LABELS = [
    "PWA projektalap", "Arculat és közös UI", "WordPress Core és session",
    "Fiók és belépés", "Valós katalógus és programok", "Médialejátszó alap",
    "Jegyek, bérletek és beléptetés", "Programfoglalás", "Havi prémium",
    "Védett Bunny médiatár", "Virág kérdezi", "Szülő–Virág üzenetek",
    "Push és értesítések", "Pilot és éles átadás",
]
# Only new, version-controlled implementation sources constitute code progress.
# Prototype/demo files and documentation changes are not production code signals.
IMPLEMENTATION_PREFIXES = (
    "ringato-dev/", "wordpress-plugins/", "packages/", "src/", "apps/",
)
IMPLEMENTATION_EXTS = {".php", ".ts", ".tsx", ".js", ".jsx", ".css", ".scss", ".json"}

def git(*args):
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return ""

def completed_count(text):
    # These values are documented implementation handoffs, NOT final acceptance.
    match = re.search(
        r"MF01\s*[–-]\s*MF(\d{2})\s+(?:implementálva|elkészült)", text, re.I
    )
    if match:
        return min(14, int(match.group(1)))
    matches = re.findall(r"MF(\d{2})\s*[:\-–]\s*(?:ellenőrzésre kész|elfogadott)", text, re.I)
    return max((int(n) for n in matches), default=0)

def loc(paths):
    count = 0
    for item in paths:
        p = ROOT / item
        if not p.is_file():
            continue
        try:
            count += len(p.read_text(encoding="utf-8").splitlines())
        except (UnicodeError, OSError):
            pass
    return count

def git_timeline(current_count):
    """Find actual changes in the documented completed-MF count."""
    log = git("log", "--format=%H|%cI", "--", PLAN).splitlines()[:120]
    records = []
    for row in log:
        if "|" not in row:
            continue
        sha, date = row.split("|", 1)
        old_text = git("show", sha + ":" + PLAN)
        records.append({"sha": sha, "at": date, "count": completed_count(old_text)})
    events = []
    for i, item in enumerate(records):
        previous = records[i + 1]["count"] if i + 1 < len(records) else 0
        if item["count"] > previous:
            events.append({
                "at": item["at"], "type": "milestone",
                "title": "Dokumentált implementáció: MF01–MF%02d" % item["count"],
                "sha": item["sha"][:10], "count": item["count"]
            })
    return events

def last_source_progress(tracked):
    sources = [
        path for path in tracked
        if path.startswith(IMPLEMENTATION_PREFIXES)
        and pathlib.Path(path).suffix.lower() in IMPLEMENTATION_EXTS
        and not path.endswith("package-lock.json")
    ]
    if not sources:
        return None, sources
    # git log pathspec excludes this dashboard (kept in docs/dev-status).
    date = git("log", "-1", "--format=%cI", "--", *sources)
    return (date or None), sources

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="docs/dev-status/status.json")
    args = parser.parse_args()
    plan_path = ROOT / PLAN
    plan = plan_path.read_text(encoding="utf-8") if plan_path.exists() else ""
    done = completed_count(plan)
    paths = [p for p in git("ls-files", "-z").split("\0") if p]
    # App/demo code only. virag-terv.html is a presentation document.
    demo_files = [p for p in paths if p in {
        "app.html", "index.html", "app.js", "v13.js", "sw.js"
    }]
    source_date, implementation_files = last_source_progress(paths)
    events = git_timeline(done)
    candidates = ([source_date] if source_date else []) + [e["at"] for e in events]
    last_at = max(candidates) if candidates else None
    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    result = {
        "schema": 1, "generated_at": now, "repository": "realabu/ringato-pwa-demo",
        "source": "GitHub main; docs/implementation-plan/10-inkrementalis-merfoldkovek.md",
        "completed": done, "total": 14,
        "milestones": [
            {"id": "MF%02d" % (i + 1), "name": name,
             "state": "Ellenőrzésre kész" if i < done else "Tervezett"}
            for i, name in enumerate(LABELS)
        ],
        "metrics": {
            "prototype_file_count": len(demo_files),
            "prototype_lines": loc(demo_files),
            "implementation_file_count": len(implementation_files) if implementation_files else None,
            "implementation_lines": loc(implementation_files) if implementation_files else None,
            "documented_custom_wp_plugins": 2 if done >= 3 else None,
            "verified_installed_wp_plugins": None,
            "verified_wp_setting_changes": None
        },
        "last_observable_progress_at": last_at,
        "progress_events": events[:8],
        "notes": [
            "MF01–MF04: implementálva, ellenőrzésre kész; nem véglegesen elfogadott.",
            "A ringato-dev helyi fejlesztői kód jelenleg nincs ebben a GitHub-repóban.",
            "A demó kódsorszáma nem egyenlő az új React/WordPress rendszer kódsorszámával.",
            "A két saját WordPress-plugin (App Shell és Core) dokumentált fejlesztési eredmény, nem igazolt éles telepítésszám.",
            "WordPress-beállításváltozásokhoz külön WP-audit és telepítési napló szükséges.",
            "Az aktivitásfigyelés csak GitHubon látható mérföldkőváltást és új implementációs kódot érzékel."
        ],
        "links": {
            "repo": "https://github.com/realabu/ringato-pwa-demo",
            "plan": "https://github.com/realabu/ringato-pwa-demo/blob/main/" + PLAN,
            "decisions": "https://github.com/realabu/ringato-pwa-demo/blob/main/docs/implementation-plan/09-nyitott-kerdesek-es-dontesek.md"
        }
    }
    target = ROOT / args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("%s: %d/14 ready; %d demo lines; last visible progress: %s" %
          (target, done, result["metrics"]["prototype_lines"], last_at))

if __name__ == "__main__":
    main()
