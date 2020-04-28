from .algorithm import Algorithm
from ..game import Game
import numpy as np

# Randomly select a direction each time
class Random(Algorithm):
    def _run(self, game):
        end = False

        while not end:
            game.swipe(np.random.choice([d for d in Game.Direction]))
            end = end or game.isGameOver()

