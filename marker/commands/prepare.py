#! /usr/bin/env python3

import os
import sys
import concurrent.futures

from ..utils import config
from ..utils import pushd
from ..utils import run_command
from ..utils.marksheet import Marksheet

def prepare_handler(student, cfg):
    '''
    Given a student's identifier, Copies over all the files to their directory
    and compiles them. Assumes that the working directory is the root of the 
    assignment directory.
    '''
    st_path = f'candidates/{student}' 
    if not os.path.isdir(st_path):
        return

    # Copy over the extra testing files into the student directory
    run_command(f"cp -rf extra-files/* {st_path}/")
    
    # If a compilation command is set, go into testing directory, and run it. 
    # Output the logs to the given file.
    if cfg['compile'] is not None:
        testing_path = f'{st_path}/{cfg["testing_dir"]}'
        with pushd(testing_path):
            print(f"- Compiling {student} ...", flush=True)
            with open(cfg['compile_log'], 'w') as log:
                run_command(cfg['compile'], output=log)

# -----------------------------------------------------------------------------

def main(args):

    cfg = config.load(args.config)

    # Import files from source dir
    run_command(f'ln -f {args.config} {args.assgn_dir}/config.yml')
    for item in cfg['imports']:
        item_path = f'{args.src_dir}/{item}'
        run_command(f'cp -rf {item_path} {args.assgn_dir}/extra-files/')

    with pushd(args.assgn_dir):

        # Prepare the submissions in parallel
        with concurrent.futures.ProcessPoolExecutor(20) as executor:
            for student in sorted(os.listdir('candidates')):
                executor.submit(prepare_handler, student, cfg)

        # Create a blank marksheet.
        marksheet = Marksheet()
        marksheet.add_students(sorted(os.listdir('candidates')))
        marksheet.save(cfg['marksheet'])

    print("Done.")

