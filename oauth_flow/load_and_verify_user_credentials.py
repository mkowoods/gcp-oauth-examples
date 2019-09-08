import argparse
import json
import logging

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token
import requests



#https://oauth2.googleapis.com/tokeninfo?id_token=

def get_credentials_from_user_file(fname):
    # Documentation:
    # https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials

    #TODO: swith to using Credentials.from_authorized_user_file(fname)
    user_credentials = json.load(open(fname))
    return Credentials(
        token=user_credentials['token'],
        refresh_token=user_credentials['_refresh_token'],
        token_uri=user_credentials['_token_uri'],
        client_id=user_credentials['_client_id'],
        client_secret=user_credentials['_client_secret'],
        id_token=user_credentials['_id_token']
    )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arguments')
    parser.add_argument('--path', action="store", dest="path")
    parser.add_argument('--test-api', action='store_true')
    results = parser.parse_args()
    

    creds = get_credentials_from_user_file(results.path)
    creds.refresh(Request())
    print('Verifying Tokens')
    print(verify_oauth2_token(creds.id_token, Request()))

    if results.test_api:
        print('Testing ')
        creds = get_credentials_from_user_file(results.path)
        creds.refresh(Request())
        #headers={'Authorization: Bearer {token}'.format(creds.id_token)}
        resp = requests.get('http://localhost:5000/api/get_claims/{token}'.format(token=creds.id_token))
        print('############ API RESPONSE ##################\n')
        print('Status Code: {}\n'.format(resp.status_code))
        print(resp.json())

        print('\n\n################ Test Header #################\n\n')
        resp = requests.get('http://localhost:5000/api/jwt-auth-hello', headers={'Authorization': 'Bearer {token}'.format(token=creds.id_token)})
        print('Status Code: {}\n'.format(resp.status_code))
        print(resp.json())


        print('\n\n################ Test Header With Stale Token 400 #################\n\n')
        creds = get_credentials_from_user_file(results.path)
        resp = requests.get('http://localhost:5000/api/jwt-auth-hello', headers={'Authorization': 'Bearer {token}'.format(token=creds.id_token)})
        print('Status Code: {}\n'.format(resp.status_code))
        print(resp.json())


        print('\n\n################ Test Access Token #################\n\n')
        creds = get_credentials_from_user_file(results.path)
        creds.refresh(Request())
        print(creds.token)
        resp = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(creds.token))
        print(resp.json())