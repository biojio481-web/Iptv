import requests

def merge_playlists():
    # আপনার দেওয়া ৪টি লিঙ্ক
    links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "https://da.gd/GXn1",
        "https://ranapk.short.gy/TG@RANAPKBDSx/tvd.m3u"
    ]
    
    combined_content = "#EXTM3U\n"
    
    for url in links:
        try:
            # allow_redirects=True দেওয়া হয়েছে শর্ট লিঙ্কের জন্য
            r = requests.get(url, timeout=30, allow_redirects=True)
            if r.status_code == 200:
                # ডুপ্লিকেট হেডার বাদ দেওয়া
                data = r.text.replace("#EXTM3U", "").strip()
                if data:
                    combined_content += data + "\n"
                    print(f"Success: {url}")
        except Exception as e:
            print(f"Error: {url} | {e}")

    # ফাইনাল ফাইল সেভ
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())

if __name__ == "__main__":
    merge_playlists()
