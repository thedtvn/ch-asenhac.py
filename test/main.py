import chiasenhac.asyncio as chiasenhac
import asyncio
import time

async def main():
    cl = chiasenhac.ChiaSeNhac()
    a = await cl.get_songinfo("https://chiasenhac.vn/mp3/mono-onionn/waiting-for-you-tsv66t5dqkkfhm.html")
    print(type(a))
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
    print((await queue.best_quality()))

start = time.time()
asyncio.run(main())
end = time.time()
print(end-start)