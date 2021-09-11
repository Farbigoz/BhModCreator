from typing import List, Dict

from PySide6.QtWidgets import QWidget, QFileDialog, QFrame, QVBoxLayout
from PySide6.QtGui import QPaintEvent, QPixmap, QColor
from PySide6.QtCore import QEvent, Qt, QTimer

from .modclass import ModClass
from .modbutton import ModButton

from ..ui_sources.ui_mods import Ui_Mods
from ..ui_sources.ui_mod_build_actions import Ui_ModsBuildActions
from ..ui_sources.ui_mod_body import Ui_ModCreator
from ..ui_sources.ui_preview_editor import Ui_SetPreviewWidget

from ..utils.layout import AddToFrame, ClearFrame
from ..utils.textformater import TextFormatter


def SelectImageDialog():
    dlg = QFileDialog()
    dlg.setFileMode(QFileDialog.AnyFile)
    dlg.setNameFilter("Image files (*.jpg *.png)")

    if dlg.exec_():
        filenames = dlg.selectedFiles()
        if filenames:
            return filenames[0]

    return None


class SetPreview(QWidget):
    cachedPreviews = {}

    def __init__(self):
        super().__init__()
        self.ui = Ui_SetPreviewWidget()
        self.ui.setupUi(self)

        self.preview = None

        # self.updateButtons()

        self.ui.add.clicked.connect(self.addClick)
        self.ui.deletePreview.clicked.connect(self.deleteClick)
        self.ui.change.clicked.connect(self.changeClick)

        self.previewAdded = lambda path: None
        self.previewChanged = lambda path: None
        self.previewDeleted = lambda path: None

    def setPreview(self, path: str):
        if path not in self.cachedPreviews:
            pixmap = QPixmap(path)
            self.cachedPreviews[path] = pixmap
        else:
            pixmap = self.cachedPreviews[path]

        self.preview = path
        self.ui.preview.setPixmap(pixmap)

        self.updateButtons()

    def clearPreview(self):
        self.preview = None
        self.ui.preview.setPixmap(None)
        self.updateButtons()

    def updateButtons(self):
        layout: QVBoxLayout = self.ui.buttons.layout()

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
                layout.removeWidget(child.widget())

        if self.preview is None:
            AddToFrame(self.ui.buttons, self.ui.add)
        else:
            AddToFrame(self.ui.buttons, self.ui.deletePreview)
            AddToFrame(self.ui.buttons, self.ui.change)

    def setHeight(self, h: int):
        self.setMinimumHeight(h)

        self.ui.buttons.setGeometry(0, 0, self.width(), self.height())
        self.ui.preview.setGeometry(0, 0, self.width(), self.height())

    def addClick(self):
        preview = SelectImageDialog()
        if preview is not None:
            self.setPreview(preview)
            self.previewAdded(preview)

    def deleteClick(self):
        preview = self.preview
        self.clearPreview()
        self.previewDeleted(preview)

    def changeClick(self):
        preview = SelectImageDialog()
        if preview is not None:
            self.setPreview(preview)
            self.previewChanged(preview)


class Mods(QWidget):
    previewSetters: List[SetPreview] = []

    descriptionOriginalFont = None
    descriptionOriginalColor = None

    selectedModButton: ModButton = None
    modsButtons: List[ModButton] = []
    modsSources: Dict[str, ModClass] = {}

    currentGameVersion = ""

    def __init__(self, saveMethod, installMethod, uninstallMethod, deleteMethod, buildMethod, createMethod,
                 reloadMethod, openFolderMethod):
        super().__init__()

        self.ui = Ui_Mods()
        self.ui.setupUi(self)

        bodyWidget = QWidget()
        self.body = Ui_ModCreator()
        self.body.setupUi(bodyWidget)
        self.ui.scrollBody.setWidget(bodyWidget)

        actionsWidget = QWidget()
        self.actions = Ui_ModsBuildActions()
        self.actions.setupUi(actionsWidget)

        self.actions.uninstall.setParent(None)

        self.ui.createModFrame.setMaximumHeight(30)
        self.ui.modsBuildActions.setMaximumHeight(95)
        self.ui.modsBuildActions.setMinimumHeight(95)
        AddToFrame(self.ui.modsBuildActions, actionsWidget)

        # Filling previews grid
        for r in range(2):
            for c in range(3):
                previewSetter = SetPreview()
                previewSetter.previewAdded = self.previewSelected
                previewSetter.previewChanged = self.previewSelected
                previewSetter.previewDeleted = self.previewSelected
                previewSetter.setParent(self.body.previews)
                self.body.previews.layout().addWidget(previewSetter, r, c)
                self.previewSetters.append(previewSetter)

        self.body.description.textChanged.connect(self.descriptionChanged)
        self.descriptionOriginalFont = self.body.description.currentFont()
        self.descriptionOriginalColor = self.body.description.textColor()
        self.body.description.installEventFilter(self)

        self.body.author.installEventFilter(self)
        self.body.gameVersion.installEventFilter(self)
        self.body.version.installEventFilter(self)
        self.body.tags.installEventFilter(self)
        self.ui.modBody.installEventFilter(self)

        modsListFrame = QFrame()
        layout = QVBoxLayout(modsListFrame)
        layout.setSpacing(0)
        layout.setContentsMargins(2, 5, 2, 5)
        self.modsList = QFrame()
        self.modsList.setMaximumWidth(self.ui.modsList.maximumWidth())
        layout2 = QVBoxLayout(self.modsList)
        layout2.setSpacing(1)
        layout2.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.modsList, 0, Qt.AlignTop)
        self.ui.scrollModsList.setWidget(modsListFrame)

        self.resizeEvent = self.onResize
        self.origScrollModsListResizeEvent = self.ui.scrollModsList.resizeEvent
        self.ui.scrollModsList.resizeEvent = self.onModsListResize

        self.saveTimer = QTimer()
        self.saveTimer.start(3000)  # Save every 5 seconds

        self.saveTimer.timeout.connect(saveMethod)
        self.actions.install.clicked.connect(installMethod)
        self.actions.uninstall.clicked.connect(uninstallMethod)
        self.actions.deleteMod.clicked.connect(deleteMethod)
        self.actions.build.clicked.connect(buildMethod)
        self.ui.createMod.clicked.connect(createMethod)
        self.ui.reloadModsList.clicked.connect(reloadMethod)
        self.ui.openModsFolderButton.clicked.connect(openFolderMethod)

        self.ui.searchArea.textChanged.connect(self.searchEvent)

        self.oldSize = (0, 0)

    def onResize(self, event):
        size = self.ui.modBody.size()
        if size == self.oldSize:
            return
        else:
            self.oldSize = size

        previewsWidth = self.body.previews.width()
        previewWidth = (previewsWidth - self.body.previews.layout().spacing() * 2) // 3
        previewHeight = int(previewWidth * 0.5625)

        for previewSetter in self.previewSetters:
            previewSetter.setHeight(previewHeight)

    def eventFilter(self, qobject, event):
        if self.selectedModButton is not None:
            if qobject == self.body.author:
                if event.type() == QEvent.Type.FocusIn:
                    self.body.author.setText(self.selectedModButton.modClass.author or " ")
                elif event.type() == QEvent.Type.FocusOut:
                    self.updateAuthor()

            elif qobject == self.body.gameVersion:
                if event.type() == QEvent.Type.FocusIn:
                    self.body.gameVersion.setText(self.selectedModButton.modClass.gameVersion or " ")
                elif event.type() == QEvent.Type.FocusOut:
                    self.updateGameVersion()

            elif qobject == self.body.version:
                if event.type() == QEvent.Type.FocusIn:
                    self.body.version.setText(self.selectedModButton.modClass.version or " ")
                elif event.type() == QEvent.Type.FocusOut:
                    self.updateVersion()

            elif qobject == self.body.tags:
                if event.type() == QEvent.Type.FocusIn:
                    self.body.tags.setText(", ".join(self.selectedModButton.modClass.tags) or " ")
                elif event.type() == QEvent.Type.FocusOut:
                    self.updateTags()

            elif qobject == self.body.description:
                if event.type() == QEvent.Type.FocusIn:
                    self.body.description.setPlainText(self.selectedModButton.modClass.description)
                elif event.type() == QEvent.Type.FocusOut:
                    self.updateDescription()

        if isinstance(event, QPaintEvent):
            self.onResize(event)

        return False

    def updateButtons(self):
        layout = self.actions.topButtons.layout()
        modSource = self.selectedModButton.modClass

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)
                layout.removeWidget(child.widget())

        if modSource.installed:
            AddToFrame(self.actions.topButtons, self.actions.uninstall)
        elif modSource.modFileExist:
            AddToFrame(self.actions.topButtons, self.actions.install)

        AddToFrame(self.actions.topButtons, self.actions.deleteMod)

    def onModsListResize(self, event):
        for n in range(self.modsList.layout().count()):
            w = self.modsList.layout().takeAt(0).widget()
            w.onParentResize()
            self.modsList.layout().addWidget(w)

        self.origScrollModsListResizeEvent(event)

    def searchEvent(self, text):
        if not text:
            displayModButtons = self.modsButtons

        else:
            text = text.casefold()

            if len(text.split(" ")) == 1:
                text = f" {text}"

            displayModButtons = [
                modButton
                for modButton in self.modsButtons
                if any([
                    text in f" {modButton.modClass.name.lower()}",
                    text in f" {modButton.modClass.author.lower()}",
                    modButton.modClass.gameVersion.startswith(text.strip()),
                    any([tag.casefold().lower().startswith(text.strip()) for tag in modButton.modClass.tags])
                ])
            ]

        for modButton in self.modsButtons:
            modButton.remove()

        for modButton in displayModButtons:
            modButton.restore(self.modsList)

    # Changed
    def nameChanged(self, text):
        if self.selectedModButton is not None:
            self.selectedModButton.modClass.name = text.strip()
            self.selectedModButton.updateData()

    def authorChanged(self, text):
        if self.selectedModButton is not None:
            self.selectedModButton.modClass.author = text.strip()
            self.selectedModButton.updateData()

    def gameVersionChanged(self, text):
        if self.selectedModButton is not None:
            gameVersion = text.strip()
            self.selectedModButton.modClass.gameVersion = gameVersion
            if gameVersion == self.currentGameVersion:
                self.selectedModButton.modClass.currentVersion = True
            else:
                self.selectedModButton.modClass.currentVersion = False
            self.selectedModButton.updateData()

    def modVersionChanged(self, text):
        if self.selectedModButton is not None:
            self.selectedModButton.modClass.version = text.strip()

    def tagsChanged(self, text):
        if self.selectedModButton is not None:
            self.selectedModButton.modClass.tags = text.strip().split(", ")

    def descriptionChanged(self):
        self.body.descriptionFrame.setMinimumHeight(self.body.description.document().size().height() +
                                                    self.body.description.minimumHeight())

        if self.body.description.currentFont() != self.descriptionOriginalFont:
            self.body.description.setCurrentFont(self.descriptionOriginalFont)

        if self.body.description.textColor() != self.descriptionOriginalColor:
            self.descriptionOriginalColor = QColor("#eeeeee")
            self.body.description.setTextColor(self.descriptionOriginalColor)

        if self.selectedModButton is not None:
            self.selectedModButton.modClass.description = self.body.description.toPlainText()

    def previewSelected(self, previewPath):
        previews = []
        for previewSetter in self.previewSetters:
            preview = previewSetter.preview
            if preview:
                previews.append(preview)

        if self.selectedModButton is not None:
            self.selectedModButton.modClass.previewsPaths = previews

    # Update ui
    def updateName(self):
        try:
            self.body.name.textChanged.disconnect()
        except RuntimeError:
            pass
        self.body.name.setText(self.selectedModButton.modClass.name)
        self.body.name.textChanged.connect(self.nameChanged)

    def updateAuthor(self):
        try:
            self.body.author.textChanged.disconnect()
        except RuntimeError:
            pass
        self.body.author.setText(f"{self.body.author.placeholderText()} {self.selectedModButton.modClass.author}")
        self.body.author.textChanged.connect(self.authorChanged)

    def updateGameVersion(self):
        try:
            self.body.gameVersion.textChanged.disconnect()
        except RuntimeError:
            pass
        self.body.gameVersion.setText(f"{self.body.gameVersion.placeholderText()} "
                                      f"{self.selectedModButton.modClass.gameVersion}")
        self.body.gameVersion.textChanged.connect(self.gameVersionChanged)

    def updateVersion(self):
        try:
            self.body.version.textChanged.disconnect()
        except RuntimeError:
            pass
        self.body.version.setText(f"{self.body.version.placeholderText()} {self.selectedModButton.modClass.version}")
        self.body.version.textChanged.connect(self.modVersionChanged)

    def updateTags(self):
        try:
            self.body.tags.textChanged.disconnect()
        except RuntimeError:
            pass
        self.body.tags.setText(f"{self.body.tags.placeholderText()} {', '.join(self.selectedModButton.modClass.tags)}")
        self.body.tags.textChanged.connect(self.tagsChanged)

    def updateModSourcesPath(self):
        self.body.modSourcesPath.setText(f"{self.body.modSourcesPath.placeholderText()} "
                                         f"{self.selectedModButton.modClass.modSourcesPath}")

    def updateDescription(self):
        try:
            self.body.description.textChanged.disconnect()
        except RuntimeError:
            pass
        self.body.description.setText(TextFormatter.format(self.selectedModButton.modClass.description))
        self.body.descriptionFrame.setMinimumHeight(self.body.description.document().size().height() +
                                                    self.body.description.minimumHeight())
        self.body.description.textChanged.connect(self.descriptionChanged)

    def updatePreviews(self):
        for n, previewSetter in enumerate(self.previewSetters):
            if len(self.selectedModButton.modClass.previewsPaths) >= n + 1:
                preview = self.selectedModButton.modClass.previewsPaths[n]
                previewSetter.setPreview(preview)
            else:
                previewSetter.clearPreview()

    def updateAll(self):
        if self.selectedModButton is not None:
            self.updateName()
            self.updateAuthor()
            self.updateGameVersion()
            self.updateVersion()
            self.updateTags()
            self.updateDescription()
            self.updatePreviews()
            self.updateModSourcesPath()

            for modButton in self.modsButtons:
                modButton.updateData()

            self.updateButtons()

    # Actions
    def selectMod(self, modClass: ModClass):
        for modButton in self.modsButtons:
            if modButton.modClass == modClass:
                self.selectedModButton = modButton

        self.updateAll()

    def addModButton(self, modClass: ModClass):
        modButton = ModButton(modClass=modClass,
                              method=self.selectMod)
        self.modsButtons.append(modButton)
        self.modsList.layout().addWidget(modButton)

        if not self.selectedModButton:
            modButton.select()
            self.saveTimer.start(3000)

    def addMod(self,
               gameVersion: str,
               name: str,
               author: str,
               version: str,
               description: str,
               tags: List[str],
               previewsPaths: List[str],
               hash: str,
               platform: str,
               #installed: bool,
               currentVersion: bool,
               #modFileExist: bool
               modSourcesPath: str):

        modSources = ModClass(gameVersion=gameVersion,
                              name=name,
                              author=author,
                              version=version,
                              description=description,
                              tags=tags,
                              previewsPaths=previewsPaths,
                              hash=hash,
                              platform=platform,
                              installed=False,
                              currentVersion=currentVersion,
                              modFileExist=False,
                              modSourcesPath=modSourcesPath)

        self.modsSources[hash] = modSources
        self.addModButton(modSources)

    def updateMod(self,
                  hash: str,
                  installed: bool,
                  modFileExist: bool):

        modSources = self.modsSources.get(hash, None)

        if modSources is not None:
            modSources.installed = installed
            modSources.modFileExist = modFileExist

    def removeAllMods(self):
        ClearFrame(self.modsList)

        self.selectedModButton = None
        for modButton in self.modsButtons:
            modButton.__del__()
            del modButton
        self.modsButtons.clear()

        for modSource in self.modsSources.values():
            del modSource
        self.modsSources.clear()

        self.saveTimer.stop()
