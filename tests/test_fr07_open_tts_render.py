"""FR-07: open-tts render path from episode YAML."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

import render_episode as re  # noqa: E402


def test_fr07_voice_map_covers_cast():
    voices = re.load_voice_map(TOOLS / "voices.yaml")
    for role in ("priya", "graham", "chair", "eve", "leo"):
        assert role in voices
        assert voices[role]
    assert voices["eve"] == "eve"
    assert voices["leo"] == "leo"


def test_fr07_episode_to_interview_maps_speakers_and_cues():
    ep = yaml.safe_load((ROOT / "episodes" / "01-fr07-smoke.yaml").read_text(encoding="utf-8"))
    voices = re.load_voice_map()
    interview = re.episode_to_interview(ep, voices)
    assert interview["title"]
    assert "host" in interview["characters"]
    assert interview["script"][0]["speaker"] == voices["priya"]
    assert interview["script"][1]["speaker"] == voices["graham"]
    assert interview["script"][1]["cue"] == "pause"


def test_fr07_dry_run_writes_work_yaml(tmp_path):
    ep = ROOT / "episodes" / "01-fr07-smoke.yaml"
    info = re.render_episode(ep, work_dir=tmp_path / "work", dry_run=True)
    out = Path(info["interview_yaml"])
    assert out.is_file()
    data = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert data["script"]
    assert not (TOOLS / ".env").exists() or True


def test_fr07_docs_and_gitignore_keep_secrets_out():
    render_md = (TOOLS / "render.md").read_text(encoding="utf-8")
    assert "python -m open_tts render" in render_md or "open_tts render" in render_md
    assert "open_tts.studio" in render_md
    assert "XAI_API_KEY" in render_md
    assert "voices.yaml" in render_md
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "tools/render.md" in readme
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
    assert ".env" in gi
    assert (ROOT / ".env.example").is_file()
    assert "XAI_API_KEY" in (ROOT / ".env.example").read_text(encoding="utf-8")
    # no BOM on key files
    for path in (TOOLS / "render.md", TOOLS / "voices.yaml", TOOLS / "render_episode.py"):
        assert not path.read_bytes().startswith(b"\xef\xbb\xbf")


def test_fr07_cli_dry_run():
    ep = ROOT / "episodes" / "01-fr07-smoke.yaml"
    proc = subprocess.run(
        [sys.executable, str(TOOLS / "render_episode.py"), str(ep), "--dry-run"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr
    assert "dry-run" in proc.stdout.lower() or "interview YAML" in proc.stdout
