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
            if cfg['force_recompile'] and (cfg['compile'] is not None) :
                with open(cfg['compile_log'], 'w') as log:
                    run_command(cfg['compile'], timeout=10, output=log)

            # -----------------------------------------------------------------

            # If the compile log exists, include it in the report based on the
            # provided option in the config file.
            if cfg['include_compile_log']:
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

def main(args):

    cfg = config.load(args.config)
    cfg['force_recompile'] = args.recompile


    # Enter assignment directory
    with pushd(args.assgn_dir):

        # Create a new marksheet, we will initialize it below
        marksheet = Marksheet()
        marksheet_path = cfg['marksheet']

        # If we want to force-remark all submissions, don't load the marksheet
        # but just create a new one
        if args.all:
            marksheet.add_students(sorted(os.listdir('candidates')))

        # Or if the marksheet doesn't exist, ask the user if they want to make 
        # a new one for all of the submissions
        elif not os.path.exists(marksheet_path):
            # Prompt the user to create
            create = input(f"{marksheet_path} does not exist. Create? [Y]/n: ")
            # Add all the students in the `candidates` directory to marksheet
            if "n" not in create:
                marksheet.add_students(sorted(os.listdir('candidates')))
            else:
                raise Exception("Marksheet not found or created")
        
        # Marksheet exists! Just load it in
        else:
            marksheet.load(marksheet_path)
    

        # If the no_parallels option is set, mark the submissions in serial
        if (args.no_parallel):
            for student in marksheet.unmarked():
                marks_list = mark_submission(student, cfg)
                marksheet.update(student, marks_list)

        # Otherwise, mark them all in parallel.
        else:
            import concurrent.futures
            with concurrent.futures.ProcessPoolExecutor(20) as executor:
                futures_dict = {}
                for student in marksheet.unmarked():
                    future = executor.submit(mark_submission, student, cfg)
                    futures_dict[future] = student 

                # As the marks come in, get them and update to marksheet
                for future in concurrent.futures.as_completed(futures_dict):
                    student = futures_dict[future]
                    try:
                        marks_list = future.result()
                        marksheet.update(student, marks_list)
                    except Exception as exc:
                        print(f'Error when marking {student}: {exc}')

        # Finally, save (and overwrite) the marksheet
        marksheet.save(marksheet_path)

    print("Done.")