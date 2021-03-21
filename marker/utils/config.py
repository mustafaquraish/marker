import yaml
import os
import sys 
from .console import console

def set_if_not(config, field, default):
    if field not in config or config[field] is None:
        config[field] = default


def set_default_values(config):
    set_if_not(config, 'default_criteria', 'tests')    # For Markus
    
    set_if_not(config, 'imports', [])
    
    set_if_not(config, 'marksheet', 'marksheet.yml')
    set_if_not(config, 'report', 'report.txt')
    set_if_not(config, 'report_header', None)

    set_if_not(config, 'compile', None)
    set_if_not(config, 'compile_log', 'compile.log')
    set_if_not(config, 'compile_check', None)
    set_if_not(config, 'include_compile_log', True)
    
    set_if_not(config, 'tests', [])

    for test in config['tests']:
        set_if_not(test, 'description', '')
        set_if_not(test, 'mark', 1)
        set_if_not(test, 'before', None)
        set_if_not(test, 'after', None)
        set_if_not(test, 'timeout', 1)
        set_if_not(test, 'output', True)
        set_if_not(test, 'exit_code', 0)    

        # For Markus
        set_if_not(test, 'criteria', config['default_criteria'])

def load(cfg_path):
    if not os.path.exists(cfg_path):
        console.error(f"Error: {cfg_path} does not exist.")
        return prompt_use_empty_config()
        
    with open(cfg_path) as cfg_file:
        try:
            config = yaml.safe_load(cfg_file)
            if config is None:
                config = {}
        except Exception as e:
            console.error(f"Error: {cfg_path} is not a valid config file.")
            return prompt_use_empty_config()

    set_default_values(config)    
    return config

def prompt_use_empty_config():
    if console.ask("Use default (empty) config?", default=True):
        config = {}
        set_default_values(config)    
        return config
    else:
        console.error("Exiting.")
        sys.exit(1)