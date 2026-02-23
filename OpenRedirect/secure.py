from flask import Flask, request, redirect, url_for, abort
from urllib.parse import urlparse
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# Allowlist of trusted hosts for redirects
ALLOWED_HOSTS = {'yoursite.com', 'www.yoursite.com'}

def is_authenticated_user():
    # This function checks if the user is authenticated and is omitted for brevity
    pass

def is_safe_redirect(url: str) -> bool:
    """Validate redirect URL to prevent open redirect attacks."""
    try:
        parsed = urlparse(url)
        # Allow only relative URLs or URLs from trusted hosts
        return not parsed.netloc or parsed.netloc in ALLOWED_HOSTS
    except ValueError:
        return False

@app.route('/')
def home():
    if not is_authenticated_user():
        logging.warning('Unauthorized access attempt from IP: %s', request.remote_addr)
        return redirect(url_for('login'))

    redirect_url = request.args.get('redirect_url')
    if redirect_url:
        if not is_safe_redirect(redirect_url):
            logging.warning('Blocked unsafe redirect attempt to: %s from IP: %s',
                            redirect_url, request.remote_addr)
            abort(400)  # Bad request — reject unsafe redirects explicitly
        logging.info('Redirecting to: %s', redirect_url)
        return redirect(redirect_url, code=302)

    return "Welcome to home page!"

@app.route('/login')
def login():
    # Simulated login page
    return 'Login page - User authentication goes here.'

if __name__ == '__main__':
    app.run(debug=False)