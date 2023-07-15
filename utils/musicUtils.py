import musicpy.algorithms


# 实时预览和弦功能组
class detectElement:
    pressing = []

    def __init__(self, pressing):
        super().__init__()
        self.pressing = pressing

    def getNormalChord(self):
        return musicpy.algorithms.detect(self.pressing)

    def getChordAttr(self):
        return musicpy.algorithms.detect(self.pressing, get_chord_type=True)

