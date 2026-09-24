#!/usr/bin/env python3
"""CI for episodes/*.yaml — FR-26 / issue #27."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_KEYS = (
    "episode",
    "slug",
    "title",
    "series",
    "length_target_s",
    "cta",
    "cta_url",
    "approved",
    "voices",
    "beats",
    "named_objects",
    "lines",
    "companion",
    "banned",
)
ALLOWED_CTA = ("simulator", "partner", "how-it-works", "product")
CTA_URL = {
    "simulator": "https://sim.ntsa.uk",
    "partner": "https://www.clubmadeira.uk/partners",
    "product": "https://www.thesmartcatalogue.com/",
}
ALLOWED_HOSTS = (
    "sim.ntsa.uk",
    "www.clubmadeira.uk",
    "clubmadeira.uk",
    "www.thesmartcatalogue.com",
    "thesmartcatalogue.com",
)
DEFAULT_BANNED = ("pyramid", "get rich", "disrupt", "just use AI")
SECRET_RE = re.compile(
    r"(XAI_API_KEY|password\s*=|(?<![A-Za-z0-9])sk-[A-Za-z0-9]{20,}|"
    r"(?<![A-Za-z0-9])[A-Fa-f0-9]{40,})",
    re.I,
)
BRIEF_TITLES = {
    1: "They asked for a shop",
    2: "Amazon Associates at 11:47pm",
    3: "The committee has thoughts",
    4: "On-site vs off-site portal",
    5: "White label, black coffee",
    6: "Scope creep: the musical",
    7: "Flying club in two months",
    8: "Priya's recurring 1%",
}


def is_template(data: dict) -> bool:
    return int(data.get("episode") or 0) == 0 or str(data.get("slug") or "") == "template"


def flatten_strings(obj) -> list[str]:
    out: list[str] = []
    if obj is None:
        return out
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        for v in obj.values():
            out.extend(flatten_strings(v))
        return out
    if isinstance(obj, (list, tuple)):
        for v in obj:
            out.extend(flatten_strings(v))
        return out
    return [str(obj)]


def normalize(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def load_metrics_titles(path: Path) -> dict[int, str]:
    found: dict[int, str] = {}
    if not path.is_file():
        return found
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.search(r"\|\s*0?(\d+)\s+([^|]+)\|", line)
        if m:
            found[int(m.group(1))] = m.group(2).strip()
    return found


def check_file(path: Path, metrics_titles: dict[int, str]) -> list[str]:
    errors: list[str] = []
    raw = path.read_text(encoding="utf-8")
    if SECRET_RE.search(raw):
        errors.append("secret-shaped string")
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        return [f"yaml: {exc}"]
    if not isinstance(data, dict):
        return ["not a mapping"]
    for key in REQUIRED_KEYS:
        if key not in data:
            errors.append(f"missing key {key}")
    if errors:
        return [f"{path.name}: {e}" for e in errors]

    tmpl = is_template(data)
    length = data.get("length_target_s")
    try:
        length_n = int(length)
    except (TypeError, ValueError):
        errors.append("length_target_s not an int")
        length_n = None
    if length_n is not None and not (45 <= length_n <= 75):
        errors.append(f"length_target_s {length_n} outside 45-75")

    cta = str(data.get("cta") or "").strip()
    url = str(data.get("cta_url") or "").strip()
    if cta not in ALLOWED_CTA:
        errors.append(f"cta {cta!r} not in {ALLOWED_CTA}")
    elif cta in CTA_URL:
        if url.rstrip("/") != CTA_URL[cta].rstrip("/"):
            errors.append(f"cta_url {url!r} does not match cta {cta}")
    else:
        from urllib.parse import urlparse

        host = (urlparse(url).hostname or "").lower()
        if urlparse(url).scheme != "https" or host not in ALLOWED_HOSTS:
            errors.append(f"how-it-works cta_url must be https on a brief host, got {url!r}")

    names = data.get("named_objects")
    if not tmpl:
        if not isinstance(names, list) or len(names) != 3:
            errors.append("named_objects must be exactly 3")

    banned = list(data.get("banned") or []) + list(DEFAULT_BANNED)
    text_blob = "\n".join(flatten_strings(data.get("lines")) + flatten_strings(data.get("companion")))
    for phrase in banned:
        if phrase and phrase.lower() in text_blob.lower():
            errors.append(f"banned phrase {phrase!r}")

    commercial = bool(data.get("commercial")) or cta in ("partner", "product")
    disclosure = str(data.get("disclosure") or "").strip()
    if commercial and not tmpl and not disclosure:
        errors.append("commercial episode needs non-empty disclosure")

    ep = int(data.get("episode") or 0)
    title = str(data.get("title") or "").strip()
    if not tmpl and 1 <= ep <= 8:
        brief = BRIEF_TITLES.get(ep, "")
        metric = metrics_titles.get(ep, "")
        nt = normalize(title)
        if brief and nt != normalize(brief) and normalize(brief) not in nt:
            if metric and nt == normalize(metric):
                errors.append(f"title {title!r} follows metrics.md but disagrees with BRIEF.md {brief!r}")
            elif metric and normalize(metric) not in nt:
                errors.append(f"title {title!r} matches neither BRIEF.md nor metrics.md")
            else:
                errors.append(f"title {title!r} disagrees with BRIEF.md {brief!r}")

    return [f"{path.name}: {e}" for e in errors]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--expect-fail", action="store_true")
    args = parser.parse_args()
    paths = args.paths or sorted((ROOT / "episodes").glob("*.yaml"))
    metrics_titles = load_metrics_titles(ROOT / "metrics.md")
    errors: list[str] = []
    for path in paths:
        if not path.is_file():
            errors.append(f"missing {path}")
            continue
        errors.extend(check_file(path, metrics_titles))
    failed = bool(errors)
    if args.expect_fail:
        if not failed:
            print("expected fixture to fail; it passed")
            return 1
        print("broken fixture failed as expected:")
        for line in errors:
            print(" ", line)
        return 0
    for line in errors:
        print(line)
    if failed:
        return 1
    print(f"ok {len(paths)} episode file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
