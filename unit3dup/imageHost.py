# -*- coding: utf-8 -*-
import base64
import sys
import time

import requests
from decouple import Config, RepositoryEnv
from rich.console import Console

config_load = Config(RepositoryEnv('service.env'))
IMGBB_KEY = config_load('IMGBB_KEY')
console = Console()


class ImgBB:

    def __init__(self, image: bytes):
        self.image = base64.b64encode(image)

    @property
    def upload(self):
        params = {
            'key': IMGBB_KEY,
        }

        files = {
            'image': (None, self.image),
        }

        upload_n = 0
        error = {}
        response = {}
        while upload_n < 5:
            """
            Send the image, and if we get 502 error, wait for a while 
            """
            try:
                upload_n += 1
                response = requests.post('https://api.imgbb.com/1/upload', params=params, files=files)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                console.log(f"[Report IMGBB try n° {upload_n}] Screenshot {e}")
                time.sleep(2)

        console.log("Unable to upload image, try Renew your API KEY")
        console.log(f"Error: {error}")
        sys.exit()

