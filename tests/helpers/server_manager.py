"""
A simple, multi-threaded HTTP server for integration testing.

This module provides a helper class, `TestServer`, which can be used to run a
local HTTP server in a separate thread. This is useful for integration tests
that need to make HTTP requests to a known endpoint. The server can be
configured with custom request handlers to serve different content on
different paths.
"""

import http.server
import socketserver
import threading
from pathlib import Path
from typing import Any

CONTENT_TYPE_HTML = "text/html"
CONTENT_TYPE_PLAIN = "text/plain"


class TestServer:
    """A simple HTTP server that runs in a separate thread."""

    def __init__(self, port: int = 8000, handler: Any = None):
        """
        Initialize the test server.

        Args:
            port: The port to run the server on.
            handler: The request handler class to use.
        """
        self.port = port
        self.handler = handler or self.DefaultHandler
        self.httpd = socketserver.TCPServer(("", self.port), self.handler)
        self.httpd.allow_reuse_address = True
        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        self.server_thread.daemon = True

    def start(self):
        """Start the server in a separate thread."""
        self.server_thread.start()

    def stop(self):
        """Stop the server and close the thread."""
        self.httpd.shutdown()
        self.httpd.server_close()
        self.server_thread.join()

    @property
    def base_url(self) -> str:
        """Get the base URL of the server."""
        return f"http://localhost:{self.port}"

    class DefaultHandler(http.server.SimpleHTTPRequestHandler):
        """
        A default request handler that serves files from the 'resources'
        directory and provides predefined responses for testing.
        """

        RESOURCES_DIR = Path(__file__).parent / ".." / "resources"

        def do_GET(self):
            """Handle GET requests."""
            if self.path == "/simple":
                self._serve_file("simple.html", CONTENT_TYPE_HTML)
            elif self.path == "/complex":
                self._serve_file("complex.html", CONTENT_TYPE_HTML)
            elif self.path == "/no_html":
                self._serve_file("no_html.txt", CONTENT_TYPE_PLAIN)
            elif self.path == "/empty":
                self.send_response(204)
                self.end_headers()
            elif self.path == "/error":
                self.send_response(500)
                self.send_header("Content-type", CONTENT_TYPE_HTML)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Internal Server Error</h1></body></html>")
            else:
                self.send_response(404)
                self.send_header("Content-type", CONTENT_TYPE_HTML)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>Not Found</h1></body></html>")

        def _serve_file(self, filename: str, content_type: str):
            """
            Serve a file from the resources directory.

            Args:
                filename: The name of the file to serve.
                content_type: The content type of the file.
            """
            filepath = self.RESOURCES_DIR / filename
            try:
                with filepath.open("rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", content_type)
                    self.end_headers()
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_response(404)
                self.send_header("Content-type", CONTENT_TYPE_HTML)
                self.end_headers()
                self.wfile.write(b"<html><body><h1>File Not Found in Resources</h1></body></html>")

        def log_message(self, format: str, *args: Any) -> None:
            """Suppress logging to keep test output clean."""
