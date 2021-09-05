# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preview_editororodab.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_SetPreviewWidget(object):
    def setupUi(self, SetPreviewWidget):
        if not SetPreviewWidget.objectName():
            SetPreviewWidget.setObjectName(u"SetPreviewWidget")
        SetPreviewWidget.resize(200, 110)
        SetPreviewWidget.setStyleSheet(u"border: none;")
        self.horizontalLayout_2 = QHBoxLayout(SetPreviewWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.main = QFrame(SetPreviewWidget)
        self.main.setObjectName(u"main")
        self.main.setStyleSheet(u"QFrame{background-color: #00000000;}\n"
"QPsuhButton{background-color: #00000000;}")
        self.main.setFrameShape(QFrame.StyledPanel)
        self.main.setFrameShadow(QFrame.Raised)
        self.buttons = QFrame(self.main)
        self.buttons.setObjectName(u"buttons")
        self.buttons.setGeometry(QRect(0, 0, 201, 111))
        self.buttons.setLayoutDirection(Qt.LeftToRight)
        self.buttons.setStyleSheet(u"QFrame{background-color: #00000000;}\n"
"QPsuhButton{background-color: #00000000;}")
        self.buttons.setFrameShape(QFrame.StyledPanel)
        self.buttons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.buttons)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.deletePreview = QPushButton(self.buttons)
        self.deletePreview.setObjectName(u"deletePreview")
        self.deletePreview.setMaximumSize(QSize(24, 24))
        self.deletePreview.setCursor(QCursor(Qt.PointingHandCursor))
        self.deletePreview.setStyleSheet(u"background-color: #00000000;")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/deletePreview.png", QSize(), QIcon.Normal, QIcon.Off)
        self.deletePreview.setIcon(icon)
        self.deletePreview.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.deletePreview)

        self.change = QPushButton(self.buttons)
        self.change.setObjectName(u"change")
        self.change.setMaximumSize(QSize(24, 24))
        self.change.setCursor(QCursor(Qt.PointingHandCursor))
        self.change.setStyleSheet(u"background-color: #00000000;")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/updatePreview.png", QSize(), QIcon.Normal, QIcon.Off)
        self.change.setIcon(icon1)
        self.change.setIconSize(QSize(24, 24))

        self.horizontalLayout.addWidget(self.change)

        self.add = QPushButton(self.buttons)
        self.add.setObjectName(u"add")
        self.add.setMaximumSize(QSize(24, 24))
        self.add.setCursor(QCursor(Qt.PointingHandCursor))
        self.add.setStyleSheet(u"background-color: #00000000;")
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/addPreview.png", QSize(), QIcon.Normal, QIcon.Off)
        self.add.setIcon(icon2)
        self.add.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.add)

        self.preview = QLabel(self.main)
        self.preview.setObjectName(u"preview")
        self.preview.setGeometry(QRect(0, 0, 201, 111))
        self.preview.setStyleSheet(u"QLabel{\n"
"background-color: #5F5F5F;\n"
"}")
        self.preview.setScaledContents(True)
        self.preview.raise_()
        self.buttons.raise_()

        self.horizontalLayout_2.addWidget(self.main)


        self.retranslateUi(SetPreviewWidget)

        QMetaObject.connectSlotsByName(SetPreviewWidget)
    # setupUi

    def retranslateUi(self, SetPreviewWidget):
        SetPreviewWidget.setWindowTitle(QCoreApplication.translate("SetPreviewWidget", u"Form", None))
        self.deletePreview.setText("")
        self.change.setText("")
        self.add.setText("")
        self.preview.setText("")
    # retranslateUi

