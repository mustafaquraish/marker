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


-----

For installation and usage, please look at `Getting Started`.


.. toctree::
   :maxdepth: 1
   :caption: Getting Started:

   getting_started/installation
   getting_started/access_tokens
   getting_started/system_overview
   getting_started/examples
   getting_started/changelog

.. toctree::
   :maxdepth: 1
   :caption: General:

   general/configuration
   general/results
   general/reports


.. toctree::
   :maxdepth: 1
   :caption: Commands:

   commands/download.rst
   commands/prepare.rst
   commands/run.rst
   commands/upload_marks.rst
   commands/upload_reports.rst
   commands/delete_reports.rst
   commands/set_status.rst
   commands/stats.rst
