import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import YamlAnnotation, YamlParser

yaml_string = """img_1:
  person:
  - coords: [0, 0, 0, 0]
    lost: false
    occluded: false
  x:
  - coords: [0, 0, 0, 0]
    lost: false
    occluded: false
img_2:
  x:
  - coords: [0, 0, 0, 0]
    lost: false
    occluded: false
  - coords: [0, 0, 0, 0]
    lost: false
    occluded: false
  - coords: [0, 0, 0, 0]
    lost: false
    occluded: false
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
        self.anno.lost = True
        self.anno.occluded = False

        key, val = self.anno.serialize()
        self.assertEqual(key, 'person')
        self.assertEqual(val['coords'], [10, 20, 30, 40])
        self.assertTrue(val['lost'])
        self.assertFalse(val['occluded'])

    def test_anno_deserialize(self):
        """ test if deserialization of one annotation works """
        self.anno.deserialize({'coords': [10, 20, 30, 40], 'lost': True, 'occluded': True}, 'person')
        self.assertEqual(self.anno.x_top_left, 10)
        self.assertEqual(self.anno.y_top_left, 20)
        self.assertEqual(self.anno.width, 30)
        self.assertEqual(self.anno.height, 40)
        self.assertTrue(self.anno.occluded)
        self.assertTrue(self.anno.lost)

    def test_parser_serialize(self):
        """ test basic serialization with parser """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        obj = {'img_1': [testanno1, testanno2], 'img_2': [testanno1, testanno1, testanno1]}

        string = self.parser.serialize(obj)
        self.assertEqual(string, yaml_string)

    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(yaml_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(type(obj['img_1']), list)
        self.assertEqual(len(obj['img_2']), 3)


if __name__ == '__main__':
    unittest.main()
