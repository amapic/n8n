import json
import urllib.error
import urllib.request

URL = "http://localhost:5678/webhook/ticket"

REQUESTS = [
    {
        'id': 'priority3-01',
        'title': 'Mouse without borders should indicate errors in new UI',
        'description': 'Mouse without borders should indicate errors in the new UI. In the old UI, errors appear in popup windows, but in the new UI users only see colors and cannot troubleshoot. The expected behavior is to show clear error messages. The actual behavior is that the connection fails silently.',
        'labels': ''
    },
    {
        'id': 'priority3-02',
        'title': 'Fancy Zones - Cannot set a 2560px width for zones',
        'description': 'Panel is 5120x1440 in resolution. In the FancyZones layout editor, setting a two-column zone to 2560x1440 always shifts the zone by 1 pixel horizontally. The expected behavior is two zones of exactly 2560x1440.',
        'labels': ''
    },
    {
        'id': 'priority3-03',
        'title': '"The REG file editor could not be opened" when clicking Edit in Registry Preview',
        'description': 'In Registry Preview, opening a .REG file and clicking Edit fails with the message "The REG file editor could not be opened". The expected behavior is that the file opens in Notepad.',
        'labels': ''
    },
    {
        'id': 'priority3-04',
        'title': 'Advances Paste Settings, Typo/Truncated words',
        'description': 'In Advanced Paste settings, some words are cut off or truncated in the UI. This makes the settings hard to read and appears to be a text formatting or layout issue.',
        'labels': ''
    },
    {
        'id': 'priority3-05',
        'title': 'Advanced Paster error when using text from a Word File with "Title" style',
        'description': 'When copying text from a Microsoft Word file that uses the Title style and pasting it as markdown, Advanced Paste inserts hidden HTML conditional tags instead of the expected markdown header. It should paste TEXT followed by ===.',
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
