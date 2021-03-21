Upload Reports
==============

.. code-block:: bash

    $ upload_reports [-h] [-l] [student]

Arguments:

- ``-h, --help``: Show help message
- ``student``: Student ID (all students if not specified)

.. admonition:: Note

    This is also aliased to ``upload-reports``, if you prefer dashes.

------------

Uploads the report file to the submission platform for the students to view. 
If you did not generate the reports externally, please make sure they are placed 
in the following paths to make sure they're found by the marker, and also set 
the ``report`` field in the configuration appropriately:

.. code-block::

    <assgn_dir>/candidates/<student_id>/<report>

The information from the configuration file is used to download the student 
submissions from the specified platform.

- *Canvas*: the file is uploaded as a submission comment (visible through SpeedGrader).

- *MarkUs*: the file is uploaded to the feedback files section.


Configuration Options
---------------------

- The expected report file name defined by:

.. code-block:: yaml

    report: <filename>