import requests

def merge_playlists():
    # অনলাইন লিঙ্কগুলো
    online_links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_OTT_Navigator.m3u"
    ]
    
    # আপনার লোকাল আইএসপি লিঙ্ক (সঠিক ফরম্যাট)
    local_isp_link = "http://172.16.29.34/get.php?username=ontest1&password=ontest1&type=m3u_plus&output=ts"
    
    # প্লেলিস্ট শুরু
    combined_content = "#EXTM3U\n\n"
    
    # লোকাল চ্যানেলটি যোগ করা (বোল্ড নাম দিয়ে যেন সহজে চেনা যায়)
    combined_content += "#EXTINF:-1 tvg-id=\"MyISP\" group-title=\"MY_LOCAL_CHANNELS\", === MY ISP LIVE TV ===\n"
    combined_content += local_isp_link + "\n\n"
    
    # বাকি অনলাইন লিঙ্কগুলো থেকে ডেটা সংগ্রহ
    for url in online_links:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                # শুধু চ্যানেল লাইনগুলো নেওয়া হচ্ছে
                lines = r.text.splitlines()
                for line in lines:
                    if not line.startswith("#EXTM3U") and line.strip():
                        combined_content += line + "\n"
                print(f"Loaded: {url}")
        except Exception as e:
            print(f"Error with {url}: {e}")

    # ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())

if __name__ == "__main__":
    merge_playlists()
