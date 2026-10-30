import argparse
import json
import urllib.error
import urllib.request
from pathlib import Path

DEFAULT_URL = "http://localhost:5678/webhook/ticket"
JSON_FILES = [
    "powertoys_priority0_no_author_feedback_essai2_avec_prompt2.json",
    # "priority1_50.json",
    # "priority2_50.json",
    # "priority3_50.json",
]


def sanitize_description(value):
    text = str(value or "")
    text = text.replace("\x00", "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = "".join(ch for ch in text if ch.isprintable() or ch in "\n\t")
    text = text.strip()
    return text[:20000]


def load_items(file_name):
    file_path = Path(__file__).resolve().parent / file_name
    with file_path.open("r", encoding="utf-16") as f:
        items = json.load(f)
    if not isinstance(items, list):
        raise ValueError(f"{file_name} ne contient pas une liste de tickets.")
    return items


def build_requests():
    requests = []
    for file_name in JSON_FILES:
        prefix = file_name.replace(".json", "")
        items = load_items(file_name)
        for index, item in enumerate(items, start=1):
            requests.append(
                {
                    "id": f"{prefix}-{index:02d}",
                    "title": item.get("title", ""),
                    "description": sanitize_description(item.get("body", "")),
                    "labels": "",
                }
            )
    return requests


def send_ticket(url, payload):
    data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print(f"{payload['id']} -> {resp.status}")
            print(body)
    except urllib.error.HTTPError as e:
        print(f"{payload['id']} -> HTTP {e.code}")
        print(e.read().decode("utf-8", errors="replace"))
    except Exception as e:
        print(f"{payload['id']} -> ERROR: {type(e).__name__}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Envoie tous les tickets priority0_50.json, priority1_50.json, priority2_50.json et priority3_50.json.")
    parser.add_argument("--url", default=DEFAULT_URL, help="URL du webhook cible")
    parser.add_argument("--dry-run", action="store_true", help="Affiche les payloads sans les envoyer")
    args = parser.parse_args()

    requests = build_requests()
    print(f"{len(requests)} tickets prêts à être envoyés.")

    if args.dry_run:
        for payload in requests:
            print(json.dumps(payload, ensure_ascii=False))
        return

    for payload in requests:
        send_ticket(args.url, payload)


if __name__ == "__main__":
    main()
