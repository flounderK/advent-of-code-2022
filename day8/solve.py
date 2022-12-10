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
        self._sceinic_score = None
        self.scenic_score_values = {}

    @property
    def scenic_score(self):
        if self._sceinic_score is not None:
            return self._sceinic_score

        scenic_value = 1
        for tree_dir in ["north", "east", "south", "west"]:
            last_tree = self
            visible_trees = 0
            tree = getattr(last_tree, tree_dir)
            while tree is not None:
                visible_trees += 1
                # tree is still visible, even if it stops more from
                # being visible
                if tree.height >= self.height:
                    break
                last_tree = tree
                tree = getattr(last_tree, tree_dir)

            scenic_value = scenic_value * visible_trees
            self.scenic_score_values[tree_dir] = visible_trees

        self._sceinic_score = scenic_value
        return scenic_value

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
        # left to right
        for r in range(grid_rowlen):
            height = grid[c][r].height

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
            height = grid[c][r].height

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
treegrid = build_tree_grid(grid)
visible_locations = check_rows_and_cols(treegrid)
print(f"part 1: {len(visible_locations)}")

best_scenic_score_tree = None
for c in range(len(treegrid)):
    for r in range(len(treegrid[0])):
        # if (r, c) in visible_locations:
        #     continue
        tree = treegrid[c][r]
        if best_scenic_score_tree is None:
            best_scenic_score_tree = tree
            continue
        scenic_score = tree.scenic_score
        if scenic_score > best_scenic_score_tree.scenic_score:
            best_scenic_score_tree = tree

print(f"part 2: {best_scenic_score_tree.scenic_score}")



