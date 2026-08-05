"""
=========================================================
Project G-EXO Wake Word Detector Version : 2.1
Developer : Thatikonda Goutham Teja
=========================================================
"""
from __future__ import annotations
from typing import Callable
import numpy as np
import openwakeword
from openwakeword.model import Model

class WakeWordDetector:
    def __init__(self):
        self.callback: Callable[[str], None] | None = None
        self.enabled = True
        self.threshold = 0.50
        
        # Download official openWakeWord pre-trained models if not present
        openwakeword.utils.download_models()
        
        self.model = Model(
            inference_framework="onnx",
        )

       
       

        self.model_names = list(
            self.model.models.keys()
        )

    # =====================================================
    # Callback
    # =====================================================
    def set_callback(
        self,
        callback,
    ):
        self.callback = callback

    # =====================================================
    # Enable
    # =====================================================
    def enable(self):
        self.enabled = True

    # =====================================================
    # Disable
    # =====================================================
    def disable(self):
        self.enabled = False

    # =====================================================
    # Process
    # =====================================================
    def process(
        self,
        audio,
    ):
    
        if not self.enabled:
            return
        if audio is None:
            return
        samples = np.frombuffer(
            audio,
            dtype=np.int16,
        )
        if samples.size == 0:
            return
        
        predictions = self.model.predict(
            samples,
        )
        

        
        if not predictions:
            return
        for wakeword, confidence in predictions.items():
            if confidence < self.threshold:
                continue
            print(
                f"[WakeWord] {wakeword} ({confidence:.2f})"
            )
            self.enabled = False
            try:
                if self.callback:
                    self.callback(
                        wakeword,
                    )
            finally:
                self.enabled = True
            break
