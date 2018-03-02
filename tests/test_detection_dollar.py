import unittest
from brambox.boxes.detections.detection import Detection
from brambox.boxes.detections import DollarDetection, DollarParser


class TestDollarDetection(unittest.TestCase):
    def setUp(self):
        self.det = DollarDetection()

    def tearDown(self):
        pass

    def test_det_deserialize(self):
        """ test deserialize """

        self.det.deserialize("20,16.3,17.4,5.6,6.7,51.2", ['person'])

        self.assertAlmostEqual(self.det.x_top_left, 16.3)
        self.assertAlmostEqual(self.det.y_top_left, 17.4)
        self.assertAlmostEqual(self.det.width, 5.6)
        self.assertAlmostEqual(self.det.height, 6.7)
        self.assertAlmostEqual(self.det.confidence, 51.2)
        self.assertEqual(self.det.class_label, "person")


dollar_string = """20,503.75,213,20.5,50,74.8391
20,540.8,166.4,37.4857,91.4286,56.4761
21,519.034,186.602,31.6574,77.2131,51.2428
"""


class TestDollarParser(unittest.TestCase):
    def setUp(self):
        self.parser = DollarParser(class_label_map=['person'])

    def tearDown(self):
        pass

    def test_no_class_label_map(self):
        """ expect error when no class label map is provided """

        self.assertRaises(ValueError, DollarParser)

    def test_parser_deserialize(self):
        """ test parser deserialize good weather """
        obj = self.parser.deserialize(dollar_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(type(obj['19']), list)
        self.assertEqual(len(obj['19']), 2)
        self.assertEqual(len(obj['20']), 1)
        self.assertEqual(obj['19'][0].class_label, 'person')
        self.assertEqual(obj['19'][0].confidence, 74.8391)


if __name__ == '__main__':
    unittest.main()
