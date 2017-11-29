import unittest
from brambox.boxes import Box


class TestBox(unittest.TestCase):
    def setUp(self):
        self.box = Box()
        assert type(self.box) == Box

    def tearDown(self):
        pass

    def test_rescale_int(self):
        """ Test rescaling of an annotation with an int """
        self.box.class_label = 'person'
        self.box.x_top_left = 10
        self.box.y_top_left = 10
        self.box.width = 10
        self.box.height = 10

        self.box.rescale(2)
        self.assertEqual(self.box.class_label, 'person')
        self.assertEqual(self.box.x_top_left, 20)
        self.assertEqual(self.box.y_top_left, 20)
        self.assertEqual(self.box.width, 20)
        self.assertEqual(self.box.height, 20)

    def test_rescale_float(self):
        """ Test rescaling of an annotation with a float """
        self.box.class_label = 'person'
        self.box.x_top_left = 10
        self.box.y_top_left = 10
        self.box.width = 5
        self.box.height = 5

        self.box.rescale(0.5)
        self.assertEqual(self.box.x_top_left, 5)
        self.assertEqual(self.box.y_top_left, 5)
        self.assertEqual(self.box.width, 2.5)
        self.assertEqual(self.box.height, 2.5)


if __name__ == '__main__':
    unittest.main()
