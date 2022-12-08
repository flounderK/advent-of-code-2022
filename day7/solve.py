#!/usr/bin/env python3


class FakeFile:
    def __init__(self, size, name):
        self.size = size
        self.name = name

    def __repr__(self):
        return f"{self.size} {self.name}"


class FakeDir:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.dirs = []
        self._haschanged = True
        self._lastsize = 0

    def __repr__(self):
        return f"dir {self.name}"

    def __str__(self):
        return f"{self.name}"

    def add(self, item):
        if isinstance(item, FakeFile):
            self.files.append(item)
        elif isinstance(item, FakeDir):
            self.dirs.append(item)

        self._haschanged = True

    def getsize(self):
        if not self._haschanged:
            return self._lastsize
        total = sum([i.size for i in self.files])
        total += sum([i.getsize() for i in self.dirs])
        self._lastsize = total
        self._haschanged = False
        return total


class PseudoFS:
    def __init__(self):
        self.fs = {}
        self._current = "/"
        self._curdir = None
        self.root = None

    def cd_rel(self, rel_path):
        if self._curdir is None:
            self._curdir = FakeDir(rel_path)
            self.root = self._curdir
            self._current = rel_path
            self.fs[self._current] = self._curdir
            return
        if rel_path == "..":
            self._current, popped_dir = self._current.rsplit("/", 1)
        else:
            self._current = "/".join([self._current, rel_path])

        self._curdir = self.fs[self._current]

    def add_listed_from_line(self, listed):
        p1, p2 = listed.split(" ")
        if listed.startswith("dir"):
            dirname = p2
            dirpath = "/".join([self._current, dirname])
            fakedir = FakeDir(dirname)
            self._curdir.add(fakedir)
            self.fs[dirpath] = fakedir
        elif p1.isdecimal():
            self._curdir.add(FakeFile(int(p1), p2))

    def add_ls(self, listed_lines):
        """
        excludes initial ls
        """
        for line in listed_lines:
            self.add_listed_from_line(line)

    def __repr__(self):
        return f"PseudoFS:{self._current}$ "


with open("input.txt", "r") as f:
    inp_raw = f.read()

commands_and_output = [i.strip("\n") for i in inp_raw.split("$ ") if i != '']

pfs = PseudoFS()

for command in commands_and_output:
    if command.startswith("ls"):
        splitcommand = command.splitlines()
        pfs.add_ls(splitcommand[1:])
    elif command.startswith("cd"):
        _, rel_dir = command.split(" ")
        pfs.cd_rel(rel_dir)

p1_total = 0

for d in pfs.fs.values():
    if d.getsize() <= 100000:
        p1_total += d.getsize()

print(f"part 1: {p1_total}")

total_drive_size = 70000000
needed_space_for_update = 30000000
remaining_needed_space = needed_space_for_update - (total_drive_size - pfs.root.getsize())

deletion_candidates = []
for d in pfs.fs.values():
    if d.getsize() >= remaining_needed_space:
        deletion_candidates.append(d.getsize())

print(f"part 2: {min(deletion_candidates)}")
