"""FR-07: adapt episodes/NN-*.yaml and call `python -m open_tts render` (do not vendor open-tts)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML required: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
VOICES_PATH = Path(__file__).resolve().parent / "voices.yaml"
WORK_DIR = Path(__file__).resolve().parent / ".render-work"


def load_voice_map(path: Path = VOICES_PATH) -> dict[str, str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"voices map must be a mapping: {path}")
    out: dict[str, str] = {}
    for k, v in data.items():
        key = str(k).strip().lower()
        if not key or key.startswith("#"):
            continue
        out[key] = str(v).strip().lower()
    required = ("priya", "graham", "chair", "eve", "leo")
    missing = [r for r in required if r not in out]
    if missing:
        raise ValueError(f"voices.yaml missing roles: {missing}")
    return out


def map_speaker(raw: str, voices: dict[str, str]) -> str:
    key = str(raw or "").strip().lower()
    if not key:
        raise ValueError("empty speaker")
    if key in voices:
        return voices[key]
    return key


def episode_to_interview(ep: dict[str, Any], voices: dict[str, str]) -> dict[str, Any]:
    title = str(ep.get("title") or ep.get("slug") or "episode").strip()
    lines_in = ep.get("lines") or []
    if not isinstance(lines_in, list) or not lines_in:
        raise ValueError("episode YAML needs a non-empty lines: list")
    script: list[dict[str, Any]] = []
    seen: list[str] = []
    for entry in lines_in:
        if not isinstance(entry, dict):
            raise ValueError("each lines[] entry must be a mapping")
        speaker = map_speaker(str(entry.get("speaker") or ""), voices)
        text = str(entry.get("text") or "").strip()
        if not text:
            raise ValueError(f"empty text for speaker={speaker}")
        row: dict[str, Any] = {"speaker": speaker, "text": text}
        cue = entry.get("cue")
        if cue:
            row["cue"] = str(cue)
        script.append(row)
        if speaker not in seen:
            seen.append(speaker)
    if not seen:
        raise ValueError("no speakers found")
    characters: dict[str, str] = {"host": seen[0]}
    if len(seen) > 1:
        characters["guest"] = seen[1]
    for i, sp in enumerate(seen[2:], start=3):
        characters[f"cast{i}"] = sp
    return {"title": title, "characters": characters, "script": script}


def write_interview_yaml(interview: dict[str, Any], dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(
        yaml.safe_dump(interview, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )
    return dest


def render_episode(
    episode_path: Path,
    *,
    voices_path: Path = VOICES_PATH,
    work_dir: Path = WORK_DIR,
    dry_run: bool = False,
    open_tts_python: str | None = None,
) -> dict[str, Any]:
    voices = load_voice_map(voices_path)
    ep = yaml.safe_load(episode_path.read_text(encoding="utf-8"))
    if not isinstance(ep, dict):
        raise ValueError(f"episode must be a mapping: {episode_path}")
    interview = episode_to_interview(ep, voices)
    slug = str(ep.get("slug") or episode_path.stem)
    out_yaml = work_dir / f"{slug}.open-tts.yaml"
    write_interview_yaml(interview, out_yaml)
    result: dict[str, Any] = {
        "episode": str(episode_path),
        "interview_yaml": str(out_yaml),
        "voices": voices,
        "dry_run": dry_run,
    }
    if dry_run:
        return result
    py = open_tts_python or sys.executable
    cmd = [py, "-m", "open_tts", "render", str(out_yaml)]
    proc = subprocess.run(cmd, check=False)
    result["cmd"] = cmd
    result["returncode"] = proc.returncode
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    return result


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Render a campaign episode YAML via SimonBarnett/open-tts (FR-07)."
    )
    p.add_argument("episode", type=Path, help="Path to episodes/NN-*.yaml")
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Convert to open-tts YAML only; do not call TTS",
    )
    p.add_argument(
        "--python",
        dest="open_tts_python",
        default=None,
        help="Python that has open_tts installed (default: this interpreter)",
    )
    args = p.parse_args(argv)
    ep = args.episode
    if not ep.is_file():
        print(f"episode not found: {ep}", file=sys.stderr)
        return 1
    info = render_episode(
        ep, dry_run=args.dry_run, open_tts_python=args.open_tts_python
    )
    print(f"interview YAML -> {info['interview_yaml']}")
    if args.dry_run:
        print("dry-run: skipped python -m open_tts render")
        return 0
    print("render complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
