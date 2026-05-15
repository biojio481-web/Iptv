import os
import requests

# ১. লোগো লিঙ্কসমূহ
SPECIAL_LOGO_URL = "https://i.postimg.cc/50qZxPkn/Gemini-Generated-Image-sumbp1sumbp1sumb.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

# ২. গ্রুপ নেমস
SPECIAL_GROUP = "IPL 2026"

# ৩. আপনার স্পেশাল ৩টি চ্যানেল
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Noor Isp
http://198.195.239.50:8095/SonyTenSports5/tracks-v1a1/mono.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Noor Isp
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Unix Tv-Isp
https://live20.bozztv.com/giatvplayout7/giatv-209902/tracks-v1a1/mono.ts.m3u8
"""

# ৪. নতুন বাহ্যিক প্লেলিস্ট (GitHub লিঙ্কটি এখানে বসানো হয়েছে)
external_playlists = {
    "Live": "https://raw.githubusercontent.com/mdarif2743/Cmcl-digital-mpd/refs/heads/main/README.m3u"
}

def clean_and_group(content, group_name):
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#EXTM3U"):
            continue
        
        if line.startswith("#EXTINF:"):
            # মেইন নাম বের করা (কমা এর পরের অংশ)
            parts = line.split(',', 1)
            channel_name = parts[1] if len(parts) > 1 else "Unknown Channel"
            # জেনারেল লোগো এবং আপনার দেওয়া গ্রুপ নাম সেট করা
            new_line = f'#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{group_name}",{channel_name}'
            cleaned.append(new_line)
        else:
            # এটি চ্যানেল ইউআরএল
            cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    print("Playlist আপডেট হচ্ছে... অনুগ্রহ করে একটু অপেক্ষা করুন।")
    final_data = special_channels_content
    
    for name, url in external_playlists.items():
        if not url: continue
        try:
            # GitHub বা অন্যান্য সার্ভার থেকে ডাটা আনতে হেডার ব্যবহার
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=30)
            
            if r.status_code == 200:
                processed = clean_and_group(r.text, name)
                final_data += "\n" + processed
                print(f"সফলভাবে {name} ক্যাটাগরির চ্যানেলগুলো যুক্ত হয়েছে।")
            else:
                print(f"লিঙ্ক থেকে ডাটা পাওয়া যায়নি। কোড: {r.status_code}")
                
        except Exception as e:
            print(f"সমস্যা হয়েছে: {e}")
            
    # ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    print("-" * 30)
    print("প্লেলিস্ট তৈরি শেষ! এখন 'playlist.m3u' ফাইলটি চেক করুন।")

if __name__ == "__main__":
    run_scraper()
