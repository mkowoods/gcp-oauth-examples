# Configuring OAUTH Authentication

### perhaps one of the worse features of GCP is configuring a *simple* security model for a REST API this project documents the steps for leveraging
### google's oauth2 based authentication model for an app engine API.

Example validating a backend token : https://developers.google.com/identity/sign-in/web/backend-auth
Documentation on just getting oauth flow working: https://stackoverflow.com/questions/10271110/python-oauth2-login-with-google
Google's test cases for oauth workflow(probably best reference): https://github.com/googleapis/google-auth-library-python/tree/master/tests/oauth2



Steps:
 - Login to console and navigate to APIS & Services > Credentials. Click Create Credentials > Other
 - run app `python main.py` and get the ID Token
 - verify the token here: https://oauth2.googleapis.com/tokeninfo?id_token=