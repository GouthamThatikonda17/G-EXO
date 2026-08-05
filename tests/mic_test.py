import time
import numpy as np
import sounddevice as sd

def callback(indata, frames, time_info, status):
    if status:
        print(status)

    audio = np.asarray(indata).flatten()

    print(
        f"RMS={np.sqrt(np.mean(audio**2)):.5f} "
        f"MIN={audio.min():.4f} "
        f"MAX={audio.max():.4f}"
    )

with sd.InputStream(
    samplerate=16000,
    channels=1,
    dtype="float32",
    blocksize=1280,
    device=1,
    callback=callback,
):
    print("Speak normally...")
    while True:
        time.sleep(1)