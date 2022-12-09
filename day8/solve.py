#!/usr/bin/env python3

def load_grid(filename="input.txt"):
    with open(filename, "r") as f:
        grid = [[int(k) for k in i] for i in f.read().splitlines()]
    return grid


class Tree:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def __repr__(self):
        return f"{self.height}"


def build_tree_grid(grid):
    tree_grid = []
    # make tree objects
    for c in range(len(grid)):
        tree_row = []
        for r in range(len(grid[0])):
            # print(grid[c][r], end='')
            tree_row.append(Tree(r, c, grid[c][r]))
        tree_grid.append(tree_row)

    # assign each tree object references to its neighbors
    for c in range(len(tree_grid)):
        for r in range(len(tree_grid[0])):
            tree = tree_grid[c][r]
            if tree.y > 0:
                tree.north = tree_grid[c-1][r]
            if tree.x > 0:
                tree.west = tree_grid[c][r-1]
            if tree.y < (len(tree_grid) - 1):
                tree.south = tree_grid[c+1][r]
            if tree.x < (len(tree_grid[0]) - 1):
                tree.east = tree_grid[c][r+1]
    return tree_grid


def check_rows(grid):
    visible = []
    gridlen = len(grid)
    grid_rowlen = len(grid[0])
    # check rows
    for c in range(gridlen):
        lastheight = 0
        lastmaxheight = 0
        for r in range(grid_rowlen):
            height = grid[c][r]

            if lastmaxheight < lastheight:
                lastmaxheight = lastheight
            if (r == 0 or c == 0) or \
               (r == grid_rowlen-1 or c == gridlen-1):
                visible.append((r, c))
                lastheight = height
                continue

            if lastheight < height and height > lastmaxheight:
                visible.append((r, c))
                lastheight = height
                continue

        # right to left
        lastheight = 0
        lastmaxheight = 0
        for r in range(grid_rowlen-1, -1, -1):
            height = grid[c][r]

            if lastmaxheight < lastheight:
                lastmaxheight = lastheight
            if (r == 0 or c == 0) or \
               (r == grid_rowlen-1 or c == gridlen-1):
                visible.append((r, c))
                lastheight = height
                continue

            if lastheight < height and height > lastmaxheight:
                visible.append((r, c))
                lastheight = height
                continue

    visible = list(set(visible))
    return visible


def check_rows_and_cols(grid):
    visible_rows = check_rows(grid)
    visible_cols = check_rows([list(i) for i in zip(*grid)])
    visible_cols = [(b, a) for a, b in visible_cols]
    return list(set(visible_rows + visible_cols))


def print_marked(grid, coords):
    for c in range(len(grid)):
        for r in range(len(grid[0])):
            if (r, c) in coords:
                print("*", end="")
            else:
                print(grid[c][r], end="")
        print()


def print_unmarked(grid, coords):
    for c in range(len(grid)):
        for r in range(len(grid[0])):
            if (r, c) not in coords:
                print("*", end="")
            else:
                print(grid[c][r], end="")
        print()


def print_grid(grid):
    for c in range(len(grid)):
        for r in range(len(grid[0])):
            print(grid[c][r], end="")
        print()


grid = load_grid("input.txt")
# tree_grid = build_tree_grid(grid)
print(f"part 1: {len(check_rows_and_cols(grid))}")



