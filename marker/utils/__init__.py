'''
Just contains some general utilities needed for all the scripts.
'''

import os
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
    try:
        exit_status = subprocess.call(
            cmd,
            stdout=output,
            stderr=output,
            timeout=timeout,
            shell=True
        )
        return ('exit', exit_status)

    except subprocess.TimeoutExpired:
        return ('timeout', None)
