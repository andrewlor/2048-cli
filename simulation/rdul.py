from .algorithm import Algorithm
from ..game import Game

# Preferred moves are right and down, only do up or left if nessecary
class Rdul(Algorithm):
    def _run(self, game):
        while True:
            # Preferred moves
            while True:
                anyChange = False
                while True:
                    changed = game.swipe(Game.Direction.RIGHT)
                    if not changed: break
                    else: anyChange = True

                while True:
                    changed = game.swipe(Game.Direction.DOWN)
                    if not changed: break
                    else: anyChange = True

                if not anyChange: break

            changed = game.swipe(Game.Direction.UP)
            if changed: continue

            changed = game.swipe(Game.Direction.LEFT)
            if changed: continue

            if game.isGameOver(): break
