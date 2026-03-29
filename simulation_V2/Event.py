from dataclasses import dataclass
from typing import Optional


@dataclass
class Event:
    tournament_id: int
    event_id: int
    event_type: str
    winner: Optional[str] = None
    looser: Optional[str] = None
    rng: Optional[int] = None
    players: Optional[int] = None
    buy_in: Optional[float] = None
