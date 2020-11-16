from flask import Flask
from flask import render_template
from flask import jsonify
from flask_bootstrap import Bootstrap
from filters import date_time_format
from filters import file_type
from flask import request
from libs.db import get_conn
from libs.parse_audio import parse_bytes
from libs.find_match import find_matches

application = app = Flask(__name__)
Bootstrap(app)

app.secret_key = 'secret'
app.jinja_env.filters['date_time_format'] = date_time_format
app.jinja_env.filters['file_type'] = file_type


@app.route('/', methods=['GET'])
def index():
    """Generates index page of website.

    Generates output from a index.html template file based on the Jinja2 engine.

    Returns:
        render_template: Renders the template file.
    """

    conn, cur = get_conn('remote')
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


@app.route('/songs', methods=['GET'])
def browse_songs():
    """Generates songs list page of website.

    Fetches songs title from database and generates output from a songs.html template file based on the Jinja2 engine.

    Returns:
        render_template: Renders the template file. If some error occurred while fetching, then a json object is
        returned.
    """

    conn, cur = get_conn('remote')
    check = cur.execute("SELECT title, artist, album FROM songs")
    if check > 0:
        rows = cur.fetchall()
        return render_template('songs.html', songs=rows)
    return jsonify({"message": "Songs page"})


@app.route('/albums', methods=['GET'])
def browse_album():
    """Generates albums list page of website.

    Fetches albums from database and generates output from a albums.html template file based on the Jinja2
    engine.

    Returns:
        render_template: Renders the template file. If some error occurred while fetching, then a json object is
        returned.
    """

    conn, cur = get_conn('remote')
    check = cur.execute("SELECT DISTINCT ALBUM FROM songs")
    if check > 0:
        rows = cur.fetchall()
        print(rows)
        return render_template('albums.html', albums=rows)
    return jsonify({"message": "Albums page"})


@app.route('/artists', methods=['GET'])
def browse_artist():
    # TODO: Prepare a template file for artists page and fetch artists from database and render it.
    return jsonify({"message": "Artists page"})


@app.route('/identify_song', methods=['POST'])
def identify_song():
    """Identifies the song.

    Processes the file sent in the request to identify the title, album and artist of song with certain confidence.

    Returns:
        json: Containing song title, album, artist and confidence.
    """

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
        conn, cur = get_conn('remote')

        cur.execute("SELECT TITLE, ARTIST, ALBUM FROM songs WHERE ID=%s", song_id)

        song_details = cur.fetchall()

        prob = (identified_songs[song_id] / len(matches)) * 100

        print("\n\nTotal Identified songs = {}".format(len(identified_songs)))

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
