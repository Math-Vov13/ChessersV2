# All abstract classes
from abc import ABC, abstractmethod

class abstract_uis(ABC):
    def __init__(self) -> None: pass

    @abstractmethod
    def chooseGamemode(self) -> str: pass