import requests

# =================================================================
#  ⚙️ শুধুমাত্র এই নিচের লিংকগুলো আপনার প্রয়োজন মতো পরিবর্তন করবেন ⚙️
# =================================================================

LIVE_1_LINK = "https://ranapkbd.site/RANAPK33g/TVD/play.php?id=661053"
LIVE_2_LINK = "https://ranapkz.site/RANAPK33k/TVD/play.php?id=944612"
LIVE_3_LINK = "https://ranapkz.site/RANAPK33k/TVD/play.php?id=372986"

# ⚽ FIFA World Cup 2026 চ্যানেলগুলোর লিংক (এখানে আপনার লিংক বসিয়ে দিন)
FIFA_1_LINK = "https://ranapkbd.site/RANAPK33g/TVD/play.php?id=372986"
FIFA_2_LINK = "http://97.74.103.44:8089/amrbd/T-SPORTS/playlist.m3u8"
FIFA_3_LINK = "http://10.10.10.2/live/fnf006/index.m3u8"

# সব চ্যানেলের জন্য কমন লোগো লিংক
LOGO_URL = "https://i.postimg.cc/2jczw2z4/file-000000009b507209933f01562a8e146a.png"

# আপনার বাহ্যিক (External) গিটহাব প্লেলিস্ট লিংক
EXTERNAL_PLAYLIST_URL = "https://raw.githubusercontent.com/mdarif2743/Cmcl-digital-mpd/refs/heads/main/README.m3u"

# =================================================================
#  🚫 নিচের কোডটিতে কোনো পরিবর্তন করার প্রয়োজন নেই (Core Logic)
# =================================================================

def generate_playlist():
    m3u_content = "#EXTM3U\n"
    m3u_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n\n"
    
    # চ্যানেল ১ জেনারেট
    m3u_content += f'#EXTINF:-1 tvg-id="live1" tvg-name="Live 1" tvg-logo="{LOGO_URL}" group-title="My Live",Live 1\n'
    m3u_content += f"{LIVE_1_LINK}\n\n"
    
    # চ্যানেল ২ জেনারেট
    m3u_content += f'#EXTINF:-1 tvg-id="live2" tvg-name="Live 2" tvg-logo="{LOGO_URL}" group-title="My Live",Live 2\n'
    m3u_content += f"{LIVE_2_LINK}\n\n"
    
    # চ্যানেল ৩ জেনারেট
    m3u_content += f'#EXTINF:-1 tvg-id="live3" tvg-name="Live 3" tvg-logo="{LOGO_URL}" group-title="My Live",Live 3\n'
    m3u_content += f"{LIVE_3_LINK}\n\n"
    
    # ⚽ FIFA World Cup 1 জেনারেট
    m3u_content += f'#EXTINF:-1 tvg-id="fifa1" tvg-name="FIFA World Cup 1" tvg-logo="{LOGO_URL}" group-title="FIFA World Cup 2026",FIFA World Cup 1\n'
    m3u_content += f"{FIFA_1_LINK}\n\n"
    
    # ⚽ FIFA World Cup 2 জেনারেট
    m3u_content += f'#EXTINF:-1 tvg-id="fifa2" tvg-name="FIFA World Cup 2" tvg-logo="{LOGO_URL}" group-title="FIFA World Cup 2026",FIFA World Cup 2\n'
    m3u_content += f"{FIFA_2_LINK}\n\n"
    
    # ⚽ FIFA World Cup 3 জেনারেট
    m3u_content += f'#EXTINF:-1 tvg-id="fifa3" tvg-name="FIFA World Cup 3" tvg-logo="{LOGO_URL}" group-title="FIFA World Cup 2026",FIFA World Cup 3\n'
    m3u_content += f"{FIFA_3_LINK}\n\n"
    
    # বাহ্যিক প্লেলিস্ট থেকে ডাটা রিড করা
    try:
        response = requests.get(EXTERNAL_PLAYLIST_URL, timeout=10)
        if response.status_code == 200:
            external_data = response.text
            for line in external_data.splitlines():
                if line.strip() and not line.startswith("#EXTM3U"):
                    m3u_content += line + "\n"
        else:
            print(f"Warning: External playlist fetch failed with status {response.status_code}")
    except Exception as e:
        print(f"Error fetching external playlist: {e}")
        
    # ফাইনাল আউটপুট ফাইল তৈরি
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("Playlist updated and generated successfully with FIFA World Cup channels!")

if __name__ == "__main__":
    generate_playlist()
