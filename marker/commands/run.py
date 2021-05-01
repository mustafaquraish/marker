#! /usr/bin/env python3

import os
import sys

from ..utils import config
from ..utils import pushd
from ..utils import run_command
from ..utils.tests import run_test
from ..utils.marksheet import Marksheet
from ..utils.console import console
import json

def mark_submission(student, cfg):
    '''
    Given a student identifier, run all the test cases defined in the config
    and build the report. The current working directory is expected to be
    the root of the assignment directory.

    Returns: Array of marks for the test cases.
    '''
    student_dir = f'candidates/{student}'

    result = { "tests": [], "marks": [] }

    # Go into the testing directory
    with pushd(student_dir):

        # Add the report header if needed
        if cfg['report_header'] is not None:
            result["header"] = cfg['report_header'] 

        # -----------------------------------------------------------------

        # Force recompile if needed
        if cfg['recompile'] and (cfg['compile'] is not None) :
            _, clog = run_command(cfg['compile'], timeout=10)
            result["compile_log"] = clog

        # -----------------------------------------------------------------

        # If the compile log exists, include it in the report based on the
        # provided option in the config file.
        if cfg['compile'] and cfg['include_compile_log']:
            if os.path.isfile(cfg['compile_log']):
                with open(cfg['compile_log']) as compile_log:
                    result["compile_log"] = compile_log.read()

        # -----------------------------------------------------------------
        
        # If a compilation check is set, run the command. If the check 
        # fails, then we don't have to run any of the tests.
        run_tests = True
        if cfg['compile_check'] is not None:
            code, output = run_command(cfg['compile_check'], timeout=1)
            if not (code == 0):
                result["compiled"] = False
                run_tests = False
            else:
                result["compiled"] = True

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
        
        with open("results.json", "w") as results_json:
            json.dump(result, results_json, indent=4)

    return result

# -----------------------------------------------------------------------------

def run_handler(cfg, student):

    if not os.path.isdir(f'{cfg["assgn_dir"]}/candidates'):
        console.error("Candidates directory does exist. Quitting.")
        return

    # Enter assignment directory
    with pushd(cfg['assgn_dir']):

        # Create a new marksheet, we will initialize it below
        marksheet = Marksheet()
        marksheet_path = cfg['marksheet']

        all_students = sorted(os.listdir('candidates'))

        # If we want to force-remark all submissions, don't load the marksheet
        # but just create a new one
        if cfg['all']:
            marksheet.add_students(all_students)

        # Or if the marksheet doesn't exist, create a new one with all students
        elif not os.path.exists(marksheet_path):
            marksheet.add_students(all_students)
            
        # Marksheet exists! Just load it in
        else:
            marksheet.load(marksheet_path)
    

        # If a specific student has been specified, re-run for only them.
        # Just reset the marksheet
        if student is not None:
            if student not in all_students:
                console.error(student, "submission directory doesn't exist. Stopping.")
                return
            students_to_mark = [ student ]
        else:
            students_to_mark = list(marksheet.unmarked_students())

        if len(students_to_mark) == 0:
            console.error("Everyone is already marked. Run with -a to re-run, or with"
                          " an individual student name")
            return

        # Run the marker!
        for student in console.track(students_to_mark, "Marking"):
            result = mark_submission(student, cfg)
            marksheet[student] = result["marks"]
            marksheet.save(marksheet_path)
            if cfg["show_marks"]:
                console.log(student, "total marks", result["total"])

