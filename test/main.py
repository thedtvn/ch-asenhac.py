import chiasenhac

cl = chiasenhac.ChiaSeNhac()
a = cl.get_songinfo("https://chiasenhac.vn/nghe-album/mud-single-xss6m63vqk8kw2.html")
print(a.titleraw)
print(a.url)
print(a.title)
print(a.artist)
print(a.thumbnail)
for i in a.list_audio():
    print(i.url)
    print(i.quality)
    print(i.format)
    print(i.is_available)
print(a.list_audio().best_quality())