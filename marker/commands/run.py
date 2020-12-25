#! /usr/bin/env python3

import os
import sys

from ..utils import config
from ..utils import pushd
from ..utils import run_command
from ..utils.tests import run_test
from ..utils.marksheet import Marksheet

def mark_submission(student, cfg):
    '''
    Given a student identifier, run all the test cases defined in the config
    and build the report. The current working directory is expected to be
    the root of the assignment directory.

    Returns: Array of marks for the test cases.
    '''
    testing_dir = f'candidates/{student}/{cfg["testing_dir"]}'
    mark_list = []

    # Go into the testing directory
    with pushd(testing_dir):
        # Open the report file
        with open(cfg['report'], 'w') as report_file:

            # Add the report header if needed
            if cfg['report_header'] is not None:
                report_file.write(cfg['report_header'] + '\n')

            # -----------------------------------------------------------------

            # Force recompile if needed
            if cfg['recompile'] and (cfg['compile'] is not None) :
                with open(cfg['compile_log'], 'w') as log:
                    run_command(cfg['compile'], timeout=10, output=log)

            # -----------------------------------------------------------------

            # If the compile log exists, include it in the report based on the
            # provided option in the config file.
            if cfg['compile'] and cfg['include_compile_log']:
                report_file.write('- Compiling code ...\n\n')
                if os.path.isfile(cfg['compile_log']):
                    with open(cfg['compile_log']) as compile_log:
                        report_file.write(compile_log.read() + '\n')

            # -----------------------------------------------------------------
            
            # If a compilation check is set, run the command. If the check 
            # fails, then we don't have to run any of the tests.
            run_tests = True
            if cfg['compile_check'] is not None:
                status, code = run_command(cfg['compile_check'], timeout=1)
                if not (status == 'exit' and code == 0):
                    report_file.write("- Compilation Failed.\n")
                    run_tests = False

            # -----------------------------------------------------------------

            
            for test_case in cfg['tests']:
                # If compilation was fine, run test and append marks to array
                if run_tests:
                    mark_list.append(run_test(test_case, report_file))
                # Otherwise just give 0 marks for each test
                else:
                    mark_list.append(0)

            # -----------------------------------------------------------------

            # Output the total mark to the report for completeness
            total_out_of = sum(test['mark'] for test in cfg['tests'])
            total_mark = sum(mark_list)

            report_file.write("-"*79 + '\n\n')
            report_file.write(f" TOTAL MARKS: {total_mark} / {total_out_of}\n")

    print(f"- Marking {student} ... {total_mark} marks.", flush=True)
    return mark_list

# -----------------------------------------------------------------------------

def run_handler(cfg, student):

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

        # Or if the marksheet doesn't exist, ask the user if they want to make 
        # a new one for all of the submissions
        elif not os.path.exists(marksheet_path):
            # Prompt the user to create
            create = input(f"{marksheet_path} does not exist. Create? [Y]/n: ")
            # Add all the students in the `candidates` directory to marksheet
            if "n" not in create:
                marksheet.add_students(all_students)
            else:
                print("Marksheet not found or created. Stopping.")
                return
        
        # Marksheet exists! Just load it in
        else:
            marksheet.load(marksheet_path)
    

        # If a specific student has been specified, re-run for only them.
        # Just reset the marksheet
        if student is not None:
            if student not in all_students:
                print(student, "submission directory doesn't exist. Stopping.")
                return
            students_to_mark = [ student ]
        else:
            students_to_mark = marksheet.unmarked()

        # Run the marker!
        for student in students_to_mark:
            try:
                marks_list = mark_submission(student, cfg)
                marksheet[student] = marks_list
                marksheet.save(marksheet_path)
            except Exception as e:
                print(f'Error when marking {student}: {e}')

    print("Done.")