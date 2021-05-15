Running Tests
=============

.. code-block:: bash

    $ run [-h] [-r] [-a] [-q] [student]

Arguments:

- ``-h, --help``: Show help message
- ``-r, --recompile``: Recompile submissions before running
- ``-a, --all``: Run for all students, even if already marked
- ``-q, --quiet``: Don't show the marks for each student as tests finish
- ``student``: Student ID (all students if not specified)

------------

Runs all the specified test cases for the submissions, generates the report files 
and outputs the list of marks (per test) for each submission into the marksheet. 
The report files are stored inside the testing directory provided.

The marksheet is a yaml file containing an array of marks for each student, with 
each array element corresponding to the test cases in the order defined in the
configuration file. If compilation fails, then an empty array is stored. This
is for your convenience to filter out any students who didn't compile.

.. admonition:: Note
    
    By default, the marker only runs on the unmarked submissions in the 
    marksheet. This is convenient to be able to remark a student/group (and *only* them) 
    by just manually clearing their mark. This can be overridden with ``--all``.


Configuration Options
---------------------

General
+++++++

- If the `--recompile` flag is used, the following defines the command for compilation, and the file to store the compilation logs in. If the compile command is `null`, nothing is run and no logs are made.
    
.. code-block:: yaml

    compile: <command>
    compile_log: <filename>
    

- The following defines a command that can be used to check for succesful compilation (ideally checking to see if the executable was formed). If provided, failing this check will not run the tests. The command should exit with a non-zero status if compilation failed. Typically, this is just something like ``ls ./executable``.
    
.. code-block:: yaml

    compile_check: <command>
    

- The following specifies the name of the marksheet to be used:
    
.. code-block:: yaml

    marksheet: <filename>
    

- The following specifies the name of the report file to be made:
    
.. code-block:: yaml

    report: <filename>

- The following specifies the name of the template to use to generate the report (relative to ``src_dir``):
    
.. code-block:: yaml

    report_template: <filename>

- The following specifies the name of the results JSON file to be made:
    
.. code-block:: yaml

    results: <filename>    

- The following specifies some text to be put at the top of report file to provide some information:
    
.. code-block:: yaml

    report_header: <text>
    

Test specifications
+++++++++++++++++++

In the configuration file, there should be a field called `tests` containing an array of the required test cases. It would look something like:


.. code-block:: yaml

    tests:
        - test 1 field 1        ‾|
          test 1 field 2         |  Test 1 config
          test 1 field 3        _|

        - test 2 field 1        ‾|
          test 2 field 2         |  Test 2 config
          test 2 field 3        _|
        
        -     ...  



For each test case, the following fields are available for configuration:


- Brief description of the test to add to the report:
    
.. code-block:: yaml

    description: <text>
    

- The amount of marks allocated to the test case:
    
.. code-block:: yaml

    mark: <number>
    

- Command to run some setup before the test case:
    
.. code-block:: yaml

    before: <command>
    

- Command to run the actual test case:
    
.. code-block:: yaml

    command: <command>
    

- Command to run some cleanup after the test case is done:
    
.. code-block:: yaml

    after: <command>
    

- Time (in seconds) allotted to all three commands above before timing out:
    
.. code-block:: yaml

    timeout: <number>
    

- Expected exit code of the test command on success (used to check if the test passed):
    
.. code-block:: yaml

    exit_code: <int>
        
- Criteria to count the test marks for. For more information, look at :ref:`markus-specific-config`
    
.. code-block:: yaml

    criteria: <criteria>
    
