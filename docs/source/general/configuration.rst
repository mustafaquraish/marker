.. _markus-specific-config:

Configuration File
==================

This page just serves to show a complete configuration file with all the default 
options filled in, including information for all the submission platforms. The 
pages for each of the specific commands describe in detail which options are 
used for what purposes.

Any option that has a default value does not need to be explicitly specified.

Heirarchy
---------

If the defaults below don't fit your needs, and you would like to more sane
defaults, you can put them in ``~/.config/marker/config.yml``. When the marker
is instantiated, options are loaded in to following order:

* Options listed on this page (*lowest priority*)
* ``~/.config/marker/config.yml``
* Configuration file specified in CLI (*highest priority*)

Platform Specific Options
-------------------------

Canvas
++++++

.. code:: yaml

   lms: canvas                         # Platform name
   base_url: {no default}              # Base URL of Canvas instance
   course: {no default}                # Course ID from Canvas
   assignment: {no default}            # Assignment ID from Canvas

   allow_late: false                   # Download late submissions
   file_name: {no default}             # Name for the downloaded submission
   submission_comment: {no default}    # Text to add to comment with report


MarkUs
++++++

.. code:: yaml

   lms: markus                         # Platform name
   base_url: {no default}              # Base URL of MarkUs instance
   assignment: {no default}            # Assignment short identifier

   allow_late: false                   # Download late submissions
   file_names: null                    # Files to get; If null, get all in zip

   default_criteria: tests             # Default criteria for test cases

General Options
---------------

.. code:: yaml
   
   results: results.json               # Testing results for each student
   
   report: report.txt                  # Report file to be generated
   report_header: "Automarker Report"  # Header text for report                 
   report_template: null               # (Jinja) template to generate report

   marksheet: marksheet.yml            # Marksheet to be used

   imports: []                         # List of files/dirs to be imported.

   compile: null                       # Command to compile the code
   compile_log: compile.log            # File to output compilation logs
   compile_check: null                 # Command to check successful compile

   tests:
      - description: ""               # Description for test
        mark: 1                       # Marks for test case
        before: null                  # Setup command before test
        command: {no default}         # Command to run test case
        after: null                   # Cleanup command after test
        exit_code: 0                  # Expected exit code for success
        timeout: 1                    # Max. seconds to run test case
        criteria: *default_criteria   # (MarkUs only) Test criteria