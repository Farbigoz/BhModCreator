import os
import sys
import threading
import webbrowser

from typing import List

import core
from core import NotificationType, Notification, Environment, CORE_VERSION

from PySide6.QtGui import QIcon, QFontDatabase
from PySide6.QtCore import QTimer, QSize, Signal
from PySide6.QtWidgets import QApplication, QMainWindow

from ui.ui_handler.window import Window
from ui.ui_handler.loading import Loading
from ui.ui_handler.header import HeaderFrame
from ui.ui_handler.mods import Mods
from ui.ui_handler.progressdialog import ProgressDialog
from ui.ui_handler.buttonsdialog import ButtonsDialog
from ui.ui_handler.acceptdialog import AcceptDialog
from ui.ui_handler.inputdialog import InputDialog

from ui.utils.layout import AddToFrame, ClearFrame
from ui.utils.textformater import TextFormatter
from ui.utils.version import GetLatest, GITHUB, REPO, VERSION, GIT_VERSION, PRERELEASE, GAMEBANANA


SUPPORT_URL = "https://www.patreon.com/bhmodloader"

PROGRAM_NAME = "Brawlhalla ModCreator"


def InitWindowSetText(text):
    if getattr(sys, "frozen", False):
        try:
            import pyi_splash
            pyi_splash.update_text(text)
        except:
            pass


def InitWindowClose():
    if getattr(sys, "frozen", False):
        try:
            import pyi_splash
            pyi_splash.update_text("application")
            pyi_splash.close()
        except:
            pass


class ModCreator(QMainWindow):
    _loaded = False

    modsPath = os.path.join(os.getcwd(), "Mods")
    modsSourcesPath = os.path.join(os.getcwd(), "Mods Sources")

    errors: List[Notification] = []

    app = False

    def __init__(self):
        super().__init__()
        self.ui = Window(self)

        self.__class__.app = self

        self.setWindowTitle(PROGRAM_NAME)
        self.setWindowIcon(QIcon(':/icons/resources/icons/App.ico'))

        InitWindowSetText("core libs")
        self.controller = core.Controller()
        self.controller.setModsPath(self.modsPath)
        self.controller.setModsSourcesPath(self.modsSourcesPath)
        self.controller.reloadMods()
        self.controller.reloadModsSources()
        InitWindowClose()

        self.controller.getModsSourcesData()
        self.controller.getModsData()

        self.loading = Loading()
        self.header = HeaderFrame(githubMethod=lambda: webbrowser.open(f"{GITHUB}/{REPO}"),
                                  supportMethod=lambda: webbrowser.open(SUPPORT_URL),
                                  infoMethod=self.showInformation)
        self.mods = Mods(saveMethod=self.saveModSource,
                         installMethod=self.installMod,
                         uninstallMethod=self.uninstallMod,
                         deleteMethod=self.deleteMod,
                         buildMethod=self.buildMod,
                         createMethod=self.createMod,
                         reloadMethod=self.reloadMods,
                         openFolderMethod=self.openModsSourcesFolder)
        self.progressDialog = ProgressDialog(self)
        self.acceptDialog = AcceptDialog(self)  # TODO: Remake to buttons dialog
        self.inputDialog = InputDialog(self)
        self.buttonsDialog = ButtonsDialog(self)

        self.setLoadingScreen()

        # Get core events
        self.controllerGetterTimer = QTimer()
        self.controllerGetterTimer.timeout.connect(self.controllerHandler)
        self.controllerGetterTimer.start(10)

        self.setMinimumSize(QSize(850, 550))

        self.versionSignal.connect(self.newVersion)
        threading.Thread(target=self.checkNewVersion).start()

    def resizeEvent(self, event):
        self.progressDialog.onResize()
        self.acceptDialog.onResize()
        self.inputDialog.onResize()
        self.buttonsDialog.onResize()
        super().resizeEvent(event)

    def controllerHandler(self):
        data = self.controller.getData()
        if data is None:
            return

        cmd = data[0]

        if cmd == Environment.Notification:
            notification: core.notifications.Notification = data[1]
            ntype = notification.notificationType

            # print(notification)

            if ntype == NotificationType.LoadingModSource:
                modPath = notification.args[0]
                try:
                    self.loading.setText(f"Loading mod '{modPath}'")
                except RuntimeError:
                    pass

            elif ntype in [NotificationType.ModElementsCount, NotificationType.CompileElementsCount]:
                modHash, count = notification.args
                self.progressDialog.setMaximum(count)

            # Check conflicts
            elif ntype == NotificationType.ModConflictSearchInSwf:
                modHash, swfName = notification.args
                self.progressDialog.setContent(f"Searching in: {swfName}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.ModConflictNotFound:
                modHash, = notification.args
                self.progressDialog.setValue(0)
                self.controller.installMod(modHash)
            elif ntype == NotificationType.ModConflict:
                modHash, modConflictHashes = notification.args
                self.acceptDialog.setTitle("Conflict mods!")
                content = "Mods:"

                for modConflictHash in modConflictHashes:
                    if modConflictHash in self.mods.modsSources:
                        mod = self.mods.modsSources[modConflictHash]
                        content += f"\n- {mod.name}"

                    else:
                        content += f"\n- UNKNOWN MOD: {modConflictHash}"
                        print("ERROR Один из установленных модов не найден в модлодере!")

                self.acceptDialog.setContent(content)
                self.acceptDialog.setAccept(lambda: [self.acceptDialog.hide(), self.controller.installMod(modHash)])
                self.acceptDialog.setCancel(self.acceptDialog.hide)

                self.progressDialog.hide()
                self.acceptDialog.show()

            # Installing
            elif ntype == NotificationType.InstallingModSwf:
                modHash, swfName = notification.args
                self.progressDialog.setContent(f"Open game file: {swfName}")
            elif ntype == NotificationType.InstallingModSwfSprite:
                modHash, sprite = notification.args
                self.progressDialog.setContent(f"Installing sprite: {sprite}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.InstallingModSwfSound:
                modHash, sound = notification.args
                self.progressDialog.setContent(f"Installing sound: {sound}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.InstallingModFile:
                modHash, fileName = notification.args
                self.progressDialog.setContent(f"Installing file: {fileName}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.InstallingModFileCache:
                modHash, fileName = notification.args
                self.progressDialog.setContent(fileName)
                self.progressDialog.addValue()
            elif ntype == NotificationType.InstallingModFinished:
                modHash = notification.args[0]
                modClass = self.mods.modsSources[modHash]
                modClass.installed = True
                self.mods.updateAll()
                # self.mods.selectedModButton.updateData()
                self.progressDialog.hide()

                self.showErrorNotifications()

            # Uninstalling
            elif ntype == NotificationType.UninstallingModSwf:
                modHash, swfName = notification.args
                self.progressDialog.setContent(swfName)
            elif ntype == NotificationType.UninstallingModSwfSprite:
                modHash, sprite = notification.args
                self.progressDialog.setContent(sprite)
                self.progressDialog.addValue()
            elif ntype == NotificationType.UninstallingModSwfSound:
                modHash, sprite = notification.args
                self.progressDialog.setContent(sprite)
                self.progressDialog.addValue()
            elif ntype == NotificationType.UninstallingModFile:
                modHash, fileName = notification.args
                self.progressDialog.setContent(fileName)
                self.progressDialog.addValue()
            elif ntype == NotificationType.UninstallingModFinished:
                modHash = notification.args[0]
                modClass = self.mods.modsSources[modHash]
                modClass.installed = False
                self.mods.updateAll()
                # self.mods.selectedModButton.updateData()

                self.progressDialog.hide()

                self.showErrorNotifications()

            # Compile
            elif ntype == NotificationType.CompileModSourcesImportActionScripts:
                modHash, actionScript = notification.args
                self.progressDialog.setContent(f"Assembly ActionScript: {actionScript}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.CompileModSourcesImportFile:
                modHash, file = notification.args
                self.progressDialog.setContent(f"Assembly file: {file}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.CompileModSourcesImportSound:
                modHash, sound = notification.args
                self.progressDialog.setContent(f"Assembly sound: {sound}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.CompileModSourcesImportSprite:
                modHash, sprite = notification.args
                self.progressDialog.setContent(f"Assembly sprite: {sprite}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.CompileModSourcesImportPreview:
                modHash, preview = notification.args
                self.progressDialog.setContent(f"Assembly preview: {preview}")
                self.progressDialog.addValue()
            elif ntype == NotificationType.CompileModSourcesFinished:
                modHash = notification.args[0]
                # modsSources = self.mods.modsSources[modHash]
                # self.mods.updateAll()
                # self.mods.selectedModButton.updateData()
                self.showErrorNotifications()

                self.controller.reloadMods()
                self.controller.getModsData()

                self.progressDialog.hide()

            # Errors
            elif ntype in [NotificationType.CompileModSourcesSpriteHasNoSymbolclass,  # Compiler
                           NotificationType.CompileModSourcesSpriteEmpty,
                           NotificationType.CompileModSourcesSpriteNotFoundInFolder,
                           NotificationType.CompileModSourcesUnsupportedCategory,
                           NotificationType.CompileModSourcesUnknownFile,
                           NotificationType.CompileModSourcesSaveError,
                           NotificationType.LoadingModIsEmpty,  # Loader
                           NotificationType.InstallingModNotFoundFileElement,  # Installer
                           NotificationType.InstallingModNotFoundGameSwf,
                           NotificationType.InstallingModSwfScriptError,
                           NotificationType.InstallingModSwfSoundSymbolclassNotExist,
                           NotificationType.InstallingModSoundNotExist,
                           NotificationType.InstallingModSwfSpriteSymbolclassNotExist,
                           NotificationType.InstallingModSpriteNotExist,
                           NotificationType.UninstallingModSwfOriginalElementNotFound,  # Uninstaller
                           NotificationType.UninstallingModSwfElementNotFound]:
                self.errors.append(notification)

        elif cmd == Environment.GetModsSourcesData:
            for modSourcesData in data[1]:
                self.mods.addMod(gameVersion=modSourcesData.get("gameVersion", ""),
                                 name=modSourcesData.get("name", ""),
                                 author=modSourcesData.get("author", ""),
                                 version=modSourcesData.get("version", ""),
                                 description=modSourcesData.get("description", ""),
                                 tags=modSourcesData.get("tags", []),
                                 previewsPaths=modSourcesData.get("previewsPaths", []),
                                 hash=modSourcesData.get("hash", ""),
                                 platform=modSourcesData.get("platform", ""),
                                 # installed=modData.get("installed", False),
                                 currentVersion=modSourcesData.get("gameVersion", "") == \
                                                modSourcesData.get("currentGameVersion", " "),
                                 # modFileExist=modData.get("modFileExist", False)
                                 modSourcesPath=modSourcesData.get("modSourcesPath", ""))

                self.mods.currentGameVersion = modSourcesData.get("currentGameVersion", "")

            self.showErrorNotifications()

        elif cmd == Environment.GetModsData:
            for modData in data[1]:
                self.mods.updateMod(hash=modData.get("hash", ""),
                                    installed=modData.get("installed", False),
                                    modFileExist=modData.get("modFileExist", False))

                self.mods.updateAll()

            self.setModsScreen()
            self.showErrorNotifications()

        elif cmd == Environment.GetModConflict:
            searching, modHash = data[1]
            if searching:
                modClass = self.mods.modsSources[modHash]
                self.progressDialog.setTitle(f"Searching conflicts '{modClass.name}'...")
                self.progressDialog.setContent("Searching...")
                self.progressDialog.show()

        elif cmd == Environment.InstallMod:
            installing, modHash = data[1]
            if installing:
                modClass = self.mods.modsSources[modHash]
                self.progressDialog.setTitle(f"Installing mod '{modClass.name}'...")
                self.progressDialog.setContent("Loading mod...")
                self.progressDialog.show()

        elif cmd == Environment.UninstallMod:
            uninstalling, modHash = data[1]
            if uninstalling:
                modClass = self.mods.modsSources[modHash]
                self.progressDialog.setTitle(f"Uninstalling mod '{modClass.name}'...")
                self.progressDialog.setContent("")
                self.progressDialog.show()

        elif cmd == Environment.CompileModSources:
            compiling, modHash = data[1]
            if compiling:
                modClass = self.mods.modsSources[modHash]
                self.progressDialog.setTitle(f"Build mod '{modClass.name}'...")
                self.progressDialog.setContent("")
                self.progressDialog.show()

        elif cmd == Environment.CreateMod:
            created, modSourcesData = data[1]
            if created:
                self.inputDialog.hide()
                self.mods.addMod(gameVersion=modSourcesData.get("gameVersion", ""),
                                 name=modSourcesData.get("name", ""),
                                 author=modSourcesData.get("author", ""),
                                 version=modSourcesData.get("version", ""),
                                 description=modSourcesData.get("description", ""),
                                 tags=modSourcesData.get("tags", []),
                                 previewsPaths=modSourcesData.get("previewsPaths", []),
                                 hash=modSourcesData.get("hash", ""),
                                 platform=modSourcesData.get("platform", ""),
                                 # installed=modData.get("installed", False),
                                 currentVersion=modSourcesData.get("gameVersion", "") == \
                                                modSourcesData.get("currentGameVersion", " "),
                                 # modFileExist=modData.get("modFileExist", False)
                                 modSourcesPath=modSourcesData.get("modSourcesPath", ""))

                self.mods.currentGameVersion = modSourcesData.get("currentGameVersion", "")
            else:
                self.inputDialog.clearInput()
                self.inputDialog.setTitle("Create mod...")
                self.inputDialog.setContent(TextFormatter.format("Enter mod folder name\n\n"
                                                                 '<color="#ff5050">This folder already exists!</color>'))
                # self.controller.reloadModsSources()

    def showErrorNotifications(self):
        if self.errors:
            errors = []
            errorsNotifications = self.errors.copy()
            self.errors.clear()

            for notif in errorsNotifications:
                ntype = notif.notificationType
                string = ""

                # Compiler
                if ntype == NotificationType.CompileModSourcesSpriteHasNoSymbolclass:
                    string = f"Sprite '{notif.args[1]}' has no name"

                elif ntype == NotificationType.CompileModSourcesSpriteEmpty:
                    string = f"Sprite '{notif.args[1]}' is empty"

                elif ntype == NotificationType.CompileModSourcesSpriteNotFoundInFolder:
                    string = f"Not found sprite in '{notif.args[1]}'"

                elif ntype == NotificationType.CompileModSourcesUnsupportedCategory:
                    string = f"Unsupported elements category '{notif.args[1]}'"

                elif ntype == NotificationType.CompileModSourcesUnknownFile:
                    string = f"Unknown file '{notif.args[1]}'"

                elif ntype == NotificationType.CompileModSourcesSaveError:
                    string = "Error save .bmod"

                # Loader
                elif ntype == NotificationType.LoadingModIsEmpty:
                    string = f"Mod '{notif.args[1]}' is empty"

                # Installer
                elif ntype == NotificationType.InstallingModNotFoundFileElement:
                    string = f"Not found element '{notif.args[1]}' in bmod "

                elif ntype == NotificationType.InstallingModNotFoundGameSwf:
                    string = f"Not found game file '{notif.args[1]}'"

                elif ntype == NotificationType.InstallingModSwfScriptError:
                    string = f"Script '{notif.args[1]}' not installed"

                elif ntype == NotificationType.InstallingModSwfSoundSymbolclassNotExist:
                    string = f"Not found sound '{notif.args[1]}' in '{notif.args[2]}'"

                elif ntype == NotificationType.InstallingModSoundNotExist:
                    string = f"Not found sound '{notif.args[1]} ({notif.args[2]})' in '{notif.args[3]}'"

                elif ntype == NotificationType.InstallingModSwfSpriteSymbolclassNotExist:
                    string = f"Not found sprite '{notif.args[1]}' in '{notif.args[2]}'"

                elif ntype == NotificationType.InstallingModSpriteNotExist:
                    string = f"Not found sprite '{notif.args[1]} ({notif.args[2]})' in '{notif.args[3]}'"

                # Uninstaller
                elif ntype == NotificationType.UninstallingModSwfOriginalElementNotFound:
                    string = f"Not found orig element '{notif.args[1]}' in '{notif.args[2]}'"

                elif ntype == NotificationType.UninstallingModSwfElementNotFound:
                    string = f"Not found mod element '{notif.args[1]}' in '{notif.args[2]}'"

                if string:
                    errors.append(string)
                else:
                    errors.append(repr(notif))

            if errors:
                string = ""
                for error in errors:
                    string += f"{error}\n"

                self.showError("Errors:", string)

    def showError(self, title, content, action=None):
        self.buttonsDialog.setTitle(title)

        if self.acceptDialog.isShown():
            self.acceptDialog.hide()

        if self.buttonsDialog.isShown():
            self.buttonsDialog.hide()

        if self.progressDialog.isShown():
            self.progressDialog.hide()

        if action is None:
            action = self.buttonsDialog.hide

        self.buttonsDialog.setContent(content)
        self.buttonsDialog.setButtons([("Copy error", lambda: self.copyToClipboard(f"{title}\n\n{content}")),
                                       ("Ok", action)])
        self.buttonsDialog.show()

    def copyToClipboard(self, text):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(text, mode=cb.Clipboard)

    def setLoadingScreen(self):
        ClearFrame(self.ui.mainFrame)
        AddToFrame(self.ui.mainFrame, self.loading)
        self.loading.setText("Loading mods sources...")

    def setModsScreen(self):
        ClearFrame(self.ui.mainFrame)

        AddToFrame(self.ui.mainFrame, self.header)
        AddToFrame(self.ui.mainFrame, self.mods)

    def showInformation(self):
        self.buttonsDialog.setTitle("About")

        string = TextFormatter.table([["Product:", PROGRAM_NAME],
                                      ["Version:", VERSION],
                                      ["GitHub tag:", GIT_VERSION or "None"],
                                      ["Status:", 'Beta' if PRERELEASE else 'Release'],
                                      ["Core version:", CORE_VERSION],
                                      ["Homepage:", f"<url=\"{GITHUB}/{REPO}\">{GITHUB}/{REPO}</url>"],
                                      [None, f"<url=\"{GAMEBANANA}\">{GAMEBANANA}</url>"],
                                      ["Author:", "I_FabrizioG_I"],
                                      ["Contacts:", "Discord: I_FabrizioG_I#8111"],
                                      [None, "VK: vk/fabriziog"]], newLine=False)

        self.buttonsDialog.setContent(TextFormatter.format(string, 11))
        self.buttonsDialog.setButtons([("Ok", self.buttonsDialog.hide)])
        self.buttonsDialog.show()

    def saveModSource(self):
        if self.mods.selectedModButton is not None:
            modSources = self.mods.selectedModButton.modClass

            self.controller.setModName(modSources.hash, modSources.name)
            self.controller.setModAuthor(modSources.hash, modSources.author)
            self.controller.setModGameVersion(modSources.hash, modSources.gameVersion)
            self.controller.setModVersion(modSources.hash, modSources.version)
            self.controller.setModTags(modSources.hash, modSources.tags)
            self.controller.setModDescription(modSources.hash, modSources.description)
            self.controller.setModPreviews(modSources.hash, modSources.previewsPaths)

            self.controller.saveModSource(modSources.hash)

    def installMod(self):
        if self.mods.selectedModButton is not None:
            modClass = self.mods.selectedModButton.modClass
            if modClass.modFileExist:
                self.controller.getModConflict(modClass.hash)

    def uninstallMod(self):
        if self.mods.selectedModButton is not None:
            modClass = self.mods.selectedModButton.modClass
            self.controller.uninstallMod(modClass.hash)

    def deleteMod(self):
        if self.mods.selectedModButton is not None:
            modClass = self.mods.selectedModButton.modClass

            self.buttonsDialog.deleteButtons()
            self.buttonsDialog.setTitle(f"Delete mod '{modClass.name}'")

            if modClass.installed:
                self.buttonsDialog.setContent("To delete mod, you need to uninstall it")
            elif modClass.modFileExist:
                self.buttonsDialog.setContent("")
                self.buttonsDialog.addButton("Delete mod and sources", self.deleteModAllData)
                self.buttonsDialog.addButton("Delete mod", self.deleteModFile)
            else:
                self.buttonsDialog.addButton("Delete sources", self.deleteModSources)

            self.buttonsDialog.addButton("Cancel", self.buttonsDialog.hide)

            self.buttonsDialog.show()

    def buildMod(self):
        if self.mods.selectedModButton is not None:
            modClass = self.mods.selectedModButton.modClass
            self.controller.compileModSources(modClass.hash)

    def createMod(self):
        folderName = self.inputDialog.getInput().strip()

        if not folderName:
            self.inputDialog.clearInput()
            self.inputDialog.setTitle("Create mod...")
            self.inputDialog.setContent("Enter mod folder name")
            self.inputDialog.setAccept(self.createMod)
            self.inputDialog.setCancel(lambda: [self.inputDialog.hide(), self.inputDialog.clearInput()])
            self.inputDialog.show()
        else:
            self.controller.createMod(folderName)

    def reloadMods(self):
        self.setLoadingScreen()
        self.mods.removeAllMods()
        self.controller.reloadModsSources()
        self.controller.reloadMods()
        self.controller.getModsSourcesData()
        self.controller.getModsData()

    def openModsSourcesFolder(self):
        os.startfile(self.modsSourcesPath)

    def deleteModFile(self):
        modClass = self.mods.selectedModButton.modClass
        modClass.modFileExist = False
        self.controller.deleteMod(modClass.hash)
        self.mods.updateButtons()
        self.buttonsDialog.hide()

    def deleteModSources(self):
        modClass = self.mods.selectedModButton.modClass
        self.controller.deleteModSources(modClass.hash)
        self.buttonsDialog.hide()
        self.reloadMods()

    def deleteModAllData(self):
        self.deleteModFile()
        self.deleteModSources()

    versionSignal = Signal(str, str, str, str)

    def newVersion(self, url: str, fileUrl: str, version: str, body: str):
        self.buttonsDialog.setTitle(f"New version available '{version}'")
        self.buttonsDialog.setContent(TextFormatter.format(body, 11))
        self.buttonsDialog.deleteButtons()
        self.buttonsDialog.addButton("GO TO SITE", lambda: [webbrowser.open(url),
                                                            self.buttonsDialog.hide()])
        self.buttonsDialog.addButton("CANCEL", self.buttonsDialog.hide)
        self.buttonsDialog.show()

    def checkNewVersion(self):
        latest = GetLatest()

        if latest is not None:
            newVersion, fileUrl, version, body = latest
            self.versionSignal.emit(newVersion, fileUrl, version, body)


def RunApp():
    app = QApplication(sys.argv)
    font_db = QFontDatabase()
    font_db.addApplicationFont(":/fonts/resources/fonts/Exo 2/Exo2-SemiBold.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-Black.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-BlackItalic.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-Bold.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-BoldItalic.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-Italic.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-Medium.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-MediumItalic.ttf")
    font_db.addApplicationFont(":/fonts/resources/fonts/Roboto/Roboto-Regular.ttf")
    window = ModCreator()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    RunApp()
