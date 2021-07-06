import os
import subprocess as subproc
import signal
import time

def run_test(test):
    '''
    Given the test object from the configuration file, run the test case. The 
    current working directory must be the testing directory of the student 
    being marked.

    Return: The mark to be assigned for the test case
    '''

    timeout = test['timeout']

    # Run the setup, main, and cleaup commands for the test case if needed
    if test['before'] is not None:
        run_command(test['before'], timeout)
    
    start_time = time.time()
    exit_code, output = run_command(test['command'], timeout=timeout)
    end_time = time.time()

    if test['after'] is not None:
        run_command(test['after'], timeout)

    result = {} 
    result["description"] = test['description']
    result["output"] = output
    result["exit_code"] = exit_code
    result["time"] = end_time - start_time
    result["passed"] = (exit_code == test['exit_code'])
    result["timed_out"] = (exit_code is None)
    result["mark"] = test["mark"] if result["passed"] else 0
    result["out_of"] = test["mark"]

    return result

def run_command(cmd, timeout=None, output=True, limit=1000):
    '''
    Run the command `cmd` in the current working directory, and return a
    tuple of:
                    (return_code, output)

    If `timeout` is specified, the process is killed after the given time,
    and in this case the `return_code` is None.

    By default both output is collected and returned, but this can be
    disabled with `output=False`. If so, an empty string is returned.
    '''
    stdout_fd = subproc.PIPE if output else subproc.DEVNULL
    if limit is None:
        limit = -1

    try:
        proc = subproc.Popen(cmd, 
                             shell=True,
                             preexec_fn=os.setsid,
                             stdout=stdout_fd,
                             stderr=subproc.STDOUT,
                             executable="/bin/bash"
                             )
    except Exception as e:
        # We have an unknown error here, possibly that the executable 
        # file does not exist. Return -1 with the error message in stderr
        return (-1, str(e))

    try:
        proc.wait(timeout=timeout)
    except subproc.TimeoutExpired:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)

    text = ""
    if output:
        text = proc.stdout.read(limit)
        text = text.decode('utf-8', errors='replace')

    return (proc.returncode, text)