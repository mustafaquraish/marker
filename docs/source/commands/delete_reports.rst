Delete Reports
==============

.. code-block:: bash

    $ delete_reports [-h] [-l] [student]

Arguments:

- ``-h, --help``: Show help message
- ``student``: Student ID (all students if not specified)

.. admonition:: Note
    
    This is also aliased to ``delete-reports``, if you prefer dashes.

------------

Delete any report files uploaded. This command works for both MarkUs and Canvas,
however it is only really useful if you are using Canvas, since it will not
overwrite the previous report when you upload a modified one, and will instead
make a new one.

MarkUs on the other hand will just replace a report if you upload it again 
without changing the name.


Configuration Options
---------------------

- The expected report file name defined by:

.. code-block:: yaml

    report: <filename>