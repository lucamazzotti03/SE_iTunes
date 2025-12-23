from dataclasses import dataclass


@dataclass
class Album:
    id: int
    title:str
    durata: int