import importlib
import unittest


class ConfigTests(unittest.TestCase):
    def test_min_audio_rms_is_lowered(self) -> None:
        config = importlib.import_module("config")
        self.assertLessEqual(config.MIN_AUDIO_RMS, 0.005)


if __name__ == "__main__":
    unittest.main()
