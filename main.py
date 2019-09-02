import logging
import os
from flask import Flask, jsonify, render_template
from google.oauth2 import id_token
from google.auth.transport import requests

import auth
from config import CLIENT_ID


app = Flask(__name__)

@app.route('/')
def hello():
    """
    Google Signin Example, jwt and auth token are printed to console
    """
    return render_template('google-signin.html', client_id=CLIENT_ID)

@app.route('/api/hello')
def api_hello():
    return 'API Hello World!'


@app.route('/api/jwt-auth-hello')
@auth.jwt_authentication
def api_hello_jwt_auth():
    """
    This Endpoint requires a valid authentication token and correct email domain
    """
    return jsonify('API Hello JWT Authentication!')

@app.route('/api/get_claims/<token>')
def parse_claims(token):
    """
    validates and returns JWT Claims
    """
    try:
        idinfo = auth.validate_claims(token, client_id=CLIENT_ID)
    except ValueError as e:
        logging.error(e)
        return jsonify('Token Error'), 400
    return jsonify(idinfo)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == "__main__":
    app.run(debug=True)

