from .algorithm import Algorithm
from ..game import Game
import numpy as np

class Axis(Algorithm):
    def getNextDirection(game):
        horizontalPreference = 0
        verticalPreference = 0
        
        for i in range(0, 4):
            for j in range(0, 4):
                entry = game._game[i][j]

                if entry == 0: break

                if (i > 0 and entry == game._game[i - 1][j]):
                    verticalPreference = verticalPreference + 1

                if (j > 0 and entry == game._game[i][j - 1]):
                    horizontalPreference = horizontalPreference + 1

                if (i < 3 and entry == game._game[i + 1][j]):
                    verticalPreference = verticalPreference + 1

                if (j < 3 and entry == game._game[i][j + 1]):
                    horizontalPreference = horizontalPreference + 1

        if horizontalPreference == verticalPreference and horizontalPreference == 0:
            return np.random.choice([d for d in Game.Direction])

        if horizontalPreference > verticalPreference:
            return np.random.choice([Game.Direction.LEFT, Game.Direction.RIGHT])
        
        return np.random.choice([Game.Direction.UP, Game.Direction.DOWN])
    
    def _run(self, game):
        end = False

        while not end:
            game.swipe(Axis.getNextDirection(game))
            end = end or game.isGameOver()

