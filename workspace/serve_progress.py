#!/usr/bin/env python3
"""Simple HTTP server to show progress"""
import json
import os
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler

class ProgressHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/progress_status.json':
            # Find latest run with progress.json
            output_dir = Path('/workspace/output')
            runs = sorted(output_dir.glob('run_*'), key=lambda x: x.name, reverse=True)

            for run_dir in runs:
                progress_file = run_dir / 'progress.json'
                if progress_file.exists():
                    with open(progress_file, 'r') as f:
                        data = json.load(f)
                        data['run_dir'] = run_dir.name

                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(data).encode())
                    return

            # No progress found
            self.send_response(404)
            self.end_headers()
        else:
            super().do_GET()

if __name__ == '__main__':
    os.chdir('/workspace')
    server = HTTPServer(('0.0.0.0', 8502), ProgressHandler)
    print('Progress monitor running at http://localhost:8502/progress.html')
    server.serve_forever()
