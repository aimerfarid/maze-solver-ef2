"""Maze generation and path finding
Emir Farid MOHD RODZI
"""

from random import shuffle, randrange


class Cell:
    """
    Cell objects represent a single maze location with up-to 4 walls.

    The .N, .E, .S, .W attributes represent the walls in the North,
    East, South and West directions. If the attribute is True, there is a
    wall in the given direction.

    The .x and .y attributes store the coordinates of the cell.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.N = True
        self.E = True
        self.S = True
        self.W = True

        self.visited = False

        self.coordinates = ['N', 'S', 'E', 'W']

    def remove_wall(self, direction):
        """
        Remove one wall - keep all neighbors consistent
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        direction = direction.upper()

        loc = ' @(x=%d, y=%d)' % (self.x, self.y)
        if direction == 'W':
            if self.x < 1:
                raise ValueError('cannot remove side wall on west' + loc)
            if self.W:
                self.W = False
                assert maze[self.x - 1][self.y].E
                maze[self.x - 1][self.y].E = False
        if direction == 'E':
            if self.x >= size_x - 1:
                raise ValueError('cannot remove side wall on east' + loc)
            if self.E:
                self.E = False
                assert maze[self.x + 1][self.y].W
                maze[self.x + 1][self.y].W = False
        if direction == 'N':
            if self.y < 1:
                raise ValueError('cannot remove side wall on north' + loc)
            if self.N:
                self.N = False
                assert maze[self.x][self.y - 1].S
                maze[self.x][self.y - 1].S = False
        if direction == 'S':
            if self.y >= size_y - 1:
                raise ValueError('cannot remove side wall on south' + loc)
            if self.S:
                self.S = False
                assert maze[self.x][self.y + 1].N
                maze[self.x][self.y + 1].N = False

    def has_wall(self, direction):
        """
        True if there is a wall in the given direction
        Direction is one of these strings: 'N', 'E', 'S', 'W'
        """
        return getattr(self, direction.upper())


# Global variables for the maze and its size
size_x = size_y = 32
maze = [[Cell(x, y) for y in range(size_y)] for x in range(size_x)]
countsteps = 0  # Extra variable


def build_maze():
    """
    Build a valid maze by tearing down walls

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    This function does not need to return any value but should modify the
    cells (walls) to create a perfect maze.
    When the function is invoked all cells have all their four walls standing.

    Solution:
    1. We pick a random cell
    2. We select a random neighbouring cell ...
    2b. ... that has not been visited
    3. We remove the wall between the two cells and add the neighbouring cell to the list of cells having been visited.
    4. If there are no unvisited neighbouring cell, we backtrack to one that has at least one unvisited neighbour;
    this is done until we backtrack to the original cell.

    """

    def buildwall(x, y):
        maze[x][y].visited = True
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)  # 2 Randomize neighbours
        for (i, j) in d:
            if (j < 0 or j > (size_y - 1) or
                        i < 0 or i > (size_x - 1) or
                        maze[i][j].visited == True):
                # 3 (ignore visited)
                continue
            if i == x:
                maze[x][max(y, j)].remove_wall('N')  # 4 Remove the lower portion
            elif j == y:
                maze[min(x, i)][y].remove_wall('E')  # 4 Remove the higher portion
            # recursive call; push ahead
            # 5; after recursion, effectively backtrack
            buildwall(i, j)

    buildwall(randrange(size_x - 1), randrange(size_y - 1))  # 1


def find_path(start, end):
    """
    Find a path from the start position to the end

    The start and end parameters are coordinate pairs (tuples) for the
    start and end (target) position. E.g. (0, 0) or (7, 13).

    The function has access to the following global variables:
        size_x - integer, the horizontal size of the maze
        size_y - integer, the vertical size of the maze
        maze - a two dimensional array (list of lists) for all cells
            e.g. maze[3][4] is a Cell object for x=3, y=4

    The function is invoked after build_maze removed the walls to create a
    perfect maze.

    This function shall return a list of coordinate pairs (tuples or lists)
    which list the cell coordinates on a valid path from start to end.
    E.g.: [(0, 0), (0, 1), (1, 1), (2, 1), (3, 1), ..., (7, 13)]
    """

    """
    1. The turtle has run into a wall. Since the square is occupied by a wall no further exploration can take place.
    2. The turtle has found a square that has already been explored. 
       We do not want to continue exploring from this position or we will get into a loop.
    3. We have found an outside edge, not occupied by a wall. In other words we have found an exit from the maze.
    4. We have explored a square unsuccessfully in all four directions.
    """

    """Test #3"""
    listRes = []
    solve_path(listRes, start, end)
    countsteps = len(listRes)
    print("Number of steps", countsteps)
    return listRes


def solve_path(listRes, start, end):
    xx = start[0]
    yy = start[1]
    print(start)

    if start in listRes:
        return False

    listRes.append(start)

    if start == end:
        print("Finish line reached at", start, "with these")
        return True

    else:
        # Otherwise, use logical short circuiting to try each
        # direction in turn (if needed)
        for move in maze[xx][yy].coordinates:
            if move == 'N' and not maze[xx][yy].has_wall('N'):
                if solve_path(listRes, (xx, yy - 1), end):
                    return True

            if move == 'E' and not maze[xx][yy].has_wall('E'):
                if solve_path(listRes, (xx + 1, yy), end):
                    return True

            if move == 'S' and not maze[xx][yy].has_wall('S'):
                if solve_path(listRes, (xx, yy + 1), end):
                    return True

            if move == 'W' and not maze[xx][yy].has_wall('W'):
                if solve_path(listRes, (xx - 1, yy), end):
                    return True

        listRes.pop()  # Ensure to remove previous unnecessary movements
        solve_path(listRes, listRes[-1], end)

    """Test #2"""
    # xx = start[0]
    # yy = start[1]
    # listRes.append(start)
    # if start == end:
    #     print("Found at ", start)
    #     return listRes
    # else:
    #     if not (maze[xx][yy+1].visited or maze[xx][yy].has_wall('S')):
    #         yy += 1
    #         maze[xx][yy].visited = True
    #         return find_path((xx, yy), end)
    #     if not (maze[xx-1][yy].visited or maze[xx][yy].has_wall('W')):
    #         xx -= 1
    #         maze[xx][yy].visited = True
    #         return find_path((xx, yy), end)
    #     if not (maze[xx][yy-1].visited or maze[xx][yy].has_wall('N')):
    #         yy -= 1
    #         maze[xx][yy].visited = True
    #         return find_path((xx, yy), end)
    #     if not (maze[xx+1][yy].visited or maze[xx][yy].has_wall('E')):
    #         xx += 1
    #         maze[xx][yy].visited = True
    #         return find_path((xx, yy), end)


    """Solution from previous chapter"""
    """Test #1"""
    # if maze[startRow][startColumn] == OBSTACLE :
    #     return False
    # #  2. We have found a square that has already been explored
    # if maze[startRow][startColumn] == TRIED:
    #     return False
    # # 3. Success, an outside edge not occupied by an obstacle
    # if maze.isExit(startRow,startColumn):
    #     maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    #     return True
    # maze.updatePosition(startRow, startColumn, TRIED)
    #
    # # Otherwise, use logical short circuiting to try each
    # # direction in turn (if needed)
    # found = searchFrom((xx-1, yy), end) or \
    #         searchFrom(xx+1, yy) or \
    #         searchFrom((xx,yy-1), end) or \
    #         searchFrom((xx,yy+1), end)
    # found = find_path(maze, startRow-1, startColumn) or \
    #         find_path(maze, startRow+1, startColumn) or \
    #         find_path(maze, startRow, startColumn-1) or \
    #         find_path(maze, startRow, startColumn+1)
    # if found:
    #     maze.updatePosition(startRow, startColumn, PART_OF_PATH)
    # else:
    #     maze.updatePosition(startRow, startColumn, DEAD_END)
    # return found


###############################################################################
# Testing and visualizing results - no need to understand and/or change

def main():
    import sys
    import Tkinter

    sys.setrecursionlimit(4096)

    start, end = (0, 0), (size_x - 1, size_y - 1)

    build_maze()
    path = find_path(start, end)

    # checking maze
    n_edges = 0
    for x in range(size_x):
        for y in range(size_y):
            n_node_edges = 0
            for direction in 'NESW':
                n_node_edges += not maze[x][y].has_wall(direction)
            if n_node_edges < 1:
                print('WARNING: walled in cell @ (x=%d, y=%d)' % (x, y))
            n_edges += n_node_edges
    n_perfect_edges = (size_x * size_y - 1) * 2
    if n_edges < n_perfect_edges:
        print('WARNING: not a perfect maze, too many walls')
    if n_edges > n_perfect_edges:
        print('WARNING: not a perfect maze, redundant paths')

    # checking path
    try:
        assert len(path) >= 2
        if path[0] != start:
            print('WARNING: invalid starting point for path', path[0])
        if path[-1] != end:
            print('WARNING: invalid endpoint for path', path[-1])

        prev = None
        for step in path:
            assert 0 <= step[0] < size_x
            assert 0 <= step[1] < size_y
            if prev is not None:
                dst = abs(step[0] - prev[0]) + abs(step[1] - prev[1])
                if dst != 1:
                    print('WARNING: invalid step in path', prev, step)
                prev = step

    except Exception as e:
        print('Ignoring invalid path object:', path, e)
        path = None

    cell_size = 20
    master = Tkinter.Tk()
    canvas = Tkinter.Canvas(master, width=size_x * cell_size + 1,
                            height=size_y * cell_size + 1,
                            bd=0, highlightthickness=0, relief='ridge')
    canvas.pack()
    for x in range(size_x):
        for y in range(size_y):
            if maze[x][y].N:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * (x + 1), cell_size * y)
            if maze[x][y].E:
                canvas.create_line(cell_size * (x + 1), cell_size * y,
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].S:
                canvas.create_line(cell_size * x, cell_size * (y + 1),
                                   cell_size * (x + 1), cell_size * (y + 1))
            if maze[x][y].W:
                canvas.create_line(cell_size * x, cell_size * y,
                                   cell_size * x, cell_size * (y + 1))

    if path:
        line = [x * cell_size + cell_size // 2 for step in path for x in step]
        canvas.create_line(*line, fill='red', width=2)

    radius = cell_size // 3
    img_start = [cell_size * x + cell_size // 2 for x in start]
    canvas.create_oval(img_start[0] - radius,
                       img_start[1] - radius,
                       img_start[0] + radius,
                       img_start[1] + radius, fill='red')
    img_end = [cell_size * x + cell_size // 2 for x in end]
    canvas.create_oval(img_end[0] - radius,
                       img_end[1] - radius,
                       img_end[0] + radius,
                       img_end[1] + radius, fill='green')

    master.title('Maze')
    master.lift()
    master.call('wm', 'attributes', '.', '-topmost', True)
    Tkinter.mainloop()


if __name__ == '__main__':
    main()
