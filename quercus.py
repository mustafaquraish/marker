'''
Utilities related to interfacing with Quercus

(C) Mustafa Quraish, 2020
Based on code by Lucy Tishkina.
'''
import requests
import os

# -----------------------------------------------------------------------------
# Helper utils for quercus-related stuff

def get_identifiers(assign_dir=None):
    '''
    Try to load the course and assignment id from the associated .metadata file
    in the directory. If not possible, prompt the user for it. Ask to save in
    the assignment directory.
    '''
    metadata_path = f'{assign_dir}/.metadata'
    if (dir is None) or (not os.path.isfile(metadata_path)):
        print(f"{metadata_path} file not found. Please enter details below.")
        course_id = input("- Course ID: ").strip()
        assgn_id = input("- Assignment ID: ").strip()

        prompt = input(f"Save assignment metadata in {metadata_path} ?: [Y]/n")
        if "n" not in prompt.lower():
            with open(metadata_path, 'w') as metadata_file:
                metadata_file.write(f"{course_id}:{assgn_id}")

    else:
        with open(metadata_path) as metadata_file:
            course_id, assgn_id = metadata_file.read().split(":")
            course_id = course_id.strip()
            assgn_id = assgn_id.strip()
    
    return course_id, assgn_id


def get_token():
    '''
    Try to load quercus token from file. If it doesn't exist, prompt
    the user and give them an option to save it locally.
    '''

    from pathlib import Path

    token_path = f'{Path.home()}/.canvas.token'
    try:
        with open(token_path) as token_file:
            token = token_file.read().strip()
    except FileNotFoundError:
        token = input("Enter Canvas Token: ").strip()
        prompt = input(f"Save token in {token_path} ?: [Y]/n")
        if "n" not in prompt.lower():
            with open(token_path, 'w') as token_file:
                token_file.write(token)
    return token


def utor_to_quercus_mapping(quercus_csv, reverse=False):
    '''
    Given the file descriptor from `open()` of the csv file from quercus,
    this function extracts the mapping from utorid to inernal quercus id.

    if reverse = False:
        { utorid : quercus_id }
    if revser = True:
        { quercus_id : utorid }
    '''
    import csv
    
    reader = csv.reader(quercus_csv)
    columns = next(reader)
    QUERCUS_ID_COLUMN = columns.index("ID")
    UTOR_ID_COLUMN = columns.index("SIS Login ID")

    mapping = {}
    for row in reader:
        quercus_id = row[QUERCUS_ID_COLUMN]
        utorid = row[UTOR_ID_COLUMN]
        if (quercus_id != "" and utorid != ""):
            if reverse:
                mapping[quercus_id] = utorid
            else:
                mapping[utorid] = quercus_id

    return mapping

# -----------------------------------------------------------------------------
# Quercus API helpers


def upload_file(token, course_id, assgn_id, student_id, report_path):
    '''
    Upload a file to the comments section of a given assignment for the given 
    (quercus) student id.
    '''

    file_size = os.path.getsize(report_path)
    endpoint = f"https://q.utoronto.ca/api/v1/courses/{course_id}/assignments/"\
               f"{assgn_id}/submissions/{student_id}/comments/files"

    data = {
        "name": report_path,
        "size": file_size,
        "content_type": "text/html",
        "parent_folder_path": "My Files/reports"
    }

    headers = {"Authorization": "Bearer " + token}
    res = requests.post(endpoint, data=data, headers=headers).json()

    if res.get('error') or res.get('errors'):
        return False

    endpoint = res.get('upload_url')
    data = {"file": open(report_path, 'rb')}

    res = requests.post(endpoint, files=data, headers=headers).json()

    if (res.get('error')):
        return False

    endpoint = res.get('location')
    res = requests.get(endpoint, headers=headers).json()
    if (res.get('upload_status') != "success"):
        return False

    file_id = res.get('id')
    endpoint = f"https://q.utoronto.ca/api/v1/courses/{course_id}/"\
               f"assignments/{assgn_id}/submissions/{student_id}"
    data = {"comment[file_ids][]": file_id}
    res = requests.put(endpoint, data=data, headers=headers).json()

    return True


def get_submission_data(token, course_id, assgn_id, student_id):
    endpoint = f"https://q.utoronto.ca/api/v1/courses/{course_id}/"\
               f"assignments/{assgn_id}/submissions/{student_id}"
    headers = {"Authorization": "Bearer " + token}
    res_json = requests.get(endpoint, data={}, headers=headers).json()
    if res_json.get('error') or res_json.get('errors'):
        return None
    return res_json


def download_submission_file(token, submission_data, file_path):
    if ('attachments' not in submission_data or
            len(submission_data['attachments']) < 1):
        return False
    
    headers = {"Authorization": "Bearer " + token}
    file_url = submission_data['attachments'][-1]['url']
    res = requests.get(file_url, data={}, headers=headers)
    
    # Assuming no errors returned for now...
    open(file_path, 'wb').write(res.content)
    return True

def upload_mark(token, course_id, assgn_id, student_id, mark):
    endpoint = f"https://q.utoronto.ca/api/v1/courses/{course_id}/"\
               f"assignments/{assgn_id}/submissions/{student_id}"
    
    headers = {"Authorization": "Bearer " + token}
    data = {"submission[posted_grade]": f"{mark}"}
    res = requests.put(endpoint, data=data, headers=headers).json()

    if res.get('error') or res.get('errors'):
        return False
    # print(res.json())
    # open('dl.json', 'wb').write(res.content)
    return True

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    print("This file won't do anything when you run it.")
