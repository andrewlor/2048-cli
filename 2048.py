import numpy as np
import readchar
import enum

# The game board
game = np.array([0] * 16).reshape(4, 4)

# Enum class to denote the direction of a move
class Direction(enum.Enum):
    UP = 0,
    RIGHT = 1,
    DOWN = 2,
    LEFT = 3

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

def printGame(game):
    print("--------------------------------")
    for row in game:
        for entry in row:
            style = styleMap[entry] if entry in styleMap else "\033[1;37m\033[48;5;0m"
            print("{}{}\t{}".format(style, entry, "\033[0m"), end="")
        print()

def spawn(game):
    pos = np.random.randint(0, 4, 2)

    while game[pos[0]][pos[1]] != 0:
        pos = np.random.randint(0, 4, 2)

    game[pos[0]][pos[1]] = 2 if np.random.randint(0, 2) == 0 else 4

def init(game):
    spawn(game)
    spawn(game)

def gameOver():
    print("GAME OVER")
    exit()

def checkGameOver(game):
    for row in game:
        for entry in row:
            if entry == 0:
                return

    gameOver()


directionSignMap = {
    Direction.UP: -1,
    Direction.DOWN: 1,
    Direction.LEFT: -1,
    Direction.RIGHT: 1,
}
colRangeMap = {
    Direction.UP: range(4),
    Direction.DOWN: range(4),
    Direction.LEFT: [3, 2, 1],
    Direction.RIGHT: range(3),
}
rowRangeMap = {
    Direction.UP: [3, 2, 1],
    Direction.DOWN: range(3),
    Direction.LEFT: range(4),
    Direction.RIGHT: range(4),
}

def isVertical(direction):
    return direction == Direction.UP or direction == Direction.DOWN
    
def collapse(game, direction):
    colOffset = directionSignMap[direction] if not isVertical(direction) else 0
    rowOffset = directionSignMap[direction] if isVertical(direction) else 0

    newCollapse = np.array([False] * 16).reshape(4, 4)
    
    for i in reversed(rowRangeMap[direction]):
        for j in reversed(colRangeMap[direction]):
            rowCoord = i + rowOffset
            colCoord = j + colOffset 
            if (game[rowCoord][colCoord] == game[i][j]
                and not newCollapse[rowCoord][colCoord]
                and not newCollapse[i][j]
                and game[i][j] != 0):
                game[rowCoord][colCoord] = game[i][j] * 2
                game[i][j] = 0
                newCollapse[rowCoord][colCoord] = True

def move(game, direction):
    colOffset = directionSignMap[direction] if not isVertical(direction) else 0
    rowOffset = directionSignMap[direction] if isVertical(direction) else 0

    for x in range(0, 4):
        for j in colRangeMap[direction]:
            changed = False
            for i in rowRangeMap[direction]:
                if game[i + rowOffset][j + colOffset] == 0:
                    game[i + rowOffset][j + colOffset] = game[i][j]
                    game[i][j] = 0
                    changed = True
                    
            if not changed: break

def turn(game, direction):
    move(game, direction)
    collapse(game, direction)
    move(game, direction)
    
    spawn(game)
    printGame(game)
    checkGameOver(game)

init(game)
printGame(game)

while 1:
    key = readchar.readchar()
    if key in ['W', 'w']:
        turn(game, Direction.UP)
    elif key in ['A', 'a']:
        turn(game, Direction.LEFT)
    elif key in ['S', 's']:
        turn(game, Direction.DOWN)
    elif key in ['D', 'd']:
        turn(game, Direction.RIGHT)
    else:
        exit()
        
