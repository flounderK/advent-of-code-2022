#!/usr/bin/env python3
from string import ascii_letters


def get_priority(letter):
    return ascii_letters.index(letter)+1


def batch(it, sz):
    length = len(it)
    for i in range(0, length, sz):
        yield it[i:i+sz]


with open("input.txt", "r") as f:
    c = f.read()

rucksacks = c.splitlines()

rucksack_compartments = [(i[:(len(i) // 2)], i[(len(i) // 2):]) for i in rucksacks]

total_priority_sum = 0
for rucksack in rucksack_compartments:
    sets = [set(i) for i in rucksack]
    shared_character = list(sets[0].intersection(sets[1]))[0]
    total_priority_sum += get_priority(shared_character)


print(f"part 1: {total_priority_sum}")

badge_priority_sums = 0
for rucksack_batch in batch(rucksacks, 3):
    rucksack_sets = [set(i) for i in rucksack_batch]
    intersecting_set = rucksack_sets[0].intersection(rucksack_sets[1])
    shared_char = list(intersecting_set.intersection(rucksack_sets[2]))[0]
    badge_priority_sums += get_priority(shared_char)

print(f"part 2: {badge_priority_sums}")
