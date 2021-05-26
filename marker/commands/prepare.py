import os
import sys

from ..utils import pushd, listdir
from ..utils import run_command
from ..utils.marksheet import Marksheet

# -----------------------------------------------------------------------------

def prepare(self, students):

    candidates_dir = os.path.join(self.cfg["assgn_dir"], "candidates")
    if not os.path.isdir(candidates_dir):
        self.console.error("Candidates directory does exist. Quitting.")
        return

    all_students = sorted(listdir(candidates_dir))
    if students == []:
        students = all_students

    no_compile = self.cfg['compile'] is None

    # Copy over all the files into each student's directory.
    for student in self.console.track(students, "Preparing Submissions"):
        student_path = os.path.join(candidates_dir, student)
        if os.path.exists(student_path):
            for item in self.cfg['imports']:
                item_path = os.path.join(self.cfg["src_dir"], item)
                
                cmdprefix = self.cfg["import_command"]
                cmd = f'{cmdprefix} {item_path} {student_path}'
                run_command(cmd)
        else:
            self.console.error(student_path, "does not exist.")
            continue

        # No compilation command set, ignore
        if no_compile:
            continue

        # If compilation command set, go into testing directory, and run it. 
        # Output the logs to the given file.
        student_path = os.path.join(candidates_dir, student)
        with pushd(student_path):
            _, clog = run_command(self.cfg['compile'], timeout=10, limit=None)
            with open(self.cfg['compile_log'], 'w') as log:
                log.write(clog)

