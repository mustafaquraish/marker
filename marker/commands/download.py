import os

import aiohttp
import asyncio

from ..utils import pushd, listdir
from ..utils.marksheet import Marksheet


# Handler to download submission for each process
async def download_dispatch(lms, students):
    '''
    Given a student's identifier, make their directory and download file(s).
    '''
    if students == []:
        students = lms.students
    
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session: 
        tasks = [lms.download_submission(session, student) for student in students]
        await lms.console.track_async(tasks, "Downloading submissions")

# -----------------------------------------------------------------------------

def download(self, students, allow_late=False):
    self.console.log("Making directory structure")
    candidates_dir = os.path.join(self.cfg["assgn_dir"], "candidates")
    os.makedirs(candidates_dir, exist_ok=True)

    self.lms.cfg["allow_late"] = allow_late

    with pushd(candidates_dir):
        asyncio.run(download_dispatch(self.lms, students))

    # Populate missing students into the marksheet...

    # Load in an existing marksheet...
    students = listdir(candidates_dir)
    marksheet_path = os.path.join(self.cfg["assgn_dir"], self.cfg["marksheet"])
    marksheet = Marksheet()
    if os.path.isfile(marksheet_path):
        marksheet.load(marksheet_path)
    # Add all students (in case new ones were downloaded...)
    marksheet.add_students(students)
    marksheet.save(marksheet_path)
