import base64, math, os, hashlib
import random as rand

from dotenv import load_dotenv
load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")

def generate_random_string(length):
    text = ''
    possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

    for i in range(length):
        text += possible[(math.floor(rand.random() * len(possible)))]

    return text


def generate_code_challenge(code_verifier):
    def base64_encode(string):
        string.join(map(unichr, [65,66,67]))



print(generate_random_string(128))

auth_headers = {
    "client_id" : spotify_client_id,
    "response_type" : "code",
    "redirect_uri" : spotify_redirect_uri,
    "scope" : "playlist-modify-private"
}