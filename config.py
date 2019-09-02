import os

CLIENT_ID =  os.environ['CLIENT_ID'] #Client ID for Oauth2.0 Client set on GCP
PROJECT_ID = os.environ['PROJECT_ID'] #PROJECT_ID used to validate service accounts by project

print('\n\n')
print('CLIENT_ID:',CLIENT_ID)
print('PROJECT_ID:',PROJECT_ID)
print('\n\n')