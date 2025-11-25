"""
OAuth Callback Server
Local Flask server to handle Spotify OAuth callbacks
"""

from flask import Flask, request, render_template_string
import threading
import time
import os
from pathlib import Path
from typing import Optional


class OAuthCallbackServer:
    """Simple Flask server to handle OAuth callbacks"""
    
    def __init__(self, port: int = 8888):
        self.port = port
        self.app = Flask(__name__)
        self.server_thread = None
        self.auth_code = None
        self.error = None
        self.received = False
        self.temp_file = Path(__file__).parent.parent / "temp_oauth_code.txt"
        
        # Setup routes
        self.app.add_url_rule('/callback', 'callback', self.handle_callback)
        
        # Disable Flask logging
        import logging
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
    
    def handle_callback(self):
        """Handle OAuth callback from Spotify"""
        # Get authorization code or error
        self.auth_code = request.args.get('code')
        self.error = request.args.get('error')
        self.received = True
        
        # Save code to temp file for Streamlit to read
        if self.auth_code:
            with open(self.temp_file, 'w') as f:
                f.write(self.auth_code)
        
        # Return success page
        if self.auth_code:
            return self._success_page()
        else:
            return self._error_page(self.error or "Unknown error")
    
    def _success_page(self):
        """HTML page shown on successful authorization"""
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Spotify Authorization Successful</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #1DB954 0%, #191414 100%);
                    }
                    .container {
                        text-align: center;
                        background: white;
                        padding: 50px;
                        border-radius: 20px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                        max-width: 500px;
                    }
                    h1 {
                        color: #1DB954;
                        margin-bottom: 20px;
                        font-size: 32px;
                    }
                    p {
                        color: #333;
                        font-size: 18px;
                        margin: 20px 0;
                    }
                    .checkmark {
                        font-size: 80px;
                        margin-bottom: 20px;
                    }
                    .close-note {
                        color: #666;
                        font-size: 14px;
                        margin-top: 30px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="checkmark">✓</div>
                    <h1>Successfully Connected!</h1>
                    <p>Your Spotify account has been authorized.</p>
                    <p>You can now close this window and return to the app.</p>
                    <div class="close-note">This window will close automatically in 3 seconds...</div>
                </div>
                <script>
                    setTimeout(function() {
                        window.close();
                    }, 3000);
                </script>
            </body>
            </html>
        ''')
    
    def _error_page(self, error_message):
        """HTML page shown on authorization error"""
        return render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Spotify Authorization Failed</title>
                <style>
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        height: 100vh;
                        margin: 0;
                        background: linear-gradient(135deg, #E74C3C 0%, #191414 100%);
                    }
                    .container {
                        text-align: center;
                        background: white;
                        padding: 50px;
                        border-radius: 20px;
                        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
                        max-width: 500px;
                    }
                    h1 {
                        color: #E74C3C;
                        margin-bottom: 20px;
                        font-size: 32px;
                    }
                    p {
                        color: #333;
                        font-size: 18px;
                        margin: 20px 0;
                    }
                    .error-icon {
                        font-size: 80px;
                        margin-bottom: 20px;
                    }
                    .error-detail {
                        background: #f8f8f8;
                        padding: 15px;
                        border-radius: 5px;
                        color: #666;
                        font-size: 14px;
                        margin-top: 20px;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="error-icon">✗</div>
                    <h1>Authorization Failed</h1>
                    <p>Could not connect to Spotify.</p>
                    <div class="error-detail">Error: {{ error }}</div>
                    <p style="margin-top: 30px;">Please close this window and try again.</p>
                </div>
            </body>
            </html>
        ''', error=error_message)
    
    def start(self):
        """Start the callback server in a background thread"""
        # Clean up any existing temp file
        if self.temp_file.exists():
            self.temp_file.unlink()
        
        # Start server in daemon thread
        self.server_thread = threading.Thread(
            target=self._run_server,
            daemon=True
        )
        self.server_thread.start()
        
        # Give server time to start
        time.sleep(0.5)
    
    def _run_server(self):
        """Run the Flask server"""
        try:
            self.app.run(
                host='127.0.0.1',
                port=self.port,
                debug=False,
                use_reloader=False,
                threaded=True
            )
        except Exception as e:
            self.error = str(e)
    
    def wait_for_callback(self, timeout: int = 60) -> Optional[str]:
        """
        Wait for the OAuth callback to be received
        
        Args:
            timeout: Maximum seconds to wait
            
        Returns:
            Authorization code if received, None if timeout or error
        """
        start_time = time.time()
        
        while not self.received:
            if time.time() - start_time > timeout:
                return None
            time.sleep(0.1)
        
        return self.auth_code
    
    def get_code_from_file(self) -> Optional[str]:
        """
        Read authorization code from temp file
        
        Returns:
            Authorization code if available
        """
        try:
            if self.temp_file.exists():
                with open(self.temp_file, 'r') as f:
                    code = f.read().strip()
                # Clean up temp file
                self.temp_file.unlink()
                return code
        except Exception:
            pass
        return None
    
    def stop(self):
        """Stop the server (Flask doesn't support clean shutdown easily)"""
        # Clean up temp file
        if self.temp_file.exists():
            try:
                self.temp_file.unlink()
            except:
                pass


def start_callback_server(port: int = 8888) -> OAuthCallbackServer:
    """
    Start OAuth callback server
    
    Args:
        port: Port to run server on (default 8888)
        
    Returns:
        OAuthCallbackServer instance
    """
    server = OAuthCallbackServer(port)
    server.start()
    return server

