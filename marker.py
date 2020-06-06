import argparse
import config
import os
import subprocess
import sys
from utils import pushd

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("assgn_dir", help="Location of the marking directory")
parser.add_argument("--config", default=None, help="Location of configuration"
                    " file, if not config.yaml in assgn_dir")
args = parser.parse_args()

if args.config is None:
    args.config = f'{args.assgn_dir}/config.yaml'

cfg = config.load(args.config)

def run_test(test, report):
    report.write("-"*100 + '\n')
    report.write("- RUNNING TEST: " + test['description'] + '\n')
    report.write("" + '\n')
    report.flush()
    # print(test)

    if test['before'] is not None:
        try:
            subprocess.call(
                test['before'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                timeout=float(test['timeout'])
            )
        except subprocess.TimeoutExpired:
            pass
    
    mark = 0
    try:
        ret = subprocess.call(
            test['command'],
            stdout=report,
            stderr=report,
            shell=True,
            timeout=float(test['timeout'])
        )
        if ret == test['exit_code']:
            mark = test['mark']
            print(f"- PASSED.  {mark} / {test['mark']}", file=report)
        else:
            print(f"- FAILED.  0 / {test['mark']}", file=report)

    except subprocess.TimeoutExpired:
        print(f"- TIMED OUT.  0 / {test['mark']}", file=report)

    if test['after'] is not None:
        try:
            subprocess.call(
                test['after'],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=True,
                timeout=float(test['timeout'])
            )
        except subprocess.TimeoutExpired:
            pass
    
    print("", file=report)
    return mark



def marker_handler(st_dir):
    testing_path = f'candidates/{st_dir}/{cfg["testing_dir"]}'
    marks = 0
    with pushd(testing_path):
        with open(cfg['report'], 'w') as report:
            for test in cfg['tests']:
                marks += run_test(test, report)
    return marks

with pushd(args.assgn_dir):
    marksheet = cfg['marksheet']
    if not os.path.exists(marksheet):
        create = input(f"{marksheet} does not exist. Create? [Y]/n: ")
        if "n" not in create:
            lines = sorted(os.listdir('candidates'))
            with open(marksheet, 'w') as mksht:
                for st_dir in lines:
                    mksht.write(f'{st_dir},\n')
            print(f"- Created {marksheet}")
        else:
            raise Exception("Marksheet not found or created")
    
    for st_dir in sorted(os.listdir('candidates')):
        print(f"- Marking {st_dir} ...", end="")
        print(marker_handler(st_dir))
