import importlib
import sys
import types
import unittest


class TextToSpeechTests(unittest.TestCase):
    def test_reports_unavailable_when_piper_missing(self) -> None:
        sys.modules.setdefault(
            "simpleaudio",
            types.SimpleNamespace(WaveObject=types.SimpleNamespace(from_wave_file=lambda *_: None)),
        )

        if "text_to_speech" in sys.modules:
            del sys.modules["text_to_speech"]

        tts_module = importlib.import_module("text_to_speech")
        original_which = tts_module.shutil.which

        try:
            tts_module.shutil.which = lambda _bin: None  # type: ignore[assignment]
            tts = tts_module.TextToSpeech()
            self.assertFalse(tts.enabled)
            with self.assertRaises(tts_module.TTSUnavailableError):
                tts.speak("hello")
        finally:
            tts_module.shutil.which = original_which  # type: ignore[assignment]


if __name__ == "__main__":
    unittest.main()
