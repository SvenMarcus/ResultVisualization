from typing import List


class LineTemplate:

    def __init__(self):
        self.name: str = ""
        self.xColumnTitle: str = ""
        self.yColumnTitle: str = ""
        self.metaColumnTitle: str = ""
        self.xLabel: str = ""
        self.yLabel: str = ""
        self.styles: List[str] = []