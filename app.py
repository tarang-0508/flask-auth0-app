from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from urllib.parse import urlencode

app = Flask(__name__)
app.secret_key = "6nHBeY432dq9OaUKB8G4v-y1scEJ1XB6-jVVjwKgFxM"

# Auth0 configuration
AUTH0_CLIENT_ID = "RIdEBneDUB8QPx5CkKglX3ZDbhMbqcKE"
AUTH0_CLIENT_SECRET = "ZqGf0w_6mXbi3KPZKE1FTYcC0nBCgFzraB6RZd7mmfs0jR4LhilXI6HTTNVFUZ1z"
AUTH0_DOMAIN = "tarang5.ca.auth0.com"
AUTH0_CALLBACK_URL = "http://127.0.0.1:5000/callback"


# Initialize OAuth
oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration',
    redirect_uri=AUTH0_CALLBACK_URL
)

# Home route
@app.route('/')
def home():
    return '''
        <h2>Hello from Flask with Auth0!</h2>
        <a href="/login"> Login</a> 
    '''

# Login route
@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL)

# Callback route
@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()
    session['user'] = token['userinfo']
    return redirect('/profile')

# Profile route
@app.route('/profile')
def profile():
    user = session.get('user')
    if user:
        return jsonify(user)
    return redirect('/')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(
        f'https://{AUTH0_DOMAIN}/v2/logout?' + urlencode({
            'returnTo': url_for('home', _external=True),
            'client_id': AUTH0_CLIENT_ID
        })
    )

if __name__ == '__main__':
    app.run(debug=True)
