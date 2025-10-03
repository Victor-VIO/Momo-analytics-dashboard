# api/server.py
from http.server import BaseHTTPRequestHandler, HTTPServer
import json, base64, os
from urllib.parse import urlparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data" / "processed" / "transactions.json"
XML_PARSER = ROOT / "dsa" / "parse_xml.py"

# Basic Auth credentials (default). For real use, set environment variables.
AUTH_USER = os.getenv("MOMO_API_USER", "admin")
AUTH_PASS = os.getenv("MOMO_API_PASS", "password123")

PORT = int(os.getenv("MOMO_API_PORT", "8000"))

def load_transactions():
    if not DATA_FILE.exists():
        # auto-run parser if no JSON file
        print("transactions.json not found, running parser...")
        os.system(f"{sys.executable} {XML_PARSER}")
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_transactions(transactions):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(transactions, f, indent=2)

def require_auth(headers):
    auth = headers.get('Authorization')
    if not auth or not auth.startswith('Basic '):
        return False
    token = auth.split(' ', 1)[1]
    try:
        decoded = base64.b64decode(token).decode('utf-8')
    except Exception:
        return False
    parts = decoded.split(':',1)
    if len(parts) != 2:
        return False
    user, pwd = parts
    return user == AUTH_USER and pwd == AUTH_PASS

class Handler(BaseHTTPRequestHandler):
    def send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))

    def send_401(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="MoMo API"')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"error":"Unauthorized"}).encode('utf-8'))

    def do_auth(self):
        if not require_auth(self.headers):
            self.send_401()
            return False
        return True

    def parse_id(self, path):
        parts = path.rstrip('/').split('/')
        if len(parts) >= 3 and parts[-2] == 'transactions':
            try:
                return int(parts[-1])
            except:
                return None
        return None

    def do_GET(self):
        if not self.do_auth(): return
        parsed = urlparse(self.path)
        path = parsed.path
        if path == '/transactions' or path == '/transactions/':
            transactions = load_transactions()
            self.send_json(200, transactions)
            return
        # GET single
        if path.startswith('/transactions/'):
            tid = self.parse_id(path)
            if tid is None:
                self.send_json(400, {"error":"Invalid ID"})
                return
            transactions = load_transactions()
            for t in transactions:
                if t.get('transaction_id') == tid:
                    self.send_json(200, t)
                    return
            self.send_json(404, {"error":"Not found"})
            return
        self.send_json(404, {"error":"Endpoint not found"})

    def read_json_body(self):
        length = int(self.headers.get('Content-Length', 0))
        if length == 0:
            return None
        data = self.rfile.read(length)
        try:
            return json.loads(data.decode('utf-8'))
        except:
            return None

    def do_POST(self):
        if not self.do_auth(): return
        parsed = urlparse(self.path)
        if parsed.path != '/transactions':
            self.send_json(404, {"error":"Endpoint not found"})
            return
        body = self.read_json_body()
        if not body:
            self.send_json(400, {"error":"Invalid or missing JSON body"})
            return
        transactions = load_transactions()
        # create ID: choose max+1
        max_id = max((t.get('transaction_id',0) for t in transactions), default=100)
        new_id = max_id + 1
        body['transaction_id'] = new_id
        transactions.append(body)
        save_transactions(transactions)
        self.send_json(201, body)

    def do_PUT(self):
        if not self.do_auth(): return
        tid = self.parse_id(self.path)
        if tid is None:
            self.send_json(400, {"error":"Invalid ID"})
            return
        body = self.read_json_body()
        if not body:
            self.send_json(400, {"error":"Invalid or missing JSON body"})
            return
        transactions = load_transactions()
        for idx, t in enumerate(transactions):
            if t.get('transaction_id') == tid:
                body['transaction_id'] = tid
                transactions[idx] = body
                save_transactions(transactions)
                self.send_json(200, body)
                return
        self.send_json(404, {"error":"Not found"})

    def do_DELETE(self):
        if not self.do_auth(): return
        tid = self.parse_id(self.path)
        if tid is None:
            self.send_json(400, {"error":"Invalid ID"})
            return
        transactions = load_transactions()
        for idx, t in enumerate(transactions):
            if t.get('transaction_id') == tid:
                removed = transactions.pop(idx)
                save_transactions(transactions)
                self.send_json(200, {"message":"Deleted", "transaction": removed})
                return
        self.send_json(404, {"error":"Not found"})

    # Avoid logging each request to console (keeps terminal clean). Override if needed.
    def log_message(self, format, *args):
        return

if __name__ == "__main__":
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    print(f"Starting server on port {PORT} (BasicAuth user='{AUTH_USER}')")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down")
        server.server_close()
