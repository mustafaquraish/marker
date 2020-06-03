#!/usr/bin/python3

'''
This script takes in a CSV file containing 2 columns: 
                   
                    utorid, mark

and updates the mark on quercus for all the students. As always, <quercus.csv>
should be passed into this script.

(C) Mustafa Quraish, 2020
'''

import sys
import os
import quercus


if len(sys.argv) != 2:
    print("============================== Usage =============================")
    print(" python3 upload_marks.py <marksheet.csv>")
    print("         - <marksheet.csv> CSV file with utorids and final marks")
    print("------------------------------------------------------------------")
    print("- `quercus.csv` should be in the same directory as this script.")
    print("- `.metadata` should exist in the same directory as the marksheet.")
    print("------------------------------------------------------------------")
    sys.exit(1)

# Read command line args
marksheet = open(sys.argv[1], 'r')

scripts_dir = os.path.dirname(os.path.abspath(__file__))
quercus_csv = open(f'{scripts_dir}/quercus.csv', 'r')

assgn_dir = os.path.dirname(os.path.abspath(sys.argv[1]))

# -----------------------------------------------------------------------------

mapping = quercus.utor_to_quercus_mapping(quercus_csv)
course_id, assgn_id = quercus.get_identifiers(assgn_dir)
token = quercus.get_token()

for line in marksheet.readlines():
    utorid, mark = line.split(',')
    # Strip whitespace if necessary
    utorid = utorid.strip()
    mark = mark.strip()
    
    if utorid not in mapping:
        print(f"!!! Error: {utorid} not found in quercus.csv")
        continue
    
    print(f"Uploading mark={mark} for {utorid}...", end=" ", flush=True)
    quercus_id = mapping[utorid]
    done = quercus.upload_mark(token, course_id, assgn_id, quercus_id, mark)
    print("Done." if done else "[ERROR] Failed.")

print("Finished.")