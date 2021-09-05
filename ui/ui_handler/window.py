from ..ui_sources import Ui_Window


class Window(Ui_Window):
    def __init__(self, app):
        self.setupUi(app)
