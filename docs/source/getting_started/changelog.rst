Changelog
---------

Version 2.1
===========

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