#!/usr/bin/env python3
"""Validate TTS comedy-timing gate records and episode line markers (FR-25 / #26)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "episodes" / "gates"
EPISODES = ROOT / "episodes"

REQUIRED_CHECKS = ("button_lands", "pause_before_turn_ok", "stranger_would_laugh")
VERDICTS = frozenset({"pending", "pass", "fail"})
BEATS = frozenset({"hook", "escalation", "turn", "button"})


def load_yaml(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path}: expected mapping")
    return data


def validate_gate(path: Path) -> list[str]:
    errs: list[str] = []
    data = load_yaml(path)
    for key in ("episode", "slug", "render_attempt", "listener", "checks", "verdict"):
        if key not in data:
            errs.append(f"{path.name}: missing '{key}'")
    checks = data.get("checks") or {}
    if not isinstance(checks, dict):
        errs.append(f"{path.name}: checks must be a mapping")
        return errs
    for c in REQUIRED_CHECKS:
        if c not in checks:
            errs.append(f"{path.name}: checks missing '{c}'")
    verdict = str(data.get("verdict", "")).lower()
    if verdict and verdict not in VERDICTS:
        errs.append(f"{path.name}: verdict must be one of {sorted(VERDICTS)}")
    if verdict == "pass":
        for c in REQUIRED_CHECKS:
            if checks.get(c) is not True:
                errs.append(f"{path.name}: pass requires checks.{c} == true")
    if data.get("fallback_triggered") is True:
        if not str(data.get("fallback_reason", "")).strip():
            errs.append(f"{path.name}: fallback_triggered needs fallback_reason")
        if verdict != "fail" and path.name != "_template.yaml":
            # Example deliberate fallback may document fail + triggered.
            if verdict not in ("fail", "pending"):
                errs.append(f"{path.name}: fallback should follow a fail (or pending ops)")
    attempt = data.get("render_attempt")
    if isinstance(attempt, int) and attempt >= 2 and verdict == "fail":
        # Soft rule documented; second fail should set fallback or explain deferral.
        if data.get("fallback_triggered") is not True and not str(
            data.get("notes", "")
        ).strip():
            errs.append(
                f"{path.name}: attempt>=2 fail needs fallback_triggered or notes"
            )
    return errs


def validate_episode_lines(path: Path) -> list[str]:
    """When lines are non-empty, require authored timing on turn/button beats."""
    errs: list[str] = []
    if path.name.startswith("_"):
        return errs
    data = load_yaml(path)
    lines = data.get("lines") or []
    if not lines:
        return errs
    saw_turn = saw_button = False
    for i, line in enumerate(lines):
        if not isinstance(line, dict):
            errs.append(f"{path.name}: lines[{i}] must be a mapping")
            continue
        beat = str(line.get("beat", "")).lower()
        if beat and beat not in BEATS:
            errs.append(f"{path.name}: lines[{i}].beat invalid '{beat}'")
        if beat == "turn":
            saw_turn = True
            pb = line.get("pause_before_ms")
            if not isinstance(pb, int) or pb < 400:
                errs.append(
                    f"{path.name}: turn line needs pause_before_ms >= 400 (got {pb!r})"
                )
        if beat == "button":
            saw_button = True
            pa = line.get("pause_after_ms")
            if not isinstance(pa, int) or pa < 500:
                errs.append(
                    f"{path.name}: button line needs pause_after_ms >= 500 (got {pa!r})"
                )
        emph = line.get("emphasis")
        if emph is not None and not isinstance(emph, list):
            errs.append(f"{path.name}: lines[{i}].emphasis must be a list")
        text = str(line.get("text", ""))
        if isinstance(emph, list):
            for word in emph:
                if str(word) not in text:
                    errs.append(
                        f"{path.name}: lines[{i}] emphasis {word!r} not in text"
                    )
    if lines and not saw_turn:
        errs.append(f"{path.name}: non-empty lines need a beat: turn")
    if lines and not saw_button:
        errs.append(f"{path.name}: non-empty lines need a beat: button")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--gates",
        type=Path,
        nargs="*",
        help="Gate YAML paths (default: episodes/gates/*.yaml except skip none)",
    )
    ap.add_argument(
        "--episodes",
        type=Path,
        nargs="*",
        help="Episode YAML paths (default: episodes/*.yaml)",
    )
    args = ap.parse_args()

    gate_paths = args.gates
    if gate_paths is None:
        gate_paths = sorted(GATES.glob("*.yaml")) if GATES.is_dir() else []
    ep_paths = args.episodes
    if ep_paths is None:
        ep_paths = sorted(EPISODES.glob("*.yaml")) if EPISODES.is_dir() else []

    errors: list[str] = []
    for p in gate_paths:
        if p.name == "_template.yaml":
            # Template may use null checks / pending — only require keys.
            try:
                data = load_yaml(p)
            except ValueError as e:
                errors.append(str(e))
                continue
            for key in ("episode", "slug", "render_attempt", "checks", "verdict"):
                if key not in data:
                    errors.append(f"{p.name}: missing '{key}'")
            continue
        try:
            errors.extend(validate_gate(p))
        except ValueError as e:
            errors.append(str(e))

    for p in ep_paths:
        try:
            errors.extend(validate_episode_lines(p))
        except ValueError as e:
            errors.append(str(e))

    if errors:
        print("TTS gate validation FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print(
        f"TTS gate validation OK ({len(gate_paths)} gates, {len(ep_paths)} episodes)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
