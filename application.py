from flask import Flask
from flask import render_template
from flask import jsonify
from flask_bootstrap import Bootstrap
from filters import date_time_format
from filters import file_type
from flask import request
# from legacy.get_fingerprint_from_web import files_from_s3
from libs.aws import *
from libs.parse_audio import parse_bytes
from libs.find_match import find_matches

application = app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'secret'
app.jinja_env.filters['date_time_format'] = date_time_format
app.jinja_env.filters['file_type'] = file_type


@app.route('/')
def index():
    conn, cur = get_conn()
    print("checking data base")
    check = cur.execute("SELECT COUNT(id) FROM songs")
    rows = ()
    if check > 0:
        rows = cur.fetchall()
        print(rows)

    print("setting params")
    params = {
        "songs_count": rows[0][0]
    }
    return render_template('index.html', params=params)


@app.route('/', methods=['POST'])
def browse_songs():
    conn, cur = get_conn()
    check = cur.execute("SELECT title, artist, album FROM songs")
    if check > 0:
        rows = cur.fetchall()
        return render_template('songs.html', songs=rows)
    return jsonify({"message": "Songs page"})


@app.route('/albums', methods=['POST'])
def browse_album():
    conn, cur = get_conn()
    check = cur.execute("SELECT DISTINCT ALBUM FROM songs")
    if check > 0:
        rows = cur.fetchall()
        print(rows)
        return render_template('albums.html', albums=rows)
    return jsonify({"message": "Albums page"})


@app.route('/artists', methods=['POST'])
def browse_artist():
    return jsonify({"message": "Artists page"})


@app.route('/find_song', methods=['POST'])
def find_song():
    file = request.files['file']
    parse_bytes(file)


@app.route('/identify_song', methods=['POST'])
def identify_song():
    file = request.files['file']
    mime_type = "wave"
    if file.mimetype == "audio/mpeg":
        mime_type = "mp3"
    elif file.mimetype == "audio/wav":
        mime_type = "wave"

    song = parse_bytes(file.stream.read(), format=mime_type)

    matches = []
    for channeln, channel in enumerate(song['channels']):
        matches.extend(find_matches(channel, sampling_rate=song['frame_rate']))

    identified_songs = {}
    song_details = {}

    if len(matches) > 0:
        for item in matches:
            title = str(item[0])
            if title in identified_songs.keys():
                identified_songs[title] += 1
            else:
                identified_songs[title] = 1

        song_id = max(identified_songs, key=identified_songs.get)
        conn, cur = get_conn()

        cur.execute("SELECT TITLE, ARTIST, ALBUM FROM songs WHERE ID=%s", song_id)

        song_details = cur.fetchall()

        prob = (identified_songs[song_id] / len(matches)) * 100
        # details = song_details[song_title]
        print("\n\nTotal Identified songs = {}".format(len(identified_songs)))
        # print("\nBest hit\n\n\t{title}\n\t{artist}\n\t{album}\n\nwith {p}% confidence\n\n".format(title=song_title,
        #                                                                                          artist=details[0],
        #                                                                                          album=details[1], p=prob))
    if file is not None:
        if len(matches) == 0:
            return jsonify({"message": "No Match Found"})
        else:
            return jsonify({
                "title": song_details[0][0],
                "artist": song_details[0][1],
                "album": song_details[0][2],
                "confidence": prob
            })

    return jsonify({"message": "error"})


if __name__ == '__main__':
    app.run(debug=True)
