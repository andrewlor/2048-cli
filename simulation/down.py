from .algorithm import Algorithm
from ..game import Game

# Always move down
class Down(Algorithm):
    def _run(self, game):
        end = False

        while not end:
            end = end or not game.swipe(Game.Direction.DOWN)
            end = end or game.isGameOver()

