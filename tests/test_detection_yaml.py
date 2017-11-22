import unittest
from brambox.boxes.detections.detection import Detection
from brambox.boxes.detections import YamlDetection, YamlParser

yaml_string = """img_1:
  person:
  - coords: [0, 0, 0, 0]
    score: 90.90909
  x:
  - coords: [0, 0, 0, 0]
    score: 0.0
img_2:
  x:
  - coords: [0, 0, 0, 0]
    score: 0.0
  - coords: [0, 0, 0, 0]
    score: 0.0
  - coords: [0, 0, 0, 0]
    score: 0.0
"""


class TestYamlDetection(unittest.TestCase):
    def setUp(self):
        self.det = YamlDetection()
        self.parser = YamlParser()

    def tearDown(self):
        pass

    def test_det_serialize(self):
        """ test if serialization of one detection works """
        self.det.class_label = 'person'
        self.det.x_top_left = 10
        self.det.y_top_left = 20
        self.det.width = 30
        self.det.height = 40
        self.det.confidence = 12.34

        key, val = self.det.serialize()
        self.assertEqual(key, 'person')
        self.assertEqual(val['coords'], [10, 20, 30, 40])
        self.assertEqual(val['score'], 12.34)

    def test_det_deserialize(self):
        """ test if deserialization of one detection works """
        self.det.deserialize({'coords': [10, 20, 30, 40], 'score': 12.34}, 'person')

        self.assertEqual(self.det.x_top_left, 10)
        self.assertEqual(self.det.y_top_left, 20)
        self.assertEqual(self.det.width, 30)
        self.assertEqual(self.det.height, 40)
        self.assertEqual(self.det.confidence, 12.34)

    def test_parser_serialize(self):
        """ test basic serialization with parser """
        testdet1 = Detection()
        testdet2 = Detection()
        testdet2.class_label = 'person'
        testdet2.confidence = 90.90909
        obj = {'img_1': [testdet1, testdet2], 'img_2': [testdet1, testdet1, testdet1]}

        string = self.parser.serialize(obj)
        self.assertEqual(string, yaml_string)

    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(yaml_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(type(obj['img_1']), list)
        self.assertEqual(len(obj['img_2']), 3)
        self.assertEqual(obj['img_1'][0].class_label, 'person')
        self.assertEqual(obj['img_1'][0].confidence, 90.90909)


if __name__ == '__main__':
    unittest.main()
