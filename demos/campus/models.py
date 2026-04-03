from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Student:
    name: str
    trait: str
    location: str = "dorm"
    target: str | None = None
    travel_remaining: int = 0
    energy: int = 100
    max_energy: int = 100
    satiety: int = 100
    credits: int = 0
    health: int = 0
    mood: int = 0
    debuffs: set[str] = field(default_factory=set)
    achievements: set[str] = field(default_factory=set)
    study_hours: int = 0
    exercise_hours: int = 0
    no_debuff_streak: int = 0
    last_action: str = "idle"


@dataclass
class GameState:
    students: list[Student]
    hour_index: int = 0
    max_hours: int = 168
    log: list[str] = field(default_factory=list)

    @property
    def is_terminal(self) -> bool:
        return self.hour_index >= self.max_hours
