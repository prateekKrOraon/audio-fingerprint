import numpy as np
from libs.record_audio import RecordAudio
from libs.constants import *
from libs.find_match import find_matches
from libs.db import get_conn


def identify_from_mic():
    """Identifies audio.

    Records audio from built-in mic and identifies the song. Works in localhost server.
    """

    recorder = RecordAudio()
    recorder.record_audio()
    frames = recorder.get_recorded_audio()
    data = [[] for i in range(DEFAULT_CHANNELS)]
    for item in frames:
        nums = np.frombuffer(item, np.int16)
        for c in range(DEFAULT_CHANNELS):
            data[c].extend(nums[c::DEFAULT_CHANNELS])

    matches = []
    print("Finding Song...")
    for channeln, channel in enumerate(data):
        print("\nProcessing channel {}/2".format(channeln+1))
        matches.extend(find_matches(channel, args='localhost'))

    identified_songs = {}
    if len(matches) > 0:
        for item in matches:
            title = str(item[0])
            if title in identified_songs.keys():
                identified_songs[title] += 1
            else:
                identified_songs[title] = 1

        song_id = max(identified_songs, key=identified_songs.get)
        conn, cur = get_conn('localhost')

        cur.execute("SELECT title, artist, album FROM songs WHERE id=%s", song_id)

        song_details = cur.fetchall()

        prob = (identified_songs[song_id] / len(matches)) * 100

        print("\n\nTotal Identified songs = {}".format(len(identified_songs)))
        print("\n\nTotal Identified songs = {}".format(len(identified_songs)))
        print("\nBest hit\n\n\t{title}\n\t{artist}\n\t{album}\n\nwith {p}% confidence\n\n".format(
            title=song_details[0][0],
            artist=song_details[0][1],
            album=song_details[0][2], p=prob))

    recorder.close_recorder()


if __name__ == '__main__':
    identify_from_mic()
