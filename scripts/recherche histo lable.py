
import json
import subprocess
import time

REPO = "microsoft/PowerToys"
PRIORITY_LABELS = {
    "Priority-0",
    "Priority-1",
    "Priority-2",
    "Priority-3",
}
EXCLUDED_LABEL = "Needs-Author-Feedback"


def gh_json(args):
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        check=True,
        encoding="utf-8",
    )
    return json.loads(result.stdout)


def get_all_issues():
    """Récupère les issues ouvertes et fermées, par lots."""
    result = gh_json([
        "issue", "list",
        "--repo", REPO,
        "--state", "all",
        "--limit", "1000",
        "--label", "priority-3",
        "--json", "number,title,body,url,state,labels",
    ])
    return result


def get_events(number):
    return gh_json([
        "api", "--paginate",
        f"repos/{REPO}/issues/{number}/events",
    ])


def main():
    issues = get_all_issues()
    selected = []

    print(f"{len(issues)} issues récupérées.")

    for index, issue in enumerate(issues, 1):
        number = issue["number"]

        try:
            events = get_events(number)
        except subprocess.CalledProcessError as exc:
            print(f"Erreur sur #{number}: {exc}")
            continue

        # Labels actuellement présents
        current_labels = {
            label["name"] for label in issue.get("labels", [])
        }

        # Reconstituer les labels ayant existé dans l'historique.
        historical_labels = set(current_labels)

        for event in events:
            label = event.get("label", {})
            label_name = label.get("name")

            if not label_name:
                continue

            if event.get("event") == "labeled":
                historical_labels.add(label_name)

        # On vérifie aussi les événements de retrait :
        # un label retiré reste considéré comme ayant existé.
        has_priority = bool(
            historical_labels.intersection(PRIORITY_LABELS)
        )

        ever_had_feedback = EXCLUDED_LABEL in historical_labels

        if has_priority and not ever_had_feedback:
            selected.append({
                "number": number,
                "title": issue["title"],
                "body": issue.get("body") or "",
                "url": issue["url"],
                "state": issue["state"],
                "current_labels": sorted(current_labels),
                "historical_priority_labels": sorted(
                    historical_labels.intersection(PRIORITY_LABELS)
                ),
            })

        if index % 25 == 0:
            print(f"{index}/{len(issues)} analysées")
            time.sleep(0.2)

    output = "powertoys_priority_no_author_feedback.json"

    with open(output, "w", encoding="utf-8") as file:
        json.dump(selected, file, ensure_ascii=False, indent=2)

    print(f"\nTerminé : {len(selected)} issues retenues.")
    print(f"Fichier créé : {output}")


if __name__ == "__main__":
    main()
