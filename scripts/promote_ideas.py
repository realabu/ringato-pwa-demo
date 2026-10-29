#!/usr/bin/env python3
"""Publish only validated IDEA-*.md changes from a same-repository PR.

The trusted main-branch checkout executes this script. Untrusted PR content
is inspected as data via git show, never checked out or executed.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.request import Request, urlopen

from build_ideas import load_catalog

ROOT = Path(__file__).resolve().parents[1]
IDEAS_DIR = ROOT / "docs" / "ideas"
IDEA_PATH = re.compile(r"docs/ideas/IDEA-\d{3}-[a-z0-9][a-z0-9-]*\.md\Z")
MAX_BYTES = 250_000


def git(*args, decode=True):
    result = subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True)
    return result.stdout.decode("utf-8") if decode else result.stdout


def get_pr(repo, number, token):
    request = Request(
        f"https://api.github.com/repos/{repo}/pulls/{number}",
        headers={"Accept": "application/vnd.github+json",
                 "Authorization": f"Bearer {token}",
                 "X-GitHub-Api-Version": "2022-11-28"},
    )
    with urlopen(request, timeout=20) as response:
        return json.load(response)


def parse_name_status(raw):
    """The -z diff format is status\0path\0, for added/modified files."""
    if not raw.endswith(b"\x00"):
        raise ValueError("Unterminated git diff fields")
    fields = raw.decode("utf-8").split("\x00")[:-1]
    if len(fields) % 2:
        raise ValueError("Unexpected git diff format")
    return list(zip(fields[::2], fields[1::2]))


def proposed_files(base, head):
    changed = parse_name_status(git(
        "diff", "--name-status", "-z", base, head,
        "--", "docs/ideas", decode=False))
    return [path for status, path in changed
            if status in ("A", "M") and IDEA_PATH.fullmatch(path)]


def show_at(revision, path):
    result = subprocess.run(
        ["git", "show", f"{revision}:{path}"], cwd=ROOT, capture_output=True)
    return result.stdout if result.returncode == 0 else None


def eligible_changes(base, head):
    """Do not overwrite main changes made after a PR branch was created."""
    selected = {}
    for path in proposed_files(base, head):
        proposed = show_at(head, path)
        if proposed is None or len(proposed) > MAX_BYTES:
            raise ValueError(f"Missing or oversized idea: {path}")
        proposed.decode("utf-8", errors="strict")
        prior = show_at(base, path)
        present = (ROOT / path).read_bytes() if (ROOT / path).exists() else None
        if proposed == present:
            continue
        if prior != present:
            raise ValueError(f"Conflicting idea change or duplicate path: {path}")
        selected[path] = proposed
    return selected


def validate_full_catalog(changes):
    with tempfile.TemporaryDirectory(prefix="ringato-ideas-") as dirname:
        folder = Path(dirname)
        for file in IDEAS_DIR.glob("IDEA-*.md"):
            shutil.copyfile(file, folder / file.name)
        for path, content in changes.items():
            (folder / Path(path).name).write_bytes(content)
        return load_catalog(folder)["count"]


def mark_output(promoted):
    if os.getenv("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as output:
            output.write(f"promoted={str(promoted).lower()}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pr", required=True, type=int)
    args = parser.parse_args()
    repo = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GITHUB_TOKEN"]
    pr = get_pr(repo, args.pr, token)
    if pr["base"]["repo"]["full_name"] != repo or pr["base"]["ref"] != "main":
        raise ValueError("PR must target this repository's main branch")
    if not pr["head"]["repo"] or pr["head"]["repo"]["full_name"] != repo or pr["draft"]:
        print("Skipping fork or draft PR")
        mark_output(False)
        return
    head = pr["head"]["sha"]
    git("fetch", "--no-tags", "origin", head)
    base = git("merge-base", "HEAD", head).strip()
    changes = eligible_changes(base, head)
    if not changes:
        print("No unpublished IDEA Markdown in PR")
        mark_output(False)
        return
    count = validate_full_catalog(changes)
    for path, content in changes.items():
        (ROOT / path).write_bytes(content)
    git("add", "--", *sorted(changes))
    git("config", "user.name", "github-actions[bot]")
    git("config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")
    git("commit", "-m", f"docs(ideas): auto-publish from PR #{args.pr}")
    git("push", "origin", "HEAD:main")
    print(f"Published {len(changes)} idea files from PR #{args.pr}; total {count}")
    mark_output(True)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Idea publication stopped: {exc}", file=sys.stderr)
        sys.exit(1)
