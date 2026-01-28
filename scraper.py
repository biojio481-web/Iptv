import os
import requests
import re

# Final Logo URL
LOGO_URL = "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Gemini_Generated_Image_md4brsmd4brsmd4b.png"

# Group Names
SPECIAL_GROUP = "T20 World Cup 2026 Bdix Special"
ENTERTAINMENT_GROUP = "Entertainment"

# Content Sections
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2
http://30.30.30.30:8088/101/index.m3u8?token=9b9a5c6dae6851f8da3d7d817417bd3c5e3ebb0d-e8ee13fe456593685a17721b2b6f21eb-1769449109-1769445509
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3
http://172.16.29.2:8090/hls/ASportsHD.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-4
http://172.16.29.34/live/ontest1/ontest1/347.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-5
http://172.16.29.34/live/ontest1/ontest1/349.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-6
http://172.16.29.34/live/ontest1/ontest1/443.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-7
http://172.16.29.34/live/ontest1/ontest1/328.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-8
http://172.16.29.34/live/ontest1/ontest1/375.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-9
http://172.16.29.34/live/ontest1/ontest1/480.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-10
http://172.16.29.34/live/ontest1/ontest1/330.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-11-Special
http://172.16.29.34/live/ontest1/ontest1/480.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-12-Special
https://ranapk.online/RANAPK33x/TVD/play.php?id=809386
"""

entertainment_channels = f"""#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-1
https://ranapk.online/OPPLEX/RANAPK1/play.php?id=167551
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{ENTERTAINMENT_GROUP}",Entertainment-2
https://bcdnxw.hakunaymatata.com/bt/8fbd6fad607047812f489c3cf9ae183b.mp4?sign=6a04579222235fe1702c9245fbbebfaf&t=1769373466
"""

external_playlists = {
    "Ontest-Plus": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
    "BDIX-IPTV": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "Main-IPTV": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u",
    "CricHD": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u",
    "Roar Zone Tv": "https://da.gd/raqHNg"
}

def clean_and_group(content, group_name):
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        if line.startswith("#EXTM3U"): continue
        if line.startswith("#EXTINF:"):
            line = re.sub(r'tvg-logo=".*?"', '', line)
            line = re.sub(r'logo=".*?"', '', line)
            line = re.sub(r'group-title=".*?"', '', line)
            line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{group_name}"')
        cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    final_data = special_channels_content + entertainment_channels
    for name, url in external_playlists.items():
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=15)
            if r.status_code == 200:
                final_data += "\n" + clean_and_group(r.text, name)
        except:
            pass
            
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)

if __name__ == "__main__":
    run_scraper()
