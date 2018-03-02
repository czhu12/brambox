import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import DollarAnnotation, DollarParser

dollar_string = """? 0 0 0 0 0 0 0 0 0 0 0
? 0 0 0 0 0 0 0 0 0 0 0
person 0 0 0 0 0 0 0 0 0 0 0
"""

dollar_string_comment = """% comment line
""" + dollar_string


class TestDollarAnnotation(unittest.TestCase):
    def setUp(self):
        self.anno = DollarAnnotation()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if major fields, label,x,y,w,h are serialized """

        self.anno.class_label = "person"
        self.anno.x_top_left = 13
        self.anno.y_top_left = 14
        self.anno.width = 15
        self.anno.height = 16

        string = self.anno.serialize()
        self.assertEqual(string, "person 13 14 15 16 0 0 0 0 0 0 0")

    def test_serialize_round(self):
        """ test if serialize rounds the x,y,w,h values correctly """

        self.anno.class_label = "person"
        self.anno.x_top_left = 12.8
        self.anno.y_top_left = 14.4
        self.anno.width = 14.56
        self.anno.height = 16.1

        string = self.anno.serialize()
        self.assertEqual(string, "person 13 14 15 16 0 0 0 0 0 0 0")

    def test_serialize_occluded(self):
        """ test if occluded flag is serialized """

        self.anno.occluded = 1
        string = self.anno.serialize()
        self.assertEqual(string, "? 0 0 0 0 1 0 0 0 0 0 0")

    def test_serialize_lost(self):
        """ test if lost flag is serialized """

        self.anno.lost = 1
        string = self.anno.serialize()
        self.assertEqual(string, "? 0 0 0 0 0 0 0 0 0 1 0")

    def test_deserialize(self):
        """ test if major fields, label,x,y,w,h are processed """

        string = "person 10 20 30 40 0 0 0 0 0 0 0"
        self.anno.deserialize(string, None)
        self.assertEqual(self.anno.class_label, "person")
        self.assertAlmostEqual(self.anno.x_top_left, 10)
        self.assertAlmostEqual(self.anno.y_top_left, 20)
        self.assertAlmostEqual(self.anno.width, 30)
        self.assertAlmostEqual(self.anno.height, 40)
        self.assertFalse(self.anno.occluded)
        self.assertFalse(self.anno.lost)

    def test_deserialize_occluded(self):
        """ test if occluded flag is processed """

        string = "person 0 0 0 0 1 0 0 0 0 0 0"
        self.anno.deserialize(string, None)
        self.assertTrue(self.anno.occluded)

    def test_deserialize_lost(self):
        """ test if lost flag is processed """

        string = "person 0 0 0 0 0 0 0 0 0 1 0"
        self.anno.deserialize(string, None)
        self.assertTrue(self.anno.lost)

    def test_deserialize_occlusion_tag_map(self):
        """ test if occluded flag is processed """

        string = "person 0 0 0 0 2 0 0 0 0 0 0"
        self.anno.deserialize(string, [0.0, 0.25, 0.75])
        self.assertTrue(self.anno.occluded)
        self.assertAlmostEqual(self.anno.occluded_fraction, 0.75)


class TestDollarParser(unittest.TestCase):
    def setUp(self):
        self.parser = DollarParser()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if basic serialize works """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        obj = [testanno1, testanno1, testanno2]

        string = self.parser.serialize(obj)
        self.assertEqual(string, dollar_string)

    def test_deserialize(self):
        """ test if basic deserialize works, make sure it ignores comment lines """
        obj = self.parser.deserialize(dollar_string_comment)
        self.assertEqual(type(obj), list)
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[0].class_label, '')
        self.assertEqual(obj[2].class_label, 'person')


if __name__ == '__main__':
    unittest.main()
