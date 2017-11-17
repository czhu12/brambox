import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import YamlAnnotation, YamlParser

yaml_string = """img_1:
  person:
  - [0, 0, 0, 0]
  x:
  - [0, 0, 0, 0]
img_2:
  x:
  - [0, 0, 0, 0]
  - [0, 0, 0, 0]
  - [0, 0, 0, 0]
"""


class TestYamlAnnotation(unittest.TestCase):

    def setUp(self):
        self.anno = YamlAnnotation()
        self.parser = YamlParser()

    def tearDown(self):
        pass

    def test_anno_serialize(self):
        """ test if serialization of one annotation works """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 10
        self.anno.y_top_left = 20
        self.anno.width = 30
        self.anno.height = 40

        key, val = self.anno.serialize()
        self.assertEqual(key, 'person')
        self.assertEqual(val, [10, 20, 30, 40])

    def test_anno_deserialize(self):
        """ test if deserialization of one annotation works """
        self.anno.deserialize([10, 20, 30, 40], 'person')
        self.assertEqual(self.anno.x_top_left, 10)
        self.assertEqual(self.anno.y_top_left, 20)
        self.assertEqual(self.anno.width, 30)
        self.assertEqual(self.anno.height, 40)
        self.assertFalse(self.anno.occluded)
        self.assertFalse(self.anno.lost)

    def test_parser_serialize(self):
        """ test basic serialization with parser """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        obj = {'img_1': [testanno1, testanno2], 'img_2': [testanno1, testanno1, testanno1]}

        string = self.parser.serialize(obj)
        self.assertEqual(string, yaml_string)

    # TODO: test if img_1 contains one anno 'x' and one anno 'person'
    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(yaml_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(type(obj['img_1']), list)
        self.assertEqual(len(obj['img_2']), 3)


if __name__ == '__main__':
    unittest.main()
