import webbrowser
import json
import requests
import pandas as pd
from stravalib.client import Client
import time
import datetime


class Authentication:
    def __init__(self, client_id, client_secret):
      client_id = self.client_id
      client_secret = self.client_secret



    def authorise(client_id, client_secret):
        token = Authentication.read_token()

        expires_at = datetime.datetime.fromtimestamp(token['expires_at'])
        print(f"expires in: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")

        token = Authentication.refresh_token(token, client_id, client_secret)

        return token


    def read_token():

        try:
            with open('strava_token_local.json', 'r') as f:
                token = json.load(f)

        except FileNotFoundError:

            # token cannot be found, so cannot be refreshed
            # instead, follow the original authorisation procedure again
            token = Authentication.initial_authorisation_token()

        return token


    def refresh_token(token, client_id, client_secret):

        # check if the token has expired
        if token['expires_at'] < time.time():
            print("Token not expired")
            try:
                # request a new access token using the refresh token
                token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                                    data={'client_id': client_id,
                                        'client_secret': client_secret,
                                        'grant_type': 'refresh_token',
                                        'refresh_token': token['refresh_token']})
                token = token.json()
                Authentication.write_token(token)
            except Exception as e:
                print("Error refreshing token:", e)
            
        return token

    def write_token(token):

        with open('strava_token_local.json', 'w') as file:
            json.dump(token, file)

    def initial_authorisation_token(client_id, client_secret):

        # client id and client secret can be given as string literals, but it 
        # is recommended to set them as environment variables instead, we can 
        # then access them as shown here

        # url the user is directed to once they have logged in
        redirect_uri = 'http://localhost:8000'
        
        # send request to server to authorize a user
        # this will prompt the user to sign into strava and grant our application permissions
        request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                                f'&response_type=code&redirect_uri={redirect_uri}' \
                                f'&approval_prompt=force' \
                                f'&scope=profile:read_all,activity:read_all'
        
        # open url in browser
        webbrowser.open(request_url)
        
        # recieve code once user has logged in
        code = input('Insert the code from the url: ')
        code = '8ed0d706d0ff7c82842cbba54b8851f481c1a92a'

        # Get the access token
        token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                            data={'client_id': client_id,
                                    'client_secret': client_secret,
                                    'code': code,
                                    'grant_type': 'authorization_code'})
        token = token.json()
        
        # save token for later (function shown below)
        Authentication.write_token(token)

        return token



