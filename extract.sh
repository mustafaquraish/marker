#!/bin/bash
: '
----------------------------------------------------------------------------
------- This is now deprecated. Use download_submissions.py ----------------
----------------------------------------------------------------------------

  This shell script is meant to be used to extract a `zip` file from Quercus
  into the directory structure expected by the automarker and other scripts.
  
  For example, if you have downloaded the submission zip for A1, and want to
  extract all the files names as `soln.c`, then you would run:
  
  ./extract.sh quercus.csv ../Marking A1 ~/submissions.zip soln.c
  
  which would create the following directory structure:
  
  ../Marking/
  |-- extra-files/
  |    `- (empty)
  `--- candidates/
          |-- utorid1/
          |    `- soln.c
          |-- utorid2/
          |    `- soln.c
          `-- ...
  
  (C) Mustafa Quraish, 2020
------------------------------------------------------------------------------
'

if [[ $# -ne 5 ]]
then
    >&2 echo "======================== Usage ================================="
    >&2 echo "$0 <quercus.csv> <extract_dir> <assignment_name> <zip> <fname>"
    >&2 echo "     - <quercus.csv> is the class list from quercus"
    >&2 echo "     - <extract_dir> where the new assignment dir should be made"
    >&2 echo "     - <assignment_name> name of the new directory"
    >&2 echo "     - <zip> zip file downloaded from quercus"
    >&2 echo "     - <fname> name to give the extracted code files"
    exit 1
fi

quercus=$1
dir=$2
assgn=$3
q_zip=$4
fname=$5

if [[ -d "$dir/$assgn" ]]
then
    >&2 echo "$dir/$assgn already exists. Aborting".
    exit 1 
fi

echo "- Making assignment directory..."
mkdir -p "$dir/$assgn/tmp"
mkdir -p "$dir/$assgn/candidates"
mkdir -p "$dir/$assgn/extra-files"

echo "- Extracting zip file..."
unzip -d "$dir/$assgn/tmp" $q_zip > /dev/null

echo "- Creating student folders..."
for file in `ls $dir/$assgn/tmp`
do
    student_id=`echo $file | cut -d '_' -f 2`
    utorid=`grep $student_id $quercus | cut -d ',' -f 5`
    mkdir $dir/$assgn/candidates/$utorid
    mv $dir/$assgn/tmp/$file $dir/$assgn/candidates/$utorid/$fname
done

echo "- Removing temporary files..."
rm -rf $dir/$assgn/tmp

echo "- Done."