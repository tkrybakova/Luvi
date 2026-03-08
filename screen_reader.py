"""Screen capture + OCR helpers."""

from pathlib import Path

import mss
import pytesseract
from PIL import Image

import config


class ScreenReader:
    """Captures the current screen and extracts OCR text."""

    def __init__(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD

    def capture_screen(self, output_path: Path = Path("latest_screen.png")) -> Path:
        """Capture primary monitor screenshot and return saved image path."""
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            image = sct.grab(monitor)
            img = Image.frombytes("RGB", image.size, image.rgb)
            img.save(output_path)
        return output_path

    def read_screen_text(self) -> str:
        """Capture and OCR the screen text."""
        screenshot = self.capture_screen()
        image = Image.open(screenshot)
        return pytesseract.image_to_string(image).strip()
