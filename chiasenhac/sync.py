import requests
from urllib.parse import urlparse
from .obj import *


class ChiaSeNhac:

    def __init__(self):
        pass

    def check_links(self, url):
        url = urlparse(url)
        return bool("chiasenhac.vn" in url.hostname and url.path.startswith(("/mp3/", "/nghe-album/", "/hd/")))

    def get_songinfo(self, url):
        if self.check_links(url):
            r = requests.get(url)
            if '<h4 class="text-danger">' not in r.text:
                return Song(r.text)
            else:
                raise CSNError("Không Tìm Thầy Info")
        else:
            raise CSNError("Link khổng hợp lệ")





