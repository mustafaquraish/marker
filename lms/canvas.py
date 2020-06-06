'''
Utilities related to interfacing with Canvas

(C) Mustafa Quraish, 2020
'''
import requests
import os


class Canvas():

    #-------------------------------------------------------------------------#

    def __init__(self, config):
        self.base_url = config['base_url']
        self.course_id = config['course']
        self.assgn_id = config['assignment']
        self.cfg = config
        self.mapping = None
        self._get_token()
        self.header = {"Authorization": "Bearer " + self.token}

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#

    def _get_token(self):
        '''
        Try to load quercus token from file. If it doesn't exist, prompt
        the user and give them an option to save it locally.
        '''

        from pathlib import Path

        token_path = f"{Path.home()}/.canvas.token"
        try:
            with open(token_path) as token_file:
                token = token_file.read().strip()
        except FileNotFoundError:
            token = input("Enter Canvas Token: ").strip()
            prompt = input(f"Save token in {token_path} ?: [Y]/n")
            if "n" not in prompt.lower():
                with open(token_path, 'w') as token_file:
                    token_file.write(token)
        self.token = token

    #-------------------------------------------------------------------------#

    def _get_mapping(self):
        if self.mapping is not None:
            return

        print("- Fetching course users...", end="", flush=True)

        url = f'{self.base_url}/api/v1/courses/{self.course_id}/users'
        page, res = 1, None

        self.mapping = {}

        while (page == 1 or res != []):
            data = { 
                'enrollment_type': 'student', 
                'per_page': 100, 
                'page': page, 
            }
            res = requests.get(url, data=data, headers=self.header).json()
            for user in res:
                if 'login_id' in user:
                    self.mapping[user['login_id']] = user['id']
                elif 'sis_user_id' in user:
                    self.mapping[user['sis_user_id']] = user['id']
                elif 'email' in user:
                    userid = user['email'].split('@')[0]
                    self.mapping[userid] = user['id']
                else:
                    raise Exception("No suitable column found in canvas data")
            page += 1
            print(".", end="", flush=True)
        
        print()
        return

    #-------------------------------------------------------------------------#
    #-------------------------------------------------------------------------#

    def students(self):
        self._get_mapping()
        return self.mapping.keys()

    #-------------------------------------------------------------------------#

    def upload_report(self, student_id, report_path):
        '''
        Upload a file to the comments section of a given assignment for the 
        given student_id
        '''
        self._get_mapping()
        if student_id not in self.mapping:
            raise ValueError(f"{student_id} not in the course.")

        canvas_id = self.mapping[student_id]

        url = (f"{self.base_url}/api/v1/courses/{self.course_id}"
               f"/assignments/{self.assgn_id}/submissions/{canvas_id}"
               f"/comments/files")

        file_size = os.path.getsize(report_path)
        data = {
            "name": report_path,
            "size": file_size,
            "content_type": "text/html",
            "parent_folder_path": "My Files/reports"
        }

        res = requests.post(url, data=data, headers=self.header).json()

        if res.get('error') or res.get('errors'):
            return False

        url = res.get('upload_url')
        data = {"file": open(report_path, 'rb')}

        res = requests.post(url, files=data, headers=self.header).json()
        if (res.get('error')):
            return False

        url = res.get('location')
        res = requests.get(url, headers=self.header).json()
        if (res.get('upload_status') != "success"):
            return False

        file_id = res.get('id')
        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/"
               f"assignments/{self.assgn_id}/submissions/{canvas_id}")

        data = {"comment[file_ids][]": file_id}
        res = requests.put(url, data=data, headers=self.header).json()

        return True

    #-------------------------------------------------------------------------#

    def download_submission(self, student_id, student_dir):
        self._get_mapping()
        if student_id not in self.mapping:
            raise ValueError(f"{student_id} not in the course.")
        canvas_id = self.mapping[student_id]

        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/"
               f"assignments/{self.assgn_id}/submissions/{canvas_id}")
        res = requests.get(url, data={}, headers=self.header).json()
        
        if res.get('error') or res.get('errors'):
            return False
        if ('attachments' not in res or len(res['attachments']) < 1):
            return False

        file_url = res['attachments'][-1]['url']
        res = requests.get(file_url, data={}, headers=self.header)
        
        fname = self.cfg['file_name']
        # Assuming no errors returned for now...
        open(f'{student_dir}/{fname}', 'wb').write(res.content)

        return True

    #-------------------------------------------------------------------------#
    
    def upload_mark(self, student_id, mark):
        self._get_mapping()
        if student_id not in self.mapping:
            raise ValueError(f"{student_id} not in the course.")
        canvas_id = self.mapping[student_id]

        url = (f"{self.base_url}/api/v1/courses/{self.course_id}/"
               f"assignments/{self.assgn_id}/submissions/{canvas_id}")

        data = {"submission[posted_grade]": f"{mark}"}
        res = requests.put(url, data=data, headers=self.header).json()

        if res.get('error') or res.get('errors'):
            return False

        return True

    #-------------------------------------------------------------------------#
