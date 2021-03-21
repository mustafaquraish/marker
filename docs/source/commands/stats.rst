Statistics
=============

.. code-block:: bash

    $ stats [-h] [-m] [student]

Arguments:

- ``-h, --help``: Show help message
- ``-m, --minimal``: Only display mean / median
- ``student``: Student ID (all students if not specified)

------------

A convenient command to show you some quick aggregate statistics including 
the mean and median for (i) all students and (ii) only students whose solution
compiled (if you've set ``compile_check`` in the configuration)

It also shows a histogram of marks, but currently the bins are of size 1 so 
if the mark range in your case is very high this may be annoying to use. This
needs to be improved in the future.