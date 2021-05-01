from . import run_command

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
    
    exit_code, output = run_command(test['command'], timeout=timeout)

    if test['after'] is not None:
        run_command(test['after'], timeout)

    result = {} 
    result["description"] = test['description']
    result["output"] = output
    result["exit_code"] = exit_code
    result["passed"] = (exit_code == test['exit_code'])
    result["timed_out"] = (exit_code is None)
    result["mark"] = test["mark"] if result["passed"] else 0

    return result