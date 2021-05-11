from .utils import config
from .utils.marksheet import Marksheet
from .utils import pushd
import os
import sys
from sys import exit
from .lms import LMS_Factory

from functools import cached_property

import asyncio

from .repl.console import REPLConsole

class Marker():
    def __init__(self, args, console=REPLConsole()):
        config_path = args["config"]
        try:
            self.cfg = config.load(config_path)
        except FileNotFoundError:
            print("CWD:", os.getcwd(),file=sys.stderr)
            print("ABS", os.path.abspath(args["config"]))
            print("exist?:", os.path.exists( os.path.abspath(args["config"])),file=sys.stderr)
            console.error(f"Could not find {config_path}. Exiting.")
            exit(1)
        self.cfg.update(args)
        self.console = console
        console.log("Config loaded")
    
    @cached_property
    def lms(self):
        lms_instance = LMS_Factory(self.cfg)
        lms_instance.console = self.console
        return lms_instance    

    def getMarksheet(self):
        marksheet_path = f'{self.cfg["assgn_dir"]}/{self.cfg["marksheet"]}'
        if not os.path.exists(marksheet_path):
            self.console.error(marksheet_path, "file not found.")
            return Marksheet()
        return Marksheet(marksheet_path)
    
    def getStudentDir(self, student):
        student_dir = f'{self.cfg["assgn_dir"]}/candidates/{student}'
        if not os.path.exists(student_dir):
            self.console.error(student_dir, "dir not found. Stopping.")
            return None
        return student_dir


    # Import in the specific command handlers...

    from .commands.prepare import prepare
    from .commands.stats import stats
    from .commands.run import run

    from .commands.delete_reports import delete_reports
    from .commands.upload_reports import upload_reports
    from .commands.upload_marks import upload_marks
    from .commands.set_status import set_status
    from .commands.download import download