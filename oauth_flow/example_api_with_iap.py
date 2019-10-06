
import argparse
import json
import os

from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google.auth.transport.requests import AuthorizedSession
from google.cloud import storage
import requests

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def credentials_to_dict(credentials):
  return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
        }

def refresh_iap_credentials(credentials: Credentials, iap_client_id: str) -> dict:

    #https://cloud.google.com/iap/docs/authentication-howto#authenticating_from_a_desktop_app
    #https://stackoverflow.com/questions/54717074/accessing-google-cloud-iap-protected-resource-with-bearer-token-gives-error-code
    data = {
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'refresh_token': credentials.refresh_token,
        'grant_type': 'refresh_token',
        'audience': iap_client_id
    }
    resp = requests.post('https://www.googleapis.com/oauth2/v4/token', data=data)
    if resp.ok:
        return resp.json()

def get_credentials(client_secrets_path):
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secrets_path,
        scopes="https://www.googleapis.com/auth/userinfo.email openid"
    )

    #this will return the credential object
    credentials = flow.run_console()
    return credentials


if __name__ == "__main__":

    DEMO_URL='https://dev-testing-features.appspot.com'

    parser = argparse.ArgumentParser(description='Commad Line argumet ')
    parser.add_argument('--client-secrets-path', action="store", dest="client_secrets_path", help="/secrets/client_secrets.json") 
    parser.add_argument('--user-credentials-ouput-dir', action="store")
    parser.add_argument('--user-secrets')
    parser.add_argument('--iap-client-id')
    args = parser.parse_args()

    if args.user_secrets is None:
        credentials = get_credentials(args.client_secrets_path) 
        try:
            json.dump(credentials_to_dict(credentials), open(os.path.join(args.user_credentials_output_dir, 'user_secrets_iap.json'), 'wb'))
        except Exception as e:
            print(e)
    else:
        credentials = Credentials(**json.load(open(args.user_secrets, 'rb')))

    credentials = refresh_iap_credentials(credentials, args.iap_client_id)
    id_token = credentials['id_token']
    print(id_token)
    response = requests.get(DEMO_URL, 
                headers = {
                    'Authorization': 'Bearer {id_token}'.format(id_token=id_token)
                    })
    print(response.status_code, response.content)

    
