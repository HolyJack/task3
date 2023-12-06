import sys
from game import Game

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

    game = Game(moves)
    game.start()

if __name__ == "__main__":
    main()


