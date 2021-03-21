#! /usr/bin/env python3

import os
import aiohttp
import asyncio

from ..utils.marksheet import Marksheet
from ..utils import config
from ..lms import LMS_Factory
from ..utils.console import console


async def set_status_dispatch(lms, status, student=None):
    '''
    Given a student's identifier, set their MarkUs submission status to
    complete / incomplete
    '''
    students = lms.students if student is None else [ student ]
    connector = aiohttp.TCPConnector(limit=10)
    async with aiohttp.ClientSession(connector=connector) as session:  
        tasks = [lms.set_status(session, student, status) for student in students]
        await console.track_async(tasks, "Setting status")


def set_status_handler(lms, status, student):    
    asyncio.run(set_status_dispatch(lms, status, student))