: '
-------------------------------------------------------------------------------
  This shell script is the meant to be run before the automarker to prepare
  the assignment for marking. It needs to be given a directory as an argument,
  and it expects certain files / folders to be present in the directory to
  facilitate the marking. For detailed information on how to use this, look
  at `README.md`.

  (C) Mustafa Quraish, 2020
-------------------------------------------------------------------------------
'

marksheet="marksheet.csv"
src_dir=""

while getopts ":m:s:" opt; do
  case ${opt} in
    m )
      marksheet=$OPTARG
      ;;
    s )
      src_dir=$OPTARG
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
    >&2 echo "$0 [-m marksheet.csv] [-s src_dir] <assignment_dir>"
    >&2 echo "    - [-m marksheet.csv]: (Optional) custom marksheet file name"
    >&2 echo "    - [-s src_dir]: (Optional) use files from this directory."
    >&2 echo "                    For more detailson this, look at README.md."
    >&2 echo "    - <assignment_dir>: Assignment's directory"
    exit 1
fi

dir=$1

# -----------------------------------------------------------------------------
# Ensure basic directory structure is correct.

if [[ ! -d "$dir" ]]
then
    >&2 echo "*** Error: assignment directory doesn't exist."
    exit 1
fi

if [[ ! -d "$dir/candidates" ]]
then
    >&2 echo "*** Error: candidates directory doesn't exist."
    exit 1
fi

if [[ ! -d "$dir/extra-files" ]]
then
    >&2 echo "*** Error: extra-files directory doesn't exist."
    exit 1
fi

# -----------------------------------------------------------------------------
# If a source directory is given, try to import the extra files, testsuite
#                       nd Makefile from it.
# -----------------------------------------------------------------------------

# If a source directory has been specified
if [[ ! -z $src_dir ]]
then
    # Check if it's not a valid directory with a `.extra-files` file in it
    if [[ ! -d $src_dir ]]
    then
        >&2 echo "*** Error: $src_dir not valid a valid directory."
        exit 1
    fi

    if [[ ! -f $src_dir/Makefile ]]
    then
        >&2 echo "*** Error: $src_dir/Makefile doesn't exist."
        exit 1
    elif [[ ! -f $src_dir/testsuite.csv ]]
    then
        >&2 echo "*** Error: $src_dir/testsuite.csv doesn't exist."
        exit 1
    fi

    echo "- Imported $src_dir/Makefile -> $dir/extra-files/Makefile "
    cp -f $src_dir/Makefile $dir/extra-files/
    echo "- Imported $src_dir/testsuite.csv -> $dir/testsuite.csv"
    cp -f $src_dir/testsuite.csv $dir/

    # If `.extra_files` exists, copy over all the files listed in there
    if [[ -f $src_dir/.extra-files ]]
    then
        # For every file/folder listed in .extra-files
        while IFS='\n' read -r fl
        do
            # If the line isn't a comment or empty
            if [[ $fl != \#* ]] && [[ ! -z $fl ]]
            then
                echo "- Imported $src_dir/$fl -> $dir/extra-files/$fl"
                # Copy over the file / folder
                cp -r "$src_dir/$fl" $dir/extra-files/ 2> /dev/null
            fi
        done < $src_dir/.extra-files
    fi
    echo "-------- Importing from source directory done. ------------"
    echo ""
fi

# -----------------------------------------------------------------------------
# Ensure that there is a Makefile here before beginning (in case src_dir is
#                                                        not being used)

if [[ ! -f "$dir/extra-files/Makefile" ]]
then
    >&2 echo "*** Error: Makefile is missing doesn't exist."
    exit 1
fi

# -----------------------------------------------------------------------------

pushd $dir > /dev/null

rm -f $marksheet

for dir in `ls candidates`
do
    echo "$dir," >> $marksheet
    cp -r extra-files/* candidates/$dir
    echo -n "- Compiling $dir... "
    pushd candidates/$dir > /dev/null
    make 2> compile.log > /dev/null

    if [[ -z `cat compile.log` ]]
    then
        echo " done."
    elif [[ $(grep "error" compile.log) ]]
    then
        echo "[ERROR] failed."
    else
        echo "[WARNING] done."
    fi

    popd > /dev/null
done

popd > /dev/null
echo "Finished. Compilation logs stored in 'compile.log'"
