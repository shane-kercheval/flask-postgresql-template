# run 'python -m unittest test_forms.py'
# 'python -m unittest -v test_forms.py' to produce more verbose output
# pep8 --first app.py
import pep8
import unittest


class AppTest(unittest.TestCase):

    def test_pep8(self):
        """Test that we conform to PEP8."""
        pep8style = pep8.StyleGuide()
        result = pep8style.check_files(['app.py'])
        self.assertEqual(result.total_errors, 0, "Found code style errors (and warnings).")

if __name__ == '__main__':
    unittest.main()
