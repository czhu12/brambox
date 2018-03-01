import unittest
from brambox.boxes.detections.detection import Detection
from brambox.boxes.detections import PascalVocDetection, PascalVocParser

pascalvoc_string = """img1 0.9090 10.01 20.02 29.03 39.04
img2 0.1234 40.0 30.0 59.0 39.0
img2 0.75 0.00 25.00 49.00 74.00
"""


class TestPascalVocDetection(unittest.TestCase):
    def setUp(self):
        self.det = PascalVocDetection()
        self.parser = PascalVocParser(class_label='person')

    def tearDown(self):
        pass

    def test_det_deserialize(self):
        """ test if deserialization of one detection works """
        self.det.deserialize('img_id 0.9090 10.01 20.02 29.03 39.04', 'person')

        self.assertEqual(self.det.class_label, 'person')
        self.assertAlmostEqual(self.det.confidence, 0.9090)
        self.assertAlmostEqual(self.det.x_top_left, 10.01)
        self.assertAlmostEqual(self.det.y_top_left, 20.02)
        self.assertAlmostEqual(self.det.width, 20.02)
        self.assertAlmostEqual(self.det.height, 20.02)

    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(pascalvoc_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(type(obj['img1']), list)
        self.assertEqual(len(obj['img2']), 2)
        self.assertEqual(obj['img1'][0].class_label, 'person')
        self.assertAlmostEqual(obj['img1'][0].confidence, 0.9090)
        self.assertAlmostEqual(obj['img2'][1].x_top_left, 0)
        self.assertAlmostEqual(obj['img2'][0].width, 20)
        self.assertAlmostEqual(obj['img2'][1].height, 50)


if __name__ == '__main__':
    unittest.main()
