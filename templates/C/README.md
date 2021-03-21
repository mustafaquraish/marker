# Marker C Template

It is possible to use any C testing framework or methodology with the marker since you can just run arbitrary bash scripts / etc to parse the output.  For most simple cases, a barebones testing framework called `marker.h` is provided here.

To run the example, first run `make` in the directory to create some student directories and populate them with a copy of the `functions.c` file (This is to emulate `marker download` which cannot be run without LMS details).

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

---

## marker.h

The is a self-contained one-include header file that allows you to define and run individual test cases by name through the command line. A test case is defined as follows:

```c
#include "marker.h"

TEST(test_math) {
    if (5 != 5) {
        TEST_FAIL("test_math failed, something is wrong");
    }
    // Finishing test case means test passed
}
```
In general, the test case should only finish successfully if it has passed. Otherwise, print out a message (for the report) and exit with a non-zero status. The provided `TEST_FAIL()` does exactly this; printing out the message and exiting with status `1`. The `assert.h` library also works really well for this, and can be used directly.

To run the test cases through the command line by name, the `main()` function needs to call the test handler, which is done as follows:

```c
int main(int argc, char **argv) {
    // Whatever you need to do here
    marker_main(argc, argv);
    return 0;
}
```

In my experience, the `main()` function usually servers no other purpose in the testing file, so `marker.h` provides the above function already for these situations. To use this default main function, just add `#define MARKER_DEFAULT_MAIN` **before** including the `marker.h` file. So, the below would be a complete test file (which can be compiled and executed).

```c
#define MARKER_DEFAULT_MAIN
#include "marker.h"

TEST(test_math) {
    if (5 != 5) {
        TEST_FAIL("test_math failed, 5 != 5\n");
    }
    // Finishing test case means test passed
}

TEST(test_math_2) {
    if (4 == 5) {
        TEST_FAIL("test_math_2 failed, %d == %d\n", 4, 5);
    }
    // Finishing test case means test passed
}
```

These file can now be saved as `tests.c` and compiled with:

```bash
$ gcc tests.c -o tests
```

and you can run the test cases with:

```bash
$ ./tests               # Run all tests
$ ./tests -v            # Run all tests with logging
$ ./tests test_math     # Run test_math test case
$ ./tests test_math_2   # Run test_math_2 test case
```

*Note:* When running all tests, due to the nature of the program it will exit as soon as the any test fails, and not run the remaining ones. It is generally recommended to have each test separately (which is how the automarker is expected to be used).