from .canvas import Canvas
from .markus import Markus

def LMS_Factory(config):
    if 'lms' not in config:         raise ValueError("Must have an LMS in the config")
    if 'base_url' not in config:    raise ValueError("Must have base url for LMS in config")
    if 'assignment' not in config:  raise ValueError("Must have assignment ID in config")

    # If the base_URL has a trailing '/', remove it
    if config["base_url"][-1] == "/":
        config["base_url"] = config["base_url"][:-1]

    if config['lms'].lower() == 'canvas':
        if 'course' not in config:      raise ValueError("Must have course ID in Config for Canvas")    
        return Canvas(config)
    
    elif config['lms'].lower() == 'markus':
        return Markus(config)
