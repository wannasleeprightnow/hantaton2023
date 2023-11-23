from dataclasses import dataclass

@dataclass
class Event:
    date: str
    title: str
    link: str


@dataclass
class News:
    date: str
    title: str
    link: str
