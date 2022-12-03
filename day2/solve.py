#!/usr/bin/env python3

import enum


class HandShape(enum.IntEnum):
    NONE = 0
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class RoundOutcome(enum.IntEnum):
    LOST = 0
    DRAW = 3
    WON = 6


WIN_LOOKUP_ARRAY = [0]*4
WIN_LOOKUP_ARRAY[HandShape.ROCK] = HandShape.SCISSORS
WIN_LOOKUP_ARRAY[HandShape.PAPER] = HandShape.ROCK
WIN_LOOKUP_ARRAY[HandShape.SCISSORS] = HandShape.PAPER

LOSS_LOOKUP_ARRAY = [0]*4
LOSS_LOOKUP_ARRAY[HandShape.PAPER] = HandShape.SCISSORS
LOSS_LOOKUP_ARRAY[HandShape.ROCK] = HandShape.PAPER
LOSS_LOOKUP_ARRAY[HandShape.SCISSORS] = HandShape.ROCK

OUTCOME_LOOKUP_ARRAY = [0]*7
OUTCOME_LOOKUP_ARRAY[RoundOutcome.WON]


def rps_opponent_round_outcome_part_1(my_play, other_play):
    if my_play == other_play:
        return my_play + RoundOutcome.DRAW

    if WIN_LOOKUP_ARRAY[my_play] == other_play:
        return my_play + RoundOutcome.WON

    return my_play + RoundOutcome.LOST


def rps_player_round_outcome_part_1(other_play, my_play):
    if my_play == other_play:
        return my_play + RoundOutcome.DRAW

    if LOSS_LOOKUP_ARRAY[my_play] == other_play:
        return my_play + RoundOutcome.LOST

    return my_play + RoundOutcome.WON


def rps_part2_outcome(other_play, round_outcome):
    score = 0
    if round_outcome == RoundOutcome.DRAW:
        score = other_play + RoundOutcome.DRAW
    elif round_outcome == RoundOutcome.WON:
        score = LOSS_LOOKUP_ARRAY[other_play] + RoundOutcome.WON
    elif round_outcome == RoundOutcome.LOST:
        score = WIN_LOOKUP_ARRAY[other_play] + RoundOutcome.LOST

    return score


with open("input.txt", "r") as f:
    inp = f.read()


ENUM_SHAPE_DICT = {
    "A": HandShape.ROCK,
    "B": HandShape.PAPER,
    "C": HandShape.SCISSORS,
    "X": HandShape.ROCK,
    "Y": HandShape.PAPER,
    "Z": HandShape.SCISSORS,
}


parsed_inputs = [[ENUM_SHAPE_DICT[sym] for sym in i.split(" ")] for i in inp.splitlines()]

total_score = 0
for round_inputs in parsed_inputs:
    total_score += rps_player_round_outcome_part_1(*round_inputs)

print(f"part 1 {total_score}")

ENUM_SHAPE_DICT_P2 = {
    "A": HandShape.ROCK,
    "B": HandShape.PAPER,
    "C": HandShape.SCISSORS,
    "X": RoundOutcome.LOST,
    "Y": RoundOutcome.DRAW,
    "Z": RoundOutcome.WON,
}

parsed_inputs_2 = [[ENUM_SHAPE_DICT_P2[sym] for sym in i.split(" ")] for i in inp.splitlines()]


p2_score = 0
for round_inputs in parsed_inputs_2:
    p2_score += rps_part2_outcome(*round_inputs)

print(f"part 2 {p2_score}")
