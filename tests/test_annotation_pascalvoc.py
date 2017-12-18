import unittest
import xml.etree.ElementTree as ET
from brambox.boxes.annotations.annotation import Annotation
from brambox.boxes.annotations import PascalVOCAnnotation, PascalVOCParser

xml_string = """<annotation>
<object>
\t<name>horse</name>
\t<pose>Unspecified</pose>
\t<truncated>0</truncated>
\t<difficult>1</difficult>
\t<bndbox>
\t\t<xmin>100</xmin>
\t\t<ymin>200</ymin>
\t\t<xmax>300</xmax>
\t\t<ymax>400</ymax>
\t</bndbox>
</object>
<object>
\t<name>person</name>
\t<pose>Unspecified</pose>
\t<truncated>1</truncated>
\t<difficult>0</difficult>
\t<bndbox>
\t\t<xmin>1</xmin>
\t\t<ymin>2</ymin>
\t\t<xmax>3</xmax>
\t\t<ymax>4</ymax>
\t</bndbox>
</object>
</annotation>
"""

xml_single_string = """<object>
\t<name>person</name>
\t<pose>Unspecified</pose>
\t<truncated>1</truncated>
\t<difficult>0</difficult>
\t<bndbox>
\t\t<xmin>10</xmin>
\t\t<ymin>20</ymin>
\t\t<xmax>40</xmax>
\t\t<ymax>60</ymax>
\t</bndbox>
</object>
"""


class TestPascalVOCAnnotation(unittest.TestCase):
    def setUp(self):
        self.anno = PascalVOCAnnotation()
        self.parser = PascalVOCParser()

    def tearDown(self):
        pass

    def test_anno_serialize(self):
        """ test if serialization of one annotation works """
        self.anno.class_label = 'person'
        self.anno.x_top_left = 10
        self.anno.y_top_left = 20
        self.anno.width = 30
        self.anno.height = 40
        self.anno.lost = False
        self.anno.occluded = True
        self.anno.difficult = False

        string = self.anno.serialize()
        self.assertEqual(string, xml_single_string)

    def test_anno_deserialize(self):
        """ test if deserialization of one annotation works """
        self.anno.deserialize(ET.fromstring(xml_single_string))
        self.assertEqual(self.anno.x_top_left, 10)
        self.assertEqual(self.anno.y_top_left, 20)
        self.assertEqual(self.anno.width, 30)
        self.assertEqual(self.anno.height, 40)
        self.assertTrue(self.anno.occluded)
        self.assertFalse(self.anno.lost)

    def test_parser_serialize(self):
        """ test basic serialization with parser """
        testanno1 = Annotation()
        testanno1.class_label = 'horse'
        testanno1.x_top_left = 100
        testanno1.y_top_left = 200
        testanno1.width = 200
        testanno1.height = 200
        testanno1.difficult = True
        testanno2 = Annotation()
        testanno2.class_label = 'person'
        testanno2.x_top_left = 1
        testanno2.y_top_left = 2
        testanno2.width = 2
        testanno2.height = 2
        testanno2.occluded = True

        string = self.parser.serialize([testanno1, testanno2])
        self.assertEqual(string, xml_string)

    def test_parser_deserialize(self):
        """ test basic deserialization with parser """
        obj = self.parser.deserialize(xml_string)
        self.assertEqual(type(obj), list)
        self.assertEqual(len(obj), 2)
        self.assertEqual(obj[0].class_label, 'horse')
        self.assertTrue(obj[0].difficult)


if __name__ == '__main__':
    unittest.main()

