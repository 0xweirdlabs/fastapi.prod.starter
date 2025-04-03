from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import requests
import os
from dotenv import load_dotenv
import logging

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For session management
load_dotenv('.env.local')

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Get URLs from environment
BACKEND_URL = os.getenv('BACKEND_URL', 'http://127.0.0.1:8000')

@app.route('/')
def home():
    logger.debug(f"Session token: {session.get('access_token')}")
    if 'access_token' in session:
        logger.debug("User is logged in")
        return redirect(url_for('profile'))
    logger.debug("User is not logged in")
    
    # Get auth URL from backend
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/auth/login/google")
        response.raise_for_status()
        auth_data = response.json()
        logger.debug(f"Got auth data from backend: {auth_data}")
        auth_url = auth_data.get('authorization_url')
        
        if not auth_url:
            logger.error("No auth URL received from backend")
            return render_template('login.html', error="Failed to get auth URL")
            
        return render_template('login.html', auth_url=auth_url)
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error getting auth URL: {str(e)}")
        return render_template('login.html', error="Error getting auth URL")

@app.route('/auth-callback')
def auth_callback():
    logger.debug("Handling auth callback")
    logger.debug(f"Request args: {request.args}")
    
    # Get the token from the URL
    token = request.args.get('token')
    error = request.args.get('error')
    
    if error:
        logger.error(f"Auth error: {error}")
        return render_template('login.html', error=error)
    
    if not token:
        logger.error("No token provided")
        return render_template('login.html', error="No token received")
    
    try:
        logger.debug("Storing token in session")
        logger.debug(f"Token type: {type(token)}")
        logger.debug(f"Token preview: {token[:10]}..." if len(token) > 10 else token)
        
        # Store token in session
        session['access_token'] = token
        logger.debug(f"Stored token in session")
        
        # Verify token by fetching user data
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        logger.debug(f"Making request to backend with token")
        # Get user data from backend
        response = requests.get(
            f"{BACKEND_URL}/api/v1/auth/me",
            headers=headers
        )
        
        logger.debug(f"Backend response status: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            logger.debug(f"Successfully verified token with user data: {user_data}")
            return render_template('profile.html', user=user_data)
        else:
            logger.error(f"Token verification failed: {response.text}")
            session.pop('access_token', None)
            return render_template('login.html', error="Token verification failed")
            
    except Exception as e:
        import traceback
        logger.error(f"Error during auth: {str(e)}")
        logger.error(traceback.format_exc())
        session.pop('access_token', None)
        return render_template('login.html', error=str(e))

@app.route('/profile')
def profile():
    logger.debug(f"Accessing profile with session token: {session.get('access_token')}")
    
    if 'access_token' not in session:
        logger.debug("No token in session, redirecting to login")
        return redirect(url_for('home'))
    
    headers = {
        'Authorization': f'Bearer {session["access_token"]}'
    }
    
    try:
        # Get user data from backend
        response = requests.get(
            f"{BACKEND_URL}/api/v1/auth/me",
            headers=headers
        )
        
        if response.status_code == 200:
            user_data = response.json()
            logger.debug(f"Fetched user data: {user_data}")
            return render_template('profile.html', user=user_data, session=session)
        else:
            logger.error(f"Failed to get user data: {response.text}")
            session.pop('access_token', None)
            return redirect(url_for('home'))
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching user data: {str(e)}")
        session.pop('access_token', None)
        return redirect(url_for('home'))

@app.route('/logout')
def logout():
    logger.debug("Logging out")
    session.pop('access_token', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
