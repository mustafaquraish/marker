#!/bin/bash
: '
-------------------------------------------------------------------------------
  This shell script is the automarker responsible for handling the logistics
  for the automarker, such as checking if the file names are all correct, etc.

  Parsing the test suits
  running the test cases
  and forming the reports. It needs to be given a directory as an argument,
  and it expects certain files / folders to be present in the directory to
  facilitate the marking. For detailed information on how to use this, look
  at `README.md`.

  (C) Mustafa Quraish, 2020
-------------------------------------------------------------------------------
'

# -----------------------------------------------------------------------------
# Handle command line args and make sure necessary files exist


report="report.txt"
marksheet="marksheet.csv"
testsuite="testsuite.csv"

while getopts ":r:m:t" opt; do
  case ${opt} in
    r )
      report=$OPTARG
      ;;
    m )
      marksheet=$OPTARG
      ;;
    t )
      testsuite=$OPTARG
      ;;
    \? )
      echo "- Invalid option: $OPTARG" 1>&2
      exit 1
      ;;
    : )
      echo "- Invalid option: $OPTARG requires an argument" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))


if [[ $# -ne 1 ]]
then
    >&2 echo "============================== Usage ==========================="
    >&2 echo " $0 [-r report.txt] [-m marksheet.csv] [-t testsuite.csv] <assignment_dir>"
    >&2 echo "    - [-r report.txt]: (Optional) custom report file name"
    >&2 echo "    - [-m marksheet.csv]: (Optional) custom marksheet file name"
    >&2 echo "    - [-t testsuite.csv]: (Optional) custom testsuite file name"
    >&2 echo "    - <assignment_dir>: Assignment directory (look: README.md)"
    exit 1
fi

dir=$1


if [[ ! -d "$dir/candidates" ]]
then
    >&2 echo "*** Error: candidates directory doesn't exist."
    exit 1
fi

if [[ ! -f "$dir/testsuite.csv" ]]
then
    >&2 echo "*** Error: testsuite.csv doesn't exist."
    exit 1
fi

# -----------------------------------------------------------------------------
# Check/create marksheet.csv if not already done by `prepare.sh`

pushd $dir > /dev/null

# Doesn't exist
if [[ ! -f $marksheet ]]
then
    read -r -p "- $marksheet does not exist. Create? [Y]/n: " create
    if [[ "$create" =~ ^([yY][eE][sS]|[yY]?)$ ]]
    then
        for i in `ls candidates`
        do
            echo "$i," >> $marksheet
        done
        echo "Created $marksheet"
    else
        echo "Exiting."
        exit 0
    fi
fi

rm -f .marksheet.tmp

while IFS=, read -r utorid prev_mark
do
    # Only want to run the tests for students NOT marked as done.
    if [[ -z $prev_mark ]]
    then
        echo -n "Testing $utorid... "
        pushd "candidates/$utorid" > /dev/null

        # Keep track of the student's awarded marks.
        student_mark=0

        # Remove old report
        rm -f $report

        if [[ ! -z `grep "error" compile.log` ]]
        then
            echo "[COMPILE ERROR] 0 marks."
            echo "Your submission failed to compile. Logs below:" >> $report
            echo "" >> $report
            cat compile.log >> $report
        else
            test_num=0
            # Extract information from testsuite.csv and run the tests cases.
            while IFS=, read -r mark timeout cmd desc;
            do
                if [[ -z $mark ]] || [[ -z $cmd ]] || [[ -z $timeout ]]
                then
                    # There's linely a mistake in the testsuite file and there
                    # is a newline. For now, quick fix to just skip.
                    continue
                fi

                echo "---------------------------------------------" >> $report
                echo "- RUNNING TEST $test_num: $desc   " >> $report
                echo "" >> $report

                # Run the test with the provided timeout, put output in log.
                timeout $timeout ${cmd} >> $report 2>&1
                exit_status=$?

                echo "" >> $report
                if [[ $exit_status -eq 0 ]]
                then
                    # The test passed. Award the student marks.
                    echo "- PASSED.  $mark / $mark" >> $report
                    student_mark=$(($student_mark + $mark))

                elif [[ $exit_status -eq 124 ]]
                then
                    # This exit code corresponds to timing out.
                    echo "- TIMED OUT.  0 / $mark" >> $report
                else
                    echo "- FAILED.  0 / $mark" >> $report
                fi

                echo "" >> $report  # Empty line for spacing
                test_num=$(($test_num+1))
            done < ../../testsuite.csv
            echo " $student_mark marks."
        fi

        echo "" >> $report
        echo "-----------------------------------------------------" >> $report
        echo "- TOTAL MARK: $student_mark" >> $report

        popd > /dev/null
        # Update the student's status and mark.
        echo "$utorid,$student_mark" >> .marksheet.tmp

    # If marking status is already DONE, no need to do / change anything.
    else
        echo "$utorid,$prev_mark" >> .marksheet.tmp
    fi
done < $marksheet

# Overwrite old status file with the modified one
mv .marksheet.tmp $marksheet

echo "Done."
