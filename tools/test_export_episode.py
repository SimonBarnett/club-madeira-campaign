"""Unit tests for FR-08 export_episode (no ffmpeg required)."""
from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import export_episode as ex


class TestExportEpisode(unittest.TestCase):
    def test_escape_subtitles_path_posix_and_drive(self):
        with tempfile.TemporaryDirectory() as td:
            cap = Path(td) / "ep01.srt"
            cap.write_text("1\n00:00:00,000 --> 00:00:01,000\nHi\n", encoding="utf-8")
            esc = ex.escape_subtitles_path(cap)
            self.assertTrue(esc.endswith("ep01.srt"))
            # ffmpeg wants forward slashes; drive colon escaped as \:
            self.assertNotIn("\\Users", esc)
            if esc[0].isalpha() and len(esc) > 2:
                self.assertTrue(esc[1:3] == "\\:" or ":" not in esc[:3])

    def test_build_commands_shapes_and_outputs(self):
        master = Path("master.mp4")
        captions = Path("captions.srt")
        out = Path("exports") / "01-demo"
        cmds = ex.build_commands(
            master=master,
            captions=captions,
            out_dir=out,
            slug="01-demo",
            hook_seconds=15,
            ffmpeg_bin="ffmpeg",
        )
        self.assertEqual(len(cmds), 3)
        feed, square, hook = cmds
        self.assertEqual(feed[0], "ffmpeg")
        self.assertIn("1080:1920", feed[feed.index("-vf") + 1])
        self.assertTrue(str(feed[-1]).endswith("01-demo_1080x1920.mp4"))
        self.assertIn("1080:1080", square[square.index("-vf") + 1])
        self.assertTrue(str(square[-1]).endswith("01-demo_1080x1080.mp4"))
        self.assertEqual(hook[hook.index("-t") + 1], "15")
        self.assertTrue(str(hook[-1]).endswith("01-demo_hook_15s_1080x1920.mp4"))
        for cmd in cmds:
            vf = cmd[cmd.index("-vf") + 1]
            self.assertIn("subtitles=", vf)

    def test_dry_run_main_prints_without_ffmpeg(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            master = td_path / "m.mp4"
            captions = td_path / "c.srt"
            master.write_bytes(b"not-a-real-mp4")
            captions.write_text("1\n00:00:00,000 --> 00:00:01,000\nx\n", encoding="utf-8")
            out = td_path / "out"
            rc = ex.main(
                [
                    "--master",
                    str(master),
                    "--captions",
                    str(captions),
                    "--slug",
                    "01-demo",
                    "--out-dir",
                    str(out),
                    "--dry-run",
                ]
            )
            self.assertEqual(rc, 0)

    def test_missing_master_fails_when_not_dry_run(self):
        rc = ex.main(
            [
                "--master",
                "missing-master.mp4",
                "--captions",
                "missing.srt",
                "--slug",
                "x",
            ]
        )
        self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
