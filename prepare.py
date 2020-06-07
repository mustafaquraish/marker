#! /usr/local/bin/python3

import argparse
import config
import os
import subprocess
import sys
from utils import pushd
from marksheet import Marksheet
from testcases import run_command

# -----------------------------------------------------------------------------

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("config", help="Location of configuration file")
parser.add_argument(dest="assgn_dir", nargs='?', default=os.getcwd(), 
                    help="Location of marking directory (Default: current)")
parser.add_argument("--src", "-s", dest="src_dir", default=None,
                    help="Source directory (Default: config. directory)")
args = parser.parse_args()

if args.src_dir is None:
    args.src_dir = os.path.dirname(os.path.abspath(args.config))

# -----------------------------------------------------------------------------

cfg = config.load(args.config)

# -----------------------------------------------------------------------------

# Import files from source dir
for item in cfg['imports']:
    item_path = f'{args.src_dir}/{item}'
    subprocess.call(
        f'cp -rf {item_path} {args.assgn_dir}/extra-files/', 
        shell=True
    )

# -----------------------------------------------------------------------------

subprocess.call(f'ln -f {args.config} {args.assgn_dir}/config.yml', shell=True)

# -----------------------------------------------------------------------------

with pushd(args.assgn_dir):

    for st_dir in sorted(os.listdir('candidates')):
        st_path = f'candidates/{st_dir}' 
        if not os.path.isdir(st_path):
            continue

        # Copy over the extra testing files into the student directory
        run_command(f"cp -rf extra-files/* {st_path}/", timeout=1)
        
        # Go into testing directory, run the compile command and output the
        # logs to the file decribed in cthe configiguration
        testing_path = f'{st_path}/{cfg["testing_dir"]}'
        with pushd(testing_path):
            print(f"- Compiling {st_dir} ...")
            cmd = cfg['compile']
            with open(cfg['compile_log'], 'w') as log:
                subprocess.call(cmd, stdout=log, stderr=log, shell=True)

    # -------------------------------------------------------------------------

    # Create a blank marksheet.
    marksheet = Marksheet()
    marksheet.add_students(sorted(os.listdir('candidates')))
    marksheet.save(cfg['marksheet'])


