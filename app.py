from flask import Flask, flash, redirect, render_template, request, send_file
import archiver
from songs_model import Song
import spotify
from archiver import Archiver

Song.load_db()

app = Flask(__name__)

app.secret_key = b'hypermedia rocks'

app.register_blueprint(spotify.bp)

@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/songs", methods=['GET'])
def songs():
    search = request.args.get("q")
    page = int(request.args.get("page", 1))
    if search is not None:
        songs_set = Song.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            return render_template("songs/rows.html", songs=songs_set, page=page)
    else:
        songs_set = Song.all(page)
    return render_template("songs/index.html", songs=songs_set, page=page, archiver=Archiver.get())

@app.route("/songs", methods=['DELETE'])
def songs_delete_all():
    song_ids = [
        int(id)
        for id in request.form.getlist("selected_song_ids")
    ]
    for song_id in song_ids:
        song = Song.find(song_id)
        song.delete()
    flash("Deleted Songs!")
    return render_template("songs/index.html", songs=Song.all(), page=1)

@app.route("/songs/count")
def songs_count():
    count = Song.count()
    return f"({count} total Songs)"

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
    if request.headers.get("HX-Trigger") == 'delete-btn':
        flash("Deleted Song!")
        return redirect("/songs", 303)
    else:
        return ""

@app.route("/songs/<song_id>/uri", methods=['GET'])
def songs_uri_get(song_id=0):
    s = Song.find(song_id)
    s.uri = request.args.get('uri')
    s.validate()
    return s.errors.get('uri') or ''

@app.route("/songs/archive", methods=["POST"])
def start_archive():
    archiver = Archiver.get()
    archiver.run()
    return render_template("archive_ui.html", archiver=archiver)


@app.route("/songs/archive", methods=["GET"])
def archive_status():
    archiver = Archiver.get()
    return render_template("archive_ui.html", archiver=archiver)


@app.route("/songs/archive/file", methods=["GET"])
def archive_content():
    archiver = Archiver.get()
    return send_file(archiver.archive_file(), "archive.json", as_attachment=True)


@app.route("/songs/archive", methods=["DELETE"])
def reset_archive():
    archiver = Archiver.get()
    archiver.reset()
    return render_template("archive_ui.html", archiver=archiver)
