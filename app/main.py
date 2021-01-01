from flask import Flask, render_template, redirect, url_for, session
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = 'random secret'


# OAuth Config
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    acess_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope':'openid profile email'},
)

@app.route("/")
def home():
    email = dict(session).get('email', None)
    return f'<h1 style="text-align:center;">Hellow {email}</h1>'


@app.route("/login")
def login():
    google = oauth.create_client('google') 
    redirect_url = url_for('authorize', _external=True)
    return oauth.twitter.authorize_redirect(redirect_url)


@app.route("/authorize")
def authorize():
    google = oauth.create_client('google') 
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    # Do something with the token and profile
    return redirect("/")




if __name__ == '__main__':
    app.run(debug=True)