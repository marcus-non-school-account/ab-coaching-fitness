#!/usr/bin/env python3
"""Local dev server that behaves like Vercel.

`python -m http.server` cannot serve /about from about.html, so extensionless
links look broken locally even though they work once deployed. This adds the
same clean-URL fallback Vercel applies, so what you see locally is what ships.

    python serve.py            # http://localhost:8137
    python serve.py 3000       # a different port
"""

import os
import sys
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8137


class CleanURLHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        local = super().translate_path(path)
        # /about -> about.html, when there is no such file or directory
        if not os.path.exists(local) and not os.path.splitext(local)[1]:
            html = local + ".html"
            if os.path.isfile(html):
                return html
        return local

    def send_response(self, code, message=None):
        # Never cache during development, or edits appear not to take effect.
        super().send_response(code, message)
        self.send_header("Cache-Control", "no-store")

    def end_headers(self):
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s\n" % (fmt % args))


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"AB Coaching site -> http://localhost:{PORT}  (Ctrl+C to stop)")
    # Threaded: a browser holding a keep-alive connection would otherwise
    # block every other request on a single-threaded server.
    ThreadingHTTPServer(("", PORT), CleanURLHandler).serve_forever()
