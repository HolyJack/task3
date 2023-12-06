import hashlib
import math
import secrets
import hmac
from prettytable import PrettyTable 

from colors import green, blue, cyan, yellow, red, bold


class ComputerMove:
    def __init__(self, moves):
        self.hmac_key = secrets.token_bytes(256//8)
        self.move = secrets.choice(moves)
        self.hmac = hmac.HMAC(
                key=self.hmac_key,
                msg=self.move.encode(),
                digestmod=hashlib.sha3_256).hexdigest()
        print(bold("HMAC: ") + self.hmac)

    def __str__(self):
        return self.move


class Game:
    def __init__(self, moves):
        self.moves = moves
        self.options = [str(i) for i in range(len(self.moves) + 1)] + ["?"]
        self.parsed_moves = self.parse_moves()
        self.game_message = self.generate_game_message()
        self.help_message = self.generate_help_message()


    def parse_moves(self):
        moves_pairs = (len(self.moves) - 1) // 2
        moves_map = {
                move: [self.moves[(i + j + 1) % len(self.moves)] for j in range(moves_pairs)] 
                for i, move in enumerate(self.moves)
                }
        return moves_map


    def generate_game_message(self):
        message = bold("Available moves:\n") + "\n".join([f"{i+1} - {move}" for i, move in enumerate(self.moves)]) + "\n0 - exit\n? - help"
        return message
    

    def generate_help_message(self):
        first_row = [cyan("v PC v") + " | " + blue("> User >")] + [blue(move) for move in self.parsed_moves.keys()]
        table = PrettyTable(first_row)
        for move, wins in self.parsed_moves.items():
            row = [
                cyan(move)] + [ yellow("Draw")
                if move==another_move
                else (green("You win")
                if another_move in self.parsed_moves[move]
                else red("You lose"))
                for another_move in self.parsed_moves.keys()
                ]
            table.add_row(row, divider=True)
        return table


    
    def start(self):
        while self.game_cycle():
            self.press_enter_to_continue()


    def game_cycle(self):
        computer_move = ComputerMove(self.moves)
        print(self.game_message)
        return self.process_user_input(computer_move)


    def process_user_input(self, computer_move):
        user_input = input(bold("Enter your move: "))
        if (user_input in self.options):
            if (user_input == "0"):
                print(bold("Bye!"))
                return False
            elif (user_input == "?"):
                print(self.help_message)
                return True

            user_move = self.moves[int(user_input)-1]
            print(bold("Your move: ") + user_move)
            print(bold("Computer move: ") + computer_move.move)
            if (user_move in self.parsed_moves[computer_move.move]):
                print(bold(green("You Won!")))
            elif (computer_move.move in self.parsed_moves[user_move]):
                print(bold(red("You Lost!")))
            else:
                print(bold(yellow("Draw!")))
            print(bold("HMAC key: ") + computer_move.hmac_key.hex())
        else:
            print(red("Wrong input!"))

        return True
    

    @staticmethod
    def press_enter_to_continue():
        print()
        print("Press " + bold("<Enter>") + " to continue...")
        input()


