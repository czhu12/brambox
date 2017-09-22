#
#   Copyright EAVISE
#

__all__ = ["DollarAnnotation"]


class DollarAnnotation:
    """ Dollar image annotation format """

    def __init__(self):
        self.class_label = ""
        self.left = 0
        self.top = 0
        self.width = 0
        self.height = 0
        self.occluded = 0
        self.visible_left = 0
        self.visible_top = 0
        self.visible_width = 0
        self.visible_height = 0
        self.ignore = 0
        self.angle = 0

    def serialize(self):
        """ generate a dollar annotation string """
        string = "{} {} {} {} {} {} {} {} {} {} {} {}" \
            .format(self.class_label, self.left, self.top, self.width, self.height,
                    self.occluded, self.visible_left, self.visible_top, self.visible_width,
                    self.visible_height, self.ignore, self.angle)
        return string

    def deserialize(self, string):
        """ parse a dollar annotation """

        raise NotImplementedError
