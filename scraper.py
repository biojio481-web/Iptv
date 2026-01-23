import requests
import re

def merge_playlists():
    # ১. আপনার নিজস্ব ১২টি চ্যানেল (সবার উপরে থাকবে)
    combined_content = """#EXTM3U
#EXTINF:-1 group-title="MY BDIX",Live-1
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-2
http://172.16.29.34/live/ontest1/ontest1/252.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-3
http://172.16.29.2:8090/hls/ASportsHD.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-4
http://172.16.29.34/live/ontest1/ontest1/347.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-5
http://172.16.29.34/live/ontest1/ontest1/349.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-6
http://172.16.29.34/live/ontest1/ontest1/443.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-7
http://172.16.29.34/live/ontest1/ontest1/328.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-8
http://172.16.29.34/live/ontest1/ontest1/375.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-9
http://172.16.29.34/live/ontest1/ontest1/480.m3u8
#EXTINF:-1 group-title="MY BDIX",Live-10
http://172.16.29.34/live/ontest1/ontest1/330.m3u8
#EXTINF:-1 group-title="SPECIAL",Live-11-Special
https://ottb.live.cf.ww.aiv-cdn.net/lhr-nitro/live/dash/enc/wf8usag51e/out/v1/bd3b0c314fff4bb1ab4693358f3cd2d3/cenc.mpd
#EXTINF:-1 group-title="SPECIAL",Live-12-Special
https://ranapk.online/RANAPK33x/TVD/play.php?id=809386
"""

    # ২. ৫টি ভিন্ন প্লেলিস্টের জন্য ৫টি ফোল্ডার নাম
    playlists = [
        {"folder": "T20 World Cup 2026 BDIX Special", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u"},
        {"folder": "Free Tv BDIX", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u"},
        {"folder": "Mrgify BDIX", "url": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u"},
        {"folder": "Main Collection", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u"},
        {"folder": "CricHD Sports", "url": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u"}
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}

    for pl in playlists:
        try:
            r = requests.get(pl['url'], headers=headers, timeout=30)
            if r.status_code == 200:
                # মেইন হেডার বাদ দেওয়া
                data = r.text.replace("#EXTM3U", "").strip()
                
                # ফোল্ডার বা ক্যাটাগরি সেট করা
                lines = data.split('\n')
                for line in lines:
                    if line.startswith("#EXTINF"):
                        # যদি আগে থেকেই group-title থাকে তবে সেটি বদলে আমাদের ফোল্ডার নাম দেওয়া
                        if 'group-title="' in line:
                            line = re.sub(r'group-title="[^"]*"', f'group-title="{pl["folder"]}"', line)
                        else:
                            # group-title না থাকলে নতুন করে যোগ করা
                            line = line.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{pl["folder"]}"')
                    
                    if line.strip():
                        combined_content += line + "\n"
        except:
            continue

    # ৩. সেভ করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())
    
    print("Update Success!")

if __name__ == "__main__":
    merge_playlists()
