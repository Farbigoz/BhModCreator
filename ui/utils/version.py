import sys
import json
import urllib.request


GITHUB = "https://github.com"
GITHUB_API = "https://api.github.com"
REPO = "Farbigoz/BhModCreator"


if sys.platform in ["win32", "win64"]:
    import win32api

    def GetFileProperties(executable):
        props = {"FileVersion": None, "FileFlags": None}

        try:
            fixedInfo = win32api.GetFileVersionInfo(executable, '\\')
            props['FileFlags'] = fixedInfo["FileFlags"]
            lang, codepage = win32api.GetFileVersionInfo(executable, '\\VarFileInfo\\Translation')[0]
            props['FileVersion'] = win32api.GetFileVersionInfo(executable, u'\\StringFileInfo\\%04X%04X\\FileVersion' %
                                                               (lang, codepage))
        except:
            pass

        return props


    if getattr(sys, 'frozen', False):
        fileProperties = GetFileProperties(sys.executable)
        VERSION = fileProperties["FileVersion"]
        PRERELEASE = bool(fileProperties["FileFlags"] & 0x2)

elif sys.platform == "darwin":
    def GetFileProperties(executable):
        props = {"FileVersion": None, "FileFlags": None}
        return props


    if getattr(sys, 'frozen', False):
        fileProperties = GetFileProperties(sys.executable)
        VERSION = fileProperties["FileVersion"]
        PRERELEASE = fileProperties["FileFlags"]

else:
    def GetFileProperties(executable):
        props = {"FileVersion": None, "FileFlags": None}
        return props


    if getattr(sys, 'frozen', False):
        fileProperties = GetFileProperties(sys.executable)
        VERSION = fileProperties["FileVersion"]
        PRERELEASE = fileProperties["FileFlags"]


if not getattr(sys, 'frozen', False):
    VERSION = None
    PRERELEASE = True


def GetLatest():
    if VERSION is None:
        return None

    try:
        resp = urllib.request.urlopen(f"{GITHUB_API}/repos/{REPO}/releases")
        json_payload = json.loads(resp.read().decode("UTF-8"))
    except:
        return None

    if json_payload:
        latest = json_payload[0]
        if latest.get("prerelease", False):
            if PRERELEASE:
                tag_name = latest.get("tag_name", None)
                if tag_name is not None and tag_name != VERSION:
                    return latest.get("html_url", None)
                else:
                    return None
            else:
                for release in json_payload:
                    if not release.get("prerelease", False):
                        latest = release
                        break
                else:
                    return None

        tag_name = latest.get("tag_name", None)
        if tag_name is not None and tag_name != VERSION:
            return latest.get("html_url", None)
