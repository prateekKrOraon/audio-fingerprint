import wave
from libs.constants import *


class RecordAudio(object):
    """Audio recorder.

    Opens stream to record audio as multi-channel frames for processing. Saves audio file in wave format.

    Attributes:
        audio: Reference to PortAudio python interface.
        frames: Multi-channel audio byte stream.
    """

    def __init__(self):
        """Inits RecordAudio"""
        self.audio = pyaudio.PyAudio()
        self.frames = []

    def record_audio(self):
        """Records audio frames

        Opens a stream to record audio through built-in mic.
        """
        stream = self.audio.open(format=DEFAULT_FORMAT,
                                 channels=DEFAULT_CHANNELS,
                                 rate=DEFAULT_RATE,
                                 input=True,
                                 frames_per_buffer=DEFAULT_CHUNK_SIZE)

        print("Recording...")

        for i in range(0, int(DEFAULT_RATE / DEFAULT_CHUNK_SIZE * RECORD_SECONDS)):
            data = stream.read(DEFAULT_CHUNK_SIZE)
            self.frames.append(data)

        print("Done.")

        stream.stop_stream()
        stream.close()

    def save_audio(self, name=DEFAULT_OUT_NAME):
        """Saves audio file.

        Saves recorded audio file in local storage in wave format.

        Args:
            name: File name of the output audio.
        """
        print("Saving...")
        wf = wave.open(name+'.wav', 'wb')
        wf.setnchannels(DEFAULT_CHANNELS)
        wf.setsampwidth(self.audio.get_sample_size(DEFAULT_FORMAT))
        wf.setframerate(DEFAULT_RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        print('Saved')

    def get_recorded_audio(self):
        """Gets recorded audio frames.

        Returns:
            list: Multi channel audio frames.
        """
        return self.frames

    def close_recorder(self):
        """Closes audio stream"""
        self.audio.terminate()
