# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mod_bodyCvezZf.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ModCreator(object):
    def setupUi(self, ModCreator):
        if not ModCreator.objectName():
            ModCreator.setObjectName(u"ModCreator")
        ModCreator.resize(590, 461)
        ModCreator.setStyleSheet(u"QWidget{border: none;}\n"
"QWidget#ModCreator{background-color: #303136;}\n"
"QLabel{color: #eeeeee;}\n"
"QLineEdit{background-color: #00000000; color: #eeeeee;font: \"Roboto Medium\";}\n"
"QTextBrowser{background-color: #00000000; color: #eeeeee;font: \"Roboto Medium\";}\n"
"QTextBrowser:focus{background-color: #555F5F5F;}\n"
"QLineEdit:focus{background-color: #555F5F5F;}\n"
"QScrollBar:vertical {         \n"
"    border: none;\n"
"    background: #2B2C32;\n"
"    width: 7px;\n"
"    margin: 0 0 0 0;\n"
"    border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:vertical {\n"
"    background-color: #616161;\n"
"    min-height: 30px;\n"
"    border-radius: 7px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{\n"
"    background-color: #A1A1A1;\n"
"}\n"
"QScrollBar::handle:vertical:pressed {\n"
"    background-color: #717171;\n"
"}\n"
"QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"}\n"
"QScrollBar::add-line:vertical {\n"
"	border: none;\n"
"}\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
""
                        "	background: none;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"	background: none;\n"
"}")
        self.verticalLayout = QVBoxLayout(ModCreator)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.previews = QFrame(ModCreator)
        self.previews.setObjectName(u"previews")
        self.previews.setFrameShape(QFrame.StyledPanel)
        self.previews.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.previews)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.previews)

        self.modInfo = QFrame(ModCreator)
        self.modInfo.setObjectName(u"modInfo")
        self.modInfo.setStyleSheet(u"")
        self.modInfo.setFrameShape(QFrame.StyledPanel)
        self.modInfo.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.modInfo)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_5 = QFrame(self.modInfo)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setStyleSheet(u"")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_5)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.frame_5)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setMinimumSize(QSize(4, 0))
        self.frame_3.setMaximumSize(QSize(4, 16777215))
        self.frame_3.setStyleSheet(u"QFrame{background-color:#4E7CC1;}")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.horizontalLayout.addWidget(self.frame_3)

        self.frame_9 = QFrame(self.frame_5)
        self.frame_9.setObjectName(u"frame_9")
        self.frame_9.setStyleSheet(u"")
        self.frame_9.setFrameShape(QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_9)
        self.verticalLayout_3.setSpacing(5)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.name = QLineEdit(self.frame_9)
        self.name.setObjectName(u"name")
        font = QFont()
        font.setFamilies([u"Roboto Medium"])
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        self.name.setFont(font)
        self.name.setStyleSheet(u"")
        self.name.setClearButtonEnabled(False)

        self.verticalLayout_3.addWidget(self.name)

        self.author = QLineEdit(self.frame_9)
        self.author.setObjectName(u"author")
        font1 = QFont()
        font1.setFamilies([u"Roboto Medium"])
        font1.setPointSize(11)
        font1.setBold(False)
        font1.setItalic(False)
        self.author.setFont(font1)
        self.author.setFrame(True)
        self.author.setDragEnabled(False)
        self.author.setReadOnly(False)
        self.author.setClearButtonEnabled(False)

        self.verticalLayout_3.addWidget(self.author)

        self.gameVersion = QLineEdit(self.frame_9)
        self.gameVersion.setObjectName(u"gameVersion")
        self.gameVersion.setFont(font1)
        self.gameVersion.setClearButtonEnabled(False)

        self.verticalLayout_3.addWidget(self.gameVersion)

        self.version = QLineEdit(self.frame_9)
        self.version.setObjectName(u"version")
        self.version.setFont(font1)
        self.version.setClearButtonEnabled(False)

        self.verticalLayout_3.addWidget(self.version)

        self.tags = QLineEdit(self.frame_9)
        self.tags.setObjectName(u"tags")
        self.tags.setFont(font1)

        self.verticalLayout_3.addWidget(self.tags)


        self.horizontalLayout.addWidget(self.frame_9)


        self.verticalLayout_2.addWidget(self.frame_5, 0, Qt.AlignTop)

        self.frame_6 = QFrame(self.modInfo)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_4 = QFrame(self.frame_6)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setMinimumSize(QSize(4, 0))
        self.frame_4.setMaximumSize(QSize(4, 16777215))
        self.frame_4.setStyleSheet(u"QFrame{background-color:#4CAA4A;}")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_2.addWidget(self.frame_4)

        self.frame_10 = QFrame(self.frame_6)
        self.frame_10.setObjectName(u"frame_10")
        self.frame_10.setFrameShape(QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QFrame.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame_10)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.source = QLineEdit(self.frame_10)
        self.source.setObjectName(u"source")
        self.source.setFont(font1)

        self.verticalLayout_4.addWidget(self.source)

        self.url = QLineEdit(self.frame_10)
        self.url.setObjectName(u"url")
        self.url.setFont(font1)

        self.verticalLayout_4.addWidget(self.url)


        self.horizontalLayout_2.addWidget(self.frame_10)


        self.verticalLayout_2.addWidget(self.frame_6, 0, Qt.AlignTop)

        self.frame = QFrame(self.modInfo)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setSpacing(5)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setMinimumSize(QSize(4, 0))
        self.frame_2.setMaximumSize(QSize(4, 16777215))
        self.frame_2.setStyleSheet(u"QFrame{background-color:#ff5050;}")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_4.addWidget(self.frame_2)

        self.frame_7 = QFrame(self.frame)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setMinimumSize(QSize(0, 0))
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.modSourcesPath = QLineEdit(self.frame_7)
        self.modSourcesPath.setObjectName(u"modSourcesPath")
        self.modSourcesPath.setFont(font1)
        self.modSourcesPath.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.modSourcesPath)


        self.horizontalLayout_4.addWidget(self.frame_7)


        self.verticalLayout_2.addWidget(self.frame)

        self.descriptionFrame = QFrame(self.modInfo)
        self.descriptionFrame.setObjectName(u"descriptionFrame")
        self.descriptionFrame.setFrameShape(QFrame.StyledPanel)
        self.descriptionFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.descriptionFrame)
        self.horizontalLayout_3.setSpacing(5)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.descriptionFrame)
        self.frame_8.setObjectName(u"frame_8")
        self.frame_8.setMinimumSize(QSize(4, 0))
        self.frame_8.setMaximumSize(QSize(4, 16777215))
        self.frame_8.setStyleSheet(u"QFrame{background-color:#DE812B;}")
        self.frame_8.setFrameShape(QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QFrame.Raised)

        self.horizontalLayout_3.addWidget(self.frame_8)

        self.frame_11 = QFrame(self.descriptionFrame)
        self.frame_11.setObjectName(u"frame_11")
        self.frame_11.setFrameShape(QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QFrame.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.frame_11)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.description = QTextBrowser(self.frame_11)
        self.description.setObjectName(u"description")
        self.description.setMinimumSize(QSize(0, 150))
        self.description.setMaximumSize(QSize(16777215, 16777215))
        font2 = QFont()
        font2.setFamilies([u"Roboto Medium"])
        font2.setPointSize(10)
        font2.setBold(False)
        font2.setItalic(False)
        self.description.setFont(font2)
        self.description.setInputMethodHints(Qt.ImhMultiLine)
        self.description.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.description.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.description.setAutoFormatting(QTextEdit.AutoNone)
        self.description.setReadOnly(False)

        self.verticalLayout_5.addWidget(self.description)


        self.horizontalLayout_3.addWidget(self.frame_11)


        self.verticalLayout_2.addWidget(self.descriptionFrame)


        self.verticalLayout.addWidget(self.modInfo)


        self.retranslateUi(ModCreator)

        QMetaObject.connectSlotsByName(ModCreator)
    # setupUi

    def retranslateUi(self, ModCreator):
        ModCreator.setWindowTitle(QCoreApplication.translate("ModCreator", u"Form", None))
        self.name.setInputMask("")
        self.name.setText(QCoreApplication.translate("ModCreator", u"Brawlhalla ModCreator", None))
        self.author.setInputMask("")
        self.author.setPlaceholderText(QCoreApplication.translate("ModCreator", u"Author:", None))
        self.gameVersion.setText("")
        self.gameVersion.setPlaceholderText(QCoreApplication.translate("ModCreator", u"Game version:", None))
        self.version.setText("")
        self.version.setPlaceholderText(QCoreApplication.translate("ModCreator", u"Mod version:", None))
        self.tags.setPlaceholderText(QCoreApplication.translate("ModCreator", u"Tags:", None))
        self.source.setPlaceholderText(QCoreApplication.translate("ModCreator", u"Source:", None))
        self.url.setPlaceholderText(QCoreApplication.translate("ModCreator", u"URL:", None))
        self.modSourcesPath.setPlaceholderText(QCoreApplication.translate("ModCreator", u"Sources:", None))
    # retranslateUi

