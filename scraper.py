import os
import requests

# ১. লোগো লিঙ্কসমূহ
SPECIAL_LOGO_URL = "https://i.postimg.cc/50qZxPkn/Gemini-Generated-Image-sumbp1sumbp1sumb.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

# ২. গ্রুপ নেমস
SPECIAL_GROUP = "IPL 2026"

# ৩. স্পেশাল ৩টি চ্যানেল (আপনার আগের পছন্দ অনুযায়ী রাখা হয়েছে)
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Noor Isp
http://198.195.239.50:8095/SonyTenSports5/tracks-v1a1/mono.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Noor Isp
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Unix Tv-Isp
https://live20.bozztv.com/giatvplayout7/giatv-209902/tracks-v1a1/mono.ts.m3u8
"""

# ৪. নতুন বাহ্যিক প্লেলিস্ট (আপনার দেওয়া লেটেস্ট লিঙ্ক)
external_playlists = {
    "Live": "https://go.skym3u.top/g5cm.m3u"
}

def clean_and_group(content, group_name):
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#EXTM3U"):
            continue
        
        if line.startswith("#EXTINF:"):
            # চ্যানেলের নাম আলাদা করা
            parts = line.split(',', 1)
            channel_name = parts[1] if len(parts) > 1 else "Unknown Channel"
            # আপনার লোগো ও গ্রুপ ট্যাগ বসানো
            new_line = f'#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{group_name}",{channel_name}'
            cleaned.append(new_line)
        else:
            # এটি চ্যানেল ইউআরএল
            cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    print("Playlist আপডেট হচ্ছে... অনুগ্রহ করে অপেক্ষা করুন।")
    final_data = special_channels_content
    
    for name, url in external_playlists.items():
        if not url: continue
        try:
            # সার্ভার থেকে ডাটা রিকোয়েস্ট করা
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            r = requests.get(url, headers=headers, timeout=30)
            
            if r.status_code == 200:
                # চ্যানেল সংখ্যা চেক করার জন্য একটি প্রিন্ট দেওয়া হলো
                processed = clean_and_group(r.text, name)
                final_data += "\n" + processed
                print(f"{name} প্লেলিস্ট থেকে চ্যানেল সফলভাবে নেওয়া হয়েছে।")
            else:
                print(f"লিঙ্ক কাজ করছে না। স্ট্যাটাস কোড: {r.status_code}")
                
        except Exception as e:
            print(f"ভুল হয়েছে: {e}")
            
    # ফাইল রাইট করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    print("-" * 30)
    print("অভিনন্দন! 'playlist.m3u' আপডেট হয়ে গেছে।")

if __name__ == "__main__":
    run_scraper()
