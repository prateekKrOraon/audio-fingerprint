import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import hashlib
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure
from scipy.ndimage.morphology import iterate_structure
from scipy.ndimage.morphology import binary_erosion
from legacy.constants import *


def fingerprint(
        channel_samples,
        sampling_rate=DEFAULT_SAMPLING_RATE,
        window_size=DEFAULT_WINDOW_SIZE,
        overlap_ratio=DEFAULT_OVERLAP_RATIO,
        fan_value=DEFAULT_FAN_VALUE,
        min_amp=DEFAULT_AMP_MIN,
        plots=False,
        matching=False):
    if plots:
        plt.plot(channel_samples)
        plt.title("{} samples".format(len(channel_samples)))
        plt.xlabel('time (s)')
        plt.ylabel('amplitude (A)')
        plt.show()
        plt.gca().invert_yaxis()

    if matching:
        arr2d = mlab.specgram(channel_samples,
                              NFFT=window_size,
                              Fs=sampling_rate,
                              window=mlab.window_hanning,
                              noverlap=int(window_size * 0.5))[0]
    else:
        arr2d = mlab.specgram(channel_samples,
                               NFFT=window_size,
                               Fs=sampling_rate,
                               window=mlab.window_hanning,
                               noverlap=int(window_size * overlap_ratio))[0]

    if plots:
        plt.plot(arr2d)
        plt.title('FFT')
        plt.show()

    arr2d = 10 * np.log10(arr2d)
    arr2d[arr2d == -np.inf] = 0

    local_maxima = generate_peaks(arr2d, min_amp=min_amp, matching=matching)

    if matching:
        return generate_hashes(local_maxima, fan_value=20)
    else:
        return generate_hashes(local_maxima, fan_value=fan_value)


def generate_peaks(arr2d, min_amp=DEFAULT_AMP_MIN, matching=False):
    bin_struct = generate_binary_structure(2, 1)
    if matching:
        neighborhood = iterate_structure(bin_struct, 35)
    else:
        neighborhood = iterate_structure(bin_struct, PEAK_NEIGHBORHOOD_SIZE)

    local_max = maximum_filter(arr2d, footprint=neighborhood) == arr2d

    background = (arr2d == 0)

    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    detected_peaks = local_max ^ eroded_background

    amps = arr2d[detected_peaks]

    j, i = np.where(detected_peaks)

    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > min_amp]

    frequency_index = [x[1] for x in peaks_filtered]
    time_index = [x[0] for x in peaks_filtered]

    return zip(frequency_index, time_index)


def generate_hashes(peaks, fan_value=DEFAULT_FAN_VALUE):
    peaks_list = list(peaks)
    for i in range(len(peaks_list)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks_list):

                freq1 = peaks_list[i][IDX_FREQ_I]
                freq2 = peaks_list[i + j][IDX_FREQ_I]

                time1 = peaks_list[i][IDX_TIME_J]
                time2 = peaks_list[i + j][IDX_TIME_J]

                delta_time = time2 - time1

                if delta_time >= MIN_HASH_TIME_DELTA and delta_time <= MAX_HASH_TIME_DELTA:
                    h = hashlib.sha1()
                    h.update(("%s|%s|%s" % (str(freq1), str(freq2), str(delta_time))).encode('utf-8'))
                    yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], time1)
