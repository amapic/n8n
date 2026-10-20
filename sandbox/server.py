from flask import Flask, request, jsonify, abort
import os

app = Flask(__name__)
API_KEY = os.environ.get('SANDBOX_API_KEY', '')

@app.route('/healthz', methods=['GET'])
def healthz():
    return 'ok', 200

# Accept any path and method, validate API key from several places
@app.route('/', defaults={'path': ''}, methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
@app.route('/<path:path>', methods=['GET','POST','PUT','DELETE','PATCH','OPTIONS'])
def catch_all(path):
    # Health endpoint should be accessible without auth
    if path == 'healthz':
        return 'ok', 200

    # Check headers
    auth = request.headers.get('Authorization', '')
    xkey = request.headers.get('x-api-key', '')
    token = ''
    if auth.startswith('Bearer '):
        token = auth[len('Bearer '):]
    else:
        token = auth

    # Check query param
    qkey = request.args.get('api_key') or request.args.get('key') or ''

    # Check JSON body or form data
    body_key = ''
    try:
        j = request.get_json(silent=True)
        if isinstance(j, dict):
            body_key = j.get('api_key') or j.get('key') or j.get('token') or ''
    except Exception:
        body_key = ''
    if not body_key:
        body_key = request.form.get('api_key') or request.form.get('key') or ''

    # Accept if any matches
    if token == API_KEY or xkey == API_KEY or qkey == API_KEY or body_key == API_KEY:
        return jsonify({'status': 'ok', 'path': path}), 200

    return jsonify({'error': 'unauthorized'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3200)
