"""
=========================================================
Project G-EXO
Text To Speech
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path
from queue import Empty, Queue


class TextToSpeech:
    """
    Production-ready Piper TTS wrapper.

    Features
    --------
    - Background worker thread
    - Speech queue
    - Auto-detect Piper executable
    - Auto-detect ONNX voice model
    - Cross-platform WAV playback
    - Graceful fallback to console output
    """

    def __init__(
        self,
        voice_model: str | Path = "voices/en_US-lessac-medium.onnx",
        piper_executable: str | Path = "piper/piper.exe",
    ) -> None:

        self.voice_model = Path(voice_model).resolve()

        self.voice_config = Path(
            str(self.voice_model) + ".json"
        ).resolve()

        self.piper = Path(piper_executable).resolve()

        self.queue: Queue[str] = Queue()

        self._shutdown = False

        self._worker = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name="PiperTTSWorker",
        )

        self._worker.start()

    # =====================================================
    # Public
    # =====================================================

    def speak(
        self,
        text: str,
    ) -> None:

        if not text:
            return

        text = str(text).strip()

        if not text:
            return

        print()
        print("G-EXO:", text)
        print()

        self.queue.put(text)

    # =====================================================
    # Stop
    # =====================================================

    def stop(self) -> None:

        while True:

            try:

                self.queue.get_nowait()
                self.queue.task_done()

            except Empty:

                break

    # =====================================================
    # Shutdown
    # =====================================================

    def shutdown(self) -> None:

        self._shutdown = True

        self.queue.put("")

        self._worker.join(timeout=2)

    # =====================================================
    # Worker
    # =====================================================

    def _worker_loop(self) -> None:

        while not self._shutdown:

            text = self.queue.get()

            try:

                if text:

                    self._generate_and_play(text)

            except Exception as e:

                print(f"[TTS ERROR] {e}")

            finally:

                self.queue.task_done()

    # =====================================================
    # Generate
    # =====================================================

    def _generate_and_play(
        self,
        text: str,
    ) -> None:

        if not self.voice_model.exists():

            raise FileNotFoundError(
                f"Voice model not found:\n{self.voice_model}"
            )

        if not self.voice_config.exists():

            raise FileNotFoundError(
                f"Voice config not found:\n{self.voice_config}"
            )

        piper = self._find_piper()

        if piper is None:

            raise FileNotFoundError(
                "Unable to locate Piper executable."
            )

        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False,
        ) as wav_file:

            wav_path = Path(wav_file.name)

        try:

            command = [

                str(piper),

                "--model",
                str(self.voice_model),

                "--output_file",
                str(wav_path),

            ]

            process = subprocess.run(

                command,

                input=text,

                text=True,

                capture_output=True,

            )

            if process.returncode != 0:

                raise RuntimeError(

                    process.stderr.strip()

                )

            self._play_audio(wav_path)

        finally:

            try:

                wav_path.unlink(missing_ok=True)

            except Exception:

                pass

    # =====================================================
    # Find Piper
    # =====================================================

    def _find_piper(self) -> Path | None:

        if self.piper.exists():

            return self.piper

        exe = shutil.which("piper")

        if exe:

            return Path(exe)

        exe = shutil.which("piper.exe")

        if exe:

            return Path(exe)

        return None

    # =====================================================
    # Audio Playback
    # =====================================================

    def _play_audio(
        self,
        wav: Path,
    ) -> None:

        if os.name == "nt":

            import winsound

            winsound.PlaySound(

                str(wav),

                winsound.SND_FILENAME,

            )

            return

        if shutil.which("ffplay"):

            subprocess.run(

                [

                    "ffplay",

                    "-nodisp",

                    "-autoexit",

                    str(wav),

                ],

                stdout=subprocess.DEVNULL,

                stderr=subprocess.DEVNULL,

            )

            return

        if shutil.which("aplay"):

            subprocess.run(

                [

                    "aplay",

                    str(wav),

                ],

                stdout=subprocess.DEVNULL,

                stderr=subprocess.DEVNULL,

            )

            return

        if shutil.which("afplay"):

            subprocess.run(

                [

                    "afplay",

                    str(wav),

                ],

                stdout=subprocess.DEVNULL,

                stderr=subprocess.DEVNULL,

            )

            return

        raise RuntimeError(
            "No supported audio player found."
        )