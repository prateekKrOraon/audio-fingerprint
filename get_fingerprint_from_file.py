import os
from libs.constants import MP3_PATH
from libs.parse_audio import parse_bytes
from libs.generate_fingerprint import fingerprint
from libs.db import get_conn
import eyed3
import argparse


def get_tags(file):
    """Gets ID3 tags of audio file.

    Process the files from local storage to get ID3 tags.

    Args:
        file:
            An audio file.

    Returns:
        list: Containing song name, artist and album
    """

    audio = eyed3.load(file)
    tags = audio.tag
    garbage_str = [
        " - www.Songs.PK",
        " - www.DJMaza.Com",
        " - www.PagalWorld.Com",
        " - www.WapKing.in",
        " - MP3Khan.Com",
        " - MP3Khan.Net",
        " - DJMaza.Com",
        " - PagalWorld.co",
        " - DJMaza.Cool",
        " - PagalWorld.com",
        " - www.WAPOCEAN.com",
        " (Www.FlowActivo.Com)",
        " - www.SongsLover.pk",
        " (www.SongsLover.pk)",
        " - www.SongsLover.com",
        " - www.SongsLover.mobi",
        " - www.RnB4U.in",
        " Downloaded From www.SongsLover.com",
        " (FlowActivo.Com)",
        " (www.SongsLover.com)",
        " - www.SongsLovel.club",
        " - DJMaza.Info",
        " - WapLoft.com",
        " - Singles"
    ]
    song_name = None
    artist = None
    album = None
    if tags is None:
        title = file.split('/')
        song_name = title[len(title) - 1]
        for i in range(len(garbage_str)):
            if song_name.endswith(garbage_str[i]):
                song_name = song_name[:-(len(garbage_str[i]))]
        song = [song_name, 'unknown', 'unknown']
    else:
        if tags.title is None:
            title = file.split('/')
            song_name, _ = os.path.splitext(title[len(title) - 1])
            for i in range(len(garbage_str)):
                if song_name.endswith(garbage_str[i]):
                    song_name = song_name[:-(len(garbage_str[i]))]
        else:
            song_name = tags.title
            artist = tags.artist
            album = tags.album
            for i in range(len(garbage_str)):
                if song_name is not None and song_name.endswith(garbage_str[i]):
                    song_name = song_name[:-(len(garbage_str[i]))]
                if artist is not None and artist.endswith(garbage_str[i]):
                    artist = artist[:-(len(garbage_str[i]))]
                if album is not None and album.endswith(garbage_str[i]):
                    album = album[:-(len(garbage_str[i]))]

            if artist is None:
                artist = 'Unknown'

            if album is None:
                album = 'Unknown'

        song = [song_name, artist, album]

    return song


def run(argument):
    """Store song data in database.

    Fetches ID3 tags from audio file in local storage and stores them in a MySQL database in AWS server.

    Args:
        argument:
            Either 'localhost' to connect to localhost server or 'remote'
    """

    files = os.listdir(MP3_PATH)
    conn, cur = get_conn(argument)
    songs = []
    count = 0
    for file in files:
        count += 1
        _, extension = os.path.splitext(MP3_PATH + file)

        if extension == '.mp3':
            song = parse_bytes(MP3_PATH + file,offline=True)
            tags = get_tags(MP3_PATH + file)
            check = cur.execute("SELECT id FROM songs WHERE title=%s", tags[0])
            if check > 0:
                print("Skipping File... Fingerprint already available...")
            else:
                cur.execute("INSERT INTO songs(title, artist, album) VALUES(%s, %s, %s)", tags)
                conn.commit()
                songs.append(song)
                print("\nSong {}/{}\n".format(count, len(files)))
                print("Generating Finger print for {}".format(tags[0]))
                hashes = set()
                channel_amount = len(song['channels'])
                for channel_number, channel in enumerate(song['channels']):
                    channel_hashes = fingerprint(channel, sampling_rate=song['frame_rate'])
                    channel_hashes = set(channel_hashes)

                    msg = '\tfinished channel {}/{}, got {} hashes'
                    print(msg.format(channel_number + 1, channel_amount, len(channel_hashes)))

                    hashes |= channel_hashes

                values = []
                check = cur.execute("SELECT id FROM songs WHERE title=%s", tags[0])
                rows = cur.fetchall()
                for h, offset in hashes:
                    values.append((rows[0][0], h, int(offset)))

                print("\tGot {total} hashes for {song}".format(total=len(values), song=tags[0]))
                if len(values) > 0:
                    print("Done")
                    cur.executemany(
                        "INSERT INTO fingerprints(song_id, hash, offset) VALUES(%s,%s,%s)",
                        values
                    )
                    conn.commit()

    cur.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help="localhost/remote")
    args = parser.parse_args()
    if args.server is None:
        print("run with -s or --server localhost/remote")
    else:
        run(args.server)
