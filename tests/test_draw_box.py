import unittest
import numpy as np
try:
    import cv2
except ModuleNotFoundError:
    cv2 = None
from PIL import Image, ImageDraw
import brambox.boxes as bbb


class TestDrawBoxes(unittest.TestCase):
    def setUp(self):
        self.img = np.zeros((50, 50, 3), dtype=np.uint8)
        self.res = self.img.copy()
        if cv2 is not None:
            cv2.rectangle(self.res, (1, 5), (11, 20), (255, 255, 255), 2)

        self.anno = bbb.annotations.Annotation()
        self.anno.x_top_left = 1
        self.anno.y_top_left = 5
        self.anno.width = 10
        self.anno.height = 15

    def tearDown(self):
        pass

    @unittest.skipIf(cv2 is None, "OpenCV not found, test depending on OpenCV")
    def test_basic_cv2(self):
        """ Test if cv2 drawing works """
        img = np.zeros((25, 25, 3), np.uint8)
        res = bbb.draw_boxes(img.copy(), [self.anno], (255, 0, 0))
        cv2.rectangle(img, (1, 5), (11, 20), (0, 0, 255), 3)

        self.assertTrue(np.array_equal(img, res))

    def test_basic_pil(self):
        """ Test if Pillow drawing works """
        img = Image.new('RGB', (25, 25))
        imgdraw = ImageDraw.Draw(img)
        res = bbb.draw_boxes(img.copy(), [self.anno], (255, 0, 0))
        imgdraw.line([(1, 5), (11, 5), (11, 20), (1, 20), (1, 5)], (255, 0, 0), 3)

        self.assertEqual(list(img.getdata()), list(res.getdata()))


if __name__ == '__main__':
    unittest.main()
