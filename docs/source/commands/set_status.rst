Set Status
==========

.. admonition:: Note

    This is for MarkUs only.

.. code-block:: bash

    $ set_status [-h] <status> [student]

Arguments:

- ``-h, --help``: Show help message
- ``status``: The status to set, ``complete`` or ``incomplete``. (Required)
- ``student``: Student ID (all students if not specified)

.. admonition:: Note

    This is also aliased to ``set-status``, if you prefer dashes.

------------

Sets the marking status of all the students in the marksheet to the given value. 
This is necessary in order to release marks on MarkUs, or to be able to re-upload
any changes once they have already been marked as completed.

Unfortunately, MarkUs doesn't provide an API endpoint to also release the marks,
so this needs to be done manually on the assignment webpage.


Configuration Options
---------------------

- The expected report file name defined by:

.. code-block:: yaml

    report: <filename>