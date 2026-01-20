import requests

def merge_online_playlists():
    # আপনার দেওয়া ৪টি লিঙ্ক এখানে সাজানো আছে
    links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "https://da.gd/GXn1",
        "https://is.gd/yf9bBw.m3u" # আপনার দেওয়া নতুন ৪ নম্বর লিঙ্ক
    ]
    
    combined_content = "#EXTM3U\n"
    
    for url in links:
        try:
            # শর্ট লিঙ্ক এবং ডিরেক্ট লিঙ্ক উভয়ের জন্যই কাজ করবে
            r = requests.get(url, timeout=30, allow_redirects=True)
            if r.status_code == 200:
                # মেইন হেডার #EXTM3U বাদ দিয়ে শুধু চ্যানেলের অংশটুকু নেওয়া
                data = r.text.replace("#EXTM3U", "").strip()
                if data:
                    combined_content += data + "\n"
                    print(f"Successfully added: {url}")
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    # ফাইনাল ফাইলটি playlist.m3u নামে সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())

if __name__ == "__main__":
    merge_online_playlists()
