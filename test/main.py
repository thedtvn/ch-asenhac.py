import chiasenhac
import asyncio

async def main():
    cl = chiasenhac.ChiaSeNhacAsync()
    a = await cl.get_songinfo("https://chiasenhac.vn/nghe-album/mud-single-xss6m63vqk8kw2.html")
    print(a.titleraw)
    print(a.url)
    print(a.title)
    print(a.artist)
    print(a.thumbnail)
    queue = await a.list_audio()
    for i in queue:
        print(i.url)
        print(i.quality)
        print(i.format)
        print(i.is_available)
    print(await queue.best_quality())

asyncio.run(main())