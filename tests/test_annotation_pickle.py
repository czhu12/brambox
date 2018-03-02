import unittest
from brambox.boxes.annotations import PickleParser, PickleAnnotation


class TestPickleAnnotation(unittest.TestCase):
    def setUp(self):
        self.parser = PickleParser()
        self.maxDiff = None

    def tearDown(self):
        pass

    def test_parser_serialize_deserialize(self):
        """ test basic serialization/deserialization with parser """
        testanno1 = PickleAnnotation()
        testanno2 = PickleAnnotation()
        testanno2.class_label = 'person'
        obj = {'img_1': [testanno1, testanno2], 'img_2': [testanno1, testanno1, testanno1]}

        bytestream = self.parser.serialize(obj)
        obj2 = self.parser.deserialize(bytestream)

        self.assertEqual(obj, obj2)

    def test_no_keep_ignore(self):
        """ Test whether the ignore property is discarded when keep_ignore is False """
        testanno = PickleAnnotation()
        testanno.ignore = True
        obj = {'img': [testanno]}

        bytestream = self.parser.serialize(obj)
        obj2 = self.parser.deserialize(bytestream)

        self.assertFalse(obj2['img'][0].ignore)

    def test_keep_ignore(self):
        """ Test whether the ignore property is saved when keep_ignore is True """
        self.parser.keep_ignore = True

        testanno = PickleAnnotation()
        testanno.ignore = True
        obj = {'img': [testanno]}

        bytestream = self.parser.serialize(obj)
        obj2 = self.parser.deserialize(bytestream)
        self.assertTrue(obj2['img'][0].ignore)

        self.parser.keep_ignore = False


if __name__ == '__main__':
    unittest.main()
