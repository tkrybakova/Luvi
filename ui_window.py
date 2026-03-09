"""Tkinter desktop UI for Luvi."""

from __future__ import annotations

import queue
import threading
import tkinter as tk
from tkinter import scrolledtext, ttk

import config
from assistant_brain import AssistantBrain
from text_to_speech import TextToSpeech


class LuviUI:
    """Styled purple desktop UI with conversation history and text input."""

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title(config.WINDOW_TITLE)
        self.root.geometry("1020x700")
        self.root.configure(bg=config.UI_BG)

        self.brain = AssistantBrain()
        self.tts = TextToSpeech()
        self.messages: "queue.Queue[tuple[str, str]]" = queue.Queue()

        self._voice_start = None
        self._voice_stop = None
        self._voice_running = None

        self._build_layout()
        self.root.after(100, self._drain_messages)

    def set_voice_controls(self, start_fn, stop_fn, running_fn) -> None:
        """Attach callbacks so UI can start/stop continuous listening."""
        self._voice_start = start_fn
        self._voice_stop = stop_fn
        self._voice_running = running_fn
        self._sync_mic_button()

    def _build_layout(self) -> None:
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Purple.Horizontal.TProgressbar",
            troughcolor=config.UI_SURFACE,
            bordercolor=config.UI_SURFACE,
            background=config.UI_ACCENT,
            lightcolor=config.UI_ACCENT,
            darkcolor=config.UI_ACCENT,
        )

        header = tk.Frame(self.root, bg=config.UI_PANEL, height=92, highlightthickness=1, highlightbackground="#4c1d95")
        header.pack(fill="x", padx=14, pady=(14, 10))

        title = tk.Label(
            header,
            text="💜 Luvi Assistant",
            bg=config.UI_PANEL,
            fg=config.UI_TEXT,
            font=("Segoe UI", 20, "bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=14, pady=(10, 0))

        self.status_label = tk.Label(
            header,
            text="Starting Luvi...",
            bg=config.UI_PANEL,
            fg=config.UI_TEXT_MUTED,
            font=("Segoe UI", 10),
            anchor="w",
        )
        self.status_label.grid(row=1, column=0, sticky="we", padx=14, pady=(0, 10))

        self.mic_button = tk.Button(
            header,
            text="🎙️ Stop listening",
            command=self._toggle_voice_listener,
            bg=config.UI_ACCENT,
            fg="white",
            relief="flat",
            activebackground=config.UI_ACCENT_ALT,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=8,
            cursor="hand2",
        )
        self.mic_button.grid(row=0, column=1, rowspan=2, sticky="e", padx=14)
        header.grid_columnconfigure(0, weight=1)

        info_row = tk.Frame(self.root, bg=config.UI_BG)
        info_row.pack(fill="x", padx=14, pady=(0, 10))

        self.intent_label = tk.Label(
            info_row,
            text="Last recognized command: -",
            bg=config.UI_SURFACE,
            fg=config.UI_TEXT,
            font=("Segoe UI", 10),
            anchor="w",
            padx=12,
            pady=8,
        )
        self.intent_label.pack(fill="x")

        meter_row = tk.Frame(self.root, bg=config.UI_BG)
        meter_row.pack(fill="x", padx=14, pady=(0, 10))

        tk.Label(
            meter_row,
            text="Voice level",
            bg=config.UI_BG,
            fg=config.UI_TEXT_MUTED,
            font=("Segoe UI", 9),
        ).pack(anchor="w")

        self.voice_level = tk.DoubleVar(value=0.0)
        self.level_bar = ttk.Progressbar(
            meter_row,
            style="Purple.Horizontal.TProgressbar",
            orient="horizontal",
            mode="determinate",
            maximum=100,
            variable=self.voice_level,
        )
        self.level_bar.pack(fill="x", pady=(4, 0))

        actions_row = tk.Frame(self.root, bg=config.UI_BG)
        actions_row.pack(fill="x", padx=14, pady=(0, 10))

        quick_actions = [
            "What is on my screen?",
            "Summarize this page",
            "Search latest AI news",
        ]
        for action in quick_actions:
            btn = tk.Button(
                actions_row,
                text=action,
                command=lambda a=action: self._send_quick_action(a),
                bg=config.UI_SURFACE,
                fg=config.UI_TEXT,
                relief="flat",
                activebackground=config.UI_ACCENT_ALT,
                activeforeground="white",
                font=("Segoe UI", 9),
                padx=10,
                pady=6,
                cursor="hand2",
            )
            btn.pack(side="left", padx=(0, 8))

        chat_frame = tk.Frame(self.root, bg=config.UI_BG)
        chat_frame.pack(fill="both", expand=True, padx=14, pady=(0, 10))

        self.chat = scrolledtext.ScrolledText(
            chat_frame,
            state="disabled",
            wrap=tk.WORD,
            bg=config.UI_PANEL,
            fg=config.UI_TEXT,
            insertbackground=config.UI_TEXT,
            relief="flat",
            font=("Segoe UI", 11),
            padx=12,
            pady=12,
            selectbackground="#6d28d9",
        )
        self.chat.pack(fill="both", expand=True)

        input_row = tk.Frame(self.root, bg=config.UI_BG)
        input_row.pack(fill="x", padx=14, pady=(0, 14))

        self.entry = tk.Entry(
            input_row,
            bg=config.UI_PANEL,
            fg=config.UI_TEXT,
            insertbackground=config.UI_TEXT,
            relief="flat",
            font=("Segoe UI", 12),
            highlightthickness=1,
            highlightbackground="#4c1d95",
            highlightcolor=config.UI_ACCENT,
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=11)
        self.entry.bind("<Return>", lambda _: self.submit_text())

        send_button = tk.Button(
            input_row,
            text="Send",
            command=self.submit_text,
            bg=config.UI_ACCENT,
            fg="white",
            relief="flat",
            activebackground=config.UI_ACCENT_ALT,
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            padx=18,
            pady=10,
            cursor="hand2",
        )
        send_button.pack(side="right", padx=(10, 0))

    def _send_quick_action(self, action: str) -> None:
        self.append_chat("You", action)
        self.messages.put(("process", action))

    def _sync_mic_button(self) -> None:
        running = self._voice_running() if self._voice_running else True
        if running:
            self.mic_button.config(text="🎙️ Stop listening", bg=config.UI_ACCENT)
        else:
            self.mic_button.config(text="🎙️ Start listening", bg="#475569")

    def _toggle_voice_listener(self) -> None:
        if not self._voice_start or not self._voice_stop or not self._voice_running:
            return

        if self._voice_running():
            self._voice_stop()
            self.messages.put(("status", "Voice listening paused."))
        else:
            self._voice_start()
            self.messages.put(("status", "Voice listening resumed."))

        self._sync_mic_button()

    def append_chat(self, speaker: str, text: str) -> None:
        self.chat.config(state="normal")
        if speaker.startswith("You"):
            self.chat.insert(tk.END, f"🧑 You\n{text}\n\n")
        else:
            self.chat.insert(tk.END, f"🤖 Luvi\n{text}\n\n")
        self.chat.config(state="disabled")
        self.chat.see(tk.END)

    def set_status(self, text: str) -> None:
        self.status_label.config(text=text)

    def set_intent(self, intent: str) -> None:
        self.intent_label.config(text=f"Last recognized command: {intent}")

    def set_voice_level(self, rms: float) -> None:
        # 0.02 ~= loud speech in normalized RMS range for most laptop mics
        percent = min(100.0, max(0.0, (rms / 0.02) * 100.0))
        self.voice_level.set(percent)

    def submit_text(self) -> None:
        text = self.entry.get().strip()
        if not text:
            return
        self.entry.delete(0, tk.END)
        self.append_chat("You", text)
        self.messages.put(("process", text))

    def on_voice_command(self, text: str) -> None:
        self.messages.put(("voice", text))

    def on_voice_status(self, text: str) -> None:
        self.messages.put(("status", text))

    def on_voice_level(self, rms: float) -> None:
        self.messages.put(("level", str(rms)))

    def _process_input(self, text: str, from_voice: bool = False) -> None:
        if from_voice:
            self.append_chat("You (voice)", text)

        def worker() -> None:
            intent, response = self.brain.handle(text)
            self.messages.put(("intent", intent))
            self.messages.put(("assistant", response))
            try:
                self.tts.speak(response)
            except Exception as exc:
                self.messages.put(("assistant", f"TTS error: {exc}"))

        threading.Thread(target=worker, daemon=True).start()

    def _drain_messages(self) -> None:
        while not self.messages.empty():
            msg_type, payload = self.messages.get()
            if msg_type == "status":
                self.set_status(payload)
                self._sync_mic_button()
            elif msg_type == "voice":
                self._process_input(payload, from_voice=True)
            elif msg_type == "process":
                self._process_input(payload, from_voice=False)
            elif msg_type == "assistant":
                self.append_chat("Luvi", payload)
            elif msg_type == "intent":
                self.set_intent(payload)
            elif msg_type == "level":
                self.set_voice_level(float(payload))

        self.root.after(100, self._drain_messages)

    def run(self) -> None:
        self.root.mainloop()
