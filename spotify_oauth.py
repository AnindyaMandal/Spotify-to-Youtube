import base64
import math
import os
import hashlib
import requests
from urllib.parse import urlencode
import webbrowser
import random as rand
import http_server
from dotenv import load_dotenv


# Not sure if I should be using random. Is it cryptographically safe?


def generate_random_string(length):
    text = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for i in range(length):
        text += possible[(math.floor(rand.random() * len(possible)))]

    return text


# Stolen from https://www.stefaanlippens.net/oauth-code-flow-pkce.html


def generate_code_challenge():
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

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
scope = "playlist-modify-private"
code_verifier = generate_random_string(128)


challenge = generate_code_challenge()
state = generate_random_string(16)

print("Challenge: " + challenge, len(challenge))
print("Code Verifier: " + code_verifier)

os.environ['CODE_VERIFIER'] = code_verifier

# print(os.environ)

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

print("PRINTING ENVS AFTER DATA RECV\n\n")
print("\t" + os.environ['SPOTIFY_CODE'])
print("\t" + os.environ['SPOTIFY_STATE'])
