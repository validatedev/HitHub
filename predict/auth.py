import requests


def getAuthenticationHeader():
    CLIENT_ID = '500445109a3147f6b55fcddf5fa5247c'
    CLIENT_SECRET = '9f50ec51bd4749d9b9bcda607d463d1a'
    AUTH_URL = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    header = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }

    return header;
