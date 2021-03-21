from .utils import config
from .utils.marksheet import Marksheet
from .utils import pushd
from .utils.console import console

from .lms import LMS_Factory

from .commands.download import download_handler
from .commands.prepare import prepare_handler
from .commands.run import run_handler
from .commands.upload_marks import upload_mark_handler
from .commands.upload_reports import upload_report_handler
from .commands.delete_reports import delete_report_handler
from .commands.set_status import set_status_handler
from .commands.stats import stats_handler

from functools import cached_property

import asyncio

class Marker():
    def __init__(self, args):
        config_path = args["config"]
        self.cfg = config.load(config_path)
        self.cfg.update(args)
        console.log("Config loaded")
    
    @cached_property
    def lms(self):
        return LMS_Factory(self.cfg)

    def download_submissions(self, student=None, late=False):
        return download_handler(self.cfg, self.lms, student, late)

    def prepare(self, student=None):
        return prepare_handler(self.cfg, student)

    def run(self, student=None, recompile=False, all=False, quiet=False):
        """
        Run takes in some additional arguments to augment behaviour such as
        forcing recompilation and running for all students.
        """
        new_cfg = self.cfg.copy()
        new_cfg['all'] = all
        new_cfg['recompile'] = recompile
        new_cfg['show_marks'] = (not quiet)
        return run_handler(new_cfg, student)
    
    def upload_reports(self, student=None):
        return upload_report_handler(self.cfg, self.lms, student)

    def upload_marks(self, student=None):
        return upload_mark_handler(self.cfg, self.lms, student)

    def delete_reports(self, student=None):
        return delete_report_handler(self.cfg, self.lms, student)

    def set_status(self, status, student=None):
        return set_status_handler(self.lms, status, student)

    def stats(self, student=None, minimal=False):
        return stats_handler(self.cfg, student, minimal)
