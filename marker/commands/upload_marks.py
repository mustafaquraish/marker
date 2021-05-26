import os
import aiohttp
import asyncio

from ..utils.marksheet import Marksheet
from ..utils import config


async def upload_mark_dispatch(lms, marksheet, students):
    '''
    Given a student's identifier, upload their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    if students == []:
        students = lms.students
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:  
        tasks = [lms.upload_mark(session, student, marksheet[student]) for student in students]
        await lms.console.track_async(tasks, "Uploading marks")


def upload_marks(self, students):
    # Force an error if token is missing...
    _ = self.lms.token
    
    marksheet_path = os.path.join(self.cfg["assgn_dir"], self.cfg["marksheet"])    
    if not os.path.exists(marksheet_path):
        self.console.error(marksheet_path, "file not found. Stopping.")
        return
    
    marksheet = Marksheet(marksheet_path)

    self.console.log("Loading marksheet")
    asyncio.run(upload_mark_dispatch(self.lms, marksheet, students))