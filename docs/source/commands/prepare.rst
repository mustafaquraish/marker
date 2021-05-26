Preparing Submissions
=====================

.. code-block:: bash

    $ prepare [-h] [student]

Arguments:

- ``-h, --help``: Show help message
- ``student``: Student ID (all students if not specified)

------------

The specified files / folders are imported over from ``src_dir`` into the 
student directories in ``candidates/``. The default behaviour is to copy 
(recursively) all files and folders listed. To change this, look at the 
configuration options below.

All the code in the student directories is then compiled if needed.


Configuration Options
---------------------


- The following specifies which files/directories to import from ``src_dir`` into student directories:

.. code-block:: yaml

    imports:
        - <file 1>
        - <file 2>
        - <directory 1>

- The following command specifies how to import the files from ``src_dir``. By default, this has the value of ``cp -rf``, but other options this can be changed to are ``ln -s`` (to soft-link), ``ln`` (to hard link), etc.

.. code-block:: yaml

    import_command: <command with flags>


.. admonition:: Note

    This command is run once for each file/folder listed in the ``imports`` fields. For instance, with:

    .. code-block:: yaml

        import_command: ln -s
        imports:
            - file0
            - folder1
    
    the marker will run the following for each student:
    
    .. code-block:: bash
        
        ln -s src_dir/file0 assgn_dir/candidates/student/
        ln -s src_dir/folder1 assgn_dir/candidates/student/


- The following define the command for compilation, and the file to store the command output in. If the compile command is explicitly set to ``null``, there are no compile logs are created.

.. code-block:: yaml

    compile: <command>
    compile_log: <filename>
