import os
import io
import numpy as np
from pydub import AudioSegment
from hashlib import sha1
from pydub.utils import audioop


def parse_bytes(bytes_data, format="mp3", offline=False):
    global channels, frame_rate, hash_val

    try:
        if not offline:
            file = io.BytesIO(bytes_data)
        else:
            file = bytes_data
        audio_file = AudioSegment.from_file(file, format=format)
        data = np.fromstring(audio_file._data, np.int16)
        channels = []
        for channel in range(audio_file.channels):
            channels.append(data[channel::audio_file.channels])
        frame_rate = audio_file.frame_rate
        hash_val = parse_file_hash(file, offline)
    except audioop.error:
        print('audioop.error')

    song = {
        'channels': channels,
        'frame_rate': frame_rate,
        'hash_value': hash_val
    }

    return song


def parse_file_hash(bytes, offline, blocksize=2 * 20):
    global file
    s = sha1()
    if offline:
        file = open(bytes, "rb")
    else:
        file = bytes
    while True:
        buf = file.read(blocksize)
        if not buf:
            break
        s.update(buf)

    if offline:
        file.close()
    return s.hexdigest().upper()
