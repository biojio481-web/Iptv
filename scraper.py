import requests
from datetime import datetime

# =================================================================
#  ⚙️ কনফিগারেশন ⚙️
# =================================================================

LIVE_1_LINK = "https://tvsen5.aynaott.com/willowhd/index.m3u8"
LIVE_2_LINK = "https://tvsen7.aynaott.com/tsports-hd/index.m3u8"

# লিংক অদলবদল করা হয়েছে যেন এখন কার্টুন চলে
LIVE_3_LINK_NIGHT = "https://ranapkbd.site/RANAPK33p/TVD/play.php?id=809382" 
LIVE_3_LINK_DAY = "https://ranapkbd.site/RANAPK33p/TVD/play.php?id=372986"   

LOGO_URL = "https://i.postimg.cc/2jczw2z4/file-000000009b507209933f01562a8e146a.png"
EXTERNAL_PLAYLIST_URL = "https://raw.githubusercontent.com/mdarif2743/Cmcl-digital-mpd/refs/heads/main/README.m3u"

# =================================================================
#  Core Logic
# =================================================================

def get_channel_3_link():
    current_hour = datetime.now().hour
    
    # রাত ৮টা (২০) থেকে রাত ১২:৫৯ (০) পর্যন্ত NIGHT লিংক
    if current_hour >= 20 or current_hour < 1:
        return LIVE_3_LINK_NIGHT
    else:
        return LIVE_3_LINK_DAY

def generate_playlist():
    m3u_content = "#EXTM3U\n"
    m3u_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n\n"
    
    m3u_content += f'#EXTINF:-1 tvg-id="live1" tvg-name="Live 1" tvg-logo="{LOGO_URL}" group-title="My Live",Live 1\n{LIVE_1_LINK}\n\n'
    m3u_content += f'#EXTINF:-1 tvg-id="live2" tvg-name="Live 2" tvg-logo="{LOGO_URL}" group-title="My Live",Live 2\n{LIVE_2_LINK}\n\n'
    
    channel_3_active = get_channel_3_link()
    m3u_content += f'#EXTINF:-1 tvg-id="live3" tvg-name="Live 3" tvg-logo="{LOGO_URL}" group-title="My Live",Live 3\n{channel_3_active}\n\n'
    
    try:
        response = requests.get(EXTERNAL_PLAYLIST_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if line.strip() and not line.startswith("#EXTM3U"):
                    m3u_content += line + "\n"
    except Exception as e:
        print(f"Error fetching external playlist: {e}")
        
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
    print("Playlist updated successfully with swapped links!")

if __name__ == "__main__":
    generate_playlist()
