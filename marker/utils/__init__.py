'''
Just contains some general utilities needed for all the scripts.
'''

import os, signal
import subprocess
from contextlib import contextmanager


@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)

def run_command(cmd, timeout=None, output=subprocess.DEVNULL):
    '''
    Run the command `cmd` in the current working directory, and return the 
    status.The command is run for a maximum of `timeout` seconds, and the 
    stdout/stderr are redirected to `output`.

    Returns: Either
        ('exit', exit_status)
            OR
        ('timeout', None)
    '''
    if timeout is not None:
        cmd = f"timeout {timeout} bash -c '{cmd}'"

    exit_status = subprocess.call(
        cmd,
        stdout=output,
        stderr=output,
        shell=True
    )

    # The exit code from `timeout` is 124 if process times out
    if exit_status == 124:
        return ('timeout', None)
    else:
        return ('exit', exit_status)