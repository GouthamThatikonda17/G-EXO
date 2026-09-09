# brain/voice/text_to_speech.py
"""
=========================================================
Project G-EXO Text To Speech
Version : 2.5
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
    Production-ready Piper TTS wrapper with active playback interruption,
    generation invalidation tokens, and race-safe speech-end callbacks.
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

        # Generation and playback control tokens
        self._playback_generation = 0
        self._active_play_id = 0
        self._current_process: subprocess.Popen | None = None
        self._lock = threading.Lock()

        # Audio Execution Lifecycles
        self.on_speech_start = None
        self.on_speech_end = None
        self._shutdown = False
        self._worker = threading.Thread(
            target=self._worker_loop,
            daemon=True,
            name="PiperTTSWorker",
        )
        self._worker.start()

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

    def stop(self) -> None:
        """
        Flushes pending queue items, increments generation token to invalidate
        active generations/playbacks, and terminates active processes.
        """
        with self._lock:
            self._playback_generation += 1

        while True:
            try:
                self.queue.get_nowait()
                self.queue.task_done()
            except Empty:
                break

        with self._lock:
            if self._current_process is not None:
                try:
                    self._current_process.terminate()
                    self._current_process.kill()
                except Exception:
                    pass
                finally:
                    self._current_process = None

        if os.name == "nt":
            try:
                import winsound
                winsound.PlaySound(None, winsound.SND_ASYNC)
            except Exception:
                pass

    def shutdown(self) -> None:
        self._shutdown = True
        self.stop()
        self.queue.put("")
        self._worker.join(timeout=2)

    def _worker_loop(self) -> None:
        while not self._shutdown:
            text = self.queue.get()
            try:
                if text and not self._shutdown:
                    self._generate_and_play(text)
            except Exception as e:
                print(f"[TTS ERROR] {e}")
            finally:
                self.queue.task_done()

    def _generate_and_play(
        self,
        text: str,
    ) -> None:
        if self._shutdown:
            return

        with self._lock:
            gen_id = self._playback_generation

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

            # Check generation token validity before heavy subprocess call
            with self._lock:
                if self._playback_generation != gen_id or self._shutdown:
                    return

            process = subprocess.run(
                command,
                input=text,
                text=True,
                capture_output=True,
            )

            # Invalidate generated audio if generation token changed during subprocess run
            with self._lock:
                if self._playback_generation != gen_id or self._shutdown:
                    return

            if process.returncode != 0:
                raise RuntimeError(
                    process.stderr.strip()
                )

            if self.on_speech_start:
                try:
                    self.on_speech_start()
                except Exception as e:
                    print(f"[TTS Callback Error] on_speech_start: {e}")
            try:
                # Bind the authoritative generation ID internally before playing
                with self._lock:
                    self._active_play_id = gen_id

                # Strict 1-argument compatibility contract maintained
                self._play_audio(wav_path)
            finally:
                # Only invoke on_speech_end if generation token remained valid throughout playback
                with self._lock:
                    is_valid = (self._playback_generation == gen_id and not self._shutdown)

                if is_valid and self.on_speech_end:
                    try:
                        self.on_speech_end()
                    except Exception as e:
                        print(f"[TTS Callback Error] on_speech_end: {e}")
        finally:
            try:
                wav_path.unlink(missing_ok=True)
            except Exception:
                pass

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

    def _play_audio(
        self,
        wav: Path,
    ) -> None:
        if self._shutdown:
            return

        with self._lock:
            # Retrieve the internal generation token specifically bound for this playback
            expected_gen = self._active_play_id
            if self._playback_generation != expected_gen:
                return

        if os.name == "nt":
            import winsound
            try:
                winsound.PlaySound(
                    str(wav),
                    winsound.SND_FILENAME | winsound.SND_ASYNC,
                )
                import time
                import wave
                with wave.open(str(wav), 'r') as wf:
                    frames = wf.getnframes()
                    rate = wf.getframerate()
                    duration = frames / float(rate)

                start_time = time.time()
                while time.time() - start_time < duration + 0.2:
                    with self._lock:
                        if self._playback_generation != expected_gen or self._shutdown:
                            winsound.PlaySound(None, winsound.SND_ASYNC)
                            break
                    time.sleep(0.05)
            except Exception:
                with self._lock:
                    if self._playback_generation == expected_gen and not self._shutdown:
                        winsound.PlaySound(str(wav), winsound.SND_FILENAME)
            return

        players = [
            ["ffplay", "-nodisp", "-autoexit", str(wav)],
            ["aplay", str(wav)],
            ["afplay", str(wav)]
        ]

        for cmd in players:
            if shutil.which(cmd[0]):
                try:
                    with self._lock:
                        if self._playback_generation != expected_gen or self._shutdown:
                            return
                        self._current_process = subprocess.Popen(
                            cmd,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL
                        )
                    self._current_process.wait()
                except Exception:
                    pass
                finally:
                    with self._lock:
                        self._current_process = None
                return

        raise RuntimeError(
            "No supported audio player found."
        )
    def synthesize_bytes(self, text: str) -> bytes:
        """
        Synchronously generates and returns WAV audio bytes strictly for API/Client usage.
        Does not perform audio playback, does not touch playback queues, and does not fire
        speech lifecycle callbacks.
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

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
                input=text.strip(),
                text=True,
                capture_output=True,
            )
            if process.returncode != 0:
                raise RuntimeError(
                    process.stderr.strip() or "Piper synthesis failed."
                )

            return wav_path.read_bytes()
        finally:
            try:
                wav_path.unlink(missing_ok=True)
            except Exception:
                pass