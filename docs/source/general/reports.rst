Report File
===========

The reports generated from the individual results using `Jinja <https://jinja.palletsprojects.com/en/3.0.x/templates/>`_ . This makes it very easy
to customize the report file you have to make it look however you want. Below on this page
the default template and a sample report output is shown.

Heirarchy
---------

As with the configuration file, if the default report template doesn't work for you, you
can place a template in ``~/.config/marker/template.txt`` and it will be used by default.
Additionally, you can set the ``report_template`` option in the configuration file with
a path to the report file relative to the ``src_dir`` directory, and it will be used for
that particular assignment. The templates are read in the following order:

* Template listed below (*lowest priority*)
* ``~/.config/marker/template.txt``
* ``<src_dir>/<report_template>`` (*highest priority*)

Template Parameters
-------------------

The template receives 2 parameters to work with:

#. ``result``: A dictionary with the individual student results as described :ref:`here<Results format>`
#. ``report_header``: Text defined in the config file (Ideally to be put at the top of the file)

Default Template
----------------

The following is what the default template looks like, if none is specified:

.. code:: 

    ********************************************************************************
    {{ report_header | center(80) }}
    ********************************************************************************
    - Compiling code ...

    {{ result.compile_log | wordwrap(75) }}
    {% if not result.compiled %}
    --------------------------------------------------------------------------------

    There were errors in compiling your submission and no executable could be 
    produced. No points will be assigned to you. If you think this is a mistake, 
    please contact us.

    {% else -%}
    {% for test in result.tests -%} 
    --------------------------------------------------------------------------------
    Running Test: {{ test.description }}
    --------------------------------------------------------------------------------
    {{ test.output }}
    {% if test.passed %}- Passed test. {{ test.mark }} / {{ test.out_of }} marks.
    {% elif test.timed_out %}- Timed out. 0 / {{ test.out_of }} marks
    {% else %}- Failed test. 0 / {{ test.out_of }} marks
    {% endif %}
    {% endfor -%}
    {% endif -%}
    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------

    Total: {{ result.total }} / {{ result.out_of }} marks

An example report generated from this template is below:

.. code:: 

    ********************************************************************************
                                Automarker Report                                
    ********************************************************************************
    - Compiling code ...

    --------------------------------------------------------------------------------
    Running Test: test description 1
    --------------------------------------------------------------------------------

    - Passed test. 1 / 1 marks.

    --------------------------------------------------------------------------------
    Running Test: test description 2
    --------------------------------------------------------------------------------
    Segmentation Fault (core dumped)

    - Failed test. 0 / 1 marks.

    --------------------------------------------------------------------------------
    --------------------------------------------------------------------------------

    Total: 1 / 2 marks