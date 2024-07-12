import json
import time


# ========================================================
# Song Model
# ========================================================
PAGE_SIZE = 4

class Song:
    # mock songs database
    db = {}

    def __init__(self, id_=None, title=None, artist=None, uri=None):
        self.id = id_
        self.title = title
        self.artist = artist
        self.uri = uri
        self.errors = {}

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def update(self, title, artist, uri):
        self.title = title
        self.artist = artist
        self.uri = uri

    def validate(self):
        if not self.title:
            self.errors['title'] = "Title Required"
        if not self.artist:
            self.errors['artist'] = "Artist Required"
        if not self.uri:
            self.errors['uri'] = "URI Required"
        existing_song = next(filter(lambda s: s.id != self.id and s.uri == self.uri, Song.db.values()), None)
        if existing_song:
            self.errors['uri'] = "URI Must Be Unique"
        return len(self.errors) == 0

    def save(self):
        if not self.validate():
            return False
        if self.id is None:
            if len(Song.db) == 0:
                max_id = 1
            else:
                max_id = max(song.id for song in Song.db.values())
            self.id = max_id + 1
            Song.db[self.id] = self
        Song.save_db()
        return True

    def delete(self):
        del Song.db[self.id]
        Song.save_db()

    @classmethod
    def count(cls):
        time.sleep(2)
        return len(cls.db)

    @classmethod
    def all(cls, page=1):
        page = int(page)
        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        return list(cls.db.values())[start:end]

    @classmethod
    def search(cls, text):
        result = []
        for s in cls.db.values():
            match_title = s.title is not None and text in s.title
            match_artist = s.artist is not None and text in s.artist
            match_uri = s.uri is not None and text in s.uri
            if match_title or match_artist or match_uri:
                result.append(s)
        return result

    @classmethod
    def load_db(cls):
        with open('songs.json', 'r') as songs_file:
            songs = json.load(songs_file)
            cls.db.clear()
            for s in songs:
                cls.db[s['id']] = Song(s['id'], s['title'], s['artist'], s['uri'])

    @staticmethod
    def save_db():
        out_arr = [s.__dict__ for s in Song.db.values()]
        with open("songs.json", "w") as f:
            json.dump(out_arr, f, indent=2)

    @classmethod
    def find(cls, id_):
        id_ = int(id_)
        s = cls.db.get(id_)
        if s is not None:
            s.errors = {}
        else:
            s = Song()

        return s

