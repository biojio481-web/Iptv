import os
import requests
import re

# 1. Logo Configuration
LOGO_URL = "Gemini_Generated_Image_36682y36682y3668.png"

# 2. Special 12 Channels Data (T20 World Cup 2026 Special BDIX)
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

# 3. All Playlists (Including Future Slots)
playlists = {
    "Ontest-Plus": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
    "BDIX-IPTV": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
    "Main-IPTV": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u",
    "CricHD": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u",
    
    # --- Future Links (Ekhane link dilei automatic logo set hobe) ---
    "Future-List-1": "", 
    "Future-List-2": "",
    "Future-List-3": ""
}

def add_logo_to_m3u(content):
    """Playlist-er protiti channel-e logo add ba replace korar function"""
    lines = content.splitlines()
    new_lines = []
    for line in lines:
        if line.startswith("#EXTINF:"):
            # Age logo thakle seta replace korbe, na thakle add korbe
            if 'tvg-logo="' in line:
                line = re.sub(r'tvg-logo=".*?"', f'tvg-logo="{LOGO_URL}"', line)
            else:
                line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{LOGO_URL}"')
                line = line.replace("#EXTINF:0", f'#EXTINF:0 tvg-logo="{LOGO_URL}"')
        new_lines.append(line)
    return "\n".join(new_lines)

def run_scraper():
    # A. Special Folder Update
    special_folder = "T20 World Cup 2026 Special BDIX"
    os.makedirs(special_folder, exist_ok=True)
    with open(f"{special_folder}/playlist.m3u", "w", encoding="utf-8") as f:
        f.write(special_channels_content)
    print(f"✅ Created/Updated: {special_folder}")

    # B. Loop for all other playlists
    for folder, url in playlists.items():
        if not url: # Link na thakle skip korbe
            continue
            
        os.makedirs(folder, exist_ok=True)
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                # Logo inject kora hochhe
                modified_content = add_logo_to_m3u(r.text)
                with open(f"{folder}/playlist.m3u", "w", encoding="utf-8") as f:
                    f.write(modified_content)
                print(f"🚀 Successfully processed: {folder}")
            else:
                print(f"❌ Failed to fetch: {folder} (Status: {r.status_code})")
        except Exception as e:
            print(f"⚠️ Error in {folder}: {e}")

if __name__ == "__main__":
    run_scraper()
