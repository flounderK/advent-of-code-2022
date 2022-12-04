#!/usr/bin/env python3
import re


def either_range_contains(thisrange, thatrange):
    thisstart, thisend = thisrange
    thatstart, thatend = thatrange
    if thisstart <= thatstart and \
       thatend <= thisend:
        return True
    if thatstart <= thisstart and \
       thisend <= thatend:
        return True

    return False


def ranges_contain_overlaps(thisrange, thatrange):
    thisstart, thisend = thisrange
    thatstart, thatend = thatrange
    thisnums = set(list(range(thisstart, thisend+1)))
    thatnums = set(list(range(thatstart, thatend+1)))
    if len(thisnums.intersection(thatnums)) > 0:
        return True
    return False


rexp = re.compile(r'(\d+)-(\d+)')
with open("input.txt", "r") as f:
    assignments = f.read().splitlines()

parsed_assignments = []
for assignment in assignments:
    section_ranges = []
    for section_range_match in re.finditer(rexp, assignment):
        sect_start, sect_end = section_range_match.groups()
        section_ranges.append((int(sect_start),
                               int(sect_end)))
    parsed_assignments.append(section_ranges)

num_contained_ranges = 0
for assignment in parsed_assignments:
    if either_range_contains(*assignment):
        num_contained_ranges += 1

print(f"part 1: {num_contained_ranges}")


num_containing_overlaps = 0
for assignment in parsed_assignments:
    if ranges_contain_overlaps(*assignment):
        num_containing_overlaps += 1
print(f"part 2: {num_containing_overlaps}")
