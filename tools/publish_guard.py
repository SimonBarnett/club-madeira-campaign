#!/usr/bin/env python3
"""Refuse to schedule an episode unless approved: true — FR-26 / issue #27."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode", type=Path)
    args = parser.parse_args()
    data = yaml.safe_load(args.episode.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("approved") is not True:
        print(f"publish-guard: refuse {args.episode} (approved is not true)")
        return 1
    print(f"publish-guard: {args.episode} approved")
    return 0


if __name__ == "__main__":
    sys.exit(main())
