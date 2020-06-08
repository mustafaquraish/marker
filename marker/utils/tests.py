from . import run_command

def run_test(test, report_file):
    '''
    Given the test object from the configuration file, run the test case. The 
    current working directory must be the testing directory of the student 
    being marked.

    Return: The mark to be assigned for the test case
    '''
    
    # Write test header to the report
    report_file.write("-"*79 + '\n')
    report_file.write(f"  Running Test: {test['description']}\n")
    report_file.write("-"*79 + '\n\n')
    report_file.flush()

    timeout = test['timeout']

    # -------------------------------------------------------------------------

    # Run the setup, main, and cleaup commands for the test case if needed
    if test['before'] is not None:
        run_command(test['before'], timeout)
    
    status, code = run_command(test['command'], timeout, report_file)

    if test['after'] is not None:
        run_command(test['after'], timeout)
    
    report_file.write("\n")

    # -------------------------------------------------------------------------

    mark = 0
    out_of = test['mark']

    if status == 'exit':
        if code == test['exit_code']:
            # Only assign the mark if the test exit with the expected code
            mark = out_of       
            report_file.write(f"- Passed test.  {mark} / {out_of} marks")
        else:
            report_file.write(f"- Failed test.  {0} / {out_of} marks")

    elif status == 'timeout':
        report_file.write(f"- Timed out ({timeout}s).  {0} / {out_of} marks")

    # -------------------------------------------------------------------------
    
    report_file.write("\n\n")
    report_file.flush()
    return mark

