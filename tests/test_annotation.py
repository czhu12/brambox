import unittest
from brambox.annotations.annotation import Annotation

class TestAnnotation(unittest.TestCase):

    def setUp(self):
        self.anno = Annotation()
        assert type(self.anno) == Annotation

    def tearDown(self):
        pass

    def test_rescale_int(self):
        """ Test rescaling of an annotation with an int """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 10
        self.anno.y_top_left = 10
        self.anno.width = 10
        self.anno.height = 10

        self.anno.rescale(2)
        self.assertEqual(self.anno.class_label, 'person')
        self.assertEqual(self.anno.x_top_left, 20)
        self.assertEqual(self.anno.y_top_left, 20)
        self.assertEqual(self.anno.width, 20)
        self.assertEqual(self.anno.height, 20)

    def test_rescale_float(self):
        """ Test rescaling of an annotation with a float """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 10
        self.anno.y_top_left = 10
        self.anno.width = 5
        self.anno.height = 5

        self.anno.rescale(0.5)
        self.assertEqual(self.anno.x_top_left, 5)
        self.assertEqual(self.anno.y_top_left, 5)
        self.assertEqual(self.anno.width, 2.5)
        self.assertEqual(self.anno.height, 2.5)
