from .canvas import Canvas
from .markus import Markus

def LMS_Factory(config):
    if config['lms'].lower() == 'canvas':
        return Canvas(config)
    elif config['lms'].lower() == 'markus':
        return Markus(config)