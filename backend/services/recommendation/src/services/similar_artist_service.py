import requests
client_id = '300cdf3993c94b429d91a6e4338a5aa7'
client_secret = '0ea1f07f5b1a473c9932b713a232ef22'
# artist_id = 'spotify:artist:0123456789'


def get_spotify_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        # Parse the JSON response and extract the access token
        access_token = response.json().get('access_token')
        return access_token
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_artist_id_by_name(artist_name, access_token):
    url = 'https://api.spotify.com/v1/search'
    params = {
        'q': artist_name,
        'type': 'artist',
        'limit': 1 
    }
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        artists = response.json()['artists']['items']
        if artists:
            return artists[0]['id']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None
    

def get_similar_artists(artist_id, access_token):
    url = f'https://api.spotify.com/v1/artists/{artist_id}/related-artists'
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()['artists']
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_similar_artists_by_name(artist_name):
    similar_artists_list = []
    access_token = get_spotify_access_token(client_id, client_secret)
    k  = 0
    if access_token:
        artist_id = get_artist_id_by_name(artist_name, access_token)
        if artist_id:
            similar_artists = get_similar_artists(artist_id, access_token)
            for artist in similar_artists:
                if k > 30:
                    break
                if isinstance(artist, dict) :
                    if 'name' in artist.keys() and '\'' not in artist['name']: 
                        similar_artists_list.append(artist['name'])
                        k = k + 1
  
    return similar_artists_list