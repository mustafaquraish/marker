#! /usr/bin/env python3

import os
import concurrent.futures

from ..utils import pushd
from ..utils import config
from ..lms import LMS_Factory

def upload_handler(student, lms, cfg):
    '''
    Given a student's identifier, upload their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    report_path = f"candidates/{student}/{cfg['testing_dir']}/{cfg['report']}"

    if not lms.student_exists(student):
        print(f" *** Error: `{student}` not recognized on LMS", flush=True)
    elif not os.path.exists(report_path):
        print(f" *** Error: `{report_path}` does not exist", flush=True)
    else:
        done = lms.upload_report(student, report_path)
        base = f"- Uploading {student} report ... "
        print(base + ("Done." if done else "[ERROR] Failed."), flush=True)


def main(args):

    # Load the configuration and get an instance of the LMS class
    cfg = config.load(args.config)
    lms = LMS_Factory(cfg)

    with pushd(args.assgn_dir):
        
        # The following will trigger fetching the students
        _ = lms.students()

        # Prepare the submissions in parallel
        with concurrent.futures.ProcessPoolExecutor(20) as executor:
            for student in sorted(os.listdir('candidates')):
                executor.submit(upload_handler, student, lms, cfg)

    print("Done.")