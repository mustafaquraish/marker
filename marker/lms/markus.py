'''
Utilities related to interfacing with MarkUs

(C) Mustafa Quraish, 2020
'''
import requests
import os
import aiofiles

from ..utils.console import console
from functools import cached_property

class Markus():

    def __init__(self, config):
        self.base_url = config['base_url']
        self.assignment = config['assignment']
        self.cfg = config
        self.header = {"Authorization": "MarkUsAuth " + self.token}

    # -------------------------------------------------------------------------
    #       Internal utils
    # -------------------------------------------------------------------------

    @cached_property
    def token(self):
        '''
        Try to load MarkUs token from file. If it doesn't exist, prompt
        the user and give them an option to save it locally.
        '''
        from pathlib import Path

        token_path = f"{Path.home()}/.markus.tokens"
        if os.path.exists(token_path):
            lst = [line.split(",") for line in open(token_path).readlines()]
            tokens_dict = { url.strip(): token.strip() for url, token in lst }
            if self.base_url in tokens_dict:
                return tokens_dict[self.base_url]

        token = console.get("Enter MarkUs Token").strip()
        save = console.ask(f"Save token in [red]{token_path}[/red]?", default=True)
        if save:
            with open(token_path, 'a') as token_file:
                token_file.write(f'{self.base_url},{token}\n')
            console.log("Access token saved")
    
        return token

    # -------------------------------------------------------------------------

    @cached_property
    def mapping(self):
        mapp = {}
        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups.json'
        res = requests.get(url, data={}, headers=self.header).json()
        for group in res:
            mapp[group['group_name']] = group['id']
        return mapp

    # -------------------------------------------------------------------------

    @cached_property
    def assgn_id(self):
        '''
        Fetch the assignment id given the short identifier
        '''
        url = f'{self.base_url}/api/assignments.json'
        res = requests.get(url, data={}, headers=self.header).json()
        
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
    
    @ cached_property
    def students(self):
        return self.mapping.keys()

    # -------------------------------------------------------------------------

    def student_exists(self, student):
        return student in self.mapping

    # -------------------------------------------------------------------------
    
    async def delete_report(self, session, student):
        if student not in self.mapping:
            console.error(student, "not found in course list")
            return False

        group_id = self.mapping[student]
        feedback_files = await self._get_ffs(session, group_id)
        if feedback_files is None:
            console.error(student, "error getting feedback files.")
            return False

        for _, rid in feedback_files.items():
            url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/feedback_files/{rid}.json'
            async with session.delete(url, headers=self.header) as resp:
                res = await resp.json()
            
            if int(res['code']) != 200:
                console.error(student, "error:", res['description'])
                return False

    # -------------------------------------------------------------------------

    async def upload_report(self, session, student):
        if student not in self.mapping:
            console.error(student, "not found in course list")
            return False

        group_id = self.mapping[student]
        
        fname = self.cfg["report"]
        report_path = f'{student}/{fname}'

        if not os.path.isfile(report_path):
            console.error(report_path, "doesn't exist.")
            return False

        existing_ffs = await self._get_ffs(session, group_id)

        if existing_ffs is None:
            console.error(student, "error getting feedback files.")
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
            console.error(student, "error uploading report:", res['error'])
            return False

        if 200 <= int(res['code']) <= 201:
            return True
        else:
            console.error(student, "error uploading report:", res['description'])
            return False
        
    # -------------------------------------------------------------------------

    async def download_submission(self, session, student):
        if student not in self.mapping:
            console.error(student, "not found in course list")
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
                    file_path = f'{student}/{fname}'
                    os.makedirs(student, exist_ok=True)
                    f = await aiofiles.open(file_path, mode='wb')
                    await f.write(content)
                    await f.close()
        else:
            data = {'collected': collected}
            async with session.get(url, data=data, headers=self.header) as resp:
                content = await resp.content.read()
                file_path = f'{student}/{student}.zip'
                os.makedirs(student, exist_ok=True)
                f = await aiofiles.open(file_path, mode='wb')
                await f.write(content)
                await f.close()

    # -------------------------------------------------------------------------
    
    async def upload_mark(self, session, student, mark_list):
        if student not in self.mapping:
            console.error(student, "not found in course list")
            return False

        group_id = self.mapping[student]
        breakdown = self._accumulate_marks(mark_list)
        
        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/update_marks.json'
        async with session.put(url, data=breakdown, headers=self.header) as resp:
            res = await resp.json()

        if int(res['code']) != 200:
            console.error(student, "error uploading mark:", res['description'])
            return False

        return True
    
    # -------------------------------------------------------------------------
    
    async def set_status(self, session, student, status):
        if student not in self.mapping:
            console.error(student, "not found in course list")
            return False
        group_id = self.mapping[student]

        url = f'{self.base_url}/api/assignments/{self.assgn_id}/groups/{group_id}/update_marking_state.json'
        
        data = { 'marking_state': status }
        async with session.put(url, data=data, headers=self.header) as resp:
            res = await resp.json()

        if int(res['code']) != 200:
            console.error(student, "error setting status:", res['description'])
            return False

        return True

