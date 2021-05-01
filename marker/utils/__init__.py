'''
Just contains some general utilities needed for all the scripts.
'''

import os
from contextlib import contextmanager
from .marksheet import Marksheet

@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)

import subprocess as subproc
import signal, shlex
import time

def run_command(cmd, timeout=None, output=True, limit=-1):
    '''
    Run the command `cmd` in the current working directory, and return a
    tuple of:
                    (return_code, output)

    If `timeout` is specified, the process is killed after the given time,
    and in this case the `return_code` is None.

    By default both output is collected and returned, but this can be
    disabled with `output=False`. If so, an empty string is returned.
    '''
    command = shlex.split(cmd)

    stdout_fd = subproc.PIPE if output else subproc.DEVNULL

    try:
        proc = subproc.Popen(command, 
                             text=True,
                             preexec_fn=os.setsid,
                             stdout=stdout_fd,
                             stderr=subproc.STDOUT
                             )
    except Exception as e:
        # We have an unknown error here, possibly that the executable 
        # file does not exist. Return -1 with the error message in stderr
        return (-1, str(e))

    try:
        proc.wait(timeout=timeout)
    except subproc.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    return (proc.returncode, proc.stdout.read(limit) if output else "")