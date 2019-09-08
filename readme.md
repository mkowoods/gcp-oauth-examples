# Configuring OAUTH Authentication

### Perhaps one of the hardest things to do on GCP is configuring a *simple* security model for a REST API this project documents the steps for leveraging
### google's oauth2 based authentication model for an app engine API.

TODO: 
 - How do you validate Audience for Service Account? Confused Deputy Problem: https://stackoverflow.com/questions/17241771/how-and-why-is-google-oauth-token-validation-performed



 FAQ:
  - How Do I get the client_secrets.json?
   - Login to console and navigate to APIS & Services > Credentials. Click Create Credentials > Other. Once Created you can now Download as JSON
  
  - How Do I get the user_secrets.json?
   - Using your client_secrets.json, example: 
     - `python ./oauth_flow/fetch_user_credentials.py --client-secrets-path=./secrets/client_secrets.json --user-credentials-ouput-dir=/tmp`
     - `python ./oauth_flow/load_and_verify_user_credentials.py --path=/tmp/credentials.json --test-api`
  - What are Scopes and what are the options?
    - https://developers.google.com/identity/protocols/googlescopes
    - Note: For configuring support for internal services use: https://www.googleapis.com/auth/userinfo.email


  - How do I authenticate a service account?
   - `python ./oauth_flow/load_and_verify_service_account.py --path=./secrets/service_account_secrets.json --test-api`

Good Highlevel Explanation of JWT and there purpose: https://medium.com/vandium-software/5-easy-steps-to-understanding-json-web-tokens-jwt-1164c0adfcec

Example validating a backend token : https://developers.google.com/identity/sign-in/web/backend-auth

Documentation on just getting oauth flow working: https://stackoverflow.com/questions/10271110/python-oauth2-login-with-google

Google's test cases for oauth workflow(probably best reference): https://github.com/googleapis/google-auth-library-python/tree/master/tests/oauth2

Good Medium Post, but out of date: https://medium.com/@ashokyogi5/a-beginners-guide-to-google-oauth-and-google-apis-450f36389184

Additional Documentation: https://github.com/salrashid123/gcpsamples/tree/master/auth/tokens
