import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

from warnings import warn
import heapq
import logging
#logging.basicConfig(filename="logAstar2.txt", level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(asctime)s: %(message)s')
logging.disable(logging.CRITICAL)
logging.debug('program begins.')


class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f

    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1]  # Return reversed path


def astar(maze, start, end, allow_diagonal_movement = False):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    logging.debug(f"start = {start}, end = {end}")

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Heapify the open_list and Add the start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # Adding a stop condition
    outer_iterations = 0
    # max_iterations = (len(maze[0]) * len(maze) // 2)
    max_iterations = (len(maze[0]) * len(maze) * 2)


    # what squares do we search
    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    if allow_diagonal_movement:
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

    # Loop until you find the end
    while len(open_list) > 0:
        outer_iterations += 1

        if outer_iterations > max_iterations:
          # if we hit this point return the path such as it is
          # it will not contain the destination
          warn("giving up on pathfinding too many iterations")
          return return_path(current_node)

        # Get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)
        logging.debug(f"choosed {current_node.position}")

        # Found the goal
        if current_node == end_node:
            return return_path(current_node)

        # Generate children
        children = []

        for new_position in adjacent_squares: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] in ["#", "?"]:
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)


        # Loop through children
        for child in children:
            # Child is on the closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add the child to the open list
            heapq.heappush(open_list, child)
            logging.debug(f"pos: {child.position}, f: {child.f}, g: {child.g}, h: {child.h} ")

        # for debug
        logging.debug(f"open list = ")
        openlog = ""
        for op in open_list:
            openlog += f"{op.position}, "
        logging.debug(f"{openlog}")
        logging.debug("")

        logging.debug(f"**close list = ")
        closelog = ""
        for cl in closed_list:
            closelog += f"{cl.position}, "
        logging.debug(f"{closelog}")
        logging.debug("")



    warn("Couldn't get a path to destination")
    return None


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
def ReturnNeighborList(now, maze, goal=False):
    # movable: list of (row, column) coordinate (numerical) tuples
    movable = []
    direction = ["UP", "RIGHT", "DOWN", "LEFT"]
    r = now[0]
    c = now[1]
    char = [".", "C", "?", "T"]
    if goal:
        char = [".", "C", "T"]

    for strdir in direction:
        dir = ChangeDirtoNum(strdir)
        if maze[r + dir[0]][c + dir[1]] in char:
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
ASTAR = False
path = []

close_list = []

# game loop
while True:
    # kr: row where Rick is located.
    # kc: column where Rick is located.
    kr, kc = [int(i) for i in input().split()]
    NOW = (kr, kc)

    print(f"START:{START}, CTRL:{CTRL}, GOAL:{GOAL}", file=sys.stderr)
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
                    GOAL = CTRL
                    print(f"Control room found!", file=sys.stderr)
                    print(f"START:{START}, CTRL:{CTRL}, GOAL:{GOAL}, NOW{NOW}", file=sys.stderr)
                    break
    if NOW == CTRL:
        close_list = []
        print("control reached!", file=sys.stderr)
        GOAL = START
        ASTAR = False

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # Rick's next move (UP DOWN LEFT or RIGHT).
    movable_list = ReturnNeighborList(NOW, maze, ASTAR)
    close_list.append(NOW)
    print("Movable List = ", movable_list, file=sys.stderr)
    print("Close List = ", close_list, file=sys.stderr)

    max = 0
    max_coord = (-1, -1)
    evalue = 0
    temp = 0
    temp_list = []

    for li in movable_list:
        if not li in close_list:
            temp_list.append(li)

    if not temp_list:
        close_list = []

    for coord in movable_list:
        if coord in close_list:
            continue
        temp = len(ReturnNeighborList(coord, maze, ASTAR))

        if temp > max:
            max = temp
            max_coord = coord
            goto = max_coord
        print(f"estimation, go to {max_coord}", file=sys.stderr)

    if GOAL != (-1, -1):
        if not ASTAR:
            print(f"A* START:{START}, CTRL:{CTRL}, GOAL:{GOAL}, NOW:{NOW}", file=sys.stderr)
            path = astar(maze, NOW, GOAL)
            ASTAR = True
            print(f"path= {path}", file=sys.stderr)
            if path:
                path.pop(0)
                goto = path[0]
                path.pop(0)
                print(f"estimation, go to {goto}", file=sys.stderr)
        else:
            if path:
                goto = path[0]
                path.pop(0)
                print(f"estimation, go to {goto}", file=sys.stderr)

    print(f"goto = {goto}", file=sys.stderr)
    goto = (goto[0] - kr, goto[1] - kc)
    print(ChangeDirtoStr(goto))

