#!/usr/bin/env python3
from collections import namedtuple


class Knot:
    def __init__(self, name):
        self._x = 0
        self._y = 0
        self.last_x = 0
        self.last_y = 0
        self.name = name

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, val):
        self.last_x = self._x
        self._x = val

    @y.setter
    def y(self, val):
        self.last_y = self._y
        self._y = val

    def __eq__(self, other):
        if isinstance(other, tuple):
            return (self._x, self._y) == other

    def __repr__(self):
        return f"{self.name}"


class RopeGrid:
    def __init__(self, length=9, do_print=False):
        self.head_x = 0
        self.head_y = 0
        self.head = Knot("H")
        self.knots = [Knot(i) for i in range(1, length+1)]
        self.tail = self.knots[-1]
        self.maxx = 6
        self.maxy = 5
        self.do_print = do_print
        self.tail_reached = set()

    def move(self, direct, num):
        if self.do_print:
            print(f"== {direct} {num}")
            print("")

        for _ in range(num):

            prev_head_x = self.head.x
            prev_head_y = self.head.y

            # head movement
            if direct == "L":
                self.head.x -= 1
            elif direct == "R":
                self.head.x += 1
            if direct == "U":
                self.head.y += 1
            elif direct == "D":
                self.head.y -= 1

            # tail catch up
            # this also handles diagonal movement
            last_head = self.head
            for tail in self.knots:
                orig_x = tail.x
                orig_y = tail.y
                x_diff = last_head.x - tail.x
                y_diff = last_head.y - tail.y
                if abs(x_diff) > 1 or abs(y_diff) > 1:
                    tail.x = prev_head_x
                    tail.y = prev_head_y
                    # tail.x = last_head.last_x
                    # tail.y = last_head.last_y
                prev_head_x = orig_x
                prev_head_y = orig_y
                last_head = tail

            self.tail_reached.add((self.tail.x, self.tail.y))
            # just modify grid boundaries for printing
            if self.head.x > self.maxx:
                self.maxx = self.head.x

            if self.head.y > self.maxy:
                self.maxy = self.head.y

            if self.do_print is True:
                self.print()

    def print(self):
        for c in range(self.maxy-1, -1, -1):
            for r in range(self.maxx):
                if c == self.head.y and r == self.head.x:
                    print("H", end="")
                elif c == self.tail.y and r == self.tail.x:
                    print("T", end="")
                elif c == 0 and r == 0:
                    print("S", end="")
                elif (r, c) in self.knots:
                    knot = self.knots[self.knots.index((r, c))]
                    print(knot, end="")
                else:
                    print(".", end="")
            print("")
        print("")


with open("test.txt", "r") as f:
    directional_movements = [i.split(" ") for i in f.read().splitlines()]
    directional_movements = [(a, int(b)) for a, b in directional_movements]


rg = RopeGrid(1, False)

for i in directional_movements:
    rg.move(*i)

print(f"part 1: {len(rg.tail_reached)}")

rg2 = RopeGrid(9, True)

for i in directional_movements:
    rg2.move(*i)
