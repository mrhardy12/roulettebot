import sys
import random

from bases import *
from objects import Player, Bet


def main():
    players = {}
    former_players = {}
    round_number = 1
    populate_game(players, former_players, round_number)

    while True:
        current_round_players = list(players.keys())
        print(f"\nRound {round_number}!")
        print(f"Players: {', '.join(current_round_players)}\n")
        get_input("Press Enter to begin inputting bets. ",
                  players, former_players, round_number)
        for player_name in current_round_players:
            wager_count = int(get_input(
                f"\nHow many bets did {player_name} place? ",
                players,
                former_players,
                round_number
            ))

            if wager_count == 0:
                print(f"{player_name} will not be betting this round. ")
                continue

            for i in range(1, wager_count + 1):
                wager = get_input(f"\n{player_name} bet {i}? ",
                                  players, former_players, round_number)
                amount = int(get_input(f"Amount for bet {i}? ",
                                       players, former_players, round_number))

                if wager.isdigit():
                    wager_int = int(wager)
                    if not validate_bet_number(wager_int, "single"):
                        continue
                    add_bet_to_player(players[player_name], "single",
                                      [wager_int], amount)
                elif wager == "BL":
                    add_bet_to_player(players[player_name], "blacks",
                                      blacks, amount)
                elif wager == "EV":
                    add_bet_to_player(players[player_name], "evens",
                                      evens, amount)
                elif wager == "FN":
                    add_bet_to_player(players[player_name], "five numbers",
                                      [0, "00", 1, 2, 3], amount)
                elif wager == "HD":
                    add_bet_to_player(players[player_name], "high dozen",
                                      high_dozen, amount)
                elif wager == "HI":
                    add_bet_to_player(players[player_name], "highs",
                                      highs, amount)
                elif wager == "LD":
                    add_bet_to_player(players[player_name], "low dozen",
                                      low_dozen, amount)
                elif wager == "LO":
                    add_bet_to_player(players[player_name], "lows",
                                      lows, amount)
                elif wager == "MD":
                    add_bet_to_player(players[player_name], "middle dozen",
                                      mid_dozen, amount)
                elif wager == "OD":
                    add_bet_to_player(players[player_name], "odds",
                                      odds, amount)
                elif wager == "RE":
                    add_bet_to_player(players[player_name], "reds",
                                      reds, amount)
                elif wager == "ZZ":
                    add_bet_to_player(players[player_name], "edge",
                                      zeroes, amount)
                elif wager.startswith("DZ"):
                    add_bet_to_player(players[player_name], "single",
                                      ["00"], amount)
                elif wager.startswith("ZE"):
                    add_bet_to_player(players[player_name], "single",
                                      [0], amount)
                elif wager.startswith("CO"):
                    process_bet(players[player_name], wager, amount,
                                "column", get_column_bet)
                elif wager.startswith("CR"):
                    process_bet(players[player_name], wager, amount,
                                "corner", get_corner_bet)
                elif wager.startswith("DR"):
                    process_bet(players[player_name], wager, amount,
                                "double row", get_double_row_bet)
                elif wager.startswith("HE"):
                    process_bet(players[player_name], wager, amount,
                                "edge", get_horizontal_edge_bet)
                elif wager.startswith("RO"):
                    process_bet(players[player_name], wager, amount,
                                "row", get_row_bet)
                elif wager.startswith("VE"):
                    process_bet(players[player_name], wager, amount,
                                "edge", get_vertical_edge_bet)
                else:
                    print(f"Invalid bet: {wager}. Skipping this bet.\n")
                    print("Valid bets are: integers, BL, EV, FN, HD, " \
                    "HI, LD, LO, MD, OD, RE, ZZ, DZ, or ZE for category " \
                    "bets, and numbers with a prefix of CO, CR, DR, HE, " \
                    "RO, or VE for number-based zone bets.\n")
                    print("These are: Blacks, evens, five-number, high " \
                    "dozen, highs, low dozen, lows, mid dozen, odds, " \
                    "reds, zeroes, double zero single, zero single, " \
                    "column, corner, double row, horizontal edge, " \
                    "row, and vertical edge, respectively.\n")
                    print("Zone bets use prefixes indexed " \
                    "by the first number that meets the criteria. " \
                    "For example, CR1 produces a bet of 1-2-4-5, and " \
                    "CO2 produces a bet of column 2. RO22 produces the " \
                    "row that begins with 22, while DR22 produces that " \
                    "row and the next row. Values such as RO24 should " \
                    "also work.")

        get_input("\nAll bets placed! Press Enter to review. \n",
                  players, former_players, round_number)
        print_bet_status(players, round_number)
        get_input("\nPress Enter to spin the wheel! ",
                  players, former_players, round_number)
        result = spin_wheel()
        get_input(f"\nThe wheel landed on {result}! " \
                  f"Press Enter to payout bets.",
                  players, former_players, round_number)
        print(f"\nRound {round_number} bet results!\n")

        for player in players.values():
            print(f"{player.name}:")
            for i, bet in enumerate(player.bets, 1):
                if result in bet.bet_list:
                    payout = calculate_payout(bet)
                    player.chips += payout
                    print(f"  Bet {i}: Won! Payout: {payout} chips!")
                else:
                    player.chips -= bet.amount
                    print(f"  Bet {i}: Lost! Lost {bet.amount} chips!")
            print(f"\nNew chip total: {player.chips} chips!\n")
            player.bets.clear()
        
        new_round = get_input("Continue game? N for no, Enter for yes. ",
                              players, former_players, round_number)
        if new_round.lower() == "n":
            print_final_results(players, former_players, round_number)
            sys.exit()
        else:
            round_number += 1


def populate_game(players, former_players, round_number):
    player_count = int(input("How many players to start? "))
    for i in range(1, player_count + 1):
        name = get_input(f"Player {i} name? ", players,
                         former_players, round_number)
        players[name] = Player(name)


def get_input(prompt, players, former_players, round_number):
    user_input = input(prompt)
    if user_input.lower() == "end":
        sys.exit()
    elif user_input.lower() == "status":
        print_game_status(players, former_players, round_number)
        return get_input(prompt, players, former_players, round_number)
    elif user_input.lower() == "add":
        add_player(players, former_players, round_number)
        return get_input(prompt, players, former_players, round_number)
    elif user_input.lower() == "remove":
        remove_player(players, former_players, round_number)
        return get_input(prompt, players, former_players, round_number)
    return user_input


def print_bet_status(players, round_number):
    print(f"Round {round_number} bets!\n")
    for player in players.values():
        print(f"{player.name}'s bets:")

        if len(player.bets) == 0:
            print("  No bets this round.")
        else:
            for i, bet in enumerate(player.bets, 1):
                numbers = []
                for num in bet.bet_list:
                    numbers.append(str(num))

                if bet.bet_type == "single":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"individual number {numbers[0]}")
                elif bet.bet_type == "edge":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"edge between {' and '.join(numbers)}")
                elif bet.bet_type == "row":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"{'-'.join(numbers)} row")
                elif bet.bet_type == "corner":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"{'-'.join(numbers)} corner")
                elif bet.bet_type == "five numbers":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"{'-'.join(numbers)}")
                elif bet.bet_type == "double row":
                    first_row = '-'.join(numbers[:3])
                    second_row = '-'.join(numbers[3:])
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"{first_row} and {second_row} rows")
                elif bet.bet_type == "column":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"column {numbers[0]}")
                elif bet.bet_type == "high dozen":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"high dozen (25-36)")
                elif bet.bet_type == "low dozen":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"low dozen (1-12)")
                elif bet.bet_type == "middle dozen":
                    print(f"  Bet {i}: {bet.amount} chips on " \
                        f"middle dozen (13-24)")
                elif bet.bet_type == "blacks":
                    print(f"  Bet {i}: {bet.amount} chips on blacks")
                elif bet.bet_type == "evens":
                    print(f"  Bet {i}: {bet.amount} chips on evens")
                elif bet.bet_type == "highs":
                    print(f"  Bet {i}: {bet.amount} chips on highs (19-36)")
                elif bet.bet_type == "lows":
                    print(f"  Bet {i}: {bet.amount} chips on lows (1-18)")
                elif bet.bet_type == "odds":
                    print(f"  Bet {i}: {bet.amount} chips on odds")
                elif bet.bet_type == "reds":
                    print(f"  Bet {i}: {bet.amount} chips on reds")


def print_game_status(players, former_players, round_number):
    print(f"Game is on round {round_number}")
    for player in players.values():
        print(f"{player.name} has {player.chips} chips, " \
              f"and is still playing.")
    for player in former_players.values():
        print(f"{player.name} had {player.chips} chips, " \
              f"and has left the table or run out of chips.")


def print_final_results(players, former_players, round_number):
    print(f"Game has ended on round {round_number}! Thank you for playing!\n")
    for player in players.values():
        print(f"{player.name} ends with {player.chips} chips!")
    for player in former_players.values():
        if player.chips != 0:
            print(f"{player.name} left the table with {player.chips} chips" \
                  f"remaining.")
        else:
            print(f"{player.name} ran out of chips and must pay off their " \
                  f"debt!")


def add_player(players, former_players, round_number):
    new_player_name = get_input("New player name? ", players,
                                former_players, round_number)
    if new_player_name in former_players:
        players[new_player_name] = former_players[new_player_name]
        del former_players[new_player_name]
    else:
        players[new_player_name] = Player(new_player_name)


def remove_player(players, former_players, round_number):
    removing_player = get_input("Who is leaving the table? ",
                                players, former_players, round_number)
    former_players[removing_player] = players[removing_player]
    del players[removing_player]


def spin_wheel():
    ball_landed_in = random.randint(0, 37)
    if ball_landed_in == 37:
        return "00"
    return ball_landed_in


def get_wager_integer(wager):
    return int(wager[2:])


def add_bet_to_player(player, bet_type, bet_numbers, amount):
    bet_obj = Bet(bet_type, bet_numbers, amount)
    player.add_bet(bet_obj)


def process_bet(player, wager, amount, bet_type, get_bet_func):
    number = get_wager_integer(wager)
    bet_numbers = get_bet_func(number)
    add_bet_to_player(player, bet_type, bet_numbers, amount)


def validate_bet_number(number, function_name):
    if number < 1 or number > 36 or not isinstance(number, int):
        print(f"Invalid number: {number}. Must be an integer between " \
              f"1 and 36, inclusive, or 0 or 00 (these have prefixes " \
              f"of ZE and DZ respectively). Skipping {function_name} bet.")
        return False
    return True


def get_column_bet(column_num):
    if not validate_bet_number(column_num, "column"):
        return []
    column_index = column_num - 1
    column_numbers = []
    for row in table:
        column_numbers.append(row[column_index])
    return column_numbers


def get_corner_bet(corner_num):
    if not validate_bet_number(corner_num, "corner"):
        return []
    elif corner_num == 36:
        new_corner_num = 32
    elif corner_num % 3 == 0:
        new_corner_num = corner_num - 1
    elif corner_num == 34 or corner_num == 35:
        new_corner_num = corner_num - 3
    else:
        new_corner_num = corner_num
    
    for row_index in range(len(table)):
        for col_index in range(len(table[row_index])):
            if table[row_index][col_index] == new_corner_num:
                corner_numbers = []
                corner_numbers.append(table[row_index][col_index])
                corner_numbers.append(table[row_index][col_index + 1])
                corner_numbers.append(table[row_index + 1][col_index])
                corner_numbers.append(table[row_index + 1][col_index + 1])
                return corner_numbers


def get_double_row_bet(row_num):
    if not validate_bet_number(row_num, "row"):
        return []
    elif row_num == 34 or row_num == 35 or row_num == 36:
        new_row_num = row_num - 3
    else:
        new_row_num = row_num

    for row_index in range(len(table)):
        if new_row_num in table[row_index]:
            return table[row_index] + table[row_index + 1]


def get_horizontal_edge_bet(edge_num):
    if not validate_bet_number(edge_num, "edge"):
        return []
    elif edge_num % 3 == 0:
        new_edge_num = edge_num - 1
    else:
        new_edge_num = edge_num

    for row_index in range(len(table)):
        for col_index in range(len(table[row_index])):
            if table[row_index][col_index] == new_edge_num:
                edge_numbers = []
                edge_numbers.append(table[row_index][col_index])
                edge_numbers.append(table[row_index][col_index + 1])
                return edge_numbers


def get_row_bet(row_num):
    if not validate_bet_number(row_num, "row"):
        return []
    for row_index in range(len(table)):
        if row_num in table[row_index]:
            return table[row_index]


def get_vertical_edge_bet(edge_num):
    if not validate_bet_number(edge_num, "edge"):
        return []
    elif edge_num == 34 or edge_num == 35 or edge_num == 36:
        new_edge_num = edge_num - 3
    else:
        new_edge_num = edge_num

    for row_index in range(len(table)):
        for col_index in range(len(table[row_index])):
            if table[row_index][col_index] == new_edge_num:
                edge_numbers = []
                edge_numbers.append(table[row_index][col_index])
                edge_numbers.append(table[row_index + 1][col_index])
                return edge_numbers


def calculate_payout(bet):
    multiplier = (36 // len(bet.bet_list)) - 1
    return bet.amount * multiplier


if __name__ == "__main__":
    main()