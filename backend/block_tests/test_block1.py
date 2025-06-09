import unittest

class Block1Test(unittest.TestCase):
    def test_output(self):
        expected = (
            "Hello, World!\n"
            "0\n1\n2\n3\n4\n"
            "Goodbye, World!\n"
        )
        self.assertEqual(user_output, expected)
