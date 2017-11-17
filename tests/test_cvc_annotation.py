import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import CvcAnnotation, CvcParser


class TestCvcAnnotation(unittest.TestCase):

    def setUp(self):
        self.anno = CvcAnnotation()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if major fields, x,y,w,h are serialized """

        self.anno.x_top_left = 13
        self.anno.y_top_left = 11
        self.anno.width = 18
        self.anno.height = 16
        self.anno.object_id = 6

        string = self.anno.serialize()
        self.assertEqual(string, "22 19 18 16 1 0 0 0 0 6 0")

    def test_serialize_round(self):
        """ test if serialize rounds the x,y,w,h,object_id values correctly """

        self.anno.x_top_left = 12.8
        self.anno.y_top_left = 11.4
        self.anno.width = 18.56
        self.anno.height = 16.1

        string = self.anno.serialize()
        self.assertEqual(string, "22 19 19 16 1 0 0 0 0 0 0")

    def test_deserialize(self):
        """ test if major fields, x,y,w,h,object_id are processed """

        string = "60 50 30 40 1 0 0 0 0 3 0"
        self.anno.deserialize(string)
        self.assertAlmostEqual(self.anno.x_top_left, 45)
        self.assertAlmostEqual(self.anno.y_top_left, 30)
        self.assertAlmostEqual(self.anno.width, 30)
        self.assertAlmostEqual(self.anno.height, 40)
        self.assertEqual(self.anno.object_id, 3)


cvc_string = """0 0 0 0 1 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0
3 0 0 0 1 0 0 0 0 0 0
"""


class TestCvcParser(unittest.TestCase):

    def setUp(self):
        self.parser = CvcParser()

    def tearDown(self):
        pass

    def test_serialize(self):
        """ test if basic serialize works """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.x_top_left = 3
        obj = [testanno1, testanno1, testanno2]

        string = self.parser.serialize(obj)
        self.assertEqual(string, cvc_string)

    def test_deserialize(self):
        """ test if basic deserialize works """
        obj = self.parser.deserialize(cvc_string)
        self.assertEqual(type(obj), list)
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[2].x_top_left, 3)

if __name__ == '__main__':
    unittest.main()
