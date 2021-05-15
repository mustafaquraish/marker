.. _Results format:

Results
=======

This page is just a reference of how the results of the automarker for are stored, in
case it is being using without LMS integration and you wish to parse the output yourself
programmatically.

Marksheet
---------

The marksheet is a ``YAML`` file, by default stored in ``assgn_dir/marksheet.yml``. Each 
row (line) of the marksheet file contains the information for exactly one student.
There are 3 possible cases, as shown below:

.. code:: yaml

    # Case 1, student is unmarked, nothing stored. (Read as `None` in Python)
    student1: 

    # Case 2: student failed the `compile_check` command. No tests were run.
    student2: []

    # Case 3: tests were run, array of marks for each test
    student3: [1, 2, 0, 1, 0, 2]

Individual Results
------------------

The individual results are stored in ``JSON`` format, by default as ``results.json``
inside each student's marking directory. Below is an annotated example of such a 
results file:

.. code:: yaml

    {
        "tests": [                      # Array of results for each test
            {  
                "description": "XXX",   # Test case description (from config)
                "output": "",           # Output from the test command
                "exit_code": 0,         # Exit code of the test case
                "passed": true,         # Passed the test case?
                "timed_out": false,     # Test case timed out?
                "mark": 1,              # Mark scored for test case
                "out_of": 1             # Mark the test case is out of
            },
            ...
        ],
        "marks": [1, 1, 0, 1, 0, 1],    # Array of marks for each test case
        "out_of": 6,                    # How much all tests are out of
        "total": 6,                     # Total score, same as sum(marks)
        "compile_log": "",              # Output generated during compilation
        "compiled": true                # Compiled successfully?
    }

