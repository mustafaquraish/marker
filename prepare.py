import argparse
import config
import os
import subprocess
import sys
from utils import pushd

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("config", help="Marker configuration file")
parser.add_argument(dest="assgn_dir", help="Location of the marking directory")
parser.add_argument("--src", dest="src_dir", default=None,
                    help="Source directory (Default: config directory)")
args = parser.parse_args()

if args.src_dir is None:
    args.src_dir = os.path.dirname(os.path.abspath(args.config))


# Load the configuration and get an instance of the LMS class
cfg = config.load(args.config)

# Import files from source dir
for item in cfg['imports']:
    item_path = f'{args.src_dir}/{item}'
    subprocess.call(
        f'cp -rf {item_path} {args.assgn_dir}/extra-files/', 
        shell=True
    )

subprocess.call(f'cp {args.config} {args.assgn_dir}/config.yaml', shell=True)

with pushd(args.assgn_dir):
    marksheet = open(cfg['marksheet'], 'w')
    for st_dir in sorted(os.listdir('candidates')):
        st_path = f'candidates/{st_dir}' 
        if not os.path.isdir(st_path):
            continue

        # Copy over the extra testing files into the student directory
        subprocess.call(f"cp -rf extra-files/* {st_path}/", shell=True)
        
        # Go into testing directory, run the compile command and output the
        # logs to the file decribed in cthe configiguration
        testing_path = f'{st_path}/{cfg["testing_dir"]}'
        with pushd(testing_path):
            print(f"- Compiling {st_dir} ...")
            cmd = cfg['compile']
            with open(cfg['compile_log'], 'w') as log:
                subprocess.call(cmd, stdout=log, stderr=log, shell=True)

        # Add student row to marksheet
        marksheet.write(f'{st_dir},\n')
    marksheet.close()


