#!/usr/bin/python3

'''
Upload report files for the assignment / exercise to quercus. This file assumes
that the directory containing submissions has the following structure:

submission_path/
 |-- .metadata
 '-- candidates/
      |-- utorid1/
      |    '-- report_name
      |-- utorid2/
      |    '-- report_name
      '-- ...

where `submission_path` and `report_name` are the passed in arguments.

(C) Mustafa Quraish, 2020
Based on code by Lucy Tishkina.
'''

import sys
import os
import quercus


if len(sys.argv) != 3:
    print("============================== Usage =============================")
    print(" python3 upload_reports.py <assgn_dir> <report_name>")
    print("     - <assgn_dir> is the where the testing reports are stored")
    print("     - <report_name> is the name of the individual report files")
    print("------------------------------------------------------------------")
    print("- `quercus.csv` should be in the same directory as this script.")
    print(" `.metadata` should exist in the assignment directory.")
    print("------------------------------------------------------------------")
    sys.exit(1)

# Read command line args
assgn_dir = sys.argv[1]
report_name = sys.argv[2]

scripts_dir = os.path.dirname(os.path.abspath(__file__))
quercus_csv = open(f'{scripts_dir}/quercus.csv', 'r')

# -----------------------------------------------------------------------------

course_id, assgn_id = quercus.get_identifiers(assgn_dir)
token = quercus.get_token()
mapping = quercus.utor_to_quercus_mapping(quercus_csv)

for student_dir in os.listdir(assgn_dir + '/candidates'):
    report_path = f"{assgn_dir}/candidates/{student_dir}/{report_name}"

    if student_dir not in mapping:
        print(f" *** Error: `{student_dir}` not recognized on Quercus")
    elif not os.path.exists(report_path):
        print(f" *** Error: `{report_path}` does not exist")
    else:
        quercus_id = mapping[student_dir]
        print(f"- Uploading {student_dir} report ...", end=" ", flush=True)
        done = quercus.upload_file(
            token=token,
            course_id=course_id,
            assgn_id=assgn_id,
            student_id=quercus_id,
            report_path=report_path
        )
        print("Done." if done else "[ERROR] Failed.")

print("Done.")
