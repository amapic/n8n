#cd "/mnt/c/Users/amo/Documents/projet dev/ia/ai-product-ops-copilot"
#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import json
import urllib.request

url = 'http://localhost:5678/webhook-test/ticket'

tickets = [
    {
        'id': 'B-01',
        'title': 'Incident bloquant tous les utilisateurs',
        'description': 'Selon le support, l’application est complètement bloquée pour tous les utilisateurs. En réalité, le problème affecte un seul compte test et un contournement est disponible. Le service est donc partiellement impacté, mais la direction veut une réponse rapide.',
        'labels': 'incident,ops'
    },
    {
        'id': 'B-02',
        'title': 'API indisponible',
        'description': 'L’API est tombée pour tout le monde. Les logs internes montrent que le service est en panne pour 2 clients seulement, avec un fallback actif.',
        'labels': 'api,incident'
    },
    {
        'id': 'B-03',
        'title': 'Panne réseau sur la région EU',
        'description': 'La région EU est en panne globale. La carte de trafic montre juste une latence élevée sur un seul pool de workers, et le trafic continue de passer sur les autres zones.',
        'labels': 'network,infra'
    },
    {
        'id': 'B-04',
        'title': 'Échec de synchronisation CRM',
        'description': 'La synchronisation CRM est cassée selon le service client. Les données contiennent pourtant des mises à jour récentes sur les comptes test et la job est toujours en cours côté backend.',
        'labels': 'crm,integration'
    },
    {
        'id': 'B-05',
        'title': 'Connexion impossible',
        'description': 'Tous les utilisateurs ne peuvent pas se connecter. Le SSO est injoignable selon l’équipe support, mais les tests internes montrent que l’authentification marche sur les comptes admin et sur un seul sous-ensemble d’utilisateurs.',
        'labels': 'auth,login'
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
