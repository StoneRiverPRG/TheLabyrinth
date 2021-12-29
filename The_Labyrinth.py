import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# change direction, string to numeric
# e.g. "UP" to (-1, 0)
def ChangeDirtoNum(dir):
    direction = ["UP", "RIGHT", "DOWN", "LEFT"]
    change_dir = (0, 0)
    if dir not in direction:
        print(f"error! dir:{dir} is not dir string.", file=sys.stderr)
        return (-1, -1)

    if dir == "UP":
        change_dir = (-1, 0)
    elif dir == "RIGHT":
        change_dir = (0, 1)
    elif dir == "DOWN":
        change_dir = (1, 0)
    elif dir == "LEFT":
        change_dir = (0, -1)
    else:
        print("something error ChangeDirtoNum", file=sys.stderr)

    return change_dir

# change direction num (r, c) tuble to string eg. "UP"
# numdir: tuple of coordinate eg. (0, 1)
def ChangeDirtoStr(numdir):
    if len(numdir) != 2:
        return "error"

    strdir = ""
    _r = numdir[0]
    _c = numdir[1]

    if _r == 0:
        if _c == 1:
            strdir = "RIGHT"
        elif _c == -1:
            strdir = "LEFT"
    elif _c == 0:
        if _r == 1:
            strdir = "DOWN"
        elif _r == -1:
            strdir = "UP"

    return strdir

# now: rick's coordinate tuple (r, c)
# maze: list of map of maze. 2 x 2 list
# check neighbor coordinate and return valid coordinate (tuples) list
def ReturnNeighborList(now, maze):
    # movable: list of (row, column) coordinate (numerical) tuples
    movable = []
    direction = ["UP", "RIGHT", "DOWN", "LEFT"]
    r = now[0]
    c = now[1]

    for strdir in direction:
        dir = ChangeDirtoNum(strdir)
        if maze[r + dir[0]][c + dir[1]] == "." or \
           maze[r + dir[0]][c + dir[1]] == "C" or \
           maze[r + dir[0]][c + dir[1]] == "T":
            movable.append((r + dir[0], c + dir[1]))

    return movable


# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]
print(f"row, column, alarm = {r}, {c}, {a}", file=sys.stderr)

# FUEL: max energy
FUEL = 1200

CONTROL = False
START = (-1, -1)
CTRL = (-1, -1)
GOAL = (-1, -1)

close_list = []

# game loop
while True:
    # kr: row where Rick is located.
    # kc: column where Rick is located.
    kr, kc = [int(i) for i in input().split()]

    # set start coordinate (kr, kc) . start means "T".
    if START == (-1, -1):
        START = (kr, kc)
    print(f"Rick is ({kr}, {kc})", file=sys.stderr)

    # maze: 迷路list
    maze = []
    print(f"maze map = ", file=sys.stderr)

    # update and print maze
    for i in range(r):
        row = input()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        maze.append(row)
        print(f"{row}", file=sys.stderr)

    print("", file=sys.stderr)

    if CTRL == (-1, -1):
        for i, row in enumerate(maze):
            if CTRL != (-1, -1):
                break
            for j, s in enumerate(row):
                if s == "C":
                    CTRL = (i, j)
                    print("Control room found!", file=sys.stderr)
                    break
    if (kr, kc) == CTRL:
        close_list = []
        GOAL = START

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Rick's next move (UP DOWN LEFT or RIGHT).
    movable_list = ReturnNeighborList((kr, kc), maze)
    close_list.append((kr, kc))
    print("Movable List = ", movable_list, file=sys.stderr)
    print("Close List = ", close_list, file=sys.stderr)

    max = 0
    max_coord = (-1, -1)
    evalue = 0
    temp = 0

    for coord in movable_list:
        if coord in close_list:
            continue
        temp = len(ReturnNeighborList(coord, maze))
        if temp > max:
            max = temp
            max_coord = coord
    print(f"estimation, go to {max_coord}", file=sys.stderr)

    goto = (max_coord[0] - kr, max_coord[1] - kc)
    print(f"goto = {goto}", file=sys.stderr)
    print(ChangeDirtoStr(goto))

