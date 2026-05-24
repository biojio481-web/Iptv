import os
import requests

# ==========================================
# ১. লোগো লিঙ্কসমূহ ও গ্রুপ নেম
# ==========================================
SPECIAL_LOGO_URL = "https://i.postimg.cc/50qZxPkn/Gemini-Generated-Image-sumbp1sumbp1sumb.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

SPECIAL_GROUP = "IPL 2026"
DORAEMON_GROUP = "Doraemon 24/7" # ডোরেমনের জন্য আলাদা সুন্দর ক্যাটাগরি

# ==========================================
# ২. স্পেশাল লাইভ চ্যানেল আপডেট (১ ও ২ নম্বর চ্যানেল)
# ==========================================
# এখানে যখন খুশি আপনি ১ ও ২ নম্বর চ্যানেলের লিংক পরিবর্তন করতে পারবেন।
LIVE_CHANNEL_1_URL = "https://tvsen7.aynaott.com/sspts1/index.m3u8"
LIVE_CHANNEL_2_URL = "https://tvsen7.aynaott.com/tsports-hd/index.m3u8"

# ==========================================
# ৩. ডোরেমন ২৪/৭ পর্বের তালিকা (এখানে ২০টি জায়গা আছে)
# ==========================================
# আপনার দেওয়া ১ম লিংকটি ১ নম্বরে বসানো আছে। বাকিগুলোতে পরে নতুন লিংক বসিয়ে নিবেন।
doraemon_episodes = [
    "https://hcdn3.hakunaymatata.com/resource/57088eff1fe9c788414dd59ca06eb898.mp4?sign=9d3699cf0cd3d59ecca25d1f762d5358&t=1779603649", # এপিসোড ১
    "", # এপিসোড ২ (এখানে নতুন লিংক বসাবেন)
    "", # এপিসোড ৩
    "", # এপিসোড ৪
    "", # এপিসোড ৫
    "", # এপিসোড ৬
    "", # এপিসোড ৭
    "", # এপিসোড ৮
    "", # এপিসোড ৯
    "", # এপিসোড ১০
    "", # এপিসোড ১১
    "", # এপিসোড ১২
    "", # এপিসোড ১৩
    "", # এপিসোড ১৪
    "", # এপিসোড ১৫
    "", # এপিসোড ১৬
    "", # এপিসোড ১৭
    "", # এপিসোড ১৮
    "", # এপিসোড ১৯
    "", # এপিসোড ২০
]

# ==========================================
# ৪. নতুন বাহ্যিক প্লেলিস্ট
# ==========================================
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
            parts = line.split(',', 1)
            channel_name = parts[1] if len(parts) > 1 else "Unknown Channel"
            new_line = f'#EXTINF:-1 tvg-logo="{GENERAL_LOGO_URL}" logo="{GENERAL_LOGO_URL}" group-title="{group_name}",{channel_name}'
            cleaned.append(new_line)
        else:
            cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    print("Playlist আপডেট হচ্ছে... অনুগ্রহ করে একটু অপেক্ষা করুন।")
    
    # ১ ও ২ নম্বর স্পেশাল চ্যানেল সেট করা
    special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Noor Isp
{LIVE_CHANNEL_1_URL}
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Noor Isp
{LIVE_CHANNEL_2_URL}
"""
    final_data = special_channels_content
    
    # ৩ নম্বরের জায়গায় ডোরেমন প্লেলিস্ট অটোমেটিক তৈরি করা
    doraemon_content = []
    for i, ep_url in enumerate(doraemon_episodes, start=1):
        if not ep_url.strip(): # লিংক খালি থাকলে সেটা বাদ দেবে
            continue
        # প্রতিটি পর্ব সুন্দর নাম দিয়ে তৈরি হবে
        meta = f'#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{DORAEMON_GROUP}",Doraemon - Episode {i:02d}'
        doraemon_content.append(meta)
        doraemon_content.append(ep_url.strip())
        
    if doraemon_content:
        final_data += "\n" + "\n".join(doraemon_content)
    
    # এক্সটার্নাল বা বাহ্যিক প্লেলিস্ট থেকে ডাটা আনা
    for name, url in external_playlists.items():
        if not url: continue
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=30)
            
            if r.status_code == 200:
                processed = clean_and_group(r.text, name)
                final_data += "\n" + processed
                print(f"সফলভাবে {name} ক্যাটাগরির চ্যানেলগুলো যুক্ত হয়েছে।")
            else:
                print(f"লিঙ্ক থেকে ডাটা পাওয়া যায়নি। কোড: {r.status_code}")
                
        except Exception as e:
            print(f"সমস্যা হয়েছে: {e}")
            
    # ফাইল ফাইনাল সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    print("-" * 30)
    print("প্লেলিস্ট তৈরি শেষ! এখন 'playlist.m3u' ফাইলটি চেক করুন।")

if __name__ == "__main__":
    run_scraper()
