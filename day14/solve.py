#!/usr/bin/env python3
from collections import namedtuple


Point = namedtuple("Point", ["x", "y"])


def parse_rock_layout(filename="input.txt"):
    paths = []
    with open(filename, "r") as f:
        for line in f.read().splitlines():
            path = []
            for coord in line.split(' -> '):
                xstr, ystr = coord.split(',')
                path.append(Point(int(xstr), int(ystr)))
            paths.append(path)

    return paths


class CavernSym:
    def __init__(self):
        self._rock_points = []
        self._paths = []
        self._sand_points = []
        self._max_x = None
        self._max_y = None
        self._min_x = None
        self._min_y = None
        self.abyss_reached = False
        self.hole_plugged = False
        self.part2 = False
        self._sand_entry = Point(500, 0)

    @staticmethod
    def create_from_layout(filename="input.txt"):
        sym = CavernSym()
        sym._paths = parse_rock_layout(filename)
        sym.find_all_points()
        sym.find_point_domain()
        return sym

    def all_points_from_path(self, path):
        last_point = path[0]
        points = [last_point]
        for point in path[1:]:
            points.append(point)
            xdiff = False
            ydiff = False
            const_val = 0
            if point.x != last_point.x:
                xdiff = True
                const_val = point.y
                smaller, larger = ((point.x, last_point.x) if
                                   point.x < last_point.x else
                                   (last_point.x, point.x))
            elif point.y != last_point.y:
                ydiff = True
                const_val = point.x
                smaller, larger = ((point.y, last_point.y) if
                                   point.y < last_point.y else
                                   (last_point.y, point.y))
            for i in range(smaller, larger+1):
                if xdiff:
                    points.append(Point(i, const_val))
                elif ydiff:
                    points.append(Point(const_val, i))

            last_point = point

        return points

    def find_all_points(self):
        points = []
        for path in self._paths:
            points.extend(self.all_points_from_path(path))
        self._rock_points = list(set(points))
        self._all_used_points = set(self._rock_points + self._sand_points)

    def find_point_domain(self):
        max_x = -99999
        max_y = -99999
        min_x = 99999
        min_y = 99999
        for p in set([self._sand_entry] + list(self._all_used_points)):
            if max_x < p.x:
                max_x = p.x
            if max_y < p.y:
                max_y = p.y
            if min_x > p.x:
                min_x = p.x
            if min_y > p.y:
                min_y = p.y
        self._max_x = max_x
        self._max_y = max_y
        self._min_x = min_x
        self._min_y = min_y

    def print(self):
        if self._max_x is None:
            self.find_point_domain()
        for c in range(self._min_y-1, self._max_y+1):
            line = ""
            for r in range(self._min_x-1, self._max_x+1):
                thispoint = (r, c)
                if thispoint in self._rock_points:
                    line += "#"
                elif thispoint == self._sand_entry:
                    line += "+"
                elif thispoint in self._sand_points:
                    line += "o"
                else:
                    line += "."
            print(line)

    def tick(self):
        # self._all_used_points = set(self._rock_points + self._sand_points)
        current_point = self._sand_entry
        point_x, point_y = current_point
        infinite_line = self._max_y + 2
        while True:
            while (point_x, point_y) not in self._all_used_points:
                point_y = point_y + 1
                if not self.part2 and point_y > self._max_y:
                    self.abyss_reached = True
                    return
                if self.part2 and point_y >= infinite_line:
                    break

            # adjust for moving into the rock or sand
            point_y -= 1
            # try to move left and down one
            down_left = (point_x - 1, point_y + 1)
            if down_left not in self._all_used_points and point_y + 1 < infinite_line:
                point_x, point_y = down_left
                continue
            # try to move down right
            down_right = (point_x + 1, point_y + 1)
            if down_right not in self._all_used_points and point_y + 1 < infinite_line:
                point_x, point_y = down_right
                continue

            # looks like the current point is too stable to continue
            new_point = Point(point_x, point_y)
            self._sand_points.append(new_point)
            self._all_used_points.add(new_point)
            if (point_x, point_y) == self._sand_entry:
                self.hole_plugged = True

            break

    def run_sym(self):
        count = 0
        while not self.abyss_reached and not self.hole_plugged:
            count += 1
            self.tick()
            # if count % 25 == 0:
            #     print(f"count {count}")
        count -= 1
        return count

filename = "input.txt"

sym = CavernSym.create_from_layout(filename)
count = sym.run_sym()
sym.print()
print(f"part 1: {count}")

sym = CavernSym.create_from_layout(filename)
sym.part2 = True
count = sym.run_sym()
sym.print()
print(f"part 2: {count+1}")

