import unittest
from brambox.boxes.detections.detection import Detection
from brambox.boxes.detections import CocoDetection, CocoParser


class TestCocoDetection(unittest.TestCase):
    def setUp(self):
        self.det = CocoDetection()

    def tearDown(self):
        pass

    def test_det_deserialize(self):
        """ test if deserialization of one detection works """
        self.det.deserialize({"image_id": "V000/I00019.png",
                              "category_id": 1,
                              "bbox": [506.547791, 216.665741, 20.434814, 39.914307],
                              "score": 0.436614},
                             None)

        self.assertAlmostEqual(self.det.x_top_left, 506.547791)
        self.assertAlmostEqual(self.det.y_top_left, 216.665741)
        self.assertAlmostEqual(self.det.width, 20.434814)
        self.assertAlmostEqual(self.det.height, 39.914307)
        self.assertAlmostEqual(self.det.confidence, 0.436614)

json_string = """[
{"image_id":"img_1", "category_id":1, "bbox":[506.547791, 216.665741, 20.434814, 39.914307], "score":0.436614},
{"image_id":"img_2", "category_id":1, "bbox":[72.131500, 207.804199, 32.555908, 63.634766], "score":0.125948},
{"image_id":"img_2", "category_id":2, "bbox":[73.131500, 207.804199, 33.555908, 64.634766], "score":0.56983}
]"""


class TestCocoParser(unittest.TestCase):
    def setUp(self):
        self.parser = CocoParser(class_label_map=None)

    def tearDown(self):
        pass

    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(json_string)
        self.assertEqual(type(obj), dict)
        self.assertEqual(type(obj['img_1']), list)
        self.assertEqual(len(obj['img_1']), 1)
        self.assertEqual(len(obj['img_2']), 2)
        self.assertEqual(obj['img_1'][0].class_label, '1')
        self.assertEqual(obj['img_1'][0].confidence, 0.436614)

    def test_parser_deserialize_class_label_map(self):
        """ test class label mapping with deserialize """
        self.parser = CocoParser(class_label_map=['person', 'car'])
        obj = self.parser.deserialize(json_string)
        self.assertEqual(obj['img_1'][0].class_label, 'person')
        self.assertEqual(obj['img_2'][1].class_label, 'car')

if __name__ == '__main__':
    unittest.main()
