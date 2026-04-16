from Event import Event
from data import tournament_info, bust_event, winner_event
import random


class Player():
    def __init__(self, name, entry) -> None:
        self.name = name
        self.eliminate = False

    def bust(self) -> None:
        self.eliminate = True

    def __str__(self) -> str:
        if self.eliminate:
            return (
                f"Je m'appelle {self.name} et ma dotation est de "
                f"{self.dotation:.2f} euro. J'ai un token de niveau "
                f"{self.token_lvl} J'ai gagne {self.gain:.2f} et eliminer "
                f"{self.kill} joueurs. Je suis eliminer. ❌"
            )
        else:
            return (
                f"Je m'appelle {self.name} et ma dotation est de "
                f"{self.dotation:.2f} euro. J'ai un token de niveau "
                f"{self.token_lvl} J'ai gagne {self.gain:.2f} et eliminer "
                f"{self.kill} joueurs. Je suis encore en lice.✔️"
            )


class Table():
    def __init__(self, id) -> None:
        self.id = id
        self.players = []

    def __str__(self) -> str:
        infos = "\n".join(str(player) for player in self.players)
        return (
            f"La table #{self.id} contient {len(self.players)} joueurs. "
            f"Voici les donnees de chaque joueurs a la table : \n"
            f"{infos}"
            f"\n"
        )


class Tournament():
    def __init__(self, id, nbr_player, buy_in) -> None:
        self.id = id
        self.event_id = 0
        self.nbr_player = nbr_player
        self.buy_in = buy_in
        self.players = self.create_players()
        self.tables = []
        self.finish = False
        self.events: list[Event] = []

    def create_players(self) -> list:
        return [
            Player(f"Player {i + 1}", self.buy_in)
            for i in range(self.nbr_player)
            ]

    def create_tables(self, tf=False) -> None:
        self.tables.clear()
        random.shuffle(self.players)
        table_id = 0
        seat = 6 if not tf else 7
        for player in self.players:
            if not player.eliminate:
                if not self.tables or len(self.tables[-1].players) == seat:
                    table_id += 1
                    self.tables.append(Table(table_id))
                self.tables[-1].players.append(player)

    def winner_annoncement(self, id) -> str:
        for player in self.tables[0].players:
            if not player.eliminate:
                return (
                    f"Le gagnant du tourois est {player.name}."
                )

    def run(self) -> list[Event]:
        self.events.append(tournament_info(self))
        self.event_id += 1
        while not self.finish:
            if self.nbr_player > 7:
                self.create_tables()
            else:
                self.create_tables(True)
            for table in self.tables:
                if len(table.players) > 1:
                    win, lost = random.sample(range(len(table.players)), 2)
                    self.simulator(table.players[win], table.players[lost])
                elif self.nbr_player == 1:
                    self.simulator(self.tables[0].players[0])

        return self.events

    def simulator(self, p_winner, p_looser=None) -> Event:
        if self.nbr_player > 1 and not p_looser == None: #Bust_event
            event = bust_event(self, p_winner.name, p_looser.name)
            self.events.append(event)
            p_looser.bust()
        elif self.nbr_player == 1: #Winner_event
            event = winner_event(self, p_winner.name)
            self.events.append(event)
            self.end()
        self.nbr_player -= 1
        self.event_id += 1

    def end(self) -> str:
        self.finish = True

    def __str__(self) -> str:
        return (
            f"Le tournois contient {len(self.players)} joueurs et le prix "
            f"d'entree est de {self.entry} euro."
        )
