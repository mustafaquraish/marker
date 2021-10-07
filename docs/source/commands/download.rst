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

- The following option can be specified to choose the specific field that is used to identify the submissions. The default value is ``None``, which tries to use one of the following (in order): ``email``, ``login_id``, ``sis_user_id``.
  Note that for courses on canvas that are old, some of these fields get removed from the API responses, so in those cases the selected identifier may not be found.

.. code-block:: yaml

    # Must be one of "email", "login_id", "sis_user_id" or null
    canvas_identifier: email


.. admonition:: Note

    If the argument below is not specified, the marker will download all the files submitted by the student in the newest submission before the deadline (unless the ``-l`` option is specified), and retain the names from the submission. 
    
    If you need more than one file as part of the submission, you should ask the students to double check they submit the exact name needed, or use a scriptto read the downloaded submissions and rename them.


- If the following option is specified, then the first attachment in the submission is downloaded and renamed to the specified filename. This is useful since Canvas doesn't allow you to restrict the file names of submissions.

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