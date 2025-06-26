#!/usr/bin/env python3
"""
Ludwig Web Framework - Native HTTP Server
No external dependencies required - pure Python implementation
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from datetime import datetime


class LudwigWebFramework:
    """Ludwig's native web framework - no Flask required!"""
    
    def __init__(self, app_config=None):
        self.routes = {}
        self.static_routes = {}
        self.config = app_config or {}
        self.middleware = []
        
    def route(self, path, handler=None):
        """Register a route handler."""
        if handler:
            self.routes[path] = handler
        else:
            # Decorator usage
            def decorator(func):
                self.routes[path] = func
                return func
            return decorator
    
    def static(self, url_path, directory):
        """Register static file serving."""
        self.static_routes[url_path] = directory
    
    def add_middleware(self, middleware_func):
        """Add middleware function."""
        self.middleware.append(middleware_func)
    
    def run(self, host="localhost", port=8000, debug=False):
        """Start the Ludwig web server."""
        handler = self._create_handler()
        
        try:
            with socketserver.TCPServer((host, port), handler) as httpd:
                print(f"🚀 Ludwig Web Server running at http://{host}:{port}")
                print("📁 Serving Ludwig application")
                if debug:
                    print("🔧 Debug mode enabled")
                print("Press Ctrl+C to stop")
                print()
                httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped")
        except Exception as e:
            print(f"❌ Server error: {e}")
    
    def _create_handler(self):
        """Create HTTP request handler class."""
        framework = self
        
        class LudwigHTTPHandler(http.server.SimpleHTTPRequestHandler):
            def do_GET(self):
                self.handle_request('GET')
            
            def do_POST(self):
                self.handle_request('POST')
            
            def do_PUT(self):
                self.handle_request('PUT')
            
            def do_DELETE(self):
                self.handle_request('DELETE')
            
            def handle_request(self, method):
                """Handle HTTP requests using Ludwig routing."""
                try:
                    # Parse URL
                    parsed_url = urllib.parse.urlparse(self.path)
                    path = parsed_url.path
                    query_params = urllib.parse.parse_qs(parsed_url.query)
                    
                    # Create request object
                    request = LudwigRequest(method, path, query_params, self)
                    
                    # Apply middleware
                    for middleware in framework.middleware:
                        request = middleware(request)
                        if hasattr(request, 'response'):
                            self.send_ludwig_response(request.response)
                            return
                    
                    # Check for static files
                    for static_path, static_dir in framework.static_routes.items():
                        if path.startswith(static_path):
                            return super().do_GET()
                    
                    # Find route handler
                    handler = framework.routes.get(path)
                    if handler:
                        response = handler(request)
                        self.send_ludwig_response(response)
                    else:
                        self.send_error(404, f"Route not found: {path}")
                
                except Exception as e:
                    self.send_error(500, f"Internal server error: {e}")
            
            def send_ludwig_response(self, response):
                """Send Ludwig response object."""
                if isinstance(response, LudwigResponse):
                    self.send_response(response.status_code)
                    for header, value in response.headers.items():
                        self.send_header(header, value)
                    self.end_headers()
                    self.wfile.write(response.content.encode('utf-8'))
                elif isinstance(response, str):
                    # Simple string response
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(response.encode('utf-8'))
                else:
                    # JSON response
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode('utf-8'))
        
        return LudwigHTTPHandler


class LudwigRequest:
    """Ludwig HTTP request object."""
    
    def __init__(self, method, path, query_params, handler):
        self.method = method
        self.path = path
        self.query_params = query_params
        self.handler = handler
        self.params = {}  # URL parameters
        self.form_data = {}  # Form data for POST requests
        
        # Parse form data for POST requests
        if method == 'POST':
            self._parse_form_data()
    
    def _parse_form_data(self):
        """Parse form data from POST request."""
        try:
            content_length = int(self.handler.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.handler.rfile.read(content_length).decode('utf-8')
                self.form_data = urllib.parse.parse_qs(post_data)
                # Convert single-item lists to values
                for key, value in self.form_data.items():
                    if len(value) == 1:
                        self.form_data[key] = value[0]
        except:
            pass


class LudwigResponse:
    """Ludwig HTTP response object."""
    
    def __init__(self, content="", status_code=200, headers=None):
        self.content = content
        self.status_code = status_code
        self.headers = headers or {'Content-type': 'text/html'}


class LudwigWeb:
    """Ludwig Web utilities and helpers."""
    
    @staticmethod
    def create_application(config=None):
        """Create a new Ludwig web application."""
        return LudwigWebFramework(config)
    
    @staticmethod
    def render(template_name, context=None):
        """Render an HTML template with context."""
        context = context or {}
        
        # Look for template in views directory
        template_path = os.path.join('views', template_name)
        
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple template rendering - replace {{ variable }} with values
            for key, value in context.items():
                content = content.replace('{{ ' + key + ' }}', str(value))
                content = content.replace('{{' + key + '}}', str(value))
            
            return LudwigResponse(content)
        else:
            return LudwigResponse(f"Template not found: {template_name}", 404)
    
    @staticmethod
    def json_response(data, status_code=200):
        """Return JSON response."""
        headers = {'Content-type': 'application/json'}
        content = json.dumps(data)
        return LudwigResponse(content, status_code, headers)
    
    @staticmethod
    def redirect(url, status_code=302):
        """Redirect to another URL."""
        headers = {'Location': url}
        return LudwigResponse("", status_code, headers)
    
    @staticmethod
    def error(status_code, message):
        """Return error response."""
        content = f"""
        <!DOCTYPE html>
        <html>
        <head><title>Error {status_code}</title></head>
        <body>
            <h1>Error {status_code}</h1>
            <p>{message}</p>
        </body>
        </html>
        """
        return LudwigResponse(content, status_code)
    
    @staticmethod
    def redirect_with_success(url, message):
        """Redirect with success message (stored in session)."""
        # For now, just redirect - session handling can be added later
        return LudwigWeb.redirect(url)
    
    @staticmethod
    def redirect_with_error(url, message):
        """Redirect with error message (stored in session)."""
        # For now, just redirect - session handling can be added later
        return LudwigWeb.redirect(url)


# Alias for compatibility
Web = LudwigWeb

# Example usage
if __name__ == "__main__":
    # Demo Ludwig web application
    app = Web.create_application({
        "name": "Ludwig Demo",
        "version": "1.0.0"
    })
    
    @app.route("/")
    def home(request):
        return Web.render("home.html", {
            "title": "Ludwig Web Framework",
            "message": "No Flask required - pure Ludwig!",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
    
    @app.route("/api/test")
    def api_test(request):
        return Web.json_response({
            "message": "Ludwig API works!",
            "framework": "Native Ludwig",
            "dependencies": "None - Pure Python!"
        })
    
    # Serve static files
    app.static("/css", "public/css")
    app.static("/js", "public/js")
    
    print("🚀 Starting Ludwig Demo Application")
    print("📦 Pure Python - No external dependencies!")
    app.run(port=8000, debug=True)
