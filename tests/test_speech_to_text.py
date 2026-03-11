import importlib
import sys
import types
import unittest


class SpeechToTextLazyLoadTests(unittest.TestCase):
    def test_model_is_lazy_loaded(self) -> None:
        fake_module = types.ModuleType("faster_whisper")

        class FakeSegment:
            def __init__(self, text: str) -> None:
                self.text = text

        class FakeModel:
            called = 0
            last_kwargs = {}

            def __init__(self, *_args, **_kwargs) -> None:
                FakeModel.called += 1

            def transcribe(self, *_args, **kwargs):
                FakeModel.last_kwargs = kwargs
                return [FakeSegment("hello"), FakeSegment("world")], {}

        fake_module.WhisperModel = FakeModel
        sys.modules["faster_whisper"] = fake_module

        if "speech_to_text" in sys.modules:
            del sys.modules["speech_to_text"]

        speech_to_text = importlib.import_module("speech_to_text")
        stt = speech_to_text.SpeechToText("base")

        self.assertIsNone(stt.model)
        result = stt.transcribe_file("tmp.wav")
        self.assertEqual(result, "hello world")
        self.assertEqual(FakeModel.called, 1)
        self.assertEqual(FakeModel.last_kwargs["beam_size"], 1)
        self.assertTrue(FakeModel.last_kwargs["vad_filter"])
        self.assertIsNone(FakeModel.last_kwargs["language"])


if __name__ == "__main__":
    unittest.main()
