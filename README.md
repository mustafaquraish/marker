# Marker

A marking utility to help automate code testing, and interfacing with the submission platform. Currently, the following platforms are supported:

- Canvas
- MarkUs


This package installs the program `marker`. It supports the following commands:

- `marker download`: Downloads files from the given LMS.
- `marker prepare`: Copies needed files into student directories, compiles code.
- `marker run`: Runs all the test cases, creates logs and compiles marks.
- `marker upload-marks`: Uploads the student marks to the LMS.
- `marker upload-reports`: Uploads the testing logs to the LMS for the student.
- `marker set-status`: Sets the marking state of the submission (MarkUs only).

---

## How to install

There are 2 ways to install this marker. The recommended way of doing this is to install from `pip`:

### - Using PIP

```
pip install automark
```

Alternatively, if you want to develop, you will need to build from source:

### - Build from source

First, clone this repository to your machine:

```sh
git clone https://github.com/mustafaquraish/marker
```

Then, go into the cloned repo and use the Makefile to build and install
```sh
cd marker
make install
```

Alternatively, use the following commands to build and install yourself if your preferred `python` and `pip` executables are named differently:

```
python3 setup.py bdist_wheel
pip3 install dist/*     
```

---

[Full Documentation available in the wiki](https://github.com/mustafaquraish/marker/wiki)

