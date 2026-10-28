"""Small intentionally vulnerable targets. Use only with disposable lab data."""
import json
import os
import socketserver
import sqlite3
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

KIND = os.environ.get('LAB_KIND', 'web')
FIXED = os.environ.get('LAB_FIXED', '0') == '1'
HOST = os.environ.get('LAB_HOST', '127.0.0.1')
PORT = int(os.environ.get('LAB_PORT', '8080'))


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def reply(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == '/health':
            return self.reply(200, {'ready': True, 'kind': KIND, 'fixed': FIXED})
        if KIND == 'api' and self.path.startswith('/documents/'):
            # Fixed synthetic identity: the token belongs to Alice.
            if self.headers.get('Authorization') != 'Bearer alice-demo-token':
                return self.reply(401, {'error': 'authentication required'})
            records = {'1': {'owner': 'alice', 'text': 'Alice demo document'},
                       '2': {'owner': 'bob', 'text': 'Bob private demo document'}}
            record = records.get(self.path.rsplit('/', 1)[-1])
            if record is None:
                return self.reply(404, {'error': 'missing'})
            if FIXED and record['owner'] != 'alice':
                return self.reply(403, {'error': 'not your document'})
            return self.reply(200, record)
        self.reply(404, {'error': 'missing'})

    def do_POST(self):
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if size < 0 or size > 8192:
                return self.reply(413, {'error': 'body too large'})
            data = json.loads(self.rfile.read(size))
            if not isinstance(data, dict):
                raise ValueError('object required')
        except (ValueError, UnicodeError):
            return self.reply(400, {'error': 'invalid JSON'})
        if KIND == 'web' and self.path == '/login':
            username, password = data.get('username', ''), data.get('password', '')
            if not isinstance(username, str) or not isinstance(password, str):
                return self.reply(400, {'error': 'strings required'})
            with sqlite3.connect(':memory:') as db:
                db.execute('CREATE TABLE users (username TEXT, password TEXT)')
                db.execute('INSERT INTO users VALUES (?, ?)', ('admin', 'lab-only-password'))
                if FIXED:
                    row = db.execute('SELECT username FROM users WHERE username=? AND password=?',
                                     (username, password)).fetchone()
                else:
                    try:
                        row = db.execute(f"SELECT username FROM users WHERE username='{username}' AND password='{password}'").fetchone()
                    except sqlite3.Error:
                        return self.reply(400, {'error': 'invalid query'})
            return self.reply(200 if row else 401, {'user': row[0] if row else None})
        if KIND == 'ai' and self.path == '/agent':
            # Explicit toy interpreter, NOT a real LLM or model safety evaluation.
            document = data.get('retrieved_document', '')
            if not isinstance(document, str):
                return self.reply(400, {'error': 'string required'})
            command = 'TOOL: read_internal_note'
            if not FIXED and command in document:
                return self.reply(200, {'tool_called': True, 'answer': 'DEMO_INTERNAL_NOTE_42'})
            return self.reply(200, {'tool_called': False, 'answer': 'Retrieved text treated as untrusted data.'})
        self.reply(404, {'error': 'missing'})


class NetworkHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.connection.settimeout(3)
        command = self.rfile.readline(1024).decode(errors='replace').strip()
        if command == 'PING':
            response = 'PONG'
        elif command == 'GET CONFIG':
            response = 'DENIED' if FIXED else 'DEMO_SERVICE_KEY=local-only-example'
        else:
            response = 'UNKNOWN'
        self.wfile.write((response + '\n').encode())


class TCPServer(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


if __name__ == '__main__':
    server = TCPServer((HOST, PORT), NetworkHandler) if KIND == 'network' else ThreadingHTTPServer((HOST, PORT), Handler)
    with server:
        server.serve_forever()
