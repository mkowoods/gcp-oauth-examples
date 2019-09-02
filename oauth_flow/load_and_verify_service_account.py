"""
Documentations for Service Accounts

https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.service_account.html#module-google.oauth2.service_account

https://developers.google.com/identity/protocols/OAuth2#serviceaccount
"""

import argparse
import json

from google.cloud import storage
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.id_token import verify_oauth2_token, verify_token
import requests

SCOPES = ['https://www.googleapis.com/auth/userinfo.email']


def verify_service_account_token(token):
    resp = requests.get('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(credentials.token))
    return resp.json()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argments to module')
    parser.add_argument('--path', action="store", dest="path")
    parser.add_argument('--test-api', action='store_true')
    results = parser.parse_args()

    #credentials = service_account.Credentials.from_service_account_file(results.path, scopes=['email'])
    
    credentials = service_account.Credentials.from_service_account_file(results.path, scopes=SCOPES)
    
    print(credentials.__dict__)
    credentials.refresh(Request())
    print(credentials.__dict__)

    print('\n\n###############  Verifying Tokens  #####################\n\n')
    claims = verify_service_account_token(credentials.token)
    print(claims)


    if results.test_api:
        print('Testing ')
        credentials = service_account.Credentials.from_service_account_file(results.path, scopes=SCOPES)
        credentials.refresh(Request())
        #headers={'Authorization: Bearer {token}'.format(creds.id_token)}
        print('\n\n################ Test Header #################\n\n')
        resp = requests.get('http://localhost:5000/api/jwt-auth-hello', headers={
            'Authorization': 'Bearer {token}'.format(token=credentials.token),
            'Authorization-Type': 'service_account'
        })
        print('Status Code: {}\n'.format(resp.status_code))
        print(resp.json())

#    import google.oauth2.credentials
#    print(google.oauth2.credentials.Credentials(credentials.token).refresh(Request()))
    #print(verify_oauth2_token(credentials.token, Request()), '103284928966445054496')

#    storage_client = storage.Client(project='dev-testing-features', credentials=credentials)