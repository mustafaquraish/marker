'''
Utilities related to interfacing with MarkUs

(C) Mustafa Quraish, 2020
'''
import requests
import os
import aiofiles

from functools import cached_property
from .base import LMS
from ..utils.token import get_or_prompt_token

class Markus(LMS):

    def __init__(self, config):
        self.base_url = config['base_url']
        self.assignment = config['assignment']
        self.cfg = config
        super().__init__("markus", self.base_url)

    # -------------------------------------------------------------------------
    #       Internal utils
    # -------------------------------------------------------------------------
    
    @cached_property 
    def header(self):
        return {"Authorization": "MarkUsAuth " + self.token}

    # -------------------------------------------------------------------------

    # MarkUs API Provides no nice way to get the actual `result_id` that we
    # Need to get the URL of the results page.
    def submissionURL(self, student):
        return None

    # -------------------------------------------------------------------------

    @cached_property
    def mapping(self):
        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups.json'
        response = requests.get(url, headers=self.header)
        if response.status_code >= 400:
            raise Exception("Error fetching students")
        res = response.json()
        mapping = {}
        for group in res:
            mapping[group['group_name']] = group['id']
        return mapping

    # -------------------------------------------------------------------------

    @cached_property
    def assgn_id(self):
        '''
        Fetch the assignment id given the short identifier
        '''
        url = f'{self.base_url}/api/assignments.json'
        response = requests.get(url, headers=self.header)
        if response.status_code >= 400:
            raise Exception("Error fetching assignment id")
        res = response.json()

        match = filter(lambda a: a['short_identifier'] == self.assignment, res)
        match = list(match)

        if len(match) != 1:
            raise ValueError("Invalid course short identifier.")
        
        return match[0]['id']

   # -------------------------------------------------------------------------

    async def _get_ffs(self, session, group_id):
        '''
        Gets and returns the feedback files for a group. Return value is of 
        the form:
                         { filename : file_id }
        '''
        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/feedback_files.json'
        async with session.get(url, headers=self.header) as resp:
            res = await resp.json()
        try:
            ret = {ff['filename']: ff['id'] for ff in res} 
        except Exception as e:
            return None
        return ret
    
    # -------------------------------------------------------------------------
    
    def _accumulate_marks(self, mark_list):
        '''
        Given a list of marks for the test cases, accumulate them into a 
        dictionary of:
                        { criteria : mark }
        using the configuration file saved internally
        '''
        from collections import defaultdict
        breakdown = defaultdict(int)
        if mark_list == []:
            mark_list = [0 for _ in self.cfg['tests']]
        for mark, test_case in zip(mark_list, self.cfg['tests']):
            breakdown[test_case['criteria']] += mark
        return breakdown

    # -------------------------------------------------------------------------
    #       Functions meant to be exposed
    # -------------------------------------------------------------------------
    
    @cached_property
    def students(self):
        return self.mapping.keys()

    # -------------------------------------------------------------------------
    
    async def delete_report(self, session, student):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False

        group_id = self.mapping[student]
        feedback_files = await self._get_ffs(session, group_id)
        if feedback_files is None:
            self.console.error(student, "error getting feedback files.")
            return False

        for _, rid in feedback_files.items():
            url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/feedback_files/{rid}.json'
            async with session.delete(url, headers=self.header) as resp:
                res = await resp.json()
            
            if int(res['code']) != 200:
                self.console.error(student, "error:", res['description'])
                return False

    # -------------------------------------------------------------------------

    async def upload_report(self, session, student):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False

        group_id = self.mapping[student]
        
        fname = self.cfg["report"]
        report_path = os.path.join(student, fname)

        if not os.path.isfile(report_path):
            self.console.error(report_path, "doesn't exist.")
            return False

        existing_ffs = await self._get_ffs(session, group_id)

        if existing_ffs is None:
            self.console.error(student, "error getting feedback files.")
            return False
        
        # Report already exists, use PUT to replace
        if fname in existing_ffs:
            url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/feedback_files/{existing_ffs[fname]}.json'
            data = { 'file_content': open(report_path, 'rb').read() }
            async with session.put(url, data=data, headers=self.header) as resp:
                res = await resp.json()
        
        # Report doesn't exist, use POST to create new file
        else:
            import mimetypes
            url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/feedback_files.json'
            data = {
                'filename': fname,
                'file_content': open(report_path, 'rb').read(),
                'mime_type': mimetypes.guess_type(report_path)[0]
            }
            async with session.post(url, data=data, headers=self.header) as resp:
                res = await resp.json()
        
        if 'status' in res and res['status'] == 500:
            self.console.error(student, "error uploading report:", res['error'])
            return False

        if 200 <= int(res['code']) <= 201:
            return True
        else:
            self.console.error(student, "error uploading report:", res['description'])
            return False
        
    # -------------------------------------------------------------------------

    async def download_submission(self, session, student):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False
        group_id = self.mapping[student]

        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/submission_files.json'
        
        collected = True
        if self.cfg["allow_late"]:
            collected = False

        if 'file_names' in self.cfg:
            for fname in self.cfg['file_names']:
                data = { 'filename': fname, 'collected': collected}
                async with session.get(url, data=data, headers=self.header) as resp:
                    content = await resp.content.read()
                    file_path = os.path.join(student, fname)
                    os.makedirs(student, exist_ok=True)
                    f = await aiofiles.open(file_path, mode='wb')
                    await f.write(content)
                    await f.close()
        else:
            data = {'collected': collected}
            async with session.get(url, data=data, headers=self.header) as resp:
                content = await resp.content.read()
                file_path = os.path.join(student, student + ".zip")
                os.makedirs(student, exist_ok=True)
                f = await aiofiles.open(file_path, mode='wb')
                await f.write(content)
                await f.close()

    # -------------------------------------------------------------------------
    
    async def upload_mark(self, session, student, mark_list):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False

        group_id = self.mapping[student]
        breakdown = self._accumulate_marks(mark_list)
        
        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/update_marks.json'
        async with session.put(url, data=breakdown, headers=self.header) as resp:
            res = await resp.json()

        if int(res['code']) != 200:
            self.console.error(student, "error uploading mark:", res['description'])
            return False

        return True
    
    # -------------------------------------------------------------------------
    
    async def set_status(self, session, student, status):
        if student not in self.mapping:
            self.console.error(student, "not found in course list")
            return False
        group_id = self.mapping[student]

        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/update_marking_state.json'
        
        data = { 'marking_state': status }
        async with session.put(url, data=data, headers=self.header) as resp:
            res = await resp.json()

        if int(res['code']) != 200:
            self.console.error(student, "error setting status:", res['description'])
            return False

        return True

