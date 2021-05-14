#! /usr/bin/env python3

import os

from ..utils.marksheet import Marksheet

# -----------------------------------------------------------------------------

def stats(self, minimal, students):

    marksheet_path = os.path.join(self.cfg["assgn_dir"], self.cfg["marksheet"])
    if not os.path.isfile(marksheet_path):
        self.console.error("Marksheet does not exist.")
        return

    marksheet = Marksheet(marksheet_path)

    if students != []:
        results = {}
        for student in students:
            results[student] = marksheet[student]
        return results

    results = {}

    if minimal:
        results["mean"] = marksheet.mean()
        results["median"] = marksheet.median()
        return results

    results["total_marked"] = marksheet.num_marked()
    results["compile_success"] = marksheet.num_compiled()
    results["compile_failed"] = marksheet.num_compile_failed()
    
    results["all"] = {}
    results["all"]["mean"] = marksheet.mean()
    results["all"]["median"] = marksheet.median()

    results["compiled"] = {}
    results["compiled"]["mean"] = marksheet.mean(True)
    results["compiled"]["median"] = marksheet.median(True)


    results["distribution"] = marksheet.get_distribution()

    return results
    