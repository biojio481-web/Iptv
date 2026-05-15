import os
import requests
import re

# ১. লোগো লিঙ্কসমূহ
SPECIAL_LOGO_URL = "https://i.postimg.cc/50qZxPkn/Gemini-Generated-Image-sumbp1sumbp1sumb.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

# ২. গ্রুপ নেমস
SPECIAL_GROUP = "IPL 2026"

# ৩. স্পেশাল চ্যানেলসমূহ
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Noor Isp
http://198.195.239.50:8095/SonyTenSports5/tracks-v1a1/mono.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Noor Isp
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Unix Tv-Isp
https://live20.bozztv.com/giatvplayout7/giatv-209902/tracks-v1a1/mono.ts.m3u8
"""

# ৪. বাহ্যিক প্লেলিস্ট (আগের গুলো বাদ দিয়ে আপনার দেওয়া নতুন লিঙ্কটি যোগ করা হয়েছে)
external_playlists = {
    "Live": "https://go.skym3u.top/69di.m3u"
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
    # স্পেশাল চ্যানেল দিয়ে শুরু
    final_data = special_channels_content
    for name, url in external_playlists.items():
        if not url: continue
        try:
            r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30)
            if r.status_code == 200:
                final_data += "\n" + clean_and_group(r.text, name)
        except Exception as e:
            print(f"Error fetching {name}: {e}")
            
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print("Playlist Updated: 3 Special Channels & New 'Live' Category Playlist added!")

if __name__ == "__main__":
    run_scraper()
