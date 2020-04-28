from ..game import Game

# Common interface for running different algorithms on a 2048 game
class Algorithm:
    # Algorithm logic to be implemented
    #   perform operations on game and then return
    def _run(self, game):
        pass

    # Harness to simulate the algorithm
    def simulate(self):
        game = Game()
        game.spawn()
        game.spawn()
        self._run(game)
        
        return game.getScore()
        
