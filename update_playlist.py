import requests

# ১. অন্য প্লেলিস্টের লিঙ্ক (এখানে আপনি অন্য কারো RAW মথু৩উ লিঙ্ক দেবেন)
OTHER_PLAYLIST_URLS = [
    "https://raw.githubusercontent.com/Iptv-Org/iptv/master/streams/bd.m3u"
]

def update_playlist():
    final_content = "#EXTM3U\n"
    for url in OTHER_PLAYLIST_URLS:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                # মেইন হেডার বাদ দিয়ে শুধু চ্যানেলগুলো নেওয়া
                data = r.text.replace("#EXTM3U", "").strip()
                final_content += data + "\n"
        except:
            pass
    
    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(final_content)

if __name__ == "__main__":
    update_playlist()
