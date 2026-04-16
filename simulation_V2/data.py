from Event import Event
import pandas as pd
import random


# Uniquement la creation des events

def tournament_info(tournament) -> Event:
    event_id = tournament.event_id

    return Event(
        tournament_id=tournament.id,
        event_id=tournament.event_id,
        event_type="tournament_info",
        players=tournament.nbr_player,
        buy_in=tournament.buy_in
    )

def bust_event(tournament, p_win, p_loose) -> Event:
    event_id = tournament.event_id
    rng = random.randint(1, 100000)

    return Event(
        tournament_id=tournament.id,
        event_id=event_id,
        event_type="bust_event",
        winner=p_win,
        looser=p_loose,
        rng=rng,
    )

def winner_event(tournament, p_win) -> Event:
    event_id = tournament.event_id
    rng = random.randint(1, 100000)

    return Event(
        tournament_id=tournament.id,
        event_id=event_id,
        event_type="winner_event",
        winner=p_win,
        rng=rng,
    )