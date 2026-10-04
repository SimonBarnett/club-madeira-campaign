#!/usr/bin/env python3
"""FR-08: build ffmpeg command lines for 9:16, 1:1, 15s hook with burned captions.

No media binaries are written into git. Default output dir is exports/<slug>/ (gitignored).
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

FEED_W, FEED_H = 1080, 1920
SQUARE = 1080
DEFAULT_HOOK_S = 15.0

REPO_ROOT = Path(__file__).resolve().parents[1]


def escape_subtitles_path(path: Path) -> str:
    """Escape a filesystem path for ffmpeg subtitles= filter."""
    s = path.resolve().as_posix()
    # ffmpeg filter: escape \ : '
    s = s.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
    return s


def vf_feed(captions: Path) -> str:
    cap = escape_subtitles_path(captions)
    return (
        f"scale={FEED_W}:{FEED_H}:force_original_aspect_ratio=decrease,"
        f"pad={FEED_W}:{FEED_H}:(ow-iw)/2:(oh-ih)/2:black,"
        f"subtitles='{cap}'"
    )


def vf_square(captions: Path) -> str:
    cap = escape_subtitles_path(captions)
    return (
        f"scale={SQUARE}:{SQUARE}:force_original_aspect_ratio=increase,"
        f"crop={SQUARE}:{SQUARE},"
        f"subtitles='{cap}'"
    )


def build_commands(
    *,
    master: Path,
    captions: Path,
    out_dir: Path,
    slug: str,
    hook_seconds: float = DEFAULT_HOOK_S,
    ffmpeg_bin: str = "ffmpeg",
) -> list[list[str]]:
    """Return ffmpeg argv lists: feed 9:16, square 1:1, 15s hook (9:16)."""
    out_dir = out_dir.resolve()
    feed = out_dir / f"{slug}_1080x1920.mp4"
    square = out_dir / f"{slug}_1080x1080.mp4"
    hook = out_dir / f"{slug}_hook_{int(hook_seconds)}s_1080x1920.mp4"

    common_out = ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-movflags", "+faststart"]

    cmds: list[list[str]] = [
        [
            ffmpeg_bin,
            "-y",
            "-i",
            str(master.resolve()),
            "-vf",
            vf_feed(captions),
            *common_out,
            str(feed),
        ],
        [
            ffmpeg_bin,
            "-y",
            "-i",
            str(master.resolve()),
            "-vf",
            vf_square(captions),
            *common_out,
            str(square),
        ],
        [
            ffmpeg_bin,
            "-y",
            "-i",
            str(master.resolve()),
            "-ss",
            "0",
            "-t",
            str(hook_seconds),
            "-vf",
            vf_feed(captions),
            *common_out,
            str(hook),
        ],
    ]
    return cmds


def format_cmd(argv: list[str]) -> str:
    parts = []
    for a in argv:
        if any(ch.isspace() for ch in a) or a.startswith("-vf"):
            parts.append(f'"{a}"' if " " in a else a)
        else:
            parts.append(a)
    # Always quote -vf payload
    out = []
    i = 0
    while i < len(argv):
        if argv[i] == "-vf" and i + 1 < len(argv):
            out.append("-vf")
            out.append("'" + argv[i + 1].replace("'", "'\\''") + "'")
            i += 2
            continue
        p = argv[i]
        if " " in p:
            out.append(f'"{p}"')
        else:
            out.append(p)
        i += 1
    return " ".join(out)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="FR-08 ffmpeg export pack (9:16, 1:1, 15s hook, burned captions)")
    p.add_argument("--master", type=Path, required=True, help="Master episode mp4/mov")
    p.add_argument("--captions", type=Path, required=True, help="Caption sidecar .srt or .ass")
    p.add_argument("--slug", required=True, help="Episode slug for output file names")
    p.add_argument(
        "--out-dir",
        type=Path,
        default=None,
        help="Output directory (default: <repo>/exports/<slug>/)",
    )
    p.add_argument("--hook-seconds", type=float, default=DEFAULT_HOOK_S)
    p.add_argument("--ffmpeg", default="ffmpeg", help="ffmpeg binary name or path")
    p.add_argument("--dry-run", action="store_true", help="Print commands only; do not run ffmpeg")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    out_dir = args.out_dir or (REPO_ROOT / "exports" / args.slug)
    if not args.dry_run:
        if not args.master.is_file():
            print(f"error: master not found: {args.master}", file=sys.stderr)
            return 2
        if not args.captions.is_file():
            print(f"error: captions not found: {args.captions}", file=sys.stderr)
            return 2
        if shutil.which(args.ffmpeg) is None and not Path(args.ffmpeg).is_file():
            print(f"error: ffmpeg not on PATH: {args.ffmpeg}", file=sys.stderr)
            return 2

    cmds = build_commands(
        master=args.master,
        captions=args.captions,
        out_dir=out_dir,
        slug=args.slug,
        hook_seconds=args.hook_seconds,
        ffmpeg_bin=args.ffmpeg,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    for cmd in cmds:
        line = format_cmd(cmd)
        print(line)
        if args.dry_run:
            continue
        subprocess.run(cmd, check=True)
    if args.dry_run:
        print(f"# dry-run ok → would write under {out_dir}")
    else:
        print(f"# wrote exports under {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
