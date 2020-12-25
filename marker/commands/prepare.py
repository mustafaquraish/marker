#! /usr/bin/env python3

import os
import sys
from tqdm import tqdm

from ..utils import pushd
from ..utils import run_command
from ..utils.marksheet import Marksheet

# -----------------------------------------------------------------------------

def prepare_handler(cfg, student):

    students = sorted(os.listdir(f'{cfg["assgn_dir"]}/candidates'))
    if student is not None:
        if student not in students:
            print(student, "submission directory doesn't exist. Stopping.")
            return
        students = [ student ]

    # Copy over all the files into each student's directory.
    progress = tqdm(students)
    for student in progress:
        student_path = f'{cfg["assgn_dir"]}/candidates/{student}/'
        if os.path.exists(student_path):
            progress.set_description(f"Copying files for {student}")
            for item in cfg['imports']:
                item_path = f'{cfg["src_dir"]}/{item}'
                run_command(f'cp -rf {item_path} {student_path}')

    # No compilation command set, leave
    if cfg['compile'] is None:
        print("Done.")
        return

    # Compile each of the student's files if needed.
    progress = tqdm(students, leave=False)
    for student in progress:
        progress.set_description(f"Preparing {student}")

        # If compilation command set, go into testing directory, and run it. 
        # Output the logs to the given file.
        testing_path = f'{cfg["assgn_dir"]}/candidates/{student}/{cfg["testing_dir"]}'
        with pushd(testing_path):
            print(f"- Compiling {student} ...", flush=True)
            with open(cfg['compile_log'], 'w') as log:
                run_command(cfg['compile'], output=log)

        # Create a blank marksheet.
        marksheet = Marksheet()
        marksheet.add_students(students)
        marksheet.save(cfg['marksheet'])

    print("Done.")

