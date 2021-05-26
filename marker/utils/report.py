from jinja2 import Template
from . import CONFIG_DIR
import os

CUSTOM_DEFAULT_TEMPLATE = os.path.join(CONFIG_DIR, "template.txt")


def generate_report(result, config):
    template_text = base_template
    if config["report_template"] is not None:
        template_path = os.path.join(config["src_dir"],
                                     config["report_template"])
        with open(template_path) as file:
            template_text = file.read()
    elif os.path.isfile(CUSTOM_DEFAULT_TEMPLATE):
        with open(CUSTOM_DEFAULT_TEMPLATE) as file:
            template_text = file.read()

    return Template(template_text).render(
        result=result, report_header=config["report_header"])


###############################################################################

base_template = """\
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
"""