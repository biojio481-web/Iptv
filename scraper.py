import requests

def merge_playlists():
    # ১. প্লেলিস্ট লিঙ্ক এবং তাদের জন্য আলাদা নাম (Folder Name)
    playlists = [
        {"name": "BDIX Special", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u"},
        {"name": "Ontest BDIX", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u"},
        {"name": "Mrgify BDIX", "url": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u"},
        {"name": "Main IPTV", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u"},
        {"name": "CricHD Sports", "url": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u"}
    ]
    
    # আপনার সেই ১২টি নিজস্ব চ্যানেল সবার উপরে যোগ করা
    my_own_channels = """#EXTM3U
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

    combined_content = my_own_channels + "\n"
    headers = {'User-Agent': 'Mozilla/5.0'}

    print("চ্যানেলগুলো ক্যাটাগরি অনুযায়ী সাজানো হচ্ছে...")

    for pl in playlists:
        try:
            r = requests.get(pl['url'], headers=headers, timeout=30)
            if r.status_code == 200:
                content = r.text
                # আগের মেইন হেডার বাদ দেওয়া
                data = content.replace("#EXTM3U", "").strip()
                
                # প্রতিটি চ্যানেলের সাথে নতুন ফোল্ডার বা গ্রুপ নাম যোগ করা
                lines = data.split('\n')
                for line in lines:
                    if line.startswith("#EXTINF"):
                        # আগের গ্রুপ টাইটেল থাকলে তা সরিয়ে আপনার দেওয়া নাম বসানো
                        if 'group-title="' in line:
                            import re
                            line = re.sub(r'group-title="[^"]*"', f'group-title="{pl["name"]}"', line)
                        else:
                            line = line.replace("#EXTINF:-1", f'#EXTINF:-1 group-title="{pl["name"]}"')
                    
                    combined_content += line + "\n"
                print(f"যুক্ত হয়েছে: {pl['name']}")
        except Exception as e:
            print(f"এরর: {pl['name']} | {e}")

    # ফাইনাল সেভ
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())
    
    print("\nঅভিনন্দন! ফোল্ডার অনুযায়ী প্লেলিস্ট আপডেট সম্পন্ন হয়েছে।")

if __name__ == "__main__":
    merge_playlists()
