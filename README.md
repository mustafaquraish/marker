# Marker

A marking utility to help automate code testing, and interfacing with the submission platform. Currently, the following platforms are supported:

- Canvas
- MarkUs


This package installs the program `marker`. It can either be run as an interactive REPL or through the command line directly. It supports the following commands:

- `download`: Downloads files from the given LMS.
- `prepare`: Copies needed files into student directories, compiles code.
- `run`: Runs all the test cases, creates logs and compiles marks.
- `upload-marks`: Uploads the student marks to the LMS.
- `upload-reports`: Uploads the testing logs to the LMS for the student.
- `delete-reports`: Deletes the testing logs from the LMS for the student.
- `set-status`: Sets the marking state of the submission (MarkUs only).
- `stats`: Gives you some basic statistics of the results.

Each of the commands can be run either for individual students or for everyone. Run `marker help` or `marker help command` for more information.

---

## How to install

There are 2 ways to install this marker. 

### (1) Using PIP
This is by far the recommended way of installing this utility. Simply run:
```bash
pip install marker
```

### (2) Build from source

Alternatively, if you want to develop, you will need to build from source. First, clone this repository to your machine:

```bash
git clone https://github.com/mustafaquraish/marker
```

Then, go into the cloned repo and use the Makefile to build and install
```bash
cd marker
make install
```

Alternatively, use the following commands to build and install yourself if your preferred `python` and `pip` executables are named differently:

```
python3 setup.py bdist_wheel
pip3 install dist/*     
```

---

## How to use

Some examples on how to use this marker with Python and C code are provided
in the `templates` directory, however it is designed to work with any programming
language as long as you can run tests from the command line. Even if you're not
using C, the template will be helpful in showing you how to set it up to work
with your environment.

---

[(Full Documentation](https://marker-docs.readthedocs.io/en/latest/)

