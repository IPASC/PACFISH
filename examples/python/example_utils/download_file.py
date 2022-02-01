"""
SPDX-FileCopyrightText: 2021 International Photoacoustics Standardisation Consortium (IPASC)
SPDX-License-Identifier: CC0
"""

import requests
import os


def download_file(url, local_filename=None):
    """
    Downloads a file from a url and saves it under the given local_filename.
    If local_filename is not given, then the last part of the URL is used.
    """
    if local_filename is None:
        local_filename = url.split('/')[-1]

    if os.path.exists(local_filename):
        print("Already found file. Not re-downloading!")
        return local_filename
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        content_length = int(r.headers['Content-length'])
        print(f"Downloading...")
        with open(local_filename, 'wb') as f:
            i = 0
            for chunk in r.iter_content(chunk_size=8192):
                print(((i*8192.0) / content_length) * 100, "%", end="\r")
                f.write(chunk)
                i += 1
    return local_filename
