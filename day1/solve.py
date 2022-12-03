#!/usr/bin/env python3

with open("input.txt", "r") as f:
    content = f.read()


elfloads = content.split("\n\n")
elfload_values = [[int(i) for i in load.splitlines()] for load in elfloads]

total_calories_per_load = [sum(i) for i in elfload_values]


print(f"part 1: {max(total_calories_per_load)}")

total_calories_per_load_cpy = total_calories_per_load.copy()

max_value_sum = 0
for _ in range(3):
    curr_max = max(total_calories_per_load_cpy)
    curr_max_idx = total_calories_per_load_cpy.index(curr_max)
    # set the old max to zero so that the next highest value can
    # be found, even if it happens to be the same as the previous max
    total_calories_per_load_cpy[curr_max_idx] = 0
    max_value_sum += curr_max

print(f"part 2: {max_value_sum}")
