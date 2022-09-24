import aiohttp
import asyncio
from .sync import ChiaSeNhac
from .obj import *


class Song(Song):
    async def list_audio(self):
        return await AudioQueue(list(set(self.raw_url_list))).start()

class AudioItem(AudioItem):
    async def start(self):
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(self.url, timeout=0.5) as r:
                    self.is_available = bool(r.status == 200)
        except:
            self.is_available = False
        return self
class AudioQueue(AudioQueue):
    async def checkaudio(self, url):
        return await AudioItem(url).start()

    async def start(self):
        self.data = await asyncio.gather(*[self.checkaudio(i) for i in self.input])
        super().extend(self.data)
        return self

    async def best_quality(self):
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


class ChiaSeNhac(ChiaSeNhac):

    async def get_songinfo(self, url):
        if self.check_links(url):
            async with aiohttp.ClientSession() as s:
                async with s.get(url) as r:
                    data = await r.text()
            if '<h4 class="text-danger">' not in data:
                return Song(data)
            else:
                raise CSNError("Không Tìm Thầy Info")
        else:
            raise CSNError("Link khổng hợp lệ")