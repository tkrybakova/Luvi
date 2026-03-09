import types
import sys
import unittest


class AssistantBrainTests(unittest.TestCase):
    def test_safe_llm_returns_error_message(self) -> None:
        # Stub third-party modules so this test can run without full runtime deps.
        sys.modules.setdefault("requests", types.SimpleNamespace(post=lambda *_, **__: None))
        sys.modules.setdefault("mss", types.SimpleNamespace(mss=lambda: None))
        pyt = types.SimpleNamespace(pytesseract=types.SimpleNamespace(tesseract_cmd=""), image_to_string=lambda _: "")
        sys.modules.setdefault("pytesseract", pyt)
        pil = types.ModuleType("PIL")
        pil.Image = types.SimpleNamespace(open=lambda *_: None, frombytes=lambda *_, **__: None)
        sys.modules.setdefault("PIL", pil)
        sys.modules.setdefault("duckduckgo_search", types.SimpleNamespace(DDGS=object))

        from assistant_brain import AssistantBrain

        brain = AssistantBrain()

        def fail(_: str) -> str:
            raise RuntimeError("connection refused")

        brain.generate_llm_response = fail  # type: ignore[method-assign]
        message = brain._safe_llm("hello")
        self.assertIn("could not reach Ollama", message)


if __name__ == "__main__":
    unittest.main()
