"""FR club-madeira-campaign#3: Week 1 episode YAML acceptance."""
from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EP = ROOT / "episodes" / "01-they-asked-for-a-shop.yaml"


def _spoken_words(data: dict) -> int:
    blob = " ".join(str(line.get("text") or "") for line in (data.get("lines") or []))
    return len(re.findall(r"[A-Za-z0-9']+", blob))


def test_ep01_exists_and_schema_basics():
    assert EP.is_file()
    raw = EP.read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert raw.endswith(b"\n")
    data = yaml.safe_load(EP.read_text(encoding="utf-8"))
    assert data["episode"] == 1
    assert data["slug"] == "they-asked-for-a-shop"
    assert data["title"] == "They asked for a shop"
    assert data["cta"] == "simulator"
    assert data["cta_url"] == "https://sim.ntsa.uk"
    assert data["approved"] is False
    assert len(data["named_objects"]) == 3
    assert set(data["named_objects"]) == {"the email", "the mug", "the hoodie"}


def test_ep01_spoken_word_count_and_companion():
    data = yaml.safe_load(EP.read_text(encoding="utf-8"))
    n = _spoken_words(data)
    assert 180 <= n <= 220, n
    beats = [str(l.get("beat") or "") for l in data["lines"]]
    assert "turn" in beats and "button" in beats
    comp = data["companion"]
    assert comp.get("linkedin_caption")
    assert comp.get("x_caption")
    assert comp.get("first_comment")
    assert "sim.ntsa.uk" in str(data.get("cta_url") or "")


def test_ep01_timing_markers_for_turn_button():
    data = yaml.safe_load(EP.read_text(encoding="utf-8"))
    saw_turn = saw_button = False
    for line in data["lines"]:
        beat = str(line.get("beat") or "")
        if beat == "turn":
            saw_turn = True
            assert int(line.get("pause_before_ms") or 0) >= 400
        if beat == "button":
            saw_button = True
            assert int(line.get("pause_after_ms") or 0) >= 500
    assert saw_turn and saw_button
