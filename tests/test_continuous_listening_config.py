import importlib
import unittest


class ContinuousListeningConfigTests(unittest.TestCase):
    def test_continuous_capture_settings(self) -> None:
        config = importlib.import_module("config")
        self.assertGreater(config.COMMAND_CHUNK_SECONDS, 0)
        self.assertGreaterEqual(config.COMMAND_MIN_SECONDS, config.COMMAND_CHUNK_SECONDS)
        self.assertGreater(config.COMMAND_MAX_SECONDS, config.COMMAND_MIN_SECONDS)
        self.assertGreater(config.COMMAND_SILENCE_SECONDS, 0)


if __name__ == "__main__":
    unittest.main()
