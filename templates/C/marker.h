/**
 *                            Marker.h
 *                           ----------
 * One-Header file simple testing framework for C code. Works best with
 *    the `marker` program (https://github.com/mustafaquraish/marker).
 *
 *  ------------------------------------------------------------------------
 *
 *  Usage:
 *      - Add this header file to your project directory and import it
 *
 *      - Define a test case as follows:
 *            TEST(test_name) {
 *                  <code>
 *            }
 *
 *      - Each test case is expected to exit with non-zero status if it fails.
 *          returning from the test function counts as a success. The provided
 *          TEST_FAIL() function prints out a given message and exits with 1,
 *          but you can also use the functionality from `assert.h`
 *
 *      - In the main function, call `marker_main(argc, argv)` to run tests.
 *
 *      - Run `./program test_name` to run a single test or `./program`
 *          to run all tests. The latter is not ideal as no further tests
 *          are fun as soon as a single one fails.
 *
 * A default main() function is included in the header file, if you don't need
 * any other functionality then you can use it by simply putting
 *
 *        #define MARKER_DEFAULT_MAIN
 *
 * in the C file before importing the header. You don't need to define any
 * main function in this case.
 *
 *  ------------------------------------------------------------------------
 *                          Mustafa Quraish, 2020
 */
#pragma once

#include <stdarg.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Main test case container */
typedef struct marker_test {
  char *name;               // User-defined name of test case
  void (*test_func)(void);  // Function pointer to test handler
  struct marker_test *next; // Next pointer for internal linked list
} marker_test;

/* Main linked list for test cases */
typedef struct marker_test_map {
  int num_tests;
  marker_test *list;
} marker_test_list;

/* Global list of all test cases */
static marker_test_list ALL_TESTS = {0, NULL};

/* Whether or not to print out logs */
static int marker_verbose = 0;

/* Log things to stdout if verbose mode is on */
static void marker_log(const char *format, ...) {
  if (marker_verbose) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
  }
}

/* Log things to stdout if verbose mode is on */
static void TEST_FAIL(const char *format, ...) {
  va_list args;
  va_start(args, format);
  vprintf(format, args);
  va_end(args);
  exit(1);
}

/* Find the test case given the name, NULL if doesn't exist */
static marker_test *marker_get_test(char *name) {
  for (marker_test *cur = ALL_TESTS.list; cur != NULL; cur = cur->next)
    if (strcmp(cur->name, name) == 0)
      return cur;
  return NULL;
}

/* Create and add test to head of linked list if it doesn't already exist */
static void marker_insert_test(char *name, void (*test_func)(void)) {
  marker_test *node = calloc(sizeof(marker_test), 1);
  node->name = name;
  node->test_func = test_func;

  if (ALL_TESTS.list == NULL) {
    ALL_TESTS.list = node;
    return;
  }

  marker_test *cur = ALL_TESTS.list;
  while (cur->next != NULL) {
    cur = cur->next;
  }
  cur->next = node;
}

/* Run test */
static void marker_run_test(marker_test *test) {
  marker_log("[+] Running test: %s\n", test->name);
  test->test_func();
}

/* Run all the tests */
static void marker_run_all_tests() {
  marker_test *cur = ALL_TESTS.list;
  while (cur != NULL) {
    marker_run_test(cur);
    cur = cur->next;
  }
}

/* Free all associated data */
static void marker_free_lists() {
  marker_test *cur = ALL_TESTS.list;
  while (cur != NULL) {
    marker_test *temp = cur->next;
    free(cur);
    cur = temp;
  }
}

/**
 * Main function to handle running all tests. Should take in argc and argv
 * from `main()`. If no arguments are passed in, all tests are run.
 */
static void marker_main(int argc, char **argv) {
  // Check arguments for `-v` flag
  if (argc > 1 && strcmp(argv[1], "-v") == 0)
    marker_verbose = 1, argc--, argv++;

  if (argc == 1) {
    marker_run_all_tests();
  } else {
    marker_test *test = marker_get_test(argv[1]);
    if (test == NULL) {
      fprintf(stderr, "Test %s not found. Exiting.\n", argv[1]);
      exit(1);
    }
    marker_run_test(test);
  }
  marker_free_lists();
  marker_log("[+] Done.\n");
}

#define TEST(name)                                                             \
  void marker_testcase_##name(void);                                           \
  __attribute__((constructor)) void marker_constructor_##name() {              \
    marker_insert_test(#name, marker_testcase_##name);                         \
  }                                                                            \
  void marker_testcase_##name(void)

/** If this flag is defined, use the default basic main function **/
#ifdef MARKER_DEFAULT_MAIN
int main(int argc, char **argv) { marker_main(argc, argv); }
#endif