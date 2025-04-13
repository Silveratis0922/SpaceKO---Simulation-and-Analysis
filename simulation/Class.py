from utils import simulator
import random


class Player():
    def __init__(self, name, entry) -> None:
        self.name = name
        self.entry = entry
        self.dotation = entry / 2
        self.gain = 0
        self.token_lvl = 1
        self.kill = 0
        self.eliminate = False

    def bust(self) -> None:
        self.eliminate = True

    def checking_token(self) -> None:
        dotation = self.dotation
        entry = self.entry
        if dotation >= entry / 2 and dotation < entry * 0.6:
            self.token_lvl = 1
        elif dotation >= entry * 0.6 and dotation < entry * 0.75:
            self.token_lvl = 2
        elif dotation >= entry * 0.75 and dotation < entry:
            self.token_lvl = 3
        elif dotation >= entry and dotation < entry * 1.5:
            self.token_lvl = 4
        elif dotation >= entry * 1.5 and dotation < entry * 2.5:
            self.token_lvl = 5
        elif dotation >= entry * 2.5 and dotation < entry * 5:
            self.token_lvl = 6
        elif dotation >= entry * 5 and dotation < entry * 10:
            self.token_lvl = 7
        elif dotation >= entry * 10 and dotation < entry * 20:
            self.token_lvl = 8
        elif dotation >= entry * 20 and dotation < entry * 50:
            self.token_lvl = 9
        elif dotation >= entry * 50 and dotation < 10000:
            self.token_lvl = 10
        elif dotation >= 10000 and dotation < 100000:
            self.token_lvl = 11
        elif dotation >= 100000 and dotation < 333333:
            self.token_lvl = 12
        elif dotation >= 333333 and dotation < 500000:
            self.token_lvl = 13
        elif dotation >= 500000:
            self.token_lvl = 14

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
    def __init__(self, nbr_player, entry) -> None:
        self.nbr_player = nbr_player
        self.entry = entry
        self.players = self.create_players()
        self.tables = []
        self.finish = False

    def create_players(self) -> list:
        return [
            Player(f"Player {i + 1}", self.entry)
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
                    f"Le gagnant du tourois est {player.name}. J'ai gagner "
                    f"{player.gain:.2f} et eliminer {player.kill} joueurs. "
                    f"🏆 {player.token_lvl}"
                )

    def run(self) -> None:
        while not self.finish:
            if self.nbr_player > 7:
                self.create_tables()
            else:
                self.create_tables(True)
            for table in self.tables:
                if len(table.players) >= 2:
                    win, lost = random.sample(range(len(table.players)), 2)
                    simulator(self, table.players[win], table.players[lost])

    def end(self) -> str:
        self.finish = True

    def __str__(self) -> str:
        return (
            f"Le tournois contient {len(self.players)} joueurs et le prix "
            f"d'entree est de {self.entry} euro."
        )
