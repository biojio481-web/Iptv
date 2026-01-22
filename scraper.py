import requests

def merge_playlists():
    # অনলাইন লিঙ্কগুলো
    online_links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_OTT_Navigator.m3u"
    ]
    
    # আপনার লোকাল আইএসপি লিঙ্ক
    local_isp_link = "http://172.16.29.34/get.php?username=ontest1&password=ontest1&type=m3u_plus&output=ts"
    
    combined_content = "#EXTM3U\n"
    
    # লোকাল লিঙ্ক যোগ
    combined_content += f'#EXTINF:-1 group-title="My ISP", ISP Live TV\n{local_isp_link}\n'
    
    # অনলাইন লিঙ্কগুলো থেকে ডাটা সংগ্রহ
    for url in online_links:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                data = r.text.replace("#EXTM3U", "").strip()
                if data:
                    combined_content += data + "\n"
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # ফাইনাল ফাইল সেভ
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())

if __name__ == "__main__":
    merge_playlists()
