#!/usr/bin/env python3


def batch(it, sz):
    length = len(it)
    for i in range(0, length, sz):
        yield it[i:i+sz]


with open("input.txt", "r") as f:
    instructions = f.read().splitlines()


def get_pixels(cycle_count, x_val):
    cycle_count_mod = cycle_count % 40
    if cycle_count_mod >= x_val - 1 and cycle_count_mod <= x_val+1:
        pixels = "#"
    else:
        pixels = "."
    return pixels


executions = []
target_counts = [20, 60, 100, 140, 180, 220]
x_vals = []
cycle_count = 0
x_val = 1
pixels = ""
for ind, line in enumerate(instructions):
    add_val = None
    xval_range = [x_val - 1, x_val, x_val+1]
    # print("".join(["." if i not in xval_range else "#" for i in range(40)]))

    if line.startswith("noop"):
        pixels += get_pixels(cycle_count, x_val)
        cycle_count += 1
        print("noop")
    elif line.startswith("addx"):
        pixels += get_pixels(cycle_count, x_val)
        cycle_count += 1
        pixels += get_pixels(cycle_count, x_val)
        cycle_count += 1
        add_val = int(line.split(" ")[-1])
        print(f"addx {add_val}")

    print(pixels)

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


for c in batch(pixels, 40):
    print(c)

