import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import KittiAnnotation, KittiParser

kitti_string = """Person 0.00 0 -10 0.00 0.00 0.00 0.00 -1 -1 -1 -1000 -1000 -1000 -10
Person 0.00 0 -10 0.00 0.00 0.00 0.00 -1 -1 -1 -1000 -1000 -1000 -10
Cyclist 0.00 0 -10 0.00 0.00 0.00 0.00 -1 -1 -1 -1000 -1000 -1000 -10
"""


class TestKittiAnnotation(unittest.TestCase):
    def setUp(self):
        self.anno = KittiAnnotation()
        self.parser = KittiParser()

    def tearDown(self):
        pass

    def test_anno_serialize(self):
        """ test if serialization of one annotation works """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 35
        self.anno.y_top_left = 30
        self.anno.width = 30
        self.anno.height = 40
        self.anno.occluded_fraction = 0.6

        string = self.anno.serialize()
        self.assertEqual(string, 'person 0.00 2 -10 35.00 30.00 65.00 70.00 -1 -1 -1 -1000 -1000 -1000 -10')

    def test_anno_deserialize(self):
        """ test if deserialization of one annotation works """
        string = 'Pedestrian 0.40 1 0.40 35.00 30.00 65.00 70.00 -1 -1 -1 123 345 456 -10'
        self.anno.deserialize(string)
        self.assertEqual(self.anno.class_label, 'Pedestrian')
        self.assertAlmostEqual(self.anno.x_top_left, 35)
        self.assertAlmostEqual(self.anno.y_top_left, 30)
        self.assertAlmostEqual(self.anno.width, 30)
        self.assertAlmostEqual(self.anno.height, 40)
        self.assertAlmostEqual(self.anno.occluded_fraction, 0.25)
        self.assertAlmostEqual(self.anno.truncated_fraction, 0.4)
        self.assertFalse(self.anno.lost)

    def test_anno_unkown_class_label(self):
        """ Test anno (de)serialisation with unkown class_label """
        self.anno.class_label = ''

        string = self.anno.serialize()
        self.assertEqual(string[0], '?')

        anno2 = KittiAnnotation.create(string)
        self.assertEqual(anno2, self.anno)

    def test_anno_occluded_state(self):
        """ Test occluded states (0,1,2) of the kitti annotations """
        string = '? 0.00 0 -10 0.00 0.00 0.00 0.00 -1 -1 -1 -1000 -1000 -1000 -10'
        anno = KittiAnnotation.create(string)
        self.assertAlmostEqual(anno.occluded_fraction, 0.0)
        self.assertEqual(string, anno.serialize())

        string = '? 0.00 1 -10 0.00 0.00 0.00 0.00 -1 -1 -1 -1000 -1000 -1000 -10'
        anno = KittiAnnotation.create(string)
        self.assertAlmostEqual(anno.occluded_fraction, 0.25)
        self.assertEqual(string, anno.serialize())

        string = '? 0.00 2 -10 0.00 0.00 0.00 0.00 -1 -1 -1 -1000 -1000 -1000 -10'
        anno = KittiAnnotation.create(string)
        self.assertAlmostEqual(anno.occluded_fraction, 0.5)
        self.assertEqual(string, anno.serialize())

    def test_parser_serialize(self):
        """ test basic serialization with parser """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno1.class_label = 'Person'
        testanno2.class_label = 'Cyclist'
        obj = [testanno1, testanno1, testanno2]

        string = self.parser.serialize(obj)
        self.assertEqual(string, kitti_string)

    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(kitti_string)
        self.assertEqual(type(obj), list)
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[0].class_label, 'Person')
        self.assertEqual(obj[2].class_label, 'Cyclist')


if __name__ == '__main__':
    unittest.main()
