import functions
import unittest

class TestFunctions(unittest.TestCase):
    def test_square(self):
        self.assertEqual(functions.square(5), 25)

    def test_sum_of_squares(self):
        self.assertEqual(functions.sum_of_squares(3), 14)

    def test_sleep_10_sec(self):
        functions.sleep_10_sec()
    
    def test_exit_with_7(self):
        with self.assertRaises(SystemExit) as cm:
            functions.exit_with_7()

        self.assertEqual(cm.exception.code, 7)

if __name__ == '__main__':
    unittest.main()