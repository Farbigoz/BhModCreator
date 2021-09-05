# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mod_build_actionsshJmPh.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_ModsBuildActions(object):
    def setupUi(self, ModsBuildActions):
        if not ModsBuildActions.objectName():
            ModsBuildActions.setObjectName(u"ModsBuildActions")
        ModsBuildActions.resize(505, 95)
        ModsBuildActions.setMinimumSize(QSize(0, 85))
        ModsBuildActions.setMaximumSize(QSize(16777215, 95))
        ModsBuildActions.setStyleSheet(u"QWidget {\n"
"border: none;\n"
"}\n"
"QPushButton{\n"
"color: #eeeeee;\n"
"}")
        self.horizontalLayout_2 = QHBoxLayout(ModsBuildActions)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.buttons = QFrame(ModsBuildActions)
        self.buttons.setObjectName(u"buttons")
        self.buttons.setMaximumSize(QSize(16777215, 95))
        self.buttons.setStyleSheet(u"QPushButton{\n"
"border-radius: 4;\n"
"font: 500 11pt \"Roboto Medium\";\n"
"}")
        self.buttons.setFrameShape(QFrame.StyledPanel)
        self.buttons.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.buttons)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.topButtons = QFrame(self.buttons)
        self.topButtons.setObjectName(u"topButtons")
        self.topButtons.setMaximumSize(QSize(16777215, 40))
        self.topButtons.setFrameShape(QFrame.StyledPanel)
        self.topButtons.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.topButtons)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.install = QPushButton(self.topButtons)
        self.install.setObjectName(u"install")
        self.install.setMinimumSize(QSize(0, 40))
        self.install.setMaximumSize(QSize(16777215, 40))
        font = QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        self.install.setFont(font)
        self.install.setCursor(QCursor(Qt.PointingHandCursor))
        self.install.setStyleSheet(u"QPushButton{\n"
"background-color: #43C15F;\n"
"}")
        icon = QIcon()
        icon.addFile(u":/icons/resources/icons/Install.png", QSize(), QIcon.Normal, QIcon.Off)
        self.install.setIcon(icon)
        self.install.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.install)

        self.uninstall = QPushButton(self.topButtons)
        self.uninstall.setObjectName(u"uninstall")
        self.uninstall.setMinimumSize(QSize(0, 40))
        self.uninstall.setMaximumSize(QSize(16777215, 40))
        self.uninstall.setFont(font)
        self.uninstall.setCursor(QCursor(Qt.PointingHandCursor))
        self.uninstall.setStyleSheet(u"QPushButton{\n"
"background-color: #00B9A3;\n"
"}")
        icon1 = QIcon()
        icon1.addFile(u":/icons/resources/icons/Uninstall.png", QSize(), QIcon.Normal, QIcon.Off)
        self.uninstall.setIcon(icon1)
        self.uninstall.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.uninstall)

        self.deleteMod = QPushButton(self.topButtons)
        self.deleteMod.setObjectName(u"deleteMod")
        self.deleteMod.setMinimumSize(QSize(0, 40))
        self.deleteMod.setMaximumSize(QSize(16777215, 40))
        self.deleteMod.setFont(font)
        self.deleteMod.setCursor(QCursor(Qt.PointingHandCursor))
        self.deleteMod.setStyleSheet(u"QPushButton{\n"
"background-color: #FF5050;\n"
"}")
        icon2 = QIcon()
        icon2.addFile(u":/icons/resources/icons/Delete.png", QSize(), QIcon.Normal, QIcon.Off)
        self.deleteMod.setIcon(icon2)
        self.deleteMod.setIconSize(QSize(22, 22))

        self.horizontalLayout.addWidget(self.deleteMod)


        self.verticalLayout_2.addWidget(self.topButtons)

        self.build = QPushButton(self.buttons)
        self.build.setObjectName(u"build")
        self.build.setMinimumSize(QSize(0, 40))
        self.build.setMaximumSize(QSize(16777215, 40))
        self.build.setFont(font)
        self.build.setCursor(QCursor(Qt.PointingHandCursor))
        self.build.setStyleSheet(u"QPushButton{\n"
"background-color: #833DBB;\n"
"}")
        icon3 = QIcon()
        icon3.addFile(u":/icons/resources/icons/hammer.png", QSize(), QIcon.Normal, QIcon.Off)
        self.build.setIcon(icon3)
        self.build.setIconSize(QSize(22, 22))

        self.verticalLayout_2.addWidget(self.build)


        self.horizontalLayout_2.addWidget(self.buttons)


        self.retranslateUi(ModsBuildActions)

        QMetaObject.connectSlotsByName(ModsBuildActions)
    # setupUi

    def retranslateUi(self, ModsBuildActions):
        ModsBuildActions.setWindowTitle(QCoreApplication.translate("ModsBuildActions", u"Form", None))
        self.install.setText(QCoreApplication.translate("ModsBuildActions", u"Install", None))
        self.uninstall.setText(QCoreApplication.translate("ModsBuildActions", u"Uninstall", None))
        self.deleteMod.setText(QCoreApplication.translate("ModsBuildActions", u"Delete", None))
        self.build.setText(QCoreApplication.translate("ModsBuildActions", u"Build", None))
    # retranslateUi

