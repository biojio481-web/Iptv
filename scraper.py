import requests

def create_playlist():
    # ১. আপনার নিজস্ব ১২টি চ্যানেল (সবার উপরে থাকবে)
    my_content = """#EXTM3U
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

    other_sources = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://iptv-scraper-zilla.pages.dev/CricHD.m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u"
    ]

    combined = my_content + "\n"
    for url in other_sources:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                data = r.text.replace("#EXTM3U", "").strip()
                combined += data + "\n"
        except:
            continue

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined.strip())

if __name__ == "__main__":
    create_playlist()
