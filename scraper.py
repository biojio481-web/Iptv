import os
import requests

# ১. লোগো লিঙ্কসমূহ
SPECIAL_LOGO_URL = "https://i.postimg.cc/50qZxPkn/Gemini-Generated-Image-sumbp1sumbp1sumb.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

# ২. গ্রুপ নেমস
SPECIAL_GROUP = "IPL 2026"

# ৩. স্পেশাল ৩টি চ্যানেল
special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Noor Isp
http://198.195.239.50:8095/SonyTenSports5/tracks-v1a1/mono.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Noor Isp
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Unix Tv-Isp
https://live20.bozztv.com/giatvplayout7/giatv-209902/tracks-v1a1/mono.ts.m3u8
"""

# ৪. আপনার দেওয়া নতুন বাহ্যিক প্লেলিস্ট (৬০০+ চ্যানেল)
external_playlists = {
    "Live": "https://go.skym3u.top/69di.m3u"
}

def clean_and_group(content, group_name):
    """চ্যানেলগুলোকে আপনার পছন্দের লোগো ও গ্রুপে সাজানোর ফাংশন"""
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        if line.startswith("#EXTM3U") or not line.strip():
            continue
        if line.startswith("#EXTINF:"):
            # নাম খুঁজে বের করা
            parts = line.split(',', 1)
            channel_name = parts[1] if len(parts) > 1 else "Unknown Channel"
            # নতুন করে লোগো ও গ্রুপ বসানো
            new_line = f'#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{group_name}",{channel_name}'
            cleaned.append(new_line)
        else:
            # এটি চ্যানেলের লিঙ্ক (URL)
            cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    print("Updating Playlist... Please wait.")
    final_data = special_channels_content
    
    for name, url in external_playlists.items():
        if not url: continue
        try:
            # লিঙ্ক থেকে ডাটা সংগ্রহ করা
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            r = requests.get(url, headers=headers, timeout=30)
            
            if r.status_code == 200:
                print(f"Successfully fetched {name} playlist.")
                # চ্যানেলগুলো প্রসেস করা
                processed_channels = clean_and_group(r.text, name)
                final_data += "\n" + processed_channels
            else:
                print(f"Failed to fetch {name}. Status code: {r.status_code}")
                
        except Exception as e:
            print(f"An error occurred with {name}: {e}")
            
    # ফাইল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    print("-" * 30)
    print("Playlist Updated Successfully!")
    print("Check 'playlist.m3u' file now.")

if __name__ == "__main__":
    run_scraper()
