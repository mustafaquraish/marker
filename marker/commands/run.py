import os
import sys

from ..utils import pushd, listdir
from ..utils import run_command
from ..utils.tests import run_test
from ..utils.marksheet import Marksheet
from ..utils.report import generate_report 
import json

def mark_submission(student, marker):
    '''
    Given a student identifier, run all the test cases defined in the config
    and build the report. The current working directory is expected to be
    the root of the assignment directory.

    Returns: Array of marks for the test cases.
    '''
    cfg = marker.cfg

    student_dir = os.path.join('candidates', student)
    result = { "tests": [], "marks": [] }
    result["out_of"] = sum(test["mark"] for test in cfg["tests"])


    # Go into the testing directory
    with pushd(student_dir):

        # -----------------------------------------------------------------
        
        result["compile_log"] = ""

        # Force recompile if needed
        if cfg['recompile'] and (cfg['compile'] is not None) :
            _, clog = run_command(cfg['compile'], timeout=10, limit=None)
            result["compile_log"] = clog

        # If the compile log exists, include it in the report based on the
        # provided option in the config file.
        elif os.path.isfile(cfg['compile_log']):
            with open(cfg['compile_log']) as compile_log:
                result["compile_log"] = compile_log.read()
            

        # -----------------------------------------------------------------
        
        result["compiled"] = True
        run_tests = True

        # If a compilation check is set, run the command. If the check 
        # fails, then we don't have to run any of the tests.
        if cfg['compile_check'] is not None:
            code, output = run_command(cfg['compile_check'], timeout=1)
            if not (code == 0):
                result["compiled"] = False
                run_tests = False

        # -----------------------------------------------------------------

        # If compilation was fine, run test and append marks to array
        if run_tests:
            for test_case in cfg['tests']:
                cur_result = run_test(test_case)
                result["marks"].append(cur_result["mark"])
                result["tests"].append(cur_result)
        
        # Otherwise, marklist remains empty

        # -----------------------------------------------------------------

        # Output the total mark to the report for completeness
        result["total"] = sum(result["marks"])
        
        with open(cfg["results"], "w") as results_json:
            json.dump(result, results_json, indent=2)

        with open(cfg["report"], "w") as report_file:
            report_text = generate_report(result, cfg)
            report_file.write(report_text)

    return result

# -----------------------------------------------------------------------------

def run(self, students, recompile, run_all, quiet):
    candidates_dir = os.path.join(self.cfg["assgn_dir"], "candidates")
    if not os.path.isdir(candidates_dir):
        self.console.error("Candidates directory does exist. Quitting.")
        return

    # Enter assignment directory
    with pushd(self.cfg['assgn_dir']):

        all_students = sorted(listdir('candidates'))

        # Load in an existing marksheet...
        marksheet_path = self.cfg['marksheet']
        marksheet = Marksheet()
        if os.path.isfile(marksheet_path):
            marksheet.load(marksheet_path)
        # Add all students (in case new ones were downloaded...)
        marksheet.add_students(all_students)

        # If -a is specified, it takes priority and everyone is run
        if run_all:
            students = all_students
        # Otherwise, if no students specified, only run unmarked ones.
        elif students == []:
            students = list(marksheet.unmarked_students())

        if len(students) == 0:
            self.console.error("Everyone is already marked. Run with -a to "
                               "re-run, or with an individual student name")
            return

        self.cfg["recompile"] = recompile

        # Run the marker!
        for student in self.console.track(students, "Marking"):
            result = mark_submission(student, self)
            marksheet[student] = result["marks"]
            if not quiet:
                self.console.log(student, "total marks", result["total"])

            # Update marksheet on disk after every change
            marksheet.save(marksheet_path)

