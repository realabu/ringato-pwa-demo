#!/usr/bin/env python3
"""Build validated deterministic JSON from human-maintained Markdown idea files."""
import argparse
import datetime
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IDEAS = ROOT / "docs" / "ideas"
FIELDS = (
    "id title area lane status moscow effort_size effort_min_days effort_max_days "
    "user_value operations_value revenue_value communication_value risk estimate_confidence "
    "rice_reach rice_impact rice_confidence rice_effort related_milestones created updated "
    "origin communication_angle"
).split()
SCORES = ("user_value", "operations_value", "revenue_value", "communication_value")
RICE = ("rice_reach", "rice_impact", "rice_confidence", "rice_effort")
ENUMS = {
    "lane": {"mvp-review", "later-feature", "research", "business-experiment"},
    "status": {"ötlet", "elemzett", "döntésre kész", "elfogadott", "fejlesztés alatt", "elkészült", "elvetett"},
    "moscow": {"Must", "Should", "Could", "Won't now"},
    "effort_size": {"S", "M", "L", "XL"},
    "risk": {"alacsony", "közepes", "magas"},
    "estimate_confidence": {"alacsony", "közepes", "magas"}
}
SECTIONS = [
    "Eredeti felvetés", "Megoldandó probléma", "Megoldási változatok",
    "Technikai hatás, előzetes hipotézis", "Kockázatok és függőségek",
    "Példa elfogadási feltétel", "Előzetes ráfordítás és értékelés",
    "Virágnak szóló rövid ajánlat", "Negyedéves kommunikációs lehetőség",
    "Következő ellenőrzendő lépés", "Kapcsolódás a fejlesztéshez"
]


class CatalogError(ValueError):
    pass


def read_idea(path):
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(r"---\r?\n(.*?)\r?\n---\r?\n(.*)", text, re.S)
    if match is None:
        raise CatalogError(f"{path}: frontmatter missing")
    fields = {}
    for lineno, line in enumerate(match.group(1).splitlines(), 2):
        if ":" not in line:
            raise CatalogError(f"{path}:{lineno}: invalid field")
        key, raw = line.split(":", 1)
        key = key.strip()
        if key in fields:
            raise CatalogError(f"{path}:{lineno}: duplicate field {key}")
        try:
            fields[key] = json.loads(raw.strip())
        except json.JSONDecodeError as exc:
            raise CatalogError(f"{path}:{lineno}: non-JSON field {key}") from exc
    if set(fields) != set(FIELDS):
        raise CatalogError(f"{path}: required fields differ: {sorted(set(fields) ^ set(FIELDS))}")
    if type(fields["id"]) is not str or not re.fullmatch(r"IDEA-\d{3}", fields["id"]):
        raise CatalogError(f"{path}: bad ID")
    if not path.name.startswith(fields["id"] + "-"):
        raise CatalogError(f"{path}: ID/filename mismatch")
    for key in ("title", "area", "origin", "communication_angle"):
        if type(fields[key]) is not str or not fields[key].strip():
            raise CatalogError(f"{path}: missing {key}")
    for key, options in ENUMS.items():
        if fields[key] not in options:
            raise CatalogError(f"{path}: invalid enum {key}")
    for key in SCORES:
        if type(fields[key]) is not int or not 1 <= fields[key] <= 5:
            raise CatalogError(f"{path}: invalid score {key}")
    for key in ("effort_min_days", "effort_max_days"):
        if type(fields[key]) is not int or fields[key] < 1:
            raise CatalogError(f"{path}: invalid effort")
    if fields["effort_min_days"] > fields["effort_max_days"]:
        raise CatalogError(f"{path}: effort range inverted")
    links = fields["related_milestones"]
    if type(links) is not list or not links or any(
        type(x) is not str or not re.fullmatch(r"MF\d{2}", x) for x in links
    ):
        raise CatalogError(f"{path}: invalid milestones")
    for key in ("created", "updated"):
        if type(fields[key]) is not str:
            raise CatalogError(f"{path}: invalid date")
        try:
            datetime.date.fromisoformat(fields[key])
        except ValueError as exc:
            raise CatalogError(f"{path}: invalid date") from exc
    if fields["updated"] < fields["created"]:
        raise CatalogError(f"{path}: dates reversed")
    numbers = [fields[key] for key in RICE]
    if any(v is None for v in numbers):
        if not all(v is None for v in numbers):
            raise CatalogError(f"{path}: partial RICE fields")
        fields["rice_score"] = None
    else:
        if any(type(v) not in (int, float) or v <= 0 for v in numbers):
            raise CatalogError(f"{path}: invalid RICE")
        fields["rice_score"] = round(numbers[0] * numbers[1] * numbers[2] / numbers[3], 2)
    body = match.group(2).strip()
    for section in SECTIONS:
        if "## " + section not in body:
            raise CatalogError(f"{path}: missing {section}")
    if not re.search(r"(?m)^> .+", body):
        raise CatalogError(f"{path}: original text quote missing")
    fields["filename"] = path.name
    fields["markdown"] = body
    return fields


def load_catalog(directory=IDEAS):
    paths = sorted(directory.glob("IDEA-*.md"))
    if not paths:
        raise CatalogError("No ideas")
    rows = [read_idea(p) for p in paths]
    if len({row["id"] for row in rows}) != len(rows):
        raise CatalogError("Duplicate ID")
    return {
        "schema_version": 1,
        "count": len(rows),
        "source": "docs/ideas/IDEA-*.md",
        "last_updated": max(x["updated"] for x in rows),
        "ideas": sorted(rows, key=lambda x: x["id"])
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=IDEAS / "catalog.json")
    target = parser.parse_args().output
    catalog = load_catalog()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Validated {catalog['count']} ideas -> {target}")
