#! /usr/bin/env python3

import os
import sys

from ..utils import pushd
from ..utils import run_command
from ..utils.marksheet import Marksheet
from ..utils.console import console

# -----------------------------------------------------------------------------

def prepare_handler(cfg, student):

    if not os.path.isdir(f'{cfg["assgn_dir"]}/candidates'):
        console.error("Candidates directory does exist. Quitting.")
        return

    students = sorted(os.listdir(f'{cfg["assgn_dir"]}/candidates'))
    if student is not None:
        if student not in students:
            console.error(student, "submission directory doesn't exist. Stopping.")
            return
        students = [ student ]

    # Copy over all the files into each student's directory.
    for student in console.track(students, "Copying files"):
        student_path = f'{cfg["assgn_dir"]}/candidates/{student}/'
        if os.path.exists(student_path):
            for item in cfg['imports']:
                item_path = f'{cfg["src_dir"]}/{item}'
                run_command(f'cp -rf {item_path} {student_path}')

    # No compilation command set, leave
    if cfg['compile'] is None:
        return

    # Compile each of the student's files if needed.
    for student in console.track(students, "Compiling code"):
        # If compilation command set, go into testing directory, and run it. 
        # Output the logs to the given file.
        testing_path = f'{cfg["assgn_dir"]}/candidates/{student}'
        with pushd(testing_path):
            with open(cfg['compile_log'], 'w') as log:
                run_command(cfg['compile'], output=log)

