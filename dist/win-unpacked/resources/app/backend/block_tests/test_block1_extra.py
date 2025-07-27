import unittest

class Block1ExtraTest(unittest.TestCase):
    def test_goodbye_present(self):
        self.assertIn('Goodbye, World!', user_output)

