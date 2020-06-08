from .canvas import Canvas
from .markus import Markus


def LMS_Factory(config):
    if config['lms'].lower() == 'canvas':
        assert('course' in config), "Must have course ID in Config for Canvas"
        assert('file_name' in config), "Must have name for downloaded file"
        return Canvas(config)
    elif config['lms'].lower() == 'markus':
        return Markus(config)
