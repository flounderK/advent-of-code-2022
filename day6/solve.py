#!/usr/bin/env python3
import re


def get_headers(inp, unique_size=4):
    offset = 0
    headers = []
    while offset < len(inp):
        fetched = inp[offset:offset+unique_size]
        if len(set(fetched)) == unique_size:
            headers.append((offset, fetched))
            offset += unique_size
            continue
        offset += 1
    return headers


print("tests")
for file in ["test1.txt", "test2.txt", "test3.txt",
             "test4.txt", "test5.txt"]:
    with open(file, "r") as f:
        inp = f.read().strip()

    print(inp)
    headers = get_headers(inp)
    print(headers[0][0])

print("")

with open("input.txt", "r") as f:
    inp = f.read().strip()

headers = get_headers(inp)

print(f"part 1: {headers[0][0]+4}")

headers = get_headers(inp, 14)

print(f"part 2: {headers[0][0]+14}")
