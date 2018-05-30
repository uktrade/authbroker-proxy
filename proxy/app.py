import os
from urllib.parse import urljoin

from flask import Flask, redirect, url_for, session, request, jsonify, abort, make_response
from flask_oauthlib.client import OAuth

from raven.contrib.flask import Sentry


ABC_CLIENT_ID = os.getenv('ABC_CLIENT_ID')
ABC_CLIENT_SECRET = os.getenv('ABC_CLIENT_SECRET')
ABC_BASE_URL = os.getenv('ABC_BASE_URL')
ABC_TOKEN_URL = urljoin(ABC_BASE_URL, '/o/token/')
ABC_AUTHORIZE_URL = urljoin(ABC_BASE_URL, '/o/authorize/')
ABC_INTROSPECT_URL = urljoin(ABC_BASE_URL, '/o/introspect/')

ABC_REDIRECT_HOST = os.getenv('ABC_REDIRECT_HOST', 'http://localhost')

PORT = int(os.getenv('PORT', 5000))


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.debug = os.getenv('DEBUG') == 'True'
oauth = OAuth(app)
sentry = Sentry(app, dsn=os.getenv('SENTRY_DSN'))

abc = oauth.remote_app(
   'abc',
   base_url=ABC_BASE_URL,
   request_token_url=None,
   access_token_url=ABC_TOKEN_URL,
   authorize_url=ABC_AUTHORIZE_URL,
   consumer_key=ABC_CLIENT_ID,
   consumer_secret=ABC_CLIENT_SECRET,
   access_token_method='POST'
)


@app.route('/auth/login')
def login():
    redirect_url = urljoin(ABC_REDIRECT_HOST, url_for('authorized'))
    return abc.authorize(callback=redirect_url)


@app.route('/auth/check')
def check():
    """
    Verify that a token is authenticated for use with nginx's auth_request directive.
    This view should only return either a 202 or a 401 response.
    """

    # TODO: cache ABC response for specified time period, e.g. 1 minute
    # to minimise number of calls to the ABC introspec view.

    if 'abc_token' in session:

        # Better to have a lightweight auth check endpoint on the ABC, rather than hitting 
        # the profile url
        me = abc.get('/api/v1/user/me/')
        if me.status == 200:
            response = make_response('OK', 202)
            response.headers['Authbroker-user-id'] = me.data['email']
            return response

    abort(401)


@app.route('/auth/response')
def authorized():
    resp = abc.authorized_response()

    if resp is None or resp.get('access_token') is None:
        app.logger.info('Failed login: {}'.format(request.remote_addr))
        abort(401)

    app.logger.info('Authenticated: {} {}'.format(resp['email'], request.remote_addr))

    session['abc_token'] = (resp['access_token'], '')

    return redirect(ABC_REDIRECT_HOST)


@abc.tokengetter
def get_abc_oauth_token():
    return session.get('abc_token')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)

