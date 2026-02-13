import os
import requests
import re

# ১. লোগো লিঙ্কসমূহ
SPECIAL_LOGO_URL = "https://i.postimg.cc/9fv12GK5/2026-Mens-T20-World-Cup.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

# ২. গ্রুপ নেমস
SPECIAL_GROUP = "T20 World Cup 2026 Bdix Special"
ENTERTAINMENT_GROUP = "Entertainment"

# ৩. স্পেশাল চ্যানেল (Live-1 থেকে Live-6)
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Unix Tv
https://xfireflix.my.id/Op.m3u8/?id=167567&e=.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Unix Tv
http://30.30.30.30:8088/115/tracks-v1a1/mono.m3u8?token=f87e8f1921082b8998b4d41d96458f583ebc4760-d411dd989ae18460ecdac5043a4e1a4b-1770744157-1770740557
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Free Tv
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-4-Free Tv
http://172.16.29.2:8090/hls/StarSports2HD.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-5-Opplex Tv
https://ranapk.online/RANAPK33x/TVDx/play.php?id=809383
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-6
https://ranapk.online/RANAPK33x/TVDx/play.php?id=809383
"""

# ৪. এন্টারটেইনমেন্ট (নতুন ২টি চ্যানেল যোগ করা হয়েছে)
entertainment_channels = f"""#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-1
http://30.30.30.30:8088/405/tracks-v1a1/mono.m3u8?token=afdb742562f7b2838e88c7554f6ed01b278423de-52cde21afba1bd0d09ac51ad0e7f941f-1770745481-1770741881
#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-2
http://172.16.29.2:8090/hls/ColorsHD.m3u8
#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-3
https://ranapk.online/RANAPK33x/TVDx/play.php?id=944612
#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",THE-50
https://ranapk.online/OPPLEX/RANAPK8/play.php?id=109947
"""

# ৫. বাহ্যিক প্লেলিস্ট
external_playlists = {
    "Ontest-Plus": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
    "BDIX-IPTV": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "Ayna-IPTV": "https://is.gd/ogCZTd.m3u",
    "New Bdix": "https://jmrj02jibon02khan.vercel.app/all/playlists.m3u",
    "Test": "https://jmrj02jibon02khan.vercel.app/all/playlists.m3u"
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
