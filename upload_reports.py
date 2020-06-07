#! /usr/bin/env python3

import os
import config
import argparse
import concurrent.futures

from utils import pushd
from lms import LMS_Factory
from marksheet import Marksheet

def main(args):

    if args.config is None:
        args.config = f'{args.assgn_dir}/config.yml'

    # -------------------------------------------------------------------------

    # Load the configuration and get an instance of the LMS class
    cfg = config.load(args.config)
    lms = LMS_Factory(cfg)

    # -------------------------------------------------------------------------

    marksheet = Marksheet()
    marksheet.load(f'{args.assgn_dir}/{cfg["marksheet"]}')

    # -------------------------------------------------------------------------
    candidates_dir = f"{args.assgn_dir}/candidates"
    
    # Handler to upload mark for each thread
    def upload_handler(student):
        '''
        Given a student's identifier, upload their report file to LMS.
        '''
        testing_dir = f"{candidates_dir}/{student}/{cfg['testing_dir']}"
        report_path = f"{testing_dir}/{cfg['report']}"

        if not lms.student_exists(student):
            print(f" *** Error: `{student}` not recognized on LMS", flush=True)
        elif not os.path.exists(report_path):
            print(f" *** Error: `{report_path}` does not exist", flush=True)
        else:
            done = lms.upload_report(student, report_path)
            base = f"- Uploading {student} report ... "
            print(base + ("Done." if done else "[ERROR] Failed."), flush=True)
    

    # -------------------------------------------------------------------------

    student_dir_list = sorted(os.listdir(f'{args.assgn_dir}/candidates'))

    # The following will trigger fetching the students before we multithread
    _ = lms.students()

    executor = concurrent.futures.ProcessPoolExecutor(20)
    fs = [executor.submit(upload_handler, st) for st in student_dir_list]
    concurrent.futures.wait(fs)
