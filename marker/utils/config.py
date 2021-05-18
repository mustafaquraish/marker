import yaml
import os

from . import CONFIG_DIR

CUSTOM_DEFAULT_CONFIG = os.path.join(CONFIG_DIR, "config.yml")

def open_config_file(cfg_path):
    with open(cfg_path) as cfg_file:
        config = yaml.safe_load(cfg_file)
    if config is None:
        config = {}
    return config

def load_config(cfg_path):
    config = yaml.safe_load(yaml.dump(base_marker_config))
    if os.path.isfile(CUSTOM_DEFAULT_CONFIG):
        update_config(config, open_config_file(CUSTOM_DEFAULT_CONFIG))
    update_config(config, open_config_file(cfg_path))
    return config


def update_config(config, updated):
    for key, value in updated.items():
        config[key] = value
    
    for test in config["tests"]:
        for key, value in base_test_config.items():
            if key not in test:
                test[key] = value
        if "criteria" not in test:
            test["criteria"] = config["default_criteria"]
    
###############################################################################

base_marker_config = {
    "default_criteria": "tests",

    "imports": [],
    
    "marksheet": "marksheet.yml",
    "results": "results.json",
    "report": "report.txt",
    "report_header": "Automarker Report",
    
    "compile": None,
    "compile_check": None,
    "compile_log": "compile.log",

    "tests": [],
}

base_test_config = {
    "description": "",
    "mark": 1,
    "before": None,
    "command": "",
    "after": None,
    "timeout": 1,
    "exit_code": 0,
}