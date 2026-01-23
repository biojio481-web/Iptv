import datetime
import pytz
import requests

def update_playlist():
    # ১. বাংলাদেশ সময় সেট করা
    tz = pytz.timezone('Asia/Dhaka')
    hour = datetime.datetime.now(tz).hour

    # ২. আপনার দেওয়া চ্যানেলের লিস্ট (বিডিআইএক্স ট্যাগ সহ)
    channels = [
        {"name": "Live-1 (T-Sports HD)", "url": "http://172.16.29.2:8090/hls/tsportshd.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-2", "url": "http://172.16.29.34/live/ontest1/ontest1/252.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-3 (A-Sports HD)", "url": "http://172.16.29.2:8090/hls/ASportsHD.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-4", "url": "http://172.16.29.34/live/ontest1/ontest1/347.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-5", "url": "http://172.16.29.34/live/ontest1/ontest1/349.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-6", "url": "http://172.16.29.34/live/ontest1/ontest1/443.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-7", "url": "http://172.16.29.34/live/ontest1/ontest1/328.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-8", "url": "http://172.16.29.34/live/ontest1/ontest1/375.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-9", "url": "http://172.16.29.34/live/ontest1/ontest1/480.m3u8", "group": "BDIX LIVE"},
        {"name": "Live-10", "url": "http://172.16.29.34/live/ontest1/ontest1/330.m3u8", "group": "BDIX LIVE"},
        # এই ২টিকে BDIX অপ্টিমাইজড করা হয়েছে
        {"name": "Live-11-Special (BDIX Optimized)", "url": "https://ottb.live.cf.ww.aiv-cdn.net/lhr-nitro/live/dash/enc/wf8usag51e/out/v1/bd3b0c314fff4bb1ab4693358f3cd2d3/cenc.mpd", "group": "BDIX SPECIAL"},
        {"name": "Live-12-Special (BDIX Optimized)", "url": "https://ranapk.online/RANAPK33x/TVD/play.php?id=809386", "group": "BDIX SPECIAL"}
    ]

    # ৩. কন্টেন্ট তৈরি শুরু
    combined_content = "#EXTM3U\n"
    
    # আপনার শিডিউল করা কার্টুন/স্পোর্টস সবার উপরে রাখার জন্য:
    if 18 <= hour < 24:
        # রাত ৬টা থেকে ১২টা পর্যন্ত ১ নম্বর চ্যানেলটি (T-Sports) স্পেশাল হিসেবে দেখাবে
        combined_content += f"#EXTINF:-1 group-title=\"CURRENT SCHEDULE\", *** SPORTS TIME (T-SPORTS) ***\n{channels[0]['url']}\n"
    
    # ৪. সব চ্যানেল প্লেলিস্টে যোগ করা
    for ch in channels:
        combined_content += f"#EXTINF:-1 group-title=\"{ch['group']}\", {ch['name']}\n"
        # BDIX স্পিড বুস্ট করার জন্য বিশেষ প্রোপার্টি যোগ করা
        combined_content += f"#KODIPROP:inputstream.adaptive.manifest_type=hls\n"
        combined_content += f"{ch['url']}\n"

    # ৫. এক্সটার্নাল প্লেলিস্ট মার্জ করা
    other_links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://iptv-scraper-zilla.pages.dev/CricHD.m3u"
    ]
    
    for link in other_links:
        try:
            r = requests.get(link, timeout=15)
            if r.status_code == 200:
                data = r.text.replace("#EXTM3U", "").strip()
                combined_content += data + "\n"
        except:
            continue

    # ৬. ফাইল সেভ
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())

    print(f"BDIX Optimized Playlist Updated at {hour}:00 Dhaka Time")

if __name__ == "__main__":
    update_playlist()
