"""
The purpose of this module is to simply fetch the users credentials. 
There's a seperate module for using those credentials to make requests. 

This is a one-time operation

Relevant Documentation:
https://github.com/googleapis/google-api-python-client/blob/master/docs/client-secrets.md
https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html

"""

import argparse
import datetime
import json

from google_auth_oauthlib.flow import InstalledAppFlow

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Commad Line argumet ')
    parser.add_argument('--client-secrets-path', action="store", dest="client_secrets_path")
    parser.add_argument('--user-credentials-ouput-dir', action="store")
    results = parser.parse_args()


    flow = InstalledAppFlow.from_client_secrets_file(
        results.client_secrets_path,
        scopes="https://www.googleapis.com/auth/userinfo.email openid"
    )

    #this will return the credential object
    credentials = flow.run_console() #https://google-auth.readthedocs.io/en/stable/reference/google.oauth2.credentials.html#google.oauth2.credentials.Credentials

    #this saves the user access token and refresh token to 
    path = None
    if results.user_credentials_ouput_dir:
        path = '{}/credentials.json'.format(results.user_credentials_ouput_dir)

    if path is None:
        print('\n\n############ credentials.json ####################\n\n')
        print(json.dumps(credentials.__dict__, default=default))
        print('\n\n')
    else:
        json.dump(credentials.__dict__, open(path, 'w'), default=default)
        print('Successfully Stored User Secrets', path)
    

