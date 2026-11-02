import json
import subprocess
import time

REPO = "microsoft/PowerToys"
TARGET_LABEL = "Needs-Author-Feedback"
LIMIT = 1000          # nombre max d'issues à analyser
FILTER_LABEL = None   # ex. "priority-3" pour restreindre, ou None pour tout prendre


def gh(args):
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    )
    return result.stdout


def get_all_issues():
    args = [
        "issue", "list",
        "--repo", REPO,
        "--state", "all",
        "--limit", str(LIMIT),
        "--json", "number,title,body,url,state,labels",
    ]
    if FILTER_LABEL:
        args += ["--label", FILTER_LABEL]
    return json.loads(gh(args))


def get_ever_labeled(number):
    """Retourne l'ensemble des labels qui ont déjà été posés sur l'issue.
    Le --jq évite le problème des pages JSON concaténées de --paginate."""
    out = gh([
        "api", "--paginate",
        f"repos/{REPO}/issues/{number}/events",
        "--jq", '.[] | select(.event=="labeled") | .label.name',
    ])
    return {line.strip() for line in out.splitlines() if line.strip()}


def main():
    issues = get_all_issues()
    print(f"{len(issues)} issues récupérées.")

    had_feedback, never_feedback = [], []

    for index, issue in enumerate(issues, 1):
        number = issue["number"]
        current_labels = {l["name"] for l in issue.get("labels", [])}

        try:
            historical = get_ever_labeled(number) | current_labels
        except subprocess.CalledProcessError as exc:
            print(f"Erreur sur #{number}: {exc}")
            continue

        record = {
            "id": number,
            "title": issue["title"],
            "body": issue.get("body") or "",
        }

        if TARGET_LABEL in historical:
            had_feedback.append(record)
        else:
            never_feedback.append(record)

        if index % 25 == 0:
            print(f"{index}/{len(issues)} analysées")
            time.sleep(0.2)

    with open("issues_had_author_feedback.json", "w", encoding="utf-8") as f:
        json.dump(had_feedback, f, ensure_ascii=False, indent=2)

    with open("issues_never_author_feedback.json", "w", encoding="utf-8") as f:
        json.dump(never_feedback, f, ensure_ascii=False, indent=2)

    print(f"\nOnt eu {TARGET_LABEL} : {len(had_feedback)}")
    print(f"Ne l'ont jamais eu : {len(never_feedback)}")


if __name__ == "__main__":
    main()