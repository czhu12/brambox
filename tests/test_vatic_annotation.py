import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import VaticAnnotation, VaticParser


class TestCvcAnnotation(unittest.TestCase):

    def setUp(self):
        self.anno = VaticAnnotation()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if major fields: label, x, y, w, h, object_id, frame_nr are serialized """

        frame_nr = 100
        self.anno.class_label = "person"
        self.anno.object_id = 3
        self.anno.x_top_left = 13
        self.anno.y_top_left = 14
        self.anno.width = 15
        self.anno.height = 16

        string = self.anno.serialize(frame_nr)
        self.assertEqual(string, "3 13 14 28 30 100 0 0 0 person")

    def test_serialize_round(self):
        """ test if serialize rounds the x,y,w,h values correctly """

        self.anno.x_top_left = 12.8
        self.anno.y_top_left = 14.4
        self.anno.width = 14.56
        self.anno.height = 16.1

        string = self.anno.serialize()
        self.assertEqual(string, "0 13 14 27 30 0 0 0 0 x")

    def test_serialize_occluded(self):
        """ test if occluded flag is serialized """

        self.anno.occluded = 1
        string = self.anno.serialize()
        self.assertEqual(string, "0 0 0 0 0 0 0 1 0 x")

    def test_serialize_lost(self):
        """ test if lost flag is serialized """

        self.anno.lost = 1
        string = self.anno.serialize()
        self.assertEqual(string, "0 0 0 0 0 0 1 0 0 x")

    def test_deserialize(self):
        """ test if major fields: label, x, y, w, h, object_id, frame_nr are processed """

        string = "3 13 14 28 30 100 0 0 0 person"
        self.anno.deserialize(string)
        self.assertEqual(self.anno.object_id, 3)
        self.assertAlmostEqual(self.anno.x_top_left, 13)
        self.assertAlmostEqual(self.anno.y_top_left, 14)
        self.assertAlmostEqual(self.anno.width, 15)
        self.assertAlmostEqual(self.anno.height, 16)
        self.assertFalse(self.anno.lost)
        self.assertFalse(self.anno.occluded)
        self.assertEqual(self.anno.class_label, "person")

    def test_deserialize_occluded(self):
        """ test if occluded flag is processed """

        string = "0 0 0 0 0 0 0 1 0 x"
        self.anno.deserialize(string)
        self.assertTrue(self.anno.occluded)

    def test_deserialize_lost(self):
        """ test if lost flag is processed """

        string = "0 0 0 0 0 0 1 0 0 x"
        self.anno.deserialize(string)
        self.assertTrue(self.anno.lost)

vatic_string = """0 0 0 0 0 0 0 0 0 x
0 0 0 0 0 0 0 0 0 x
0 0 0 0 0 0 0 0 0 person
0 0 0 0 0 1 0 0 0 person"""

class TestVaticParser(unittest.TestCase):

    def setUp(self):
        self.parser = VaticParser()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if basic serialize works """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        obj = {}
        obj['0'] = [testanno1, testanno1, testanno2]
        obj['1'] = [testanno2]

        string = self.parser.serialize(obj)
        self.assertEqual(string, vatic_string)

    def test_deserialize(self):
        """ test if basic deserialize works """
        obj = self.parser.deserialize(vatic_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(len(obj), 2)
        self.assertEqual(len(obj['0']), 3)
        self.assertEqual(len(obj['1']), 1)
        self.assertEqual(obj['0'][0].class_label, 'x')
        self.assertEqual(obj['1'][0].class_label, 'person')
