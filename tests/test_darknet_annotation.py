import unittest
from brambox.annotations import DarknetAnnotation


class TestDarknetAnnotation(unittest.TestCase):

    def setUp(self):
        self.frame_width = 1000
        self.frame_height = 500
        self.class_label_map = ["person", "car", "tv"]
        self.anno = DarknetAnnotation(frame_width=self.frame_width,
                                      frame_height=self.frame_height,
                                      class_label_map=self.class_label_map)

    def tearDown(self):
        pass

    def test_required_kwargs(self):
        """ test if constructor raises correct error when required kwargs
            are missing
        """
        self.assertRaises(TypeError, DarknetAnnotation)
        self.assertRaises(TypeError, DarknetAnnotation, frame_width=0)
        self.assertRaises(TypeError, DarknetAnnotation, frame_width=0,
                          frame_height=0)
        self.assertRaises(TypeError, DarknetAnnotation, frame_width=None,
                          frame_height=0,
                          class_label_map=[])
        self.assertRaises(TypeError, DarknetAnnotation, frame_width=0,
                          frame_height=None,
                          class_label_map=[])

    def test_optional_kwargs(self):
        """ frame number can also be provided to the constructor """
        self.anno = DarknetAnnotation(frame_width=self.frame_width,
                                      frame_height=self.frame_height,
                                      class_label_map=self.class_label_map,
                                      frame_number=10)
        self.assertEqual(self.anno.frame_number, 10)

    def test_serialize(self):
        """ test if major fields, label,x,y,w,h are serialized """

        # NOTE: we use numbers so that the resulting float value has
        # a short finite number of digits
        self.anno.class_label = "person"
        self.anno.x_top_left = 35
        self.anno.y_top_left = 30
        self.anno.width = 30
        self.anno.height = 40

        string = self.anno.serialize()
        self.assertEqual(string, "0 0.05 0.1 0.03 0.08")

    def test_serialize_class_label_index(self):
        """ test if class label index is correctly mapped """

        self.anno.class_label = "tv"

        string = self.anno.serialize()
        self.assertEqual(string, "2 0.0 0.0 0.0 0.0")

    def test_serialize_lost(self):
        """ lost flag is not supported in darknet, so it must
        return None
        """

        self.anno.lost = True
        self.assertIsNone(self.anno.serialize())

    def test_serialize_no_label_map(self):
        """ if class_label_map is None, the class label index must be 0 """

        self.anno = DarknetAnnotation(frame_width=self.frame_width,
                                      frame_height=self.frame_height,
                                      class_label_map=None)

        string = self.anno.serialize()
        self.assertEqual(string, "0 0.0 0.0 0.0 0.0")

    def test_deserialize(self):
        """ test if major fields, label,x,y,w,h are processed """

        string = "1 0.05 0.1 0.03 0.08"
        self.anno.deserialize(string)
        self.assertEqual(self.anno.class_label, "car")
        self.assertAlmostEqual(self.anno.x_top_left, 35)
        self.assertAlmostEqual(self.anno.y_top_left, 30)
        self.assertAlmostEqual(self.anno.width, 30)
        self.assertAlmostEqual(self.anno.height, 40)
        self.assertFalse(self.anno.occluded)
        self.assertFalse(self.anno.lost)

if __name__ == '__main__':
    unittest.main()
