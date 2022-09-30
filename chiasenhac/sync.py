import time

import requests
from urllib.parse import urlparse
from .obj import *


class ChiaSeNhac:

    def __init__(self, *, email=None, password=None):
        self.email = email
        self.password = password
        self.cookies = {}
        self.last_cookies_modified = 0

    def login(self):
        if self.email and self.password:
            if self.last_cookies_modified + 864000 < int(time.time()):
                with requests.Session() as s:
                    with s.get("https://chiasenhac.vn/login") as r:
                        csrf_token = re.findall(r'<meta name="csrf-token" content="(.*?)" />', r.text)
                    data = {"_token": csrf_token, "email": self.email, "password": self.password}
                    with s.post("https://chiasenhac.vn/login", data=data) as r:
                        if urlparse(r.url).path == "":
                            self.cookies = r.cookies
                            self.last_cookies_modified = int(time.time())
                            return self.cookies
                        else:
                            raise CSNError("Login failed")
            else:
                return self.cookies


    def check_links(self, url):
        url = urlparse(url)
        return bool("chiasenhac.vn" in url.hostname and url.path.startswith(("/mp3/", "/nghe-album/", "/hd/")))

    def get_songinfo(self, url):
        if self.check_links(url):
            r = requests.get(url, cookies=self.login())
            if '<h4 class="text-danger">' not in r.text:
                return Song(r.text)
            else:
                raise CSNError("Không Tìm Thầy Info")
        else:
            raise CSNError("Link khổng hợp lệ")





