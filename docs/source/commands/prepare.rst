Preparing Submissions
=====================

.. code-block:: bash

    $ prepare [-h] [student]

Arguments:

- ``-h, --help``: Show help message
- ``student``: Student ID (all students if not specified)

------------

The specified files / folders are copied over from ``src_dir`` into the 
student directories in ``candidates/``

All the code in the student directories is then compiled if needed.


Configuration Options
---------------------


- The following specifies which files/directories to import from ``src_dir`` into student directories:

.. code-block:: yaml

    imports:
        - <file 1>
        - <file 2>
        - <directory 1>


- The following define the command for compilation, and the file to store the command output in. If the compile command is explicitly set to ``null``, there are no compile logs are created.

.. code-block:: yaml

    compile: <command>
    compile_log: <filename>
