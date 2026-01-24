import requests
import re

def merge_playlists():
    # আপনার সেই ৩ডি লোগো
    STAR_LOGO = "https://raw.githubusercontent.com/biojio481-web/Iptv/main/Gemini_Generated_Image_36682y36682y3668.png"

    # ১. Emby-র জন্য ইউনিক ID (tvg-id) সহ আপনার চ্যানেলগুলো
    my_content = f"""#EXTM3U
#EXTINF:-1 tvg-id="bdix-tsports" tvg-logo="{STAR_LOGO}" group-title="MY BDIX",Live-1: T-Sports HD
http://172.16.29.2:8090/hls/tsportshd.m3u8
#EXTINF:-1 tvg-id="bdix-live2" tvg-logo="{STAR_LOGO}" group-title="MY BDIX",Live-2
http://172.16.29.34/live/ontest1/ontest1/252.m3u8
#EXTINF:-1 tvg-id="bdix-asports" tvg-logo="{STAR_LOGO}" group-title="MY BDIX",Live-3: A-Sports HD
http://172.16.29.2:8090/hls/ASportsHD.m3u8
#EXTINF:-1 tvg-id="bdix-live4" tvg-logo="{STAR_LOGO}" group-title="MY BDIX",Live-4
http://172.16.29.34/live/ontest1/ontest1/347.m3u8
#EXTINF:-1 tvg-id="bdix-live11" tvg-logo="{STAR_LOGO}" group-title="SPECIAL",Live-11-Special
https://ottb.live.cf.ww.aiv-cdn.net/lhr-nitro/live/dash/enc/wf8usag51e/out/v1/bd3b0c314fff4bb1ab4693358f3cd2d3/cenc.mpd
#EXTINF:-1 tvg-id="special-ranapk" tvg-logo="{STAR_LOGO}" group-title="SPECIAL",Live-12-Special
#EXTVLCOPT:http-user-agent=Mozilla/5.0
#EXTVLCOPT:http-referrer=https://ranapk.online/
https://ranapk.online/RANAPK33x/TVD/play.php?id=809386
"""

    playlists = [
        {"folder": "T20 World Cup 2026 BDIX Special", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u"},
        {"folder": "Ontest Plus", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u"},
        {"folder": "Mrgify BDIX", "url": "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u"},
        {"folder": "Main Collection", "url": "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u"},
        {"folder": "CricHD Sports", "url": "https://iptv-scraper-zilla.pages.dev/CricHD.m3u"}
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    combined_content = my_content + "\n"

    for pl in playlists:
        try:
            r = requests.get(pl['url'], headers=headers, timeout=30)
            if r.status_code == 200:
                data = r.text.replace("#EXTM3U", "").strip()
                lines = data.split('\n')
                count = 0
                for line in lines:
                    if line.startswith("#EXTINF"):
                        count += 1
                        # Emby-র জন্য প্রতিটি লাইনে অটোমেটিক tvg-id যোগ করা
                        if 'tvg-id="' not in line:
                            line = line.replace("#EXTINF:-1", f'#EXTINF:-1 tvg-id="{pl["folder"].replace(" ","")}_{count}"')
                        
                        # লোগো এবং ক্যাটাগরি ফিক্স
                        line = re.sub(r'group-title="[^"]*"', f'group-title="{pl["folder"]}"', line)
                        line = re.sub(r'tvg-logo="[^"]*"', f'tvg-logo="{STAR_LOGO}"', line)

                    if line.strip():
                        combined_content += line + "\n"
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())
    
    print("সফলভাবে Emby ফ্রেন্ডলি প্লেলিস্ট তৈরি হয়েছে।")

if __name__ == "__main__":
    merge_playlists()
