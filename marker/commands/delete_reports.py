import os
import aiohttp
import asyncio

from ..utils import pushd

async def delete_report_dispatch(lms, students):
    '''
    Given a student's identifier, delete their report file to LMS. Assumes
    the working directory is the root of the assignment directory
    '''
    if students == []:
        students = lms.students
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session: 
        tasks = [lms.delete_report(session, student) for student in students]
        await lms.console.track_async(tasks, "Deleting reports")


def delete_reports(self, students):
    asyncio.run(delete_report_dispatch(self.lms, students))
  