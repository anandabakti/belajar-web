import feedparser
import json

url_rss = "https://megapolitan.antaranews.com/rss/bogor-update.xml"

feed = feedparser.parse(url_rss)
daftar_berita = []

for berita in feed.entries[:10]:
    data = {
        "judul": berita.title,
        "sumber": "ANTARA Bogor Update",
        "link": berita.link,
        "tanggal": berita.get("published", "Tanggal tidak tersedia"),
        "status": "Baru"
    }

    daftar_berita.append(data)

with open("isu_otomatis.json", "w", encoding="utf-8") as file:
    json.dump(daftar_berita, file, ensure_ascii=False, indent=2)

print("Berhasil mengambil", len(daftar_berita), "berita.")
print("Data disimpan di file isu_otomatis.json")

for berita in daftar_berita:
    print("-", berita["judul"])