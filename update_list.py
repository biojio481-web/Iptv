import requests
urls = [
    "https://iptv-org.github.io/iptv/countries/bd.m3u",
    "https://iptv-org.github.io/iptv/categories/news.m3u"
]
def main():
    content = "#EXTM3U\n"
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                lines = r.text.splitlines()
                content += "\n".join(lines[1:]) + "\n"
        except:
            pass
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(content)
if __name__ == "__main__":
    main()
