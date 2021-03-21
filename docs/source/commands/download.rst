Download Submissions
====================

.. code-block:: bash

    $ download [-h] [-l] [student]

Arguments:

- ``-h, --help``: Show help message
- ``-l, --allow_late``: Allow submissions after the deadline (Canvas)
- ``student``: Student ID (all students if not specified)

------------


The information from the configuration file is used to download the student 
submissions from the specified platform.

The following directory structure will be created after the command finishes:

.. code-block::

    assgn_dir/
    └── candidates/
        ├── student_1_id/
        │   └── <submitted code files>
        ├── student_2_id/
        │   └── <submitted code files>
        └── ...


Platform specific configurations
--------------------------------

Canvas
++++++

- Since Canvas does not give you a way to restrict the file names of the submissions, it is recommended to only get the students to submit one file per Canvas assignment. The following line in the configuration controls what the file should be renamed to:

.. code-block:: yaml

    file_name: <filename>


- The following line enables / disables downloading of late submissions:

.. code-block:: yaml

    allow_late: <true/false>

MarkUs
++++++

- You can only download collected submissions. By default, all the submitted files will be downloaded in a zip file. If you want to download them individually (unarchived), specify each of the wanted files as follows:

.. code-block:: yaml

    file_names:
        - <file 1>
        - <file 2>
        -   ...