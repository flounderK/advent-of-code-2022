#!/usr/bin/env python3
import string
import re
from collections import defaultdict


class StackMove:
    def __init__(self, num, src, dest):
        self.num = int(num)
        self.src = src
        self.dest = dest

    def single_move(self, stack_lookup):
        from_stack = stack_lookup[self.src]
        to_stack = stack_lookup[self.dest]

        for i in range(self.num):
            crate = from_stack.pop()
            to_stack.append(crate)

    def multi_move(self, stack_lookup):
        from_stack = stack_lookup[self.src]
        to_stack = stack_lookup[self.dest]

        crates = from_stack[-self.num:]
        from_stack = from_stack[:-self.num]
        to_stack = to_stack + crates

        stack_lookup[self.src] = from_stack
        stack_lookup[self.dest] = to_stack

    def __repr__(self):
        return "move %d from %s to %s" % (self.num, self.src, self.dest)


with open("input.txt", "r") as f:
    inp_raw = f.read()

stacks_raw, moves_raw = inp_raw.split("\n\n")

stacks_lines = stacks_raw.splitlines()

largest_line = max([len(i) for i in stacks_lines])
stacks_lines = [i.ljust(largest_line, ' ') for i in stacks_lines]
# parse the stack diagram
parsed_stacks = [list(k.strip()) for k in [''.join(i[::-1]) for i in zip(*stacks_lines)] if k[0] in string.digits]


stack_lookup_p1 = {i[0]: i[1:] for i in parsed_stacks}
stack_lookup_p2 = {k: v.copy() for k, v in stack_lookup_p1.items()}
stack_lookup_orig = {k: v.copy() for k, v in stack_lookup_p1.items()}

# parse the moves
moves = [StackMove(*i.groups()) for i in re.finditer(r'move (\d+) from (\d+) to (\d+)', moves_raw)]

for move in moves:
    move.single_move(stack_lookup_p1)


p1_output = ''
for i in range(len(stack_lookup_p1.keys())):
    p1_output += stack_lookup_p1[str(i+1)][-1]

print(f"part 1: {p1_output}")

for move in moves:
    move.multi_move(stack_lookup_p2)

p2_output = ''
for i in range(len(stack_lookup_p2.keys())):
    p2_output += stack_lookup_p2[str(i+1)][-1]

print(f"part 2: {p2_output}")
