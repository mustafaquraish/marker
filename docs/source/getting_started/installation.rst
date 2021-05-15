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

If you want to install from source, you can clone the repo and install using:

.. code-block:: bash

   $ git clone https://github.com/mustafaquraish/marker
   $ cd marker
   $ python setup.py install

If you wish to develop, you might want to install in editable mode so that Any
changes made to the code are immediately reflected in the ``marker`` command-line
utility without having to reinstall.

.. code-block:: bash

   $ cd marker
   $ pip install -e .