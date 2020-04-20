import numpy as np
import readchar
import enum

# The game board and score
game = np.array([0] * 16).reshape(4, 4)
score = 0

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

# Print the game board
def printGame(game):
    print("--------------------------------")
    print("Score: {}".format(score))
    for row in game:
        for entry in row:
            style = styleMap[entry] if entry in styleMap else "\033[1;37m\033[48;5;0m"
            print("{}{}\t{}".format(style, entry, "\033[0m"), end="")
        print()

# Spawn either a 2 or 4 in a random unfilled position
def spawn(game):
    pos = np.random.randint(0, 4, 2)

    while game[pos[0]][pos[1]] != 0:
        pos = np.random.randint(0, 4, 2)

    game[pos[0]][pos[1]] = 2 if np.random.randint(0, 2) == 0 else 4

# Check if there are any possible moves,
#   if not print a message and exit
def checkGameOver(game):
    for i in range(0, 4):
        for j in range(0, 4):
            entry = game[i][j]
            
            if entry == 0:
                return

            if (i > 0 and entry == game[i - 1][j]):
                return

            if (j > 0 and entry == game[i][j - 1]):
                return

            if (i < 3 and entry == game[i + 1][j]):
                return

            if (j < 3 and entry == game[i][j + 1]):
                return

    print("Game over")
    print("Score: {}".format(score))
    exit()

# Helper predicate for axis of a direction
def isVertical(direction):
    return direction == Direction.UP or direction == Direction.DOWN

# Collpase the game board entries in a given direction
def collapse(game, direction):
    global score
    
    colOffset = directionSignMap[direction] if not isVertical(direction) else 0
    rowOffset = directionSignMap[direction] if isVertical(direction) else 0

    newCollapse = np.array([False] * 16).reshape(4, 4)
    changed = False
    
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

                score = score + game[rowCoord][colCoord]
                newCollapse[rowCoord][colCoord] = True
                changed = True

    return changed

# Move the game board entries in a given direction
def move(game, direction):
    colOffset = directionSignMap[direction] if not isVertical(direction) else 0
    rowOffset = directionSignMap[direction] if isVertical(direction) else 0

    changed = False

    for x in range(0, 4):
        for j in colRangeMap[direction]:
            for i in rowRangeMap[direction]:
                if (game[i + rowOffset][j + colOffset] == 0
                    and game[i][j] != 0):
                    game[i + rowOffset][j + colOffset] = game[i][j]
                    game[i][j] = 0
                    changed = True

    return changed

# The player's swipe in a given direction
def swipe(game, direction):
    changed = False
    changed = move(game, direction) or changed
    changed = collapse(game, direction) or changed
    changed = move(game, direction) or changed
    
    if changed:
        spawn(game)
        printGame(game)
        checkGameOver(game)

# init
spawn(game)
spawn(game)
print("Welcome to 2048 CLI! Use W, A, S, D to control. Press any other key to exit.")
printGame(game)

# Main game loop
while 1:
    key = readchar.readchar()
    if key in ['W', 'w']:
        swipe(game, Direction.UP)
    elif key in ['A', 'a']:
        swipe(game, Direction.LEFT)
    elif key in ['S', 's']:
        swipe(game, Direction.DOWN)
    elif key in ['D', 'd']:
        swipe(game, Direction.RIGHT)
    else:
        exit()
        
