import json
import urllib.error
import urllib.request

URL = "http://localhost:5678/webhook-test/ticket"

REQUESTS = [
    {
        'id': 'vague-01',
        'title': 'Ça ne marche plus depuis la dernière mise à jour',
        'description': 'Ça ne marche plus depuis la dernière mise à jour. Urgent !!! Tout est cassé et on n’a pas de logs utiles. On a juste l’impression que le système est planté.',
        'labels': 'urgent,noise'
    },
    {
        'id': 'vague-02',
        'title': 'Erreur de synchronisation',
        'description': 'Le sync est cassé et ça devient vraiment horrible. Personne ne sait si c’est le pipeline ou la prod. On n’a pas la trace exacte ni le moment de la panne.',
        'labels': 'sync,ops'
    },
    {
        'id': 'vague-03',
        'title': 'Le bouton ne répond plus',
        'description': 'Le bouton sur la page principale ne répond plus, c’est super ennuyeux. On pense que c’est un bug front, mais on n’a pas les erreurs, ni l’URL, ni la version du navigateur.',
        'labels': 'ui,frontend'
    },
    {
        'id': 'vague-04',
        'title': 'Données désynchronisées',
        'description': 'Les données ne coincide pas, on a l’impression que quelque chose cloche. Les utilisateurs disent que les infos sont bidouillées, sans précision sur le périmètre ni le moment de la dégradation.',
        'labels': 'data,quality'
    },
    {
        'id': 'vague-05',
        'title': 'Bug du workflow de validation',
        'description': 'Le workflow de validation a l’air cassé. C’est urgent, c’est bloquant et ça semble incompréhensible. Le ticket est très vague et il manque les captures d’écran et les logs.',
        'labels': 'workflow,validation'
    },
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
