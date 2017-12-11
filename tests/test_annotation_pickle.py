import unittest
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import PickleParser


class TestPickleAnnotation(unittest.TestCase):
    def setUp(self):
        self.parser = PickleParser()

    def tearDown(self):
        pass

    def test_parser_serialize_deserialize(self):
        """ test basic serialization/deserialization with parser """
        testanno1 = Annotation()
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        obj = {'img_1': [testanno1, testanno2], 'img_2': [testanno1, testanno1, testanno1]}

        bytestream = self.parser.serialize(obj)
        obj2 = self.parser.deserialize(bytestream)

        self.assertEqual(obj, obj2)


if __name__ == '__main__':
    unittest.main()
