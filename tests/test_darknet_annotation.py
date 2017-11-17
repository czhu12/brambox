import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import DarknetAnnotation, DarknetParser

darknet_string = """3 0.0 0.0 0.0 0.0
3 0.0 0.0 0.0 0.0
0 0.0 0.0 0.0 0.0
"""


class TestDarknetAnnotation(unittest.TestCase):

    def setUp(self):
        self.image_width = 1000
        self.image_height = 500
        self.class_label_map = ['person', 'car', 'tv', 'x']
        self.anno = DarknetAnnotation()
        self.parser = DarknetParser(image_width=self.image_width,
                                    image_height=self.image_height,
                                    class_label_map=self.class_label_map)

    def tearDown(self):
        pass

    def test_anno_serialize(self):
        """ test if serialization of one annotation works """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 35
        self.anno.y_top_left = 30
        self.anno.width = 30
        self.anno.height = 40

        string = self.anno.serialize(self.class_label_map, self.image_width, self.image_height)
        self.assertEqual(string, '0 0.05 0.1 0.03 0.08')

    def test_anno_serialize_class_label_index(self):
        """ test if class label index is correctly mapped """
        self.anno.class_label = 'tv'
        string = self.anno.serialize(self.class_label_map, self.image_width, self.image_height)
        self.assertEqual(string, '2 0.0 0.0 0.0 0.0')

    def test_anno_serialize_no_label_map(self):
        """ if class_label_map is None, the class label index must be 0 """
        string = self.anno.serialize(None, self.image_width, self.image_height)
        self.assertEqual(string, '0 0.0 0.0 0.0 0.0')

    def test_anno_deserialize(self):
        """ test if deserialization of one annotation works """
        string = '1 0.05 0.1 0.03 0.08'
        self.anno.deserialize(string, self.class_label_map, self.image_width, self.image_height)
        self.assertEqual(self.anno.class_label, 'car')
        self.assertAlmostEqual(self.anno.x_top_left, 35)
        self.assertAlmostEqual(self.anno.y_top_left, 30)
        self.assertAlmostEqual(self.anno.width, 30)
        self.assertAlmostEqual(self.anno.height, 40)
        self.assertFalse(self.anno.occluded)
        self.assertFalse(self.anno.lost)

    def test_parser_required_kwargs(self):
        """ test if constructor raises correct error when required kwargs
            are missing
        """
        self.assertRaises(TypeError, DarknetParser)
        self.assertRaises(TypeError, DarknetParser, frame_width=0)
        self.assertRaises(TypeError, DarknetParser, frame_width=0,
                          frame_height=0)
        self.assertRaises(TypeError, DarknetParser, frame_width=None,
                          frame_height=0,
                          class_label_map=[])
        self.assertRaises(TypeError, DarknetParser, frame_width=0,
                          frame_height=None,
                          class_label_map=[])

    def test_parser_serialize(self):
        """ test basic serialization with parser """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        obj = [testanno1, testanno1, testanno2]

        string = self.parser.serialize(obj)
        self.assertEqual(string, darknet_string)

    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(darknet_string)
        self.assertEqual(type(obj), list)
        self.assertEqual(len(obj), 3)
        self.assertEqual(obj[0].class_label, 'x')
        self.assertEqual(obj[2].class_label, 'person')


if __name__ == '__main__':
    unittest.main()
