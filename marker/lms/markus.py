'''
Utilities related to interfacing with Canvas

(C) Mustafa Quraish, 2020
'''
import requests
import os


class Markus():

    def __init__(self, config):
        self.base_url = config['base_url']
        self.assignment = config['assignment']
        self.cfg = config
        self.assgn_id = None
        self.mapping = None
        self._get_token()
        self.header = {"Authorization": "MarkUsAuth " + self.token}

        self._get_assgn_id()

    # -------------------------------------------------------------------------
    #       Internal utils
    # -------------------------------------------------------------------------

    def _get_token(self):
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
                self.token = tokens_dict[self.base_url]
                return

        token = input("Enter Markus Token: ").strip()
        prompt = input(f"Save token in {token_path} ?: [Y]/n")
        if 'n' not in prompt.lower():
            with open(token_path, 'a') as token_file:
                token_file.write(f'{self.base_url},{token}\n')
    
        self.token = token

    # -------------------------------------------------------------------------

    def _get_assgn_id(self):
        '''
        Fetch the assignment id given the short identifier
        '''
        if self.assgn_id is not None:
            return

        url = (f'{self.base_url}/api/assignments.json')
        res = requests.get(url, data={}, headers=self.header).json()
        
        match = filter(lambda a: a['short_identifier'] == self.assignment, res)
        match = list(match)

        if len(match) != 1:
            raise ValueError("Invalid course short identifier.")
        
        self.assgn_id = match[0]['id']

    # -------------------------------------------------------------------------

    def _get_mapping(self):

        if self.mapping is not None:
            return

        self._get_assgn_id()
        
        self.mapping = {}

        url = (f'{self.base_url}/api/assignments/{self.assgn_id}'
               f'/groups.json')
        res = requests.get(url, data={}, headers=self.header).json()
        for group in res:
            self.mapping[group['group_name']] = group['id']
        
        return

    # -------------------------------------------------------------------------

    def _get_ffs(self, group_id):
        '''
        Gets and returns the feedback files for a group. Return value is of 
        the form:
                         { filename : file_id }
        '''
        url = (f'{self.base_url}/api/assignments/{self.assgn_id}/'
               f'groups/{group_id}/feedback_files.json')
        res = requests.get(url, data={}, headers=self.header).json()
        ret = {ff['filename']: ff['id'] for ff in res} 
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
        for mark, test_case in zip(mark_list, self.cfg['tests']):
            breakdown[test_case['criteria']] += mark
        return breakdown

    # -------------------------------------------------------------------------
    #       Functions meant to be exposed
    # -------------------------------------------------------------------------
    
    def students(self):
        self._get_mapping()
        return self.mapping.keys()
    # -------------------------------------------------------------------------

    def student_exists(self, student):
        self._get_mapping()
        return student in self.mapping

    # -------------------------------------------------------------------------
    
    def delete_reports(self, student):
        self._get_mapping()
        if student not in self.mapping:
            raise ValueError(f"{student} not in the course.")
        group_id = self.mapping[student]

        for _, rid in self._get_ffs(group_id).items():
            url = (f'{self.base_url}/api/assignments/{self.assgn_id}/'
                   f'groups/{group_id}/feedback_files/{rid}'
                   f'.json')
            res = requests.delete(url, data={}, headers=self.header).json()
            if int(res['code']) != 200:
                print(f" ** Error: {res['description']}")

    # -------------------------------------------------------------------------

    def upload_report(self, student, file_path):
        self._get_mapping()
        if student not in self.mapping:
            raise ValueError(f"{student} not in the course.")
        group_id = self.mapping[student]
        
        fname = os.path.basename(file_path)
        existing_ffs = self._get_ffs(group_id)
        
        if fname in existing_ffs:
            url = (f'{self.base_url}/api/assignments/{self.assgn_id}/'
                   f'groups/{group_id}/feedback_files/{existing_ffs[fname]}'
                   f'.json')
            data = { 'file_content': open(file_path, 'rb').read() }
            res = requests.put(url, data=data, headers=self.header).json()
        else:
            import mimetypes
            url = (f'{self.base_url}/api/assignments/{self.assgn_id}/'
                   f'groups/{group_id}/feedback_files.json')
            data = {
                'filename': os.path.basename(file_path),
                'file_content': open(file_path, 'rb').read(),
                'mime_type': mimetypes.guess_type(file_path)[0]
            }
            res = requests.post(url, data=data, headers=self.header).json()
        return 200 <= int(res['code']) <= 201

    # -------------------------------------------------------------------------

    def download_submission(self, student, path):
        self._get_mapping()
        if student not in self.mapping:
            raise ValueError(f"{student} not in the course.")
        group_id = self.mapping[student]

        url = (f'{self.base_url}/api/assignments/{self.assgn_id}/'
               f'groups/{group_id}/submission_files.json')
        
        collected = ('collected' in self.cfg and self.cfg['collected'])

        if 'file_names' in self.cfg:
            for fname in self.cfg['file_names']:
                data = { 'filename': fname, 'collected': collected}
                res = requests.get(url, data=data, headers=self.header)
                with open(f'{path}/{fname}', 'wb') as outfile:
                    outfile.write(res.content)
        else:
            data = {'collected': collected}
            res = requests.get(url, data=data, headers=self.header)
            with open(f'{path}/{student}.zip', 'wb') as outfile:
                outfile.write(res.content)

    # -------------------------------------------------------------------------
    
    def upload_mark(self, student, mark_list):
        self._get_mapping()
        if student not in self.mapping:
            raise ValueError(f"{student} not in the course.")
        group_id = self.mapping[student]

        breakdown = self._accumulate_marks(mark_list)

        url =(f'{self.base_url}/api/assignments/{self.assgn_id}/groups/'
              f'{group_id}/update_marks.json')
        res = requests.put(url, data=breakdown, headers=self.header).json()
        return int(res['code']) == 200
    
    # -------------------------------------------------------------------------
    
    def set_status(self, student, status):
        self._get_mapping()
        if student not in self.mapping:
            raise ValueError(f"{student} not in the course.")
        group_id = self.mapping[student]

        url =(f'{self.base_url}/api/assignments/{self.assgn_id}/groups/'
              f'{group_id}/update_marking_state.json')
        
        data = { 'marking_state': status }
        res = requests.put(url, data=data, headers=self.header).json()
        return int(res['code']) == 200

