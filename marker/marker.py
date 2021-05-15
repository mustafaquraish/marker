import asyncio
import os
import sys
from functools import cached_property
from sys import exit

from .lms import LMSFactory
from .repl.console import REPLConsole
from .utils.config import load_config
from .utils.marksheet import Marksheet


class Marker():
    def __init__(self, args, console=REPLConsole()):
        """
        Initializing the marker requires passing in a dictionary with the 
        following fields:

        ```
        args = {
            'assgn_dir': '...',
               'config': '...',
              'src_dir': '...'
        }
        ```
        Optionally, also pass in a `Console` object to handle errors/progress.
        """
        config_path = args["config"]
        try:
            self.cfg = load_config(config_path)
            console.log(f"Config Loaded")
        except FileNotFoundError:
            console.error(f"Could not find {config_path}. Exiting.")
            exit(1)
        self.cfg.update(args)
        self.console = console
    
    @cached_property
    def lms(self):
        lms_instance = LMSFactory.create(self.cfg)
        lms_instance.console = self.console
        return lms_instance    

    def getMarksheet(self):
        marksheet_path = os.path.join(self.cfg["assgn_dir"], self.cfg["marksheet"])
        if not os.path.exists(marksheet_path):
            self.console.error(marksheet_path, "file not found.")
            return Marksheet()
        return Marksheet(marksheet_path)
    
    def getStudentDir(self, student):
        student_dir = os.path.join(self.cfg["assgn_dir"], "candidates", student)
        if not os.path.exists(student_dir):
            self.console.error(student_dir, "dir not found. Stopping.")
            return None
        return student_dir


    # Import in the specific command handlers...

    from .commands.delete_reports import delete_reports
    from .commands.download import download
    from .commands.prepare import prepare
    from .commands.run import run
    from .commands.set_status import set_status
    from .commands.stats import stats
    from .commands.upload_marks import upload_marks
    from .commands.upload_reports import upload_reports
