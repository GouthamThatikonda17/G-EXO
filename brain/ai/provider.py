"""
=========================================================
Project G-EXO
AI Provider Interface
Version : 2.0
Developer : Thatikonda Goutham Teja
=========================================================
"""

from abc import ABC, abstractmethod


class AIProvider(ABC):

    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass