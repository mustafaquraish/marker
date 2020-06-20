from .canvas import Canvas
from .markus import Markus

def LMS_Factory(config):
    assert('lms' in config), "Must have an LMS in the config"
    assert('base_url' in config), "Must have base url for LMS in config"
    assert('assignment' in config), "Must have assignment ID in config"

    # If the base_URL has a trailing '/', remove it
    if config["base_url"][-1] == "/":
        config["base_url"] = config["base_url"][:-1]

    if config['lms'].lower() == 'canvas':
        assert('course' in config), "Must have course ID in Config for Canvas"
        assert('file_name' in config), "Must have name for downloaded file"
        return Canvas(config)
    
    elif config['lms'].lower() == 'markus':
        return Markus(config)
