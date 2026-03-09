import importlib
import unittest


class MicrophoneRecoveryConfigTests(unittest.TestCase):
    def test_microphone_recovery_defaults(self) -> None:
        config = importlib.import_module("config")
        self.assertGreaterEqual(config.AUDIO_MAX_RETRIES, 1)
        self.assertGreater(config.AUDIO_RETRY_SECONDS, 0)
        self.assertIsInstance(config.INPUT_DEVICE_HINT, str)


if __name__ == "__main__":
    unittest.main()
