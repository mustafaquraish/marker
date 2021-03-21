#! /usr/bin/env python3

import os
import sys
import math

from ..utils.marksheet import Marksheet
from ..utils.console import console

from rich.markdown import HorizontalRule


def getMean(arr):
    return sum(arr) / len(arr)

def getMedian(arr):
    return sorted(arr)[ len(arr) // 2 ]


# -----------------------------------------------------------------------------

def stats_handler(cfg, student, minimal):

    marksheet_path = f'{cfg["assgn_dir"]}/{cfg["marksheet"]}'
    if not os.path.isfile(marksheet_path):
        console.error("Marksheet does not exist.")
        return

    marksheet = Marksheet(marksheet_path)

    if student is not None:
        marks = marksheet[student]
        if marks == []:
            console.print(f"Compile failed for [yellow]{student}[/yellow]:",
                           "0 marks.")
        else:
            console.print(f"Marks for [yellow]{student}[/yellow]: {marks}",
                          f"(total: {sum(marks)})")
        return

    if minimal:
        console.print(f"  Mean score: {marksheet.mean():.3f}")
        console.print(f"Median score: {marksheet.median()}")
        return

    console.print(HorizontalRule())

    console.print(f"   Total marked: {marksheet.num_marked()}")
    console.print(f"Compile success: {marksheet.num_compiled()}")
    console.print(f" Compile failed: {marksheet.num_compile_failed()}")
    console.print(HorizontalRule())

    console.print(f"  Mean score [yellow]     (all)[/yellow]: {marksheet.mean():.3f}")
    console.print(f"Median score [yellow]     (all)[/yellow]: {marksheet.median()}")
    console.print(HorizontalRule())

    console.print(f"  Mean score [yellow](compiled)[/yellow]: {marksheet.mean(True):.3f}")
    console.print(f"Median score [yellow](compiled)[/yellow]: {marksheet.median(True)}")
    console.print(HorizontalRule())


    console.print("Mark distribution:")
    
    HIST_LINE_LEN = 20

    distribution = marksheet.get_distribution()

    output_scale = HIST_LINE_LEN / max(k for _,k in distribution.items())
    for mark, count in distribution.items():
        line_count = math.ceil(count * output_scale)
        hist_line = 'x' * (line_count) + ' ' * (HIST_LINE_LEN - line_count)
        console.print(f" {mark:3d} : [green]{hist_line}[/green] | {count:3d} students")

    console.print(HorizontalRule())
    