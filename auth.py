import functools
import logging
import os

from flask import request, abort, jsonify
from google.oauth2 import id_token
from google.auth.transport import requests

from config import CLIENT_ID

WHITE_LIST_DOMANS = ['gmail.com']

def check_domain(email):
    return email.split('@')[1] in WHITE_LIST_DOMANS

def validate_claims(token: str, client_id: str = CLIENT_ID) -> dict:
    # Specify the CLIENT_ID of the app that accesses the backend:
    assert client_id is not None

    idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)

    # Or, if multiple clients access the backend server:
    # idinfo = id_token.verify_oauth2_token(token, requests.Request())
    # if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
    #     raise ValueError('Could not verify audience.')

    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise ValueError('Wrong issuer.')

    # If auth request is from a G Suite domain:
    # if idinfo['hd'] != GSUITE_DOMAIN_NAME:
    #     raise ValueError('Wrong hosted domain.')

    # ID token is valid. Get the user's Google Account ID from the decoded token.
    userid = idinfo['sub']

    return idinfo

def jwt_authentication(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        # Do something with your request here
        bearer_token = request.headers.get('Authorization')
        if bearer_token is None:
            return jsonify('Not Authorized'), 401

        kw, id_token = bearer_token.split(' ')
        if kw != 'Bearer':
            return jsonify('Not Authorized'), 401
        
        try:
            claims = validate_claims(id_token) 
        except ValueError as e:
            logging.error(e)
            return jsonify('Not Authorized'), 401

        is_authenticated = check_domain(claims['email'])                
        if not is_authenticated:
            return jsonify('Not Authorized'), 401

        return f(*args, **kwargs)
    return decorated_function