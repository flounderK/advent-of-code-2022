#!/usr/bin/env python3


class ClockCPU:
    def __init__(self):
        self.x = 0
        self.queue = []



with open("input.txt", "r") as f:
    instructions = f.read().splitlines()


executions = []
target_counts = [20, 60, 100, 140, 180, 220]
x_vals = []
cycle_count = 0
x_val = 1
for ind, line in enumerate(instructions):
    add_val = None
    if line.startswith("noop"):
        cycle_count += 1
        print("noop")
    elif line.startswith("addx"):
        cycle_count += 2
        add_val = int(line.split(" ")[-1])
        print(f"addx {add_val}")

    to_pop = []
    for i in target_counts:
        if cycle_count == i:
            x_vals.append((x_val, cycle_count))
            to_pop.append(i)
        elif cycle_count > i:
            real_cycle_count = cycle_count - 1
            x_vals.append((x_val, real_cycle_count))
            to_pop.append(i)

    for i in to_pop:
        target_counts.remove(i)

    if add_val is not None:
        x_val = x_val + add_val


for a, b in x_vals:
    print(f"{b} * x: {a} = {a*b}")

signal_strength = sum([a*b for a, b in x_vals])

print(f"part 1: {signal_strength}")

