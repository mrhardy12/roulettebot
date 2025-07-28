class Bet:
    def __init__(self, bet_type, bet_list, amount):
        self.bet_type = bet_type
        self.bet_list = bet_list
        self.amount = amount


class Player:
    def __init__(self, name):
        self.name = name
        self.bets = []
        self.chips = 1000    # starting chips
    
    def add_bet(self, bet):
        self.bets.append(bet)
