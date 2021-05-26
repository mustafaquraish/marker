import os
import aiohttp
import asyncio

from ..utils import pushd, listdir

async def upload_report_dispatch(lms, students):
    '''
    Given a student's identifier, upload their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    if students == []:
        students = sorted(listdir("."))
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [lms.upload_report(session, student) for student in students]
        await lms.console.track_async(tasks, "Uploading reports")


def upload_reports(self, students):
    # Force an error if token is missing...
    _ = self.lms.token

    candidates_dir = os.path.join(self.cfg["assgn_dir"], "candidates")
    with pushd(candidates_dir):
        asyncio.run(upload_report_dispatch(self.lms, students))