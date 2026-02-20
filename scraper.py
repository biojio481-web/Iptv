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
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Unix Tv-Isp
http://30.30.30.30:8088/101/index.m3u8?token=36a0a20c364ebbc4579a8acc926b05e1752927c1-ffb05932ae7743892f661677efc10d8b-1771187674-1771184074
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Unix Tv-Isp
http://30.30.30.30:8088/102/index.m3u8?token=d46a2e934191b183ba2eaefb1bbe9c81d759c570-bdb46eeeb67341758d157434872e8048-1771187762-1771184162
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Unix Tv-Isp
http://30.30.30.30:8088/115/index.m3u8?token=6096fdf2281883e467cd8eaf87639b5b88cde369-a19692c2d4e9dd12b0832110b1a5d756-1771187805-1771184205
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-4-Free Tv-Isp
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-5-Free Tv-Isp
http://172.16.29.2:8090/hls/StarSports1HD.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-6-Cloud Tv-Isp
https://backend.plusbox.tv/StarSports1HD/index.fmp4.m3u8?token=daacd458cbf7b6e72594a5c339829fcc65cad47c-e0b0ffc885e0c963ff9c9368ba08cdf3-1771195278-1771184478
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
    "Falcon Tv": "https://sm-live-tv-auto-update-playlist.pages.dev/Combined_Live_TV.m3u",
    "New Bdix": "https://jmrj02jibon02khan.vercel.app/all/playlists.m3u",
    "Dish Tv": "https://raw.githubusercontent.com/mdarif2743/Sky-dish/refs/heads/main/README.md"
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
