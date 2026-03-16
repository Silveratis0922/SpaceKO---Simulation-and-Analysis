from Class import Tournament
import pandas as pd
import random


def data_collector(tournament: Tournament, index: int) -> pd.DataFrame:
    data = []

    for player in tournament.players:
        data.append({
            "name": player.name,
            "dotation": player.dotation,
            "gain": player.gain,
            "kill": player.kill,
            "token_lvl": player.token_lvl,
            "t_win": not player.eliminate
        })

    df = pd.DataFrame(data)
    df.set_index("name", inplace=True)
    df.columns = pd.MultiIndex.from_product(
        [[f"Tournament {index}"], df.columns]
    )
    return df

# Uniquement la creation des events
def tournament_info(tournament) -> list:

    return[{
        "tournament_id" : tournament.id,
        "event_id": tournament.event_id,
        "event_type": "Tournament_info",
        "winner": None,
        "looser": None,
        "rng": None,
        "players": tournament.nbr_player,
        "buy_in": tournament.buy_in
    }]

def bust_event(tournament, p_win, p_loose) -> list:
    event_id = tournament.event_id
    rng = random.randint(1, 100000)

    return [{
        "tournament_id": tournament.id,
        "event_id": event_id,
        "event_type": "Bust event",
        "winner": p_win,
        "looser": p_loose,
        "rng": rng,
        "players": None,
        "buy_in": None
    }]

def winner_event(tournament, p_win) -> list:
    event_id = tournament.event_id
    rng = random.randint(1, 100000)

    return[{
        "tournament_id": tournament.id,
        "event_id": event_id,
        "event_type": "Winner event",
        "winner": p_win,
        "looser": None,
        "rng": rng,
        "players": None,
        "buy_in": None
    }]

def new_event(tournament, p_win, p_loose=None) -> pd.DataFrame:
    event_id = tournament.event_id
    data = []

    if event_id == 0 :
    {
        data = tournament_info(tournament)
        tournament.event_id += 1
    }
    else if event_id == tournament.nbr_player :
        data = winner_event(tournament, p_win)
        tournament.event_id = 0 #On securise mais pas besoin normalement
    else :
    {
        data = bust_event(tournament, p_win, p_loose)
        tournament.event_id += 1
    }

    df = pd.DataFrame(data)
    df.set_index("tournament_id", inplace=True)

    return df