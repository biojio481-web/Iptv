import os
import requests
import re

# 1. New Logo Configuration (Updated)
LOGO_URL = "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Gemini_Generated_Image_md4brsmd4brsmd4b.png"

# 2. Special Group Name
SPECIAL_GROUP = "T20 World Cup 2026 Bdix Special"

# 3. Special 12 Channels Data
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2
http://172.16.29.34/live/ontest1/ontest1/252.m3u8
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

# 4. Playlist Config (With 3 Extra Future Slots)
external_playlists = {
    "Ontest-Plus": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
    "BDIX-IPTV": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "Main-IPTV": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u",
    "CricHD": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u",
    
    # --- Future Slots: Bhabishyot-e ekhane link boshaban ---
    "New-Playlist-1": "", 
    "New-Playlist-2": "",
    "New-Playlist-3": ""
}

def clean_and_add_logo_with_group(content, group_name):
    lines = content.splitlines()
    cleaned_lines = []
    for line in lines:
        if line.startswith("#EXTM3U"):
            continue
        if line.startswith("#EXTINF:"):
            # Existing logo replace ba notun kore add
            if 'tvg-logo="' in line:
                line = re.sub(r'tvg-logo=".*?"', f'tvg-logo="{LOGO_URL}"', line)
            else:
                line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{LOGO_URL}"')
                line = line.replace("#EXTINF:0", f'#EXTINF:0 tvg-logo="{LOGO_URL}"')
            
            # Folder/Group management
            if 'group-title="' in line:
                line = re.sub(r'group-title=".*?"', f'group-title="{group_name}"', line)
            else:
                line = line.replace('tvg-logo=', f'group-title="{group_name}" tvg-logo=')
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def run_scraper():
    final_playlist = special_channels_content
    
    for group_name, url in external_playlists.items():
        if not url or not url.startswith("http"):
            continue
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                final_playlist += "\n" + clean_and_add_logo_with_group(r.text, group_name)
                print(f"✅ Group Added with New Logo: {group_name}")
        except:
            print(f"⚠️ Failed to fetch link for: {group_name}")

    # Single M3U file creation
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_playlist)
    print("🚀 playlist.m3u successfully updated with new logo!")

if __name__ == "__main__":
    run_scraper()
