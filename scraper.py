import os
import requests
import re

# ১. লোগো লিঙ্কসমূহ
SPECIAL_LOGO_URL = "https://i.postimg.cc/mrmyjYhy/IMG-20260128-195914.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

# ২. গ্রুপ নেমস
SPECIAL_GROUP = "T20 World Cup 2026 Bdix Special"
ENTERTAINMENT_GROUP = "Entertainment"

# ৩. স্পেশাল চ্যানেল (Live-1 থেকে Live-6)
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2
http://30.30.30.30:8088/101/index.m3u8?token=9b9a5c6dae6851f8da3d7d817417bd3c5e3ebb0d-e8ee13fe456593685a17721b2b6f21eb-1769449109-1769445509
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3
http://172.16.29.2:8090/hls/ASportsHD.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-4
http://172.16.29.34/live/ontest1/ontest1/347.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-5
http://172.16.29.34/live/ontest1/ontest1/349.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-6-IND VS NZ
https://ranapk.online/OPPLEX/RANAPK1/play.php?id=109987
"""

# ৪. এন্টারটেইনমেন্ট (নতুন ২টি চ্যানেল যোগ করা হয়েছে)
entertainment_channels = f"""#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-1
https://ranapk.online/OPPLEX/RANAPK1/play.php?id=109947
#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-2
https://ranapk.online/RANAPK33x/TVD/play.php?id=372986
#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-3
https://ranapk.online/OPPLEX/RANAPK1/play.php?id=167551
#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",THE-50
https://ranapk.online/OPPLEX/RANAPK1/play.php?id=109947
"""

# ৫. বাহ্যিক প্লেলিস্ট
external_playlists = {
    "Ontest-Plus": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
    "BDIX-IPTV": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "Main-IPTV": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u",
    "CricHD": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u",
    "Test": "https://da.gd/sdKRf"
}

def clean_and_group(content, group_name):
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        if line.startswith("#EXTM3U"): continue
        if line.startswith("#EXTINF:"):
            parts = line.split(',', 1)
            channel_name = parts[1] if len(parts) > 1 else "Unknown Channel"
            new_line = f'#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{group_name}",{channel_name}'
            cleaned.append(new_line)
        elif line.strip():
            cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    final_data = special_channels_content + "\n" + entertainment_channels
    for name, url in external_playlists.items():
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
            if r.status_code == 200:
                final_data += "\n" + clean_and_group(r.text, name)
        except:
            pass
            
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print("Playlist Updated: Entertainment 3 & 4 added!")

if __name__ == "__main__":
    run_scraper()
