#! /usr/bin/env python3

import os
import concurrent.futures

from ..utils import config
from ..utils import pushd
from ..lms import LMS_Factory


# Handler to download submission for each process
def download_handler(student, lms):
    '''
    Given a student's identifier, make their directory and download file(s).
    '''
    print(f"- Getting {student} ...", flush=True)
    os.makedirs(student, exist_ok=True)
    lms.download_submission(student, student)

# -----------------------------------------------------------------------------

def main(args):

    # Load the configuration and get an instance of the LMS class
    cfg = config.load(args.config)
    lms = LMS_Factory(cfg)

    print("Making directory structure...")
    os.makedirs(args.assgn_dir, exist_ok=True)
    os.makedirs(f'{args.assgn_dir}/extra-files', exist_ok=True)
    os.makedirs(f'{args.assgn_dir}/candidates', exist_ok=True)
    candidates_dir = f'{args.assgn_dir}/candidates'

    with pushd(candidates_dir):
        futures = []
        with concurrent.futures.ProcessPoolExecutor(20) as executor:
            for student in lms.students():
                futures.append(executor.submit(download_handler, student, lms))
        concurrent.futures.wait(futures)
