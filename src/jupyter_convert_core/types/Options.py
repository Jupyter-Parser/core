from dataclasses import dataclass


@dataclass
class Section:
    width: int = 210
    height: int = 297
    top: int = 20
    right: int = 15
    bottom: int = 20
    left: int = 30
