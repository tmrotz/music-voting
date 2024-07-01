from flask import Flask, flash, redirect, render_template, request
from songs_model import Song

Song.load_db()

app = Flask(__name__)

app.secret_key = b'hypermedia rocks'

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/songs")
def songs():
    search = request.args.get("q")
    if search is not None:
        songs_set = Song.search(search)
    else:
        songs_set = Song.all()
    return render_template("index.html", songs=songs_set)

@app.route("/songs/new", methods=['GET'])
def new_song():
    return render_template("new.html", song=Song())

@app.route("/songs/new", methods=['POST'])
def create_song():
    s = Song(
        None,
        request.form['title'],
        request.form['artist'])
    if s.save():
        flash("Created New Song!")
        return redirect("/songs")
    else:
        return render_template("new.html", song=s)

@app.route("/songs/<song_id>")
def song(song_id=0):
    song = Song.find(song_id)
    return render_template("show.html", song=song)


@app.route("/songs/<song_id>/edit", methods=['GET'])
def song_edit_get(song_id=0):
    song = Song.find(song_id)
    return render_template("edit.html", song=song)

@app.route("/songs/<song_id>/edit", methods=['POST'])
def songs_edit_post(song_id=0):
    s = Song.find(song_id)
    s.update(
      request.form['title'],
      request.form['artist'])
    if s.save():
        flash("Updated Song!")
        return redirect("/songs/" + str(song_id))
    else:
        return render_template("edit.html", song=s)

@app.route("/songs/<song_id>", methods=['DELETE'])
def songs_delete(song_id=0):
    song = Song.find(song_id)
    song.delete()
    flash("Deleted Song!")
    return redirect("/songs", 303)
