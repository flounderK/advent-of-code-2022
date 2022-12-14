#!/usr/bin/env python3
import string
from collections import deque


def colorize(val, fmt='\x1b[31m%s\x1b[0m'):
    return fmt % (str(val))


class MapCoord:
    START = None
    END = None

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name
        if name == "E":
            self.height = 26
            MapCoord.END = self
        elif name == "S":
            self.height = -1
            MapCoord.START = self
        else:
            self.height = string.ascii_lowercase.index(name)
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.visited = False
        self.travel_mark = None
        self.visitor = None
        self._edges = []

    @property
    def edges(self):
        if self._edges:
            return self._edges

        for n, dir_ in zip(["north", "east", "south", "west"],
                           ["^", ">", "v", "<"]):
            attr = getattr(self, n)
            if not attr:
                continue
            self._edges.append((attr, dir_))
        return self._edges

    def __repr__(self):
        if self.travel_mark:
            return f"{self.travel_mark}"
        return f"{self.name}"

    def reset_visited(self):
        self.visited = False
        self.visitor = None
        self.travel_mark = None


class HeightMap:
    def __init__(self):
        self.start = None
        self.end = None
        self.grid = None
        self.coord_grid = None
        self.route = []

    def build_coord_grid(self, grid):
        coord_grid = []
        # make coord objects
        for c in range(len(grid)):
            coord_row = []
            for r in range(len(grid[0])):
                # print(grid[c][r], end='')
                coord_row.append(MapCoord(r, c, grid[c][r]))
            coord_grid.append(coord_row)

        # assign each coord object references to its neighbors
        for c in range(len(coord_grid)):
            for r in range(len(coord_grid[0])):
                coord = coord_grid[c][r]
                if coord.y > 0:
                    coord.north = coord_grid[c-1][r]
                if coord.x > 0:
                    coord.west = coord_grid[c][r-1]
                if coord.y < (len(coord_grid) - 1):
                    coord.south = coord_grid[c+1][r]
                if coord.x < (len(coord_grid[0]) - 1):
                    coord.east = coord_grid[c][r+1]
        self.coord_grid = coord_grid
        # return coord_grid

    @staticmethod
    def from_file(filename):
        hm = HeightMap()
        with open(filename, "r") as f:
            inp_lines = f.read().splitlines()

        hm.grid = inp_lines
        hm.build_coord_grid(hm.grid)
        return hm

    def print(self):
        for c in self.coord_grid:
            print("".join([str(i) for i in c]))

    def print_raw_grid(self):
        print("\n".join(self.grid))

    def get_steps_traveled(self):
        node = MapCoord.END
        count = 0
        while node.visitor:
            count += 1
            node = node.visitor
        if count:
            return count
        return None

    def bfs(self):
        """
        starting at S
        """
        root = MapCoord.START
        end = MapCoord.END
        queue = deque([root])
        root.visited = True
        while queue:
            v = queue.popleft()
            # print(f"processing {v}")
            # self.print()
            # print()
            if v == end:
                return v
            added_edge = False
            for edge, dir_ in v.edges:
                if edge.height <= v.height+1 and not edge.visited:
                    added_edge = True
                    edge.visited = True
                    edge.visitor = v
                    # v.travel_mark = colorize(dir_)
                    queue.append(edge)
            if not added_edge:
                v.travel_mark = colorize(v.name, '\x1b[34m%s\x1b[0m')

    def reset(self):
        for row in self.coord_grid:
            for coord in row:
                coord.reset_visited()

    def set_start(self, new_start):
        MapCoord.START = new_start


hm = HeightMap.from_file("input.txt")
hm.bfs()
hm.print()
print(f"part 1: {hm.get_steps_traveled()}")
hm.reset()

# get all of the starting points
starting_points = []
for row in hm.coord_grid:
    for i in row:
        if i.name in ["S", "a"]:
            starting_points.append(i)

lowest = 9999
lowest_starting_point = None
for s in starting_points:
    hm.set_start(s)
    hm.bfs()
    new_count = hm.get_steps_traveled()
    if new_count and new_count < lowest:
        lowest = new_count
        lowest_starting_point = s
    hm.reset()

print(f"part 2: {lowest}")
