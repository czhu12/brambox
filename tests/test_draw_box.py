import unittest
import numpy as np
import cv2
import brambox.boxes as bbb


class TestDrawBox(unittest.TestCase):
    def setUp(self):
        self.img = np.zeros((50,50,3), dtype=np.uint8)
        self.res = self.img.copy()
        cv2.rectangle(self.res, (1,5), (11,20), (255,255,255), 2)

        self.anno = bbb.annotations.Annotation()
        self.anno.x_top_left = 1
        self.anno.y_top_left = 5
        self.anno.width = 10
        self.anno.height = 15

    def tearDown(self):
        pass

    def test_drawing(self):
        """ Test drawing function """
        img_b = bbb.draw_box(self.img, [self.anno], (255,255,255))
        self.assertTrue(np.array_equal(self.res, img_b))

    def test_inline_drawing(self):
        """ Test inline drawing """
        bbb.draw_box(self.img, [self.anno], (255,255,255), False, True)
        self.assertTrue(np.array_equal(self.res, self.img))


if __name__ == '__main__':
    unittest.main()
