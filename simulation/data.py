from Class import Tournament
import pandas as pd


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
