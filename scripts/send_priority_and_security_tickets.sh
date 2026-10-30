#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import json
import urllib.request

url = 'http://localhost:5678/webhook-test/ticket'

tickets = [
    {
        'id': 'C-01',
        'title': 'Demande from blockbuster prospect',
        'description': 'Le plus gros prospect nous demande une fonctionnalité clé dans les 48h. On a peu d’informations sur la valeur commerciale, le coût réel et l’impact si on ne le fait pas. Le besoin semble important mais on ne sait pas encore si c’est un vrai blocker.',
        'labels': 'sales,priority'
    },
    {
        'id': 'C-02',
        'title': 'Feature demandée à haut niveau',
        'description': 'Le leadership a demandé un correctif de priorité élevée pour une fonctionnalité super utile, mais le nombre de clients concernés, l’ampleur du retard et le coût de développement ne sont pas encore connus.',
        'labels': 'leadership,roadmap'
    },
    {
        'id': 'C-03',
        'title': 'Demande d’un compte enterprise',
        'description': 'Un client enterprise veut une évolution qui pourrait générer beaucoup de revenus. Nous n’avons pas encore calculé l’impact, la complexité ni la date d’échéance.',
        'labels': 'enterprise,feature'
    },
    {
        'id': 'D-01',
        'title': 'Je pense avoir vu un autre compte',
        'description': 'J’ai peut-être vu les données d’un autre compte sur un écran de debug. Je ne suis pas sûr, mais je pense que cela peut être un problème de sécurité.',
        'labels': 'security,possible-leak'
    },
    {
        'id': 'D-02',
        'title': 'Anomalie de permissions',
        'description': 'Un utilisateur a pu ouvrir un document de quelqu’un d’autre. Nous n’avons pas confirmé que cela a été exploité, mais il y a un doute sur le contrôle d’accès.',
        'labels': 'security,access-control'
    },
]

for ticket in tickets:
    payload = json.dumps(ticket).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode('utf-8', errors='replace')
        print(f"{ticket['id']} -> {resp.status} -> {body[:200]}")
PY
