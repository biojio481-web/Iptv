import requests

def merge_online_playlists():
    url1 = "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u"
    url2 = "https://da.gd/YWCS05"
    
    links = [url1, url2]
    combined_content = "#EXTM3U\n"

    for url in links:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                data = r.text.replace("#EXTM3U", "").strip()
                if data:
                    combined_content += data + "\n"
        except:
            pass

    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(combined_content)

if __name__ == "__main__":
    merge_online_playlists()
