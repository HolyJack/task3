import sys
import hashlib
import math
import secrets
import hmac
from prettytable import PrettyTable 

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def green(s):
    return f"{bcolors().OKGREEN}{s}{bcolors().ENDC}"

def red(s):
    return f"{bcolors().FAIL}{s}{bcolors().ENDC}"

def yellow(s):
    return f"{bcolors().WARNING}{s}{bcolors().ENDC}"

def blue(s):
    return f"{bcolors().OKBLUE}{s}{bcolors().ENDC}"

def cyan(s):
    return f"{bcolors().OKCYAN}{s}{bcolors().ENDC}"

def bold(s):
    return f"{bcolors().BOLD}{s}{bcolors().ENDC}"


def parse_moves(moves): 
    moves_pairs = (len(moves) - 1) // 2
    moves_map = {
                move: [moves[(i + j + 1) % len(moves)] for j in range(moves_pairs)] 
                for i, move in enumerate(moves)
                }
    return moves_map

def help(parsed_moves):
    first_row = [cyan("v PC v") + " | " + blue("> User >")] + [blue(move) for move in parsed_moves.keys()]
    table = PrettyTable(first_row)
    for move, wins in parsed_moves.items():
        row = [
            cyan(move)] + [ yellow("Draw")
            if move==another_move
            else (green("You win")
            if another_move in parsed_moves[move]
            else red("You lose"))
            for another_move in parsed_moves.keys()
              ]
        table.add_row(row, divider=True)
    return table

def game(moves):
    options = [str(i) for i in range(len(moves) + 1)] + ["?"]
    print(options)
    parsed_moves = parse_moves(moves)
    help_message = help(parsed_moves)

    while True:
        hmac_key = secrets.token_bytes(256 // 8)
        computer_move = secrets.choice(moves)
        hmac_value = hmac.HMAC(
            key=hmac_key,
            msg=computer_move.encode(),
            digestmod=hashlib.sha3_256).hexdigest()
        
        print(bold("HMAC: ") + hmac_value)
        print(bold("Available moves:"))
        for i, move in enumerate(moves):
            print(f"{i+1} - {move}")
        print("0 - exit")
        print("? - help")
        
        user_input = input(bold("Enter your move: "))
        if (user_input in options):
            if (user_input == "0"):
                print(bold("Bye!"))
                break
            elif (user_input == "?"):
                print(help_message)
                continue

            user_move = moves[int(user_input)-1]
            print(bold("Your move: ") + user_move)
            print(bold("Computer move: ") + computer_move)
            if (user_move in parsed_moves[computer_move]):
                print(bold(green("You Won!")))
            elif (computer_move in parsed_moves[user_move]):
                print(bold(red("You Lost!")))
            else:
                print(bold(yellow("Draw!")))
            print(bold("HMAC key: ") + hmac_key.hex())
        else:
            print(red("Wrong input!"))
        
        print()
        print("Press " + bold("<Enter>") + " to continue...")
        input()

def main():
    moves = sys.argv[1:]

    if (len(moves) <= 1):
        print(red("Error: number of moves is less then 3!"))
        return;
    if (len(moves) % 2 == 0):
        print(red("Error: even number of moves!"))
        return;
    if (len(set(moves)) != len(moves)):
        print(red("Error: 2 or more moves have the same value!"))
        return;
    game(moves)

if __name__ == "__main__":
    main()


