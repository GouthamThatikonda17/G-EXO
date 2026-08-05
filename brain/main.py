"""
=========================================================
Project G-EXO Main Bootstrap
Version : 2.3
Developer : Thatikonda Goutham Teja
=========================================================
"""
import time
from runtime.voice_runtime import VoiceRuntime

def main() -> None:
    """
    Explicit production bootstrap function.
    Initializes and starts the VoiceRuntime lifecycle cleanly
    without any import-time side effects or embedded HTTP servers,
    utilizing a low-CPU keep-alive loop and graceful resource cleanup.
    """
    runtime = VoiceRuntime()
    try:
        runtime.start()
        while True:
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n[Runtime] Shutting down...")
    finally:
        runtime.stop()

if __name__ == "__main__":
    main()
