"""Screen capture + OCR helpers."""

from __future__ import annotations

import base64
from pathlib import Path

import mss
import pytesseract
from PIL import Image

import config


class ScreenReader:
    """Captures the current screen and extracts OCR text."""

    def __init__(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = config.TESSERACT_CMD
        self.last_ocr_error: str = ""

    def capture_screen(self, output_path: Path = Path("latest_screen.png")) -> Path:
        """Capture primary monitor screenshot and return saved image path."""
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            image = sct.grab(monitor)
            img = Image.frombytes("RGB", image.size, image.rgb)
            img.save(output_path)
        return output_path

    def read_screen_text(self) -> str:
        """Capture and OCR the screen text; return empty string on OCR backend failure."""
        screenshot = self.capture_screen()
        image = Image.open(screenshot)

        try:
            self.last_ocr_error = ""
            return pytesseract.image_to_string(image).strip()
        except pytesseract.pytesseract.TesseractNotFoundError as exc:
            self.last_ocr_error = str(exc)
            return ""
        except FileNotFoundError as exc:
            self.last_ocr_error = str(exc)
            return ""

    def capture_screen_base64(self) -> str:
        """Capture screenshot and return base64-encoded image for multimodal LLMs."""
        screenshot = self.capture_screen()
        return base64.b64encode(screenshot.read_bytes()).decode("utf-8")
