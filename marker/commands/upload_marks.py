#! /usr/bin/env python3

import os
import concurrent.futures

from ..utils import config
from ..lms import LMS_Factory
from ..utils.marksheet import Marksheet


def upload_handler(student, marks_list, lms):
    '''
    Given a student's identifier, and mark, upload to LMS.
    '''
    done = lms.upload_mark(student, marks_list)
    base = f"- Uploading {student} mark ... "
    print(base + ("Done." if done else "[ERROR] Failed."), flush=True)


def main(args):

    # Load the configuration and get an instance of the LMS class
    cfg = config.load(args.config)
    lms = LMS_Factory(cfg)

    # Load Marksheet
    marksheet = Marksheet()
    marksheet.load(f'{args.assgn_dir}/{cfg["marksheet"]}')

    # The following will trigger fetching the students before we multithread
    _ = lms.students()

    # Upload the marks submissions in parallel
    with concurrent.futures.ProcessPoolExecutor(20) as executor:
        for student, mark_list in marksheet.marked_items():
            executor.submit(upload_handler, student, mark_list, lms)
    
    print("Done.")