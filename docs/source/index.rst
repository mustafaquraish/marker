Welcome to marker's documentation!
==================================

Marker is a highly configurable code-testing utility to automate downloading and 
testing code, as well as returning detailed reports to the students. Currently it 
supports the following platforms:

- Canvas
- MarkUs

Who is this for?
----------------

This tool is aimed to primarily help instructors of university computer science
courses who want to automate code tests for classes. It can also be useful to
simply fetch student submissions from the learning platforms or to upload marks
or report files that were generated through any other means.

What's new? (v2.0)
------------------

- Redesigned internals, can now import an instance of the `Marker` class in your Python code and script testing / handling of marks, etc. (Documentation for this is not available yet, but you can look in `src/repl.py` for code examples)

- Now uses Python's async abilities instead of multithreading to speed up API requests

- Interactive CLI now available, with autocompletion of commands / student IDs.

- Ability to run each command for individual students through the CLI directly

- Can see some basic statistics from the marksheet in the CLI directly

-----

For installation and usage, please look at `Getting Started`.


.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   getting_started/installation
   getting_started/access_tokens
   getting_started/system_overview
   getting_started/configuration
   getting_started/examples


.. toctree::
   :maxdepth: 0
   :caption: Commands:

   commands/download.rst
   commands/prepare.rst
   commands/run.rst
   commands/upload_marks.rst
   commands/upload_reports.rst
   commands/delete_reports.rst
   commands/set_status.rst
   commands/stats.rst
