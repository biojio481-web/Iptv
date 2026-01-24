import os
import requests
import re

# 1. Logo Configuration
LOGO_URL = "Gemini_Generated_Image_36682y36682y3668.png"

# 2. Special 12 Channels Header
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-1
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-2
http://172.16.29.34/live/ontest1/ontest1/252.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-3
http://172.16.29.2:8090/hls/ASportsHD.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-4
http://172.16.29.34/live/ontest1/ontest1/347.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-5
http://172.16.29.34/live/ontest1/ontest1/349.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-6
http://172.16.29.34/live/ontest1/ontest1/443.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-7
http://172.16.29.34/live/ontest1/ontest1/328.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-8
http://172.16.29.34/live/ontest1/ontest1/375.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-9
http://172.16.29.34/live/ontest1/ontest1/480.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-10
http://172.16.29.34/live/ontest1/ontest1/330.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-11-Special
http://172.16.29.34/live/ontest1/ontest1/480.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}",Live-12-Special
https://ranapk.online/RANAPK33x/TVD/play.php?id=809386
"""

# 3. External Playlists to fetch
external_links = [
    "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
    "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u",
    "https://iptv-scraper-zilla.pages.dev/CricHD.m3u",
    # Future Slots (Link thakle koman moddhe boshaban)
    "", 
    "",
    ""
]

def clean_and_add_logo(content):
    """External content theke EXTM3U tag soriye logo add korar function"""
    lines = content.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.startswith("#EXTM3U"):
            continue # Header bar bar dorkar nai
        if line.startswith("#EXTINF:"):
            # Logo add ba replace
            if 'tvg-logo="' in line:
                line = re.sub(r'tvg-logo=".*?"', f'tvg-logo="{LOGO_URL}"', line)
            else:
                line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{LOGO_URL}"')
                line = line.replace("#EXTINF:0", f'#EXTINF:0 tvg-logo="{LOGO_URL}"')
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def run_scraper():
    final_playlist = special_channels_content
    
    for url in external_links:
        if not url:
            continue
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                final_playlist += "\n" + clean_and_add_logo(r.text)
                print(f"✅ Added: {url[:30]}...")
        except:
            print(f"⚠️ Failed: {url[:30]}")

    # Sob kichu ekta file-ei save hobe
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_playlist)
    print("🚀 Single playlist.m3u is ready!")

if __name__ == "__main__":
    run_scraper()
