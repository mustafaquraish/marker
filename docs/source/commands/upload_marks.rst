Upload Marks
============

.. code-block:: bash

    $ upload_marks [-h] [-l] [student]

Arguments:

- ``-h, --help``: Show help message
- ``student``: Student ID (all students if not specified)

.. admonition:: Note

    This is also aliased to ``upload-marks``, if you prefer dashes.

------------

For each student in the LMS, checks the marksheet for their mark and uploads it.
If the student is not in the marksheet, or if their submission is unmarked /
uncompiled, they are given a mark of 0.

- *MarkUs:* The per-test marks list is loaded from the marksheet, and the configuration is used to accumulate them into per-criteria marks, which are then uploaded.

- *Canvas:* Mark breakdowns are not supported in the Canvas gradesheet. The list of marks for each submission is summed for a total mark which is then uploaded. The report files will contain the breakdown.

-------------

.. admonition:: Note

    This command will overwrite the marks of all students in the course if it is 
    run without without a specific ``student`` argument, regardless of whether they 
    are in the marksheet. 

    If for some reason you are only want to upload the marks for a certain group of 
    students, you can write a little bash script to repeatedly call this command with 
    each of those students.

    This may be improved in the future, though I have personally never needed to do 
    this. A usual workflow involves me having an up-to-date marksheet on my machine
    at all times, since ideally I would re-run the marker for all students if I've
    made some changes to the test cases, or I can manually edit the marksheet if 
    needed.


Configuration Options
---------------------

- The expected report file name defined by:

.. code-block:: yaml

    report: <filename>