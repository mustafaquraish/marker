import os
import aiohttp
import asyncio

from ..utils.marksheet import Marksheet
from ..utils import config


async def set_status_dispatch(lms, status, students):
    '''
    Given a student's identifier, set their MarkUs submission status to
    complete / incomplete
    '''
    if students == []:
        students = lms.students
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:  
        tasks = [lms.set_status(session, student, status) for student in students]
        await lms.console.track_async(tasks, "Setting status")


def set_status(self, status, students):    
    asyncio.run(set_status_dispatch(self.lms, status, students))