import unittest
from brambox.boxes import Box


class TestBox(unittest.TestCase):
    def setUp(self):
        self.box = Box()
        assert type(self.box) == Box

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
