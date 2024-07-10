from flask import Blueprint, redirect, render_template
import re
import requests

payload = {
    'grant_type': 'client_credentials',
    'client_id': "8645bb1a4b5547e8bf421540cb4f83cf",
    'client_secret': "7f2557a2198548df8fb3fe1710a7f5f8"
}
access_token = None

bp = Blueprint('spotify', __name__, url_prefix='/spotify')

@bp.route("/")
def spotify():
    global access_token
    if access_token is None:
        r = requests.post(
            url="https://accounts.spotify.com/api/token",
            data=payload,
            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        if 'access_token' in r.json():
            access_token = r.json().get('access_token')
            return render_template("spotify/index.html", data=r.json(), token=access_token)
    return render_template("spotify/index.html", token=access_token)

@bp.route("/tracks")
def get_track():
    if access_token is None:
        return redirect("/spotify")
    else:
        r = requests.get(
            url="https://api.spotify.com/v1/tracks/11dFghVXANMlKmJXsNCbNl",
            headers={'Authorization': "Bearer " + access_token})
        if r.status_code == 200:
            json = r.json()
            title = json.get('name')
            title_link = json['external_urls']['spotify']
            artist = json.get('artists')[0]
            artist_name = artist.get('name')
            artist_link = artist['external_urls']['spotify']
            return render_template("/spotify/track.html", title=title, title_link=title_link, artist_name=artist_name, artist_link=artist_link)
    return redirect("/")

@bp.route("/validate")
def validate():
    pattern = '(\w{20,30})'
    text = 'https://open.spotify.com/track/6rqhFgbbKwnb9MLmUQDhG6'
    if match := re.search(pattern, text, re.IGNORECASE):
      title = match.group(1)
    # hello


