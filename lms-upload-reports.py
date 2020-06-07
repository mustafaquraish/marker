#! /usr/local/bin/python3

import os
import config
import argparse
import concurrent.futures

from utils import pushd
from lms import LMS_Factory
from marksheet import Marksheet

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                    help="Location of assignment dir (Default: current)")
parser.add_argument("--config", default=None, help="Location of "
                    "configuration file, if not config.yml in assgn_dir")
args = parser.parse_args()

if args.config is None:
    args.config = f'{args.assgn_dir}/config.yml'

# -----------------------------------------------------------------------------

# Load the configuration and get an instance of the LMS class
cfg = config.load(args.config)
lms = LMS_Factory(cfg)

# -----------------------------------------------------------------------------

marksheet = Marksheet()
marksheet.load(f'{args.assgn_dir}/{cfg["marksheet"]}')

# -----------------------------------------------------------------------------

# Handler to upload mark for each thread
def upload_handler(student):
    '''
    Given a student's identifier, upload their report file to LMS.
    '''
    testing_dir = f"{args.assgn_dir}/candidates/{student}/{cfg['testing_dir']}"
    report_path = f"{testing_dir}/{cfg['report']}"

    if not lms.student_exists(student):
        print(f" *** Error: `{student}` not recognized on LMS", flush=True)
    elif not os.path.exists(report_path):
        print(f" *** Error: `{report_path}` does not exist", flush=True)
    else:
        done = lms.upload_report(student, report_path)
        base = f"- Uploading {student} report ... "
        print(base + ("Done." if done else "[ERROR] Failed."), flush=True)
 

# -----------------------------------------------------------------------------

student_dir_list = sorted(os.listdir(f'{args.assgn_dir}/candidates'))

# The following will trigger fetching the students before we multithread
_ = lms.students()

executor = concurrent.futures.ProcessPoolExecutor(20)
fs = [executor.submit(upload_handler, st) for st in student_dir_list]
concurrent.futures.wait(fs)
