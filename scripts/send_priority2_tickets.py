import json
import urllib.error
import urllib.request

URL = "http://localhost:5678/webhook/ticket"

REQUESTS = [
    {
        'id': 'priority2-01',
        'title': 'After Windows update the Command Palette Icon Disappear in Windows Tray',
        'description': 'After a Windows update and restart, the Command Palette icon disappears from the system tray. The expected behavior is that the icon should be recreated automatically after a normal restart or a patch-related reboot. The actual behavior is that the tray icon is not initialized until it is manually disabled and re-enabled in settings.',
        'labels': ''
    },
    {
        'id': 'priority2-02',
        'title': 'How to disable Command Palette with DSC installation',
        'description': 'When deploying PowerToys with DSC after the 0.90.1 winget release, the user is not sure how to define Command Palette in DSC. They tried using CommandPalette and CmdPal but neither option worked. The expected behavior is to define the tool in DSC so it is not enabled during installation.',
        'labels': ''
    },
    {
        'id': 'priority2-03',
        'title': 'CmdPal not finding a extension (winget)',
        'description': 'When opening Install Command Palette extensions, the extension list is missing expected entries. The expected behavior is to see the EverythingCmdPal extension in the list. The actual behavior is that the extension is missing and the search only finds a limited number of packages tagged as windows-commandpalette-extension.',
        'labels': ''
    },
    {
        'id': 'priority2-04',
        'title': 'Chinese descriptions for apps in English Systems',
        'description': 'In an English-language Windows system, app descriptions in Command Palette are displayed in Mandarin for some apps. The expected behavior is that all descriptions should be shown in English because the system display language is English.',
        'labels': ''
    },
    {
        'id': 'priority2-05',
        'title': 'Turn off admin?',
        'description': 'The user started both machines with Run as administrator and now wants to return to a normal user session. They cannot figure out how to disable the admin option or restart without admin selected. The expected behavior is to be able to return to a standard user mode.',
        'labels': ''
    }
]

for body in REQUESTS:
    data = json.dumps(body, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"{body['id']} -> {resp.status}")
            print(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        print(f"{body['id']} -> HTTP {e.code}")
        print(e.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"{body['id']} -> ERROR: {type(e).__name__}: {e}")
