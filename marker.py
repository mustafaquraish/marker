#! /usr/local/bin/python3

import argparse
import config
import os
import subprocess
from utils import pushd
import concurrent.futures
from testcases import run_test, run_command
from marksheet import Marksheet

# -----------------------------------------------------------------------------

def mark_submission(student):
    '''
    Given a student directory, run all the test cases defined in the config
    and build the report. The current working directory should be `assgn_dir`.

    Returns: Array of marks for each of the test cases.
    '''
    testing_dir = f'candidates/{student}/{cfg["testing_dir"]}'
    marks = []

    # Go into the testing directory
    with pushd(testing_dir):
        # Open the report file
        with open(cfg['report'], 'w') as report_file:

            # Add the report header if needed
            if cfg['report_header'] is not None:
                report_file.write(cfg['report_header'] + '\n')

            # -----------------------------------------------------------------

            # Add the compile log if needed
            if cfg['include_compile_log']:
                report_file.write('- Compiling code ...\n\n')
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
                    marks.append(run_test(test_case, report_file))
                # Otherwise just give 0 marks for each test
                else:
                    marks.append(0)

            # -----------------------------------------------------------------

            # Output the total mark to the report for completeness
            total_out_of = sum(test['mark'] for test in cfg['tests'])
            total_mark = sum(marks)

            report_file.write("-"*79 + '\n\n')
            report_file.write(f" TOTAL MARKS: {total_mark} / {total_out_of}\n")

    return marks

# -----------------------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                    help="Location of marking directory (Default: current)")
parser.add_argument("--config", default=None, help="Location of "
                    "configuration file, if not config.yml in assgn_dir")
args = parser.parse_args()

if args.config is None:
    args.config = f'{args.assgn_dir}/config.yml'

# -----------------------------------------------------------------------------

cfg = config.load(args.config)

# -----------------------------------------------------------------------------


# Enter assignment directory
with pushd(args.assgn_dir):

    # Create a new marksheet, we will initialize it below
    marksheet = Marksheet()
    marksheet_path = cfg['marksheet']

    # -------------------------------------------------------------------------

    # If the marksheet doesn't exist
    if not os.path.exists(marksheet_path):
        # Prompt the user to create
        create = input(f"{marksheet_path} does not exist. Create? [Y]/n: ")
        # Add all the students in the `candidates` directory to marksheet
        if "n" not in create:
            marksheet.add_students(sorted(os.listdir('candidates')))
            print(f"- Created blank marksheet.")
            marksheet.save(marksheet_path)
        else:
            raise Exception("Marksheet not found or created")
    
    # Marksheet exists! Just load it in
    else:
        marksheet.load(marksheet_path)
    
    # -------------------------------------------------------------------------

    def marker_handler(student):
        marks_list = mark_submission(student)
        marksheet.update(student, marks_list)
    
        total = sum(marks_list)
        print(f"- Marking {student} ... {total} marks.", flush=True)

    # -------------------------------------------------------------------------

    executor = concurrent.futures.ProcessPoolExecutor(20)
    fs = [executor.submit(marker_handler, st) for st in marksheet.unmarked()]
    concurrent.futures.wait(fs)

    # -------------------------------------------------------------------------

    marksheet.save(marksheet_path)

# -----------------------------------------------------------------------------

print("Done.")