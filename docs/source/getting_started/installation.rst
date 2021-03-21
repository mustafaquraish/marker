Installation
------------

Marker requires Python 3.8 or newer. It is recommended to install the `latest
stable Python release <https://www.python.org/downloads/>`_ .

From package manager
====================

The recommended way to install *marker* is through pip:

.. code-block:: bash

   pip install marker

This installs the command line utility directly. You can check it if is 
installed correctly by running 

.. code-block:: bash

   $ marker -h
   usage: marker [-h] [-d ASSGN_DIR] [-c CONFIG] [-s SRC_DIR]
        ...

Manual installation from source
===============================

If you want to develop, you can use the included Makefile to compile:

.. code-block:: bash

   $ make install

Or do-it-yourself using `setuputils` and `pip` (if your executables are named
differently than in the Makefile)

.. code-block:: bash

   $ python -m setup.py bdist_wheel
   $ pip install dist/*