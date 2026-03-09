import sys
import types
import unittest


class AssistantBrainTests(unittest.TestCase):
    def _stub_runtime_modules(self) -> None:
        sys.modules.setdefault("requests", types.SimpleNamespace(post=lambda *_, **__: None))
        sys.modules.setdefault("mss", types.SimpleNamespace(mss=lambda: None))
        pyt = types.SimpleNamespace(pytesseract=types.SimpleNamespace(tesseract_cmd=""), image_to_string=lambda _: "")
        sys.modules.setdefault("pytesseract", pyt)
        pil = types.ModuleType("PIL")
        pil.Image = types.SimpleNamespace(open=lambda *_: None, frombytes=lambda *_, **__: None)
        sys.modules.setdefault("PIL", pil)
        sys.modules.setdefault("ddgs", types.SimpleNamespace(DDGS=object))

    def test_safe_llm_returns_error_message(self) -> None:
        self._stub_runtime_modules()
        from assistant_brain import AssistantBrain

        brain = AssistantBrain()

        def fail(_: str) -> str:
            raise RuntimeError("connection refused")

        brain.generate_llm_response = fail  # type: ignore[method-assign]
        message = brain._safe_llm("hello")
        self.assertIn("could not reach Ollama", message)

    def test_screen_without_ocr_and_vision_config(self) -> None:
        self._stub_runtime_modules()
        from assistant_brain import AssistantBrain

        brain = AssistantBrain()
        brain.screen_reader.read_screen_text = lambda: ""  # type: ignore[method-assign]
        brain.screen_reader.last_ocr_error = "tesseract missing"
        intent, message = brain.handle("what is on my screen")
        self.assertEqual(intent, "screen")
        self.assertIn("tesseract", message.lower())
        self.assertIn("ollama_vision_model", message.lower())


if __name__ == "__main__":
    unittest.main()
