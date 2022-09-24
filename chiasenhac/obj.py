import re
import urllib.parse
import requests
from multiprocessing.pool import ThreadPool


class CSNError(Exception):
    def __init__(self, message):
        super().__init__(message)


class Song(object):
    def __init__(self, html):
        self.page = html
        self.titleraw = re.compile(r'<meta property="og:title" content="(.*?)" />').findall(self.page)[0]
        self.url = re.compile(r'<meta property="og:url" content="(.*?)" />').findall(self.page)[0]
        self.thumbnail = re.compile(r'<meta property="og:image" content="(.*?)" />').findall(self.page)[0]
        self.title = self.titleraw.split(" - ")[0]
        self.artist = self.titleraw.split(" - ")[1]
        data = re.compile(r'<a class="download_item" href="(.*?)" title=".*?">').findall(self.page)
        data2 = re.compile(r'{"file": "(.*?)", "label": .*?, "type": .*?, "default": .*?}').findall(self.page)
        data.extend(data2)
        self.raw_url_list = data
        if not self.raw_url_list:
            raise CSNError("Audio not found")

    def list_audio(self):
        return AudioQueue(list(set(self.raw_url_list))).start()

class AudioQueue(list):
    def checkaudio(self, url):
        return AudioItem(url).start()

    def start(self):
        self.data = [self.checkaudio(i) for i in self.input]
        super().extend(self.data)
        return self

    def __init__(self, input):
        self.input = input

    def best_quality(self):
        best_quality = None
        for i in self.data:
            if best_quality is not None:
                if i.is_available and (i.quality > best_quality.quality):
                    best_quality = i
            else:
                if i.is_available:
                    best_quality = i
        if best_quality is not None:
            return best_quality
        else:
            raise CSNError("Could not find best quality")



class AudioItem(object):
    def __init__(self,  url):
        prh = [i for i in urllib.parse.urlparse(url).path.split("/") if i]
        self.url = url
        self.quality = int(prh[-2])
        self.format = prh[-1].split(".")[-1]

    def start(self):
        try:
            r = requests.get(self.url, timeout=0.5)
            self.is_available = bool(r.status_code == 200)
        except:
            self.is_available = False
        return self

