from libs.generate_fingerprint import fingerprint
from libs.constants import *
from itertools import zip_longest
from libs.db import get_conn
import math


def find_matches(channel, sampling_rate=DEFAULT_SAMPLING_RATE, args='remote'):
    """Matches audio fingerprints.

    Fingerprints of an audio channel is matched against the stored fingerprints in the database.

    Args:
        channel:
            An audio channel. Array of bytes.
        sampling_rate:
            Number of samples per second taken to construct a discrete signal.
        args:
            Either 'localhost' to connect to localhost server or 'remote'

    Yields:
        song_id: Song id of matched fingerprint.
    """

    hashes = fingerprint(channel, sampling_rate)
    mapper = {}

    for hash_val, offset in hashes:
        mapper[hash_val.upper()] = offset

    values = mapper.keys()

    if values is None:
        print("no values")
    else:
        conn, cur = get_conn(args)

        counter = 0
        print("\nTaking step length of {}\n".format(MATCH_STEP_LENGTH))
        for split_values in grouper(values, MATCH_STEP_LENGTH):
            counter += 1
            query = '''
            SELECT upper(hash), song_id
            FROM fingerprints
            WHERE upper(hash) IN (%s)
            '''
            split_values = list(split_values)
            lis = ['%s'] * len(split_values)
            query = query % ', '.join(lis)

            x = cur.execute(query, split_values)
            val = ()
            if x > 0:
                val = cur.fetchall()

            matches_found = len(val)
            if matches_found > 0:
                msg = "\tFound {a} hash matches at step {b}/{c}"
                print(msg.format(a=matches_found, b=counter, c=math.ceil(len(values)/MATCH_STEP_LENGTH)))
            else:
                msg = "\tNo hash matches found at step {b}/{c}"
                print(msg.format(b=counter, c=math.ceil(len(values)/MATCH_STEP_LENGTH)))

            for hashs, song_id in val:
                yield [song_id]

        cur.close()


def grouper(iterable, n, fill_value=None):
    """Generates iterator.

    Generates iterables of fingerprints.

    Args:
        iterable:
            List of objects to generate iterator.
        n:
            Number of iterables
        fill_value:
            A value placed in case of missing value from the iterable

    Returns:
        iterator: Aggregated elements of each iterable
    """

    args = [iter(iterable)] * n
    return (filter(None, values) for values
            in zip_longest(fillvalue=fill_value, *args))
