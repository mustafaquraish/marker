#! /usr/local/bin/python3

import os
import config
import argparse
import subprocess
import concurrent.futures

from lms import LMS_Factory

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("config", help="Path to the marker conig file")
parser.add_argument("assgn_dir", nargs='?', default=os.getcwd(), 
                    help="Location to create directories (Default: current)")
args = parser.parse_args()

# -----------------------------------------------------------------------------

# Load the configuration and get an instance of the LMS class
cfg = config.load(args.config)
lms = LMS_Factory(cfg)

# -----------------------------------------------------------------------------

print("Making directory structure...")
os.makedirs(args.assgn_dir, exist_ok=True)
os.makedirs(f'{args.assgn_dir}/extra-files', exist_ok=True)
os.makedirs(f'{args.assgn_dir}/candidates', exist_ok=True)
candidates_dir = f'{args.assgn_dir}/candidates'

# -----------------------------------------------------------------------------

# Handler to download submission for each thread
def download_handler(student):
    '''
    Given a student's identifier, make their directory and download file(s).
    '''
    print(f"- Getting {student} ...", flush=True)
    os.makedirs(f'{candidates_dir}/{student}', exist_ok=True)
    lms.download_submission(student, f'{candidates_dir}/{student}')

# -----------------------------------------------------------------------------

executor = concurrent.futures.ProcessPoolExecutor(20)
fs = [executor.submit(download_handler, st) for st in lms.students()]
concurrent.futures.wait(fs)