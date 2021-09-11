import sys
import json
import urllib.request
import win32api



GITHUB_API = "https://api.github.com"
REPO = "Farbigoz/BhModCreator"


def GetFileProperties(fname):
    props = {"FileVersion": None, "FileFlags": None}

    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FileFlags'] = fixedInfo["FileFlags"]
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]
        props['FileVersion'] = win32api.GetFileVersionInfo(fname, u'\\StringFileInfo\\%04X%04X\\FileVersion' %
                                                           (lang, codepage))
    except:
        pass

    return props


if getattr(sys, 'frozen', False):
    fileProperties = GetFileProperties(sys.executable)
    VERSION = fileProperties["FileVersion"]
    PRERELEASE = bool(fileProperties["FileFlags"] & 0x2)
else:
    VERSION = None
    PRERELEASE = True


def GetLasted():
    if VERSION is None:
        return None

    try:
        resp = urllib.request.urlopen(f"{GITHUB_API}/repos/{REPO}/releases")
        json_payload = json.loads(resp.read().decode("UTF-8"))
    except:
        return None

    if json_payload:
        lasted = json_payload[0]
        if lasted.get("prerelease", False):
            if PRERELEASE:
                tag_name = lasted.get("tag_name", None)
                if tag_name is not None and tag_name != VERSION:
                    return lasted.get("html_url", None)
                else:
                    return None
            else:
                for release in json_payload:
                    if not release.get("prerelease", False):
                        lasted = release
                        break
                else:
                    return None

        tag_name = lasted.get("tag_name", None)
        if tag_name is not None and tag_name != VERSION:
            return lasted.get("html_url", None)
