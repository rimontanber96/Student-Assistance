from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import mimetypes

BASE_DIR = Path(__file__).parent
STATIC_DIR = (BASE_DIR / "static").resolve()

PAGES = {
    "/": "index.html",
    "/courses": "courses.html",
    "/attendance": "attendance.html",
    "/grades": "grades.html"
}


class Website(BaseHTTPRequestHandler):

    def do_GET(self):
        path = urlparse(self.path).path      # ignore ?query=...

        # Static files (css)
        if path.startswith("/static/"):
            file_path = (BASE_DIR / path.lstrip("/")).resolve()

            # only allow real files inside the static folder
            if file_path.is_file() and file_path.is_relative_to(STATIC_DIR):
                mime = mimetypes.guess_type(file_path)[0] or "text/plain"
                self.send_file(file_path, mime)
            else:
                self.send_error(404)
            return

        # HTML pages
        page = PAGES.get(path)

        if page:
            self.send_file(BASE_DIR / "templates" / page, "text/html")
        else:
            self.send_error(404)

    def send_file(self, file_path, content_type):
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(file_path.read_bytes())


if __name__ == "__main__":
    server = HTTPServer(("localhost", 8000), Website)
    print("Server running at http://localhost:8000")
    server.serve_forever()