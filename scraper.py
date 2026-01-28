import os
import requests
import re

# ১. আপনার ৪ডি কালারফুল স্টার টিভি এইচডি লোগো (Raw Link)
LOGO_URL = "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Gemini_Generated_Image_md4brsmd4brsmd4b.png"

def clean_and_group(content, group_name):
    lines = content.splitlines()
    cleaned = []
    for line in lines:
        if line.startswith("#EXTM3U"): continue
        if line.startswith("#EXTINF:"):
            # পুরনো সব লোগো ট্যাগ পরিষ্কার করা হচ্ছে
            line = re.sub(r'tvg-logo=".*?"', '', line)
            line = re.sub(r'logo=".*?"', '', line)
            line = re.sub(r'group-title=".*?"', '', line)
            
            # নিখুঁতভাবে লোগো এবং গ্রুপ সেট করা (Universal Support)
            # এখানে tvg-logo এবং logo দুটিই রাখা হয়েছে যাতে সব অ্যাপে কাজ করে
            line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-logo="{LOGO_URL}" logo="{LOGO_URL}" group-title="{group_name}"')
        
        if line.strip():
            cleaned.append(line)
    return "\n".join(cleaned)

def run_scraper():
    # প্লেলিস্টের শুরুতে হেডার
    final_data = "#EXTM3U\n"
    
    # আপনার এক্সটারনাল প্লেলিস্টগুলো
    external_playlists = {
        "Ontest-Plus": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
        "BDIX-IPTV": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "Main-IPTV": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u",
        "CricHD": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u"
    }

    for name, url in external_playlists.items():
        try:
            # সার্ভার ব্লক এড়াতে হেডার ব্যবহার
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                final_data += clean_and_group(r.text, name) + "\n"
        except Exception as e:
            print(f"Failed to fetch {name}: {e}")
            
    # ফাইলটি সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print("✅ Playlist with Star TV HD Logo is Ready!")

if __name__ == "__main__":
    run_scraper()
