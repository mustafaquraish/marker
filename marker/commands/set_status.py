#! /usr/bin/env python3

import os
import sys
import concurrent.futures

from ..utils import config
from ..utils import pushd
from ..utils import run_command
from ..utils.marksheet import Marksheet

from ..lms import Markus

# Handler to upload mark for each thread
def status_handler(student, status, lms):
    '''
    Given a student's identifier, and mark, upload to LMS.
    '''
    done = lms.set_status(student, status)
    base = f"- Setting {student} to {status} ... "
    print(base + ("Done." if done else "[ERROR] Failed."), flush=True)

# -----------------------------------------------------------------------------

def main(args):

    if args.config is None:
        args.config = f'{args.assgn_dir}/config.yml'

    # -------------------------------------------------------------------------

    # Load the configuration and get an instance of the LMS class
    cfg = config.load(args.config)

    # Load LMS
    if cfg['lms'].lower() != "markus":
        print(f"- Nothing to do on {cfg['lms']}; this is only for MarkUs.")
        sys.exit(0)
    lms = Markus(cfg)

    # Load marksheet
    marksheet = Marksheet()
    marksheet.load(f'{args.assgn_dir}/{cfg["marksheet"]}')

    # -------------------------------------------------------------------------
    
    # The following will trigger fetching the students before we multithread
    _ = lms.students()

    executor = concurrent.futures.ProcessPoolExecutor(20)
    fs = [executor.submit(status_handler, student, args.status, lms) 
          for student, _ in marksheet.items()]
    concurrent.futures.wait(fs)
