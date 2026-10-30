#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import json
import urllib.request

url = 'http://localhost:5678/webhook-test/ticket'

tickets = [
    {
        'id': 'A-01',
        'title': 'Conversion en baisse sur la page produit',
        'description': 'Le taux de conversion a baissé. Il faut corriger le parcours.',
        'labels': 'growth,product'
    },
    {
        'id': 'A-02',
        'title': 'Baisse du volume d’inscription',
        'description': 'Les inscriptions ont chuté depuis la dernière mise en prod. Il faut réparer au plus vite.',
        'labels': 'growth,signup'
    },
    {
        'id': 'A-03',
        'title': 'Le funnel de paiement est mauvais',
        'description': 'De moins en moins de clients passent au paiement. Le parcours semble poser problème.',
        'labels': 'checkout,product'
    },
    {
        'id': 'A-04',
        'title': 'Taux de clic très bas sur le CTA',
        'description': 'Le bouton principal est peu utilisé, il faut améliorer le parcours et la valeur.',
        'labels': 'ux,marketing'
    },
    {
        'id': 'A-05',
        'title': 'Rétention des nouveaux utilisateurs',
        'description': 'La rétention a diminué. Le produit semble moins engageant. Il faut agir.',
        'labels': 'retention,product'
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
