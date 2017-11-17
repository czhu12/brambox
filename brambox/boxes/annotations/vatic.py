#
#   Copyright EAVISE
#   Author: Maarten Vandersteegen
#

from .annotation import *

__all__ = ["VaticAnnotation", "VaticParser"]


class VaticAnnotation(Annotation):
    """ VATIC tool annotation """

    def serialize(self, frame_nr=0):
        """ generate a vatic annotation string """

        object_id = self.object_id
        x_min = round(self.x_top_left)
        y_min = round(self.y_top_left)
        x_max = round(self.x_top_left + self.width)
        y_max = round(self.y_top_left + self.height)
        lost = int(self.lost)
        occluded = int(self.occluded)
        generated = 0
        class_label = self.class_label

        string = "{} {} {} {} {} {} {} {} {} {}" \
            .format(object_id,
                    x_min,
                    y_min,
                    x_max,
                    y_max,
                    frame_nr,
                    lost,
                    occluded,
                    generated,
                    class_label)

        return string

    def deserialize(self, string):
        """ parse a valitc annotation """

        elements = string.split()
        self.object_id = int(elements[0])
        self.x_top_left = float(elements[1])
        self.y_top_left = float(elements[2])
        self.width = abs(float(elements[3]) - self.x_top_left)
        self.height = abs(float(elements[4]) - self.y_top_left)
        frame_nr = int(elements[5])
        self.lost = elements[6] != '0'
        self.occluded = elements[7] != '0'
        self.class_label = elements[9].strip('\"')


class VaticParser(Parser):
    """ VATIC tool annotation parser """
    parser_type = ParserType.SINGLE_FILE
    box_type = VaticAnnotation
    extension = '.txt'

    def serialize(self, annotations):
        """ Serialize input dictionary of annotations into one string """

        result = []
        for img_id, annos in annotations.items():
            for anno in annos:
                new_anno = self.box_type.create(anno)
                result += [new_anno.serialize(img_id)]

        return "\n".join(result)

    def deserialize(self, string):
        """ Deserialize an annotation file into a dictionary of annotations """

        result = {}
        for line in string.splitlines():
            img_id = line.split()[5]
            if img_id not in result:
                result[img_id] = []

            anno = self.box_type()
            anno.deserialize(line)
            result[img_id] += [anno]

        return result
