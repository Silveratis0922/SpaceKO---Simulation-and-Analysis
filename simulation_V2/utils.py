import random


def bank_robbery(token: int, dotation: float) -> float:
    number = random.randint(1, 100000)
    if token <= 10:
        if number <= 100:
            return dotation * 100
        elif number <= 600:
            return dotation * 10
        elif number <= 5100:
            return dotation * 3
        elif number <= 17700:
            return dotation * 2
        elif number <= 40000:
            return dotation
        else:
            return dotation * 0.4
    elif token == 11:
        if number <= 1000:
            return dotation * 10
        elif number <= 6000:
            return dotation * 3
        elif number <= 17000:
            return dotation * 2
        elif number <= 40000:
            return dotation
        else:
            return dotation * 0.5
    elif token == 12:
        if number <= 6000:
            return dotation * 3
        elif number <= 18000:
            return dotation * 2
        elif number <= 40000:
            return dotation
        else:
            return dotation * 0.6
    elif token == 13:
        if number <= 16002:
            return dotation * 2
        elif number <= 46660:
            return dotation
        else:
            return dotation * 0.7
    elif token == 14:
        if number <= 18570:
            return dotation * 1.5
        elif number <= 53575:
            return dotation
        else:
            return dotation * 0.8


def simulator(tournament, p_winner, p_looser) -> None:
    money = bank_robbery(p_looser.token_lvl, p_looser.dotation)
    split = round(money / 2, 2)
    p_winner.dotation += split
    p_winner.gain += split
    p_winner.kill += 1
    p_winner.checking_token()
    p_looser.bust()
    if tournament.nbr_player == 2:
        money = bank_robbery(p_winner.token_lvl, p_winner.dotation)
        p_winner.gain += money
        tournament.end()
    tournament.nbr_player -= 1
