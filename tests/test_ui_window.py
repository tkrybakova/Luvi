import sys
import types
import unittest


class UIWindowTests(unittest.TestCase):
    def test_voice_level_percent_bounds(self) -> None:
        sys.modules.setdefault("requests", types.SimpleNamespace(post=lambda *_, **__: None))
        sys.modules.setdefault("mss", types.SimpleNamespace(mss=lambda: None))
        pyt = types.SimpleNamespace(pytesseract=types.SimpleNamespace(tesseract_cmd=""), image_to_string=lambda _: "")
        sys.modules.setdefault("pytesseract", pyt)
        pil = types.ModuleType("PIL")
        pil.Image = types.SimpleNamespace(open=lambda *_: None, frombytes=lambda *_, **__: None)
        sys.modules.setdefault("PIL", pil)
        sys.modules.setdefault("ddgs", types.SimpleNamespace(DDGS=object))
        sys.modules.setdefault(
            "simpleaudio",
            types.SimpleNamespace(WaveObject=types.SimpleNamespace(from_wave_file=lambda *_: None)),
        )

        from ui_window import LuviUI

        self.assertEqual(LuviUI._voice_level_percent(-1.0), 0.0)
        self.assertEqual(LuviUI._voice_level_percent(0.0), 0.0)
        self.assertEqual(LuviUI._voice_level_percent(0.02), 100.0)
        self.assertEqual(LuviUI._voice_level_percent(1.0), 100.0)


if __name__ == "__main__":
    unittest.main()
