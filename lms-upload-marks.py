#! /usr/local/bin/python3 import os

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
def upload_handler(student, marks_list):
    '''
    Given a student's identifier, and mark, upload to LMS.
    '''
    print(f"- Uploading {student} mark ...", flush=True)
    done = lms.upload_mark(student, marks_list)
    base = f"- Uploading {student} mark ... "
    print(base + ("Done." if done else "[ERROR] Failed."), flush=True)

# -----------------------------------------------------------------------------

# The following will trigger fetching the students before we multithread
_ = lms.students()

executor = concurrent.futures.ProcessPoolExecutor(20)
fs = [executor.submit(upload_handler, st, ml) for st, ml in marksheet.items()]
concurrent.futures.wait(fs)
