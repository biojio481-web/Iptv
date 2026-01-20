import requests

def merge_online_playlists():
    # এখানে আপনার সব সোর্স লিঙ্কগুলো থাকবে
    links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "এখানে_৩_নম্বর_লিঙ্ক_দিন",
        "এখানে_৪_নম্বর_লিঙ্ক_দিন"
    ]
    
    combined_content = "#EXTM3U\n"

    for url in links:
        if not url.startswith("http"): # যদি লিঙ্ক না থাকে তবে স্কিপ করবে
            continue
            
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                # #EXTM3U রিমুভ করে ক্লিন ডেটা নেওয়া
                data = r.text.replace("#EXTM3U", "").strip()
                if data:
                    combined_content += data + "\n"
                    print(f"Added: {url}")
        except Exception as e:
            print(f"Failed: {url} | Error: {e}")

    # ফাইনাল ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())

if __name__ == "__main__":
    merge_online_playlists()
