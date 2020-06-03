'''
This script downloads all the submissions for a given assignment from quercus,
and puts them in the desired directory structure used by the automarker.

For example, if you want downloaded the submissions for ex0, and want to name
the individual files as `ex0.c`, then you would run:

python3 download_submissions.py 160057 343885 ../tests/ex0 ex0.c
                                ^       ^
                                course   assgn
                                id       id

which would create the following directory structure:
  
  ../tests/
     └── ex0/
          ├── .metadata
          ├── extra-files/
          │    └─ (empty)
          └─── candidates/
                ├── utorid1/
                │    └─ ex0.c
                ├── utorid2/
                │    └─ ex0.c
                └── ...
     
(C) Mustafa Quraish, 2020
'''

import sys
import os
import requests
import quercus

if len(sys.argv) != 5:
    print("============================== Usage =============================")
    print(" python3 download_submissions.py "
          "<course_id> <assgn_id> <assgn_dir> <file_name>")
    print("     - <course_id> is the course id from quercus")
    print("     - <assgn_id> is the assignment id from quercus")
    print("     - <assgn_dir> path of the directory to be created")
    print("     - <file_name> name to give the individual submission files")
    print("------------------------------------------------------------------")
    print("- `quercus.csv` should be in the same directory as this script.")
    print("------------------------------------------------------------------")
    sys.exit(1)

# Read command line args
course_id = sys.argv[1]
assgn_id = sys.argv[2]
assgn_dir = sys.argv[3]
file_name = sys.argv[4]


parent_dir = os.path.dirname(os.path.abspath(assgn_dir))

scripts_dir = os.path.dirname(os.path.abspath(__file__))
quercus_csv = open(f'{scripts_dir}/quercus.csv', 'r')

# -----------------------------------------------------------------------------
# Make sure given paths are valid.

if not os.path.exists(parent_dir):
    create = input(f"{parent_dir} does not exist. Create? [Y]/n: ")
    if "n" in create.lower():
        print("Exiting.")
        sys.exit(1)
    else:
        os.makedirs(parent_dir, exist_ok=True)

elif not os.path.isdir(parent_dir):
    print(f"{parent_dir} is a file. Exiting.")
    sys.exit(1)

elif os.path.isdir(f"{parent_dir}/{assgn_dir}"):
    create = input(f"{parent_dir}/{assgn_dir} exists. Overwrite? y/[N]: ")
    if not "y" in create.lower():
        print("Exiting.")
        sys.exit(1)

elif os.path.exists(f"{parent_dir}/{assgn_dir}"):
    print(f"{parent_dir}/{assgn_dir} is a file. Exiting.")
    sys.exit(1)

# -----------------------------------------------------------------------------

print("Making directory structure...")
os.makedirs(f'{parent_dir}/{assgn_dir}', exist_ok=True)
os.makedirs(f'{parent_dir}/{assgn_dir}/extra-files', exist_ok=True)
os.makedirs(f'{parent_dir}/{assgn_dir}/candidates', exist_ok=True)

# Write course ID and assignment ID into folder for later reference.
with open(f'{parent_dir}/{assgn_dir}/.metadata', 'w') as metadata_file:
    metadata_file.write(f"{course_id}:{assgn_id}") 

candidates_dir = f'{parent_dir}/{assgn_dir}/candidates'

# Get the mapping from quercus id to UTORid
mapping = quercus.utor_to_quercus_mapping(quercus_csv)

token = quercus.get_token()

cur_index = 0
num_submissions = len(mapping)

for utorid, quercus_id in mapping.items():
    cur_index += 1
    print(f"- [{cur_index:3d}/{num_submissions:3d}] "
          f"Getting submission for {utorid}...", end=" ", flush=True)

    submission_data = quercus.get_submission_data(
        token=token,
        course_id=course_id,
        assgn_id=assgn_id,
        student_id=quercus_id
    )
    if submission_data is None:
        print(f"[ERROR] User not found.")
        continue
    if submission_data['missing']:
        print(f"[MISSING] Skipping...")
        continue
    if submission_data['late']:
        print(f"[LATE] Skipping...")
        continue
    
    os.makedirs(f'{candidates_dir}/{utorid}', exist_ok=True)
    file_path = f'{candidates_dir}/{utorid}/{file_name}'
    
    done = quercus.download_submission_file(token, submission_data, file_path)
    print("Done." if done else "[ERROR] Failed.")

print("Finished.")