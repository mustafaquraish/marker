Changelog
---------

Version 2.1.3 (Minor update)
============================

* New ``clean`` command added to REPL which removes all marking information (``candidates/`` and ``marksheet.yml``)
* Fix off-by-one error in progress tracker
* Change default shell for running commands to ``/bin/bash``

Version 2.1.2
=============

* Ignore hidden files when performing ``os.listdir()``
* Add running time per test to results
* Can now set ``submission_comment`` in configuration (for Canvas) to add some text comments along with the posted report.
* Can change the ``import_command`` used to import files in ``prepare`` to soft/hard link them instead of copying, etc.
* Can now use ``marker.getLMSSubmissionURL()`` to get (for Canvas) the URL to open the submission directly.

Version 2.1.1
=============

* Can now download all files in Canvas submission by omitting ``file_name`` in configuration.

Version 2.1.0
=============

* API largely the same, but internals restructured to make it very simple to write wrappers over it (such as a web-server).
* Use of Abstract Base Classes for ``Console`` and ``LMS`` objects, to make extended implementations have necessary methods.
* Test results are now stored in a parseable JSON format instead of directly being dumped to report
* Report generation now uses Jinja based on the results, much easier to customize.
* Tokens, CLI history, default templates / configurations now all stored in ``~/.config/marker/``

Version 2.0
===========

* Redesigned internals, can now import an instance of the ``Marker`` class in your Python code and script testing / handling of marks, etc. (Documentation for this is not available yet, but you can look in ``src/repl.py`` for code examples)
* Now uses Python's async abilities instead of multithreading to speed up API requests
* Interactive CLI now available, with autocompletion of commands / student IDs.
* Ability to run each command for individual students through the CLI directly
* Can see some basic statistics from the marksheet in the CLI directly