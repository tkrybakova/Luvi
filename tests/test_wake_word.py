import sys
import types
import unittest


class WakeWordTests(unittest.TestCase):
    def test_detect_and_strip_luvi_aliases(self) -> None:
        fake_stt_module = types.ModuleType("speech_to_text")

        class FakeSpeechToText:
            def transcribe_file(self, _):
                return ""

        fake_stt_module.SpeechToText = FakeSpeechToText
        sys.modules.setdefault("speech_to_text", fake_stt_module)

        import wake_word

        detector = wake_word.WakeWordDetector(("luvi", "луви"))
        self.assertTrue(detector.detect_in_text("Луви, открой браузер"))
        self.assertEqual(detector.remove_wake_word("Luvi, search black holes"), "search black holes")


if __name__ == "__main__":
    unittest.main()
