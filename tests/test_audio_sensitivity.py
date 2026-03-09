import importlib
import unittest


class AudioSensitivityConfigTests(unittest.TestCase):
    def test_default_sensitivity_and_gains(self) -> None:
        config = importlib.import_module("config")
        self.assertLessEqual(config.MIN_AUDIO_RMS, 0.002)
        self.assertGreater(config.WAKE_AUDIO_GAIN, 1.0)
        self.assertGreater(config.COMMAND_AUDIO_GAIN, 1.0)


if __name__ == "__main__":
    unittest.main()
