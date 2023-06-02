import unittest

from apps.utils import expect


class TestExpectFunction(unittest.TestCase):
    def test_valid_input_int(self):
        result = expect(5, int, "field")
        self.assertEqual(result, 5)

    def test_valid_input_str(self):
        result = expect("hello", str, "field")
        self.assertEqual(result, "hello")

    def test_valid_input_list(self):
        result = expect([1, 2, 3], list, "field")
        self.assertEqual(result, [1, 2, 3])

    def test_valid_input_dict(self):
        result = expect({"key": "value"}, dict, "field")
        self.assertEqual(result, {"key": "value"})

    def test_valid_input_bool(self):
        result = expect(True, bool, "field")
        self.assertEqual(result, True)

    def test_invalid_input_int(self):
        with self.assertRaises(AssertionError):
            expect(5, str, "field")

    def test_invalid_input_str(self):
        with self.assertRaises(AssertionError):
            expect("hello", int, "field")

    def test_invalid_input_list(self):
        with self.assertRaises(AssertionError):
            expect([1, 2, 3], dict, "field")

    def test_invalid_input_dict(self):
        with self.assertRaises(AssertionError):
            expect({"key": "value"}, list, "field")

    def test_invalid_input_bool(self):
        with self.assertRaises(AssertionError):
            expect(5, bool, "field")


if __name__ == '__main__':
    unittest.main()
