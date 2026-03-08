"""Entrypoint for running the Luvi local AI assistant."""

from ui_window import LuviUI
from voice_listener import VoiceListener


def main() -> None:
    ui = LuviUI()

    listener = VoiceListener(
        on_command=ui.on_voice_command,
        on_status=ui.on_voice_status,
    )
    listener.start()

    try:
        ui.run()
    finally:
        listener.stop()


if __name__ == "__main__":
    main()
