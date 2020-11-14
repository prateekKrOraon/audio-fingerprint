import os
import io
import numpy as np
from pydub import AudioSegment
from hashlib import sha1
from pydub.utils import audioop


def parse_bytes(bytes_data, format="mp3", offline=False):
    """Processes the bytes received to extract audio information.

    Extracts audio channels, frame rate and SHA-1 hash digest.

    Args:
        bytes_data:
            A bytes stream.
        format:
            Audio coding format.
        offline:
            If the file is coming from local storage.

    Returns:
        A dict of Audio information containing channels, frame rate and hash value.

    Raises:
        audioop.error: An error occurred while processing audio file
    """

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
    """Generates SHA-1 hash of file

    Args:
        bytes:
            File object.
        offline:
            File coming from local storage or not.
        blocksize:
            Size of block to be processed in each iteration while generating hash.

    Returns:
        str : Hex digest of the file in upper case.
    """

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
