'''
Just contains some general utilities needed for all the scripts.
'''
import os
from contextlib import contextmanager

from .marksheet import Marksheet
from .tests import run_command, run_test

from pathlib import Path

HOMEDIR = os.path.abspath(Path.home())
CONFIG_DIR = os.path.join(HOMEDIR, ".config", "marker")

@contextmanager
def pushd(new_dir):
    previous_dir = os.getcwd()
    os.chdir(new_dir)
    try:
        yield
    finally:
        os.chdir(previous_dir)

def ensure_config_dir():
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR, exist_ok=True)

def listdir(path, hidden=False):
    for x in os.listdir(path):
        if hidden or not x.startswith("."):
            yield x