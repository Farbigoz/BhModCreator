import re

from PySide6.QtWidgets import QWidget, QScrollArea
from PySide6.QtGui import QFontMetrics, Qt, QPixmap
from PySide6.QtCore import QEvent

from .modclass import ModClass

from ..ui_sources.ui_mod_button import Ui_ModButton


class ModButton(QWidget):
    buttons = []

    def __init__(self, modClass: ModClass, method):
        self.pressed = False
        self.modClass = modClass
        self.method = method

        super().__init__()

        self.ui = Ui_ModButton()
        self.ui.setupUi(self)

        self.updateData()

        self.ui.background.installEventFilter(self)

        self.buttons.append(self)

    def updateData(self):
        self.ui.modName.setText(self.modClass.name)
        self.ui.gameVersion.setText(f"[{self.modClass.gameVersion}]")
        self.ui.modAuthor.setText("Author: " + self.modClass.author)
        if self.modClass.currentVersion:
            gameVersionColor = "#43C15F"
        else:
            gameVersionColor = "#3FAED1"
        self.ui.gameVersion.setStyleSheet(f"color: {gameVersionColor}")

        if self.modClass.installed and self.modClass.modFileExist:
            self.ui.modState.setPixmap(QPixmap(u":/icons/resources/icons/Installed.png"))
        elif self.modClass.installed:
            self.ui.modState.setPixmap(QPixmap(u":/icons/resources/icons/GhostInstalled.png"))
        else:
            self.ui.modState.setPixmap(QPixmap(u":/icons/resources/icons/NotInstalled.png"))

    def onParentResize(self):
        parent = self
        while True:
            parent = parent.parent()
            if type(parent) == QScrollArea:
                break

            if parent is None:
                return False

        versionWidth = self.ui.gameVersion.fontMetrics().boundingRect(self.ui.gameVersion.text()).width()

        elided = self.ui.modName.fontMetrics().elidedText(self.modClass.name,
                                                          Qt.ElideRight, parent.width() - 60 - versionWidth)
        self.ui.modName.setText(elided)
        self.ui.modName.setMaximumWidth(parent.width() - 100)

        elided = self.ui.modAuthor.fontMetrics().elidedText(f"Author: {self.modClass.author}",
                                                            Qt.ElideRight, parent.width() - 50)
        self.ui.modAuthor.setText(elided)

    def select(self):
        if self.pressed:
            pass
        else:
            for button in self.buttons:
                if button.pressed:
                    button.pressed = False
                    styleSheet = button.ui.background.styleSheet()
                    bgColor = re.findall(r"background-color: #FF(.+);", styleSheet)[0]
                    button.ui.background.setStyleSheet(
                        styleSheet.replace(f"#FF{bgColor}", f"#00{bgColor}").replace(f"#FE{bgColor}", f"#77{bgColor}"))

            self.pressed = True
            ss = self.ui.background.styleSheet()
            bgColor = re.findall(r"background-color: #00(.+);", ss)[0]
            self.ui.background.setStyleSheet(
                ss.replace(f"#00{bgColor}", f"#FF{bgColor}").replace(f"#77{bgColor}", f"#FE{bgColor}"))

            self.method(self.modClass)

    def remove(self):
        self.layout().removeWidget(self)
        self.setParent(None)

    def restore(self, frame):
        self.setParent(frame)
        frame.layout().addWidget(self)

    def eventFilter(self, qobject: QWidget, event):
        if event.type() == QEvent.MouseButtonPress:
            self.select()

        return False

    def __del__(self):
        if self in self.buttons:
            self.buttons.pop(self.buttons.index(self))
