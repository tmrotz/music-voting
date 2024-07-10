from flask import Flask, flash, redirect, render_template, request
from songs_model import Song
from spotify import bp

Song.load_db()

app = Flask(__name__)

app.secret_key = b'hypermedia rocks'

app.register_blueprint(bp)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/songs")
def songs():
    search = request.args.get("q")
    page = int(request.args.get("page", 1))
    if search is not None:
        songs_set = Song.search(search)
    else:
        songs_set = Song.all(page)
    return render_template("songs/index.html", songs=songs_set, page=page)

@app.route("/songs/new", methods=['GET'])
def new_song():
    return render_template("songs/new.html", song=Song())

@app.route("/songs/new", methods=['POST'])
def create_song():
    s = Song(
        None,
        request.form['title'],
        request.form['artist'],
        request.form['uri'])
    if s.save():
        flash("Created New Song!")
        return redirect("/songs")
    else:
        return render_template("songs/new.html", song=s)

@app.route("/songs/<song_id>")
def song(song_id=0):
    song = Song.find(song_id)
    return render_template("songs/show.html", song=song)


@app.route("/songs/<song_id>/edit", methods=['GET'])
def song_edit_get(song_id=0):
    song = Song.find(song_id)
    return render_template("songs/edit.html", song=song)

@app.route("/songs/<song_id>/edit", methods=['POST'])
def songs_edit_post(song_id=0):
    s = Song.find(song_id)
    s.update(
      request.form['title'],
      request.form['artist'],
      request.form['uri'])
    if s.save():
        flash("Updated Song!")
        return redirect(f"/songs/{song_id}")
    else:
        return render_template("songs/edit.html", song=s)

@app.route("/songs/<song_id>", methods=['DELETE'])
def songs_delete(song_id=0):
    song = Song.find(song_id)
    song.delete()
    flash("Deleted Song!")
    return redirect("/songs", 303)
