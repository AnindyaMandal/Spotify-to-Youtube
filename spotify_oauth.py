import base64
import math
import os
import hashlib
import requests
from urllib.parse import urlencode
import webbrowser
import random as rand
import http_server
import re
from dotenv import load_dotenv


# Not sure if I should be using random. Is it cryptographically safe?


def generate_random_string(length):
    text = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for i in range(length):
        text += possible[(math.floor(rand.random() * len(possible)))]

    return text


# Stolen from https://www.stefaanlippens.net/oauth-code-flow-pkce.html


def generate_code_challenge(code_verifier):
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8')
    code_challenge = code_challenge.replace('=', '')
    return code_challenge


# JS EQUIVALENT FROM https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
"""
#
# async function generateCodeChallenge(codeVerifier) {
#   function base64encode(string) {
#     return btoa(String.fromCharCode.apply(null, new Uint8Array(string)))
#       .replace(/\+/g, '-')
#       .replace(/\//g, '_')
#       .replace(/=+$/, '');
#   }

#   const encoder = new TextEncoder();
#   const data = encoder.encode(codeVerifier);
#   const digest = await window.crypto.subtle.digest('SHA-256', data);

#   return base64encode(digest);
# }
"""


def auth():
    load_dotenv()

    spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
    spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
    spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
    scope = "playlist-modify-private user-library-read"
    code_verifier = generate_random_string(128)

    challenge = generate_code_challenge(code_verifier)
    state = generate_random_string(16)

    # print("Challenge: " + challenge, len(challenge))
    # print("Code Verifier: " + code_verifier)

    os.environ['CODE_VERIFIER'] = code_verifier

    auth_headers = {
        "response_type": "code",
        "client_id": spotify_client_id,
        "scope": scope,
        "redirect_uri": spotify_redirect_uri,
        "state": state,
        "code_challenge_method": "S256",
        "code_challenge": challenge,
    }

    # r = requests.get("https://accounts.spotify.com/authorize?" +
    #                  urlencode(auth_headers))

    # print(r)

    webbrowser.open("https://accounts.spotify.com/authorize?" +
                    urlencode(auth_headers))

    http_server.get_codestate()

    # print("PRINTING ENVS AFTER DATA RECV\n\n")
    # print("\t" + os.environ['SPOTIFY_CODE'])
    # print("\t" + os.environ['SPOTIFY_STATE'])

    access_headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # print(os.environ['SPOTIFY_CODE'])

    access_payload = {
        'grant_type': 'authorization_code',
        'code': os.environ['SPOTIFY_CODE'],
        'redirect_uri': spotify_redirect_uri,
        'client_id': spotify_client_id,
        'code_verifier': os.environ['CODE_VERIFIER']
    }

    access_uri = 'https://accounts.spotify.com/api/token'

    response = requests.post(
        access_uri, data=access_payload, headers=access_headers)

    print(response.status_code)
    print(response.reason)

    response_utf8 = response.content.decode("utf-8")
    # print(response_utf8)

    access_token = re.search(r'(?<={"access_token":").*?(?=","token_type":)',
                                response_utf8).group()
    print("\n" + access_token)

    os.environ['SPOTIFY_ACCESS_TOKEN'] = access_token

    base_uri = 'https://api.spotify.com/v1'
    profile_uri = 'https://api.spotify.com/v1/me'

    response = requests.get(profile_uri, headers={
        'Authorization': 'Bearer ' + access_token
    })

    user_id = re.search(r'(?<="id" : ").*?(?=",)', response.content.decode("utf-8")).group()
    print("USER ID: " + user_id)

    os.environ['SPOTIFY_USER_ID'] = user_id

    print(response.content.decode("utf-8"))
