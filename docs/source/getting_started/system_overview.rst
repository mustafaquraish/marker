System Overview
===============

Directory structure
-------------------

All the utilities use (and assume) the following directory structure:

.. code-block:: text

   assgn_dir/
   ├── config.yml
   ├── candidates/
   │   ├── student_1_id/
   │   │   └── <student files>
   │   ├── student_2_id/
   │   │   └── <student files>
   │   └── ...
   ├── marksheet.yml 
   └── <other files / starter code>

Here's what each of the notable things here are:

- ``assgn_dir``: Top level directory containing everything.
- ``config.yml``: Marker configuration file. Discussed in `Configuration`.
- ``candidates``: The directory containing subdirectories with code for each student / group
- ``marksheet.yml``: A list of marks for each student for the test cases.

.. admonition:: Note

   If you are using the *marker* utility to download the submissions from the
   platform, the directory structure will be created automatically. Otherwise,
   please set up the ``candidates`` directory yourself.

Using the CLI
-------------

The utility can be used as a regular CLI or in interactive mode. For the most
part, all the functionality is the same, but the interactive environment allows
you to use the autocompletion features.

When running the marker utility, there are 3 command line arguments you can set 
if you don't want to use the corresponding defaults (though it is recommended 
you do):

- ``-d <assgn_dir>``: assignment directory as described above. (Default: ``.``)
- ``-c <config>``: the configuration file. (Default: ``<assgn_dir>/config.yml``)
- ``-s <src_dir>``: source directory from where any files specified in the configuration file are copied over to the student directories (Default: directory containing ``config``)


To run a command in the regular mode, you can simply run:

.. code-block:: bash

   $ marker [[command]] 

Or you can start up the interactive environment:

.. code-block:: bash

   $ marker
   [+] Config loaded
   marker > [[command]]

By default any commands that are not recognized by the interactive REPL are 
passed to your shell, so you can still run ``cat`` or ``ls``, or even
mix-and-match by piping the results of some of the commands to another script
or redirecting to a file. You can also use the TAB key to autocomplete 
command names and student IDs (but only after you've run ``download``).
