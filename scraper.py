import requests
from datetime import datetime

# কনফিগারেশন
LIVE_1_LINK = "https://tvsen5.aynaott.com/willowhd/index.m3u8"
LIVE_2_LINK = "https://tvsen7.aynaott.com/tsports-hd/index.m3u8"
CARTOON_LINK = "https://ranapkbd.site/RANAPK33p/TVD/play.php?id=734320" 
SPORTS_LINK = "https://ranapkbd.site/RANAPK33p/TVD/play.php?id=809382"    
LOGO_URL = "https://i.postimg.cc/2jczw2z4/file-000000009b507209933f01562a8e146a.png"
EXTERNAL_PLAYLIST_URL = "https://raw.githubusercontent.com/mdarif2743/Cmcl-digital-mpd/refs/heads/main/README.m3u"

def get_channel_3_link():
    # UTC থেকে বাংলাদেশ সময় পেতে ৬ ঘণ্টা যোগ করতে হয়
    # রাত ৮টা (২০:০০) = UTC ১৪:০০
    # রাত ১টা (০১:০০) = UTC ১৯:০০
    # দুপুর ১২টা (১২:০০) = UTC ০৬:০০
    
    current_hour_utc = datetime.utcnow().hour
    # বাংলাদেশ সময় = (current_hour_utc + 6) % 24
    current_hour_bd = (current_hour_utc + 6) % 24
    
    if current_hour_bd >= 20 or current_hour_bd < 1:
        return SPORTS_LINK
    else:
        return CARTOON_LINK

def generate_playlist():
    m3u_content = "#EXTM3U\n#EXTVLCOPT:http-user-agent=Mozilla/5.0\n\n"
    m3u_content += f'#EXTINF:-1 tvg-id="live1" tvg-name="Live 1" tvg-logo="{LOGO_URL}" group-title="My Live",Live 1\n{LIVE_1_LINK}\n\n'
    m3u_content += f'#EXTINF:-1 tvg-id="live2" tvg-name="Live 2" tvg-logo="{LOGO_URL}" group-title="My Live",Live 2\n{LIVE_2_LINK}\n\n'
    m3u_content += f'#EXTINF:-1 tvg-id="live3" tvg-name="Live 3" tvg-logo="{LOGO_URL}" group-title="My Live",Live 3\n{get_channel_3_link()}\n\n'
    
    try:
        response = requests.get(EXTERNAL_PLAYLIST_URL, timeout=10)
        if response.status_code == 200:
            for line in response.text.splitlines():
                if line.strip() and not line.startswith("#EXTM3U"):
                    m3u_content += line + "\n"
    except: pass
        
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)

if __name__ == "__main__":
    generate_playlist()
