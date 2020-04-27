# Driver to play the game on the CLI

import readchar
from game import Game

# init
game = Game()
print("Welcome to 2048 CLI! Use W, A, S, D to control. Press any other key to exit.")
game.spawn()
game.spawn()
game.print()

# Main game loop
while 1:
    key = readchar.readchar()
    changed = False
    
    if key in ['W', 'w']:
        changed = game.swipe(Game.Direction.UP)
    elif key in ['A', 'a']:
        changed = game.swipe(Game.Direction.LEFT)
    elif key in ['S', 's']:
        changed = game.swipe(Game.Direction.DOWN)
    elif key in ['D', 'd']:
        changed = game.swipe(Game.Direction.RIGHT)
    else:
        break

    if changed: game.print()
    if game.isGameOver(): break

print("Game over")
print("Score: {}".format(game.getScore()))
