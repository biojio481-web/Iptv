import os
import requests

# =================================================================
#  ⚙️ SOCKS5 প্রক্সি কনফিগারেশন (গিটহাব অ্যাকশন থেকে লোড হবে)
# =================================================================
proxy_url = os.getenv('MY_SOCKS5_PROXY')

if proxy_url:
    print("SOCKS5 প্রক্সি সাকসেসফুলি লোড হয়েছে...")
    proxies = {
        'http': proxy_url,
        'https': proxy_url
    }
else:
    print("সতর্কতা: কোনো প্রক্সি পাওয়া যায়নি! নরমাল ইন্টারনেটে রান হচ্ছে...")
    proxies = None

# =================================================================
#  ⚙️ শুধুমাত্র এই নিচের লিংকগুলো আপনার প্রয়োজন মতো পরিবর্তন করবেন ⚙️
# =================================================================

LIVE_1_LINK = "https://tvsen5.aynaott.com/willowhd/index.m3u8"
LIVE_2_LINK = "https://tvsen7.aynaott.com/tsports-hd/index.m3u8"
LIVE_3_LINK = "https://live20.bozztv.com/giatvplayout7/giatv-209902/tracks-v1a1/mono.ts.m3u8"

# ৩টি চ্যানেলের জন্য কমন লোগো লিংক
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
    
    # বাহ্যিক প্লেলিস্ট থেকে ডাটা রিড করা
    try:
        print("SOCKS5 প্রক্সি ব্যবহার করে বাহ্যিক প্লেলিস্ট লোড করা হচ্ছে...")
        # এখানে proxies=proxies যুক্ত করা হয়েছে, যার ফলে এই রিকোয়েস্টটি আপনার প্রক্সি দিয়ে যাবে
        response = requests.get(EXTERNAL_PLAYLIST_URL, proxies=proxies, timeout=15)
        
        if response.status_code == 200:
            external_data = response.text
            for line in external_data.splitlines():
                # ডুপ্লিকেট #EXTM3U ট্যাগ বাদ দিয়ে বাকি চ্যানেলগুলো যুক্ত করা
                if line.strip() and not line.startswith("#EXTM3U"):
                    m3u_content += line + "\n"
        else:
            print(f"Warning: External playlist fetch failed with status {response.status_code}")
    except Exception as e:
        print(f"Error fetching external playlist: {e}")
        
    # ফাইনাল আউটপুট ফাইল তৈরি
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("Playlist updated and generated successfully!")

if __name__ == "__main__":
    generate_playlist()
