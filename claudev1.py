from creds import cid, secret
import requests
import base64

# Encode client ID and client secret
client_creds = f"{cid}:{secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

# Get access token
token_url = 'https://accounts.spotify.com/api/token'
headers = {
    'Authorization': f'Basic {client_creds_b64.decode()}'
}
data = {
    'grant_type': 'client_credentials'
}
r = requests.post(token_url, headers=headers, data=data)
token = r.json()['access_token']

# Use the token to fetch the user's top tracks
top_tracks_url = 'https://api.spotify.com/v1/me/top/tracks'
headers = {
    'Authorization': f'Bearer {token}'
}
params = {
    'time_range': 'medium_term',  # Options: short_term, medium_term, long_term
    'limit': 10  # Number of tracks to fetch
}
r = requests.get(top_tracks_url, headers=headers, params=params)

if r.status_code == 200:
    print("Successfully fetched top tracks!")
    tracks = r.json()['items']
    print("\nYour top 10 tracks:")
    for i, track in enumerate(tracks, 1):
        print(f"{i}. {track['name']} by {track['artists'][0]['name']}")
elif r.status_code == 401:
    print("Error: Unauthorized. The token might not have the required scopes.")
    print("You may need to use user authentication (OAuth) for this endpoint.")
else:
    print(f"Failed to retrieve top tracks. Status code: {r.status_code}")
    print(f"Error message: {r.text}")