#!/usr/bin/env python3


class RopeGrid:
    def __init__(self, do_print=False, length=2):
        self.head_x = 0
        self.head_y = 0
        self.tail_x = 0
        self.tail_y = 0
        self.maxx = 0
        self.maxy = 0
        self.do_print = do_print
        self.tail_reached = set()

    def move(self, direct, num):
        if self.do_print:
            print(f"== {direct} {num}")
            print("")

        for _ in range(num):

            prev_head_x = self.head_x
            prev_head_y = self.head_y
            # head movement
            if direct == "L":
                self.head_x -= 1
            elif direct == "R":
                self.head_x += 1
            if direct == "U":
                self.head_y += 1
            elif direct == "D":
                self.head_y -= 1

            # tail catch up
            # this also handles diagonal movement
            x_diff = self.head_x - self.tail_x
            y_diff = self.head_y - self.tail_y
            if abs(x_diff) > 1 or abs(y_diff) > 1:
                self.tail_x = prev_head_x
                self.tail_y = prev_head_y

            self.tail_reached.add((self.tail_x, self.tail_y))
            if self.head_x > self.maxx:
                self.maxx = self.head_x

            if self.head_y > self.maxy:
                self.maxy = self.head_y

            if self.do_print is True:
                self.print()

    def print(self):
        for c in range(self.maxy-1, -1, -1):
            for r in range(self.maxx):
                if c == self.head_y and r == self.head_x:
                    print("H", end="")
                elif c == self.tail_y and r == self.tail_x:
                    print("T", end="")
                elif c == 0 and r == 0:
                    print("S", end="")
                else:
                    print(".", end="")
            print("")
        print("")


with open("input.txt", "r") as f:
    directional_movements = [i.split(" ") for i in f.read().splitlines()]
    directional_movements = [(a, int(b)) for a, b in directional_movements]


rg = RopeGrid(False)

for i in directional_movements:
    rg.move(*i)

print(f"part 1: {len(rg.tail_reached)}")
