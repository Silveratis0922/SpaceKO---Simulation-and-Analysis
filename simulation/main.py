from Class import Tournament
from data import data_collector
import pandas as pd
import time


def main():
    tournaments = 100
    players = 7500
    pay_in = 10
    whole_data = []
    start = time.time()
    for i in range(tournaments):
        Spaceko = Tournament(players, pay_in)
        # running tournament:
        Spaceko.run()
        # We have a winner !
        print(Spaceko.winner_annoncement(i + 1))
        # Saving stats from players
        df = data_collector(Spaceko, i + 1)
        whole_data.append(df)
    # Tournaments are finish.
    # Concatanate the list of DataFrame into a single one
    df_all = pd.concat(whole_data, axis=1)
    df_all.to_csv(f"../data_{tournaments}t_{players}p_{pay_in}.csv")
    end = time.time()
    # print("Donnees de tous les tournois :")
    # print(df_all)
    print(f"Le programme a mit {round(end - start, 2)} secondes pour {tournaments} tournois.")


if __name__ == "__main__":
    main()


# Organisation d'un tournois
# -Creer le tournois ✔️
# -Creer les instances de joueurs ✔️
# -Creer les tables et y placer les joueurs. ✔️
# -Creer la liste de token. ✔️
# -Faire une premiere "main"✔️
# -Choisir un gagnant et un perdant de maniere random sur chaque table.✔️
# -Loterie du gain avec le token du perdant✔️
# -Mettre a jour le statut eliminer du perdant ✔️
# -Mettre a jour le gain, dotation et token_lvl (si besoin) du gagnant. ✔️
# -Faire cela jusqu'a avoir un gagnant.✔️
#
# - Stocker les resultat du tournois dans un dataFrame. ✔️
# - Visualisation avec Matplotlib
# - Visualisation avec Power BI/ Tableau BI
# - Redistribution de la variance des tokens en fonction des resultats.

# Quelles que donnees qui peuvent etre interessante
# - Joueurs qui a gagner le plus de tournois
# - Joueurs qui a gagner le plus de gains (au cumul)
# - Joueurs qui a gagner le plus gros gains (1 tournois)
# - Joueurs qui a fait le plus d'elimination (au cumul)
# - Joueurs qui a fait le plus d'elimination (1 tournois)
# - Joueurs qui a eu la plus grosse dotation (au cumul)
# - Joueurs qui a eu la plus grosse dotation (1 tournois)
# - Meilleurs joueurs (Attribution de points en fonctions des differents classement)

# - Joueurs qui a fait le moins de gain (total)
# - Joueurs qui a fait le moins d'elimination (total)
# - Nombre de joueurs qui n'ont pas gagner de tournois

# Aspect financier

# Mettre une ligne droite horizontal qui simulerai le gain normal sans variance.
# Graphique gain total(y) et tournois(x) en ligne
# Cambembert qui nous montrerai certain %age si on est en dessous ou au dessus de la variance
