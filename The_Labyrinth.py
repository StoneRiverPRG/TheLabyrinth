import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]
print(f"row, column, alarm = {r}, {c}, {a}", file=sys.stderr)

# game loop
while True:
    # kr: row where Rick is located.
    # kc: column where Rick is located.
    kr, kc = [int(i) for i in input().split()]
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


    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Rick's next move (UP DOWN LEFT or RIGHT).
    print("RIGHT")
