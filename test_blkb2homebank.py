import unittest
import blkb2homebank
import os


class blkb2homebankTest(unittest.TestCase):
    out_filename = "test-output.csv"

    def test_append_to_filename(self):
        actual = blkb2homebank.append_to_filename("foo/bar.csv", "-test")
        self.assertEqual(actual, "foo/bar-test.csv")

    def test_convert_to_homebank_date(self):
        actual = blkb2homebank.convert_to_homebank_date("2000-12-31", "%Y-%m-%d")
        self.assertEqual(actual, "31-12-2000")

    def test_convert_csv(self):
        blkb2homebank.convert_csv("testdata/test-input.csv", self.out_filename)
        with open(self.out_filename, "r") as actual_out_file:
            actual = actual_out_file.read()
        with open("testdata/test-output.csv", "r") as expected_out_file:
            expected = expected_out_file.read()
        self.assertEqual(actual, expected)

    def _delete_if_exits(self, filename):
        if os.path.isfile(filename):
            os.remove(filename)

    def tearDown(self):
        self._delete_if_exits(self.out_filename)


if __name__ == "__main__":
    unittest.main()
