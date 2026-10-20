
import csv
import json
from pathlib import Path

import requests

DATA = Path("data")
DATA.mkdir(exist_ok=True)

# Dataset A : exemples synthétiques, sans données personnelles réelles.
synthetic = [
    {
        "id": "SYN-001",
        "title": "Abandon du formulaire d'inscription",
        "description": "Plusieurs utilisateurs signalent un blocage à l'étape de vérification de l'adresse e-mail. 18 signalements par semaine.",
        "labels": "activation",
        "source": "synthetic",
    },
    {
        "id": "SYN-002",
        "title": "Ajouter un thème sombre",
        "description": "Quelques utilisateurs demandent un thème sombre. Aucun impact sur la rétention n'est documenté.",
        "labels": "experience-utilisateur",
        "source": "synthetic",
    },
    {
        "id": "SYN-003",
        "title": "Automatiser le rapport mensuel",
        "description": "Une équipe consacre environ six heures par mois à compiler manuellement trois fichiers CSV.",
        "labels": "automatisation",
        "source": "synthetic",
    },
    {
        "id": "SYN-004",
        "title": "Connexion SSO demandée par un prospect",
        "description": "Un prospect important souhaite le SSO avant de signer. L'effort technique et la probabilité de signature sont inconnus.",
        "labels": "vente",
        "source": "synthetic",
    },
    {
        "id": "SYN-005",
        "title": "Suspicion d'accès aux données d'un autre compte",
        "description": "Un signalement suggère qu'un utilisateur pourrait voir des données d'un autre compte. Le problème n'est pas encore reproduit.",
        "labels": "securite",
        "source": "synthetic",
    },
    {
        "id": "SYN-006",
        "title": "Export Excel demandé par plusieurs clients",
        "description": "Quatre clients demandent l'export Excel. Deux l'ont évoqué lors d'une discussion de renouvellement, sans risque confirmé.",
        "labels": "fonctionnalite",
        "source": "synthetic",
    },
    {
        "id": "SYN-007",
        "title": "Import de données créant des doublons",
        "description": "Relancer un import après un délai d'attente peut créer des doublons. La fréquence exacte est inconnue.",
        "labels": "fiabilite",
        "source": "synthetic",
    },
    {
        "id": "SYN-008",
        "title": "Rapport de direction à enrichir",
        "description": "La direction demande quinze indicateurs supplémentaires, mais les décisions que ces indicateurs doivent éclairer ne sont pas définies.",
        "labels": "reporting",
        "source": "synthetic",
    },
    {
        "id": "SYN-009",
        "title": "Recherche très lente sur les gros comptes",
        "description": "La recherche peut dépasser huit secondes pour les comptes volumineux. Douze tickets ont été remontés ce mois-ci.",
        "labels": "performance",
        "source": "synthetic",
    },
    {
        "id": "SYN-010",
        "title": "Suppression de compte en libre-service",
        "description": "Les utilisateurs ne trouvent pas d'option pour supprimer leur compte. Les obligations et règles de conservation doivent être vérifiées.",
        "labels": "conformite",
        "source": "synthetic",
    },
]

def write_csv(filename, rows):
    if not rows:
        print(f"Aucune donnée à écrire pour {filename}")
        return
    with (DATA / filename).open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"{filename}: {len(rows)} lignes")

write_csv("synthetic_issues.csv", synthetic)

# Dataset B : issues publiques GitHub.
# Les commentaires et noms d'utilisateurs ne sont pas récupérés.
url = "https://api.github.com/repos/microsoft/PowerToys/issues"
params = {"state": "all", "per_page": 30, "page": 1, "sort": "updated", "direction": "desc"}

response = requests.get(
    url,
    params=params,
    headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "ai-product-ops-copilot-demo",
    },
    timeout=30,
)
response.raise_for_status()

issues = []
for item in response.json():
    # L'endpoint GitHub peut également renvoyer des pull requests.
    if "pull_request" in item:
        continue

    labels = [
        label.get("name", "")
        for label in item.get("labels", [])
        if isinstance(label, dict)
    ]

    issues.append({
        "id": f"GH-{item['number']}",
        "title": item.get("title") or "",
        "description": (item.get("body") or "")[:5000],
        "labels": "; ".join(labels),
        "state": item.get("state", ""),
        "created_at": item.get("created_at", ""),
        "updated_at": item.get("updated_at", ""),
        "url": item.get("html_url", ""),
        "source": "github_public",
    })

write_csv("github_issues.csv", issues)

print("\nPréparation terminée.")
print("Les données GitHub sont publiques, mais cela ne garantit pas leur anonymat.")
print("Inspecte les descriptions avant de les transmettre à un service externe.")
