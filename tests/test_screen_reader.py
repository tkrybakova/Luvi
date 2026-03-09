import importlib
import sys
import types
import unittest
from pathlib import Path


class ScreenReaderTests(unittest.TestCase):
    def test_read_screen_text_handles_missing_tesseract(self) -> None:
        sys.modules["mss"] = types.SimpleNamespace(mss=lambda: None)

        class FakePytInner:
            tesseract_cmd = ""

            class TesseractNotFoundError(Exception):
                pass

        fake_pyt = types.SimpleNamespace(
            pytesseract=FakePytInner,
            image_to_string=lambda _img: (_ for _ in ()).throw(FileNotFoundError("tesseract missing")),
        )
        sys.modules["pytesseract"] = fake_pyt

        pil = types.ModuleType("PIL")
        pil.Image = types.SimpleNamespace(open=lambda _p: object(), frombytes=lambda *_, **__: object())
        sys.modules["PIL"] = pil

        if "screen_reader" in sys.modules:
            del sys.modules["screen_reader"]

        screen_reader = importlib.import_module("screen_reader")
        reader = screen_reader.ScreenReader()
        reader.capture_screen = lambda: Path("dummy.png")  # type: ignore[method-assign]

        text = reader.read_screen_text()
        self.assertEqual(text, "")
        self.assertTrue(reader.last_ocr_error)


if __name__ == "__main__":
    unittest.main()
