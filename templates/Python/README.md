# Marker Python Template

The easiest way to unit test with Python is to use the `unittest` standard library. It already lets us individually run test cases through the command line, which is ideal for the marker.

To run the example, first run `make` in the directory to create some student directories and populate them with a copy of the `functions.py` file (This is to emulate `marker download` which cannot be run without LMS details).

```bash
$ make candidates
```

After that, run the following commands in the interactive REPL:
```bash
$ marker
[+] Config loaded
marker > prepare
    ...
marker > run -v         # -v set verbose to see marks
    ...
```

or run them directly through the command line as follows:
```bash
$ marker prepare
$ marker run -v
```