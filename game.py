import numpy as np
import enum

class Game:
    # Enum class to denote the direction of a move
    class Direction(enum.Enum):
        UP = 0,
        RIGHT = 1,
        DOWN = 2,
        LEFT = 3

    # The sign associated with each direction
    directionSignMap = {
        Direction.UP: -1,
        Direction.DOWN: 1,
        Direction.LEFT: -1,
        Direction.RIGHT: 1,
    }

    # The range of columns that can possibly
    #   be have their values increased during a swipe
    colRangeMap = {
        Direction.UP: range(4),
        Direction.DOWN: range(4),
        Direction.LEFT: [3, 2, 1],
        Direction.RIGHT: range(3),
    }

    # The range of columns that can possibly
    #   be have their values increased during a swipe
    rowRangeMap = {
        Direction.UP: [3, 2, 1],
        Direction.DOWN: range(3),
        Direction.LEFT: range(4),
        Direction.RIGHT: range(4),
    }

    # Map from entry value to it's style string
    styleTemplate = "\033[1;30m\033[48;5;{}m"
    styleMap = {
        0: styleTemplate.format(7),
        2: styleTemplate.format(223),
        4: styleTemplate.format(221),
        8: styleTemplate.format(220),
        16: styleTemplate.format(208),
        32: styleTemplate.format(203),
        64: styleTemplate.format(160),
        128: styleTemplate.format(136),
        256: styleTemplate.format(178),
        512: styleTemplate.format(214),
        1024: styleTemplate.format(208),
        2048: styleTemplate.format(202)
    }

    # Constructor
    def __init__(self):
        self._game = np.array([0] * 16).reshape(4, 4)
        self._score = 0

    # Print the game board
    def print(self):
        print("--------------------------------")
        print("Score: {}".format(self._score))
        for row in self._game:
            for entry in row:
                style = Game.styleMap[entry] if entry in Game.styleMap else "\033[1;37m\033[48;5;0m"
                print("{}{}\t{}".format(style, entry, "\033[0m"), end="")
            print()

    # Score accessor
    def getScore(self):
        return self._score

    # Spawn either a 2 or 4 in a random unfilled position
    def spawn(self):
        pos = np.random.randint(0, 4, 2)

        while self._game[pos[0]][pos[1]] != 0:
            pos = np.random.randint(0, 4, 2)

        self._game[pos[0]][pos[1]] = 2 if np.random.randint(0, 2) == 0 else 4

    # Check if there are any possible moves,
    #   if not print a message and exit
    def isGameOver(self):
        for i in range(0, 4):
            for j in range(0, 4):
                entry = self._game[i][j]
            
                if entry == 0:
                    return False

                if (i > 0 and entry == self._game[i - 1][j]):
                    return False

                if (j > 0 and entry == self._game[i][j - 1]):
                    return False

                if (i < 3 and entry == self._game[i + 1][j]):
                    return False

                if (j < 3 and entry == self._game[i][j + 1]):
                    return False

        return True


    # Helper predicate for axis of a direction
    def isVertical(self, direction):
        return direction == Game.Direction.UP or direction == Game.Direction.DOWN

    # Collpase the game board entries in a given direction
    def collapse(self, direction):
        colOffset = Game.directionSignMap[direction] if not self.isVertical(direction) else 0
        rowOffset = Game.directionSignMap[direction] if self.isVertical(direction) else 0

        newCollapse = np.array([False] * 16).reshape(4, 4)
        changed = False
    
        for i in reversed(Game.rowRangeMap[direction]):
            for j in reversed(Game.colRangeMap[direction]):
                rowCoord = i + rowOffset
                colCoord = j + colOffset 
                if (self._game[rowCoord][colCoord] == self._game[i][j]
                    and not newCollapse[rowCoord][colCoord]
                    and not newCollapse[i][j]
                    and self._game[i][j] != 0):
                    self._game[rowCoord][colCoord] = self._game[i][j] * 2
                    self._game[i][j] = 0

                    self._score = self._score + self._game[rowCoord][colCoord]
                    newCollapse[rowCoord][colCoord] = True
                    changed = True

        return changed

    # Move the game board entries in a given direction
    def move(self, direction):
        colOffset = Game.directionSignMap[direction] if not self.isVertical(direction) else 0
        rowOffset = Game.directionSignMap[direction] if self.isVertical(direction) else 0

        changed = False

        for x in range(0, 4):
            for j in Game.colRangeMap[direction]:
                for i in Game.rowRangeMap[direction]:
                    if (self._game[i + rowOffset][j + colOffset] == 0
                        and self._game[i][j] != 0):
                        self._game[i + rowOffset][j + colOffset] = self._game[i][j]
                        self._game[i][j] = 0
                        changed = True

        return changed

    # The player's swipe in a given direction
    #   returns if the game state changed
    def swipe(self, direction):
        if self.isGameOver(): return
            
        changed = False
        changed = self.move(direction) or changed
        changed = self.collapse(direction) or changed
        changed = self.move(direction) or changed

        if changed: self.spawn()

        return changed
