import os
import sys
import subprocess
import requests
from flask import Flask, Response

app = Flask(__name__)

# ==========================================
# ১. লোগো লিঙ্কসমূহ
# ==========================================
SPECIAL_LOGO_URL = "https://i.postimg.cc/50qZxPkn/Gemini-Generated-Image-sumbp1sumbp1sumb.png" 
GENERAL_LOGO_URL = "https://i.postimg.cc/htPYZxk7/IMG-20260128-153357.png" 

SPECIAL_GROUP = "IPL 2026"

# ==========================================
# ২. স্পেশাল লাইভ চ্যানেল আপডেট
# ==========================================
LIVE_CHANNEL_1_URL = "https://tvsen7.aynaott.com/sspts1/index.m3u8"
LIVE_CHANNEL_2_URL = "https://tvsen7.aynaott.com/tsports-hd/index.m3u8"

# ==========================================
# ৩. ডোরেমন ২৪/৭ পর্বের তালিকা (২০টি জায়গা)
# ==========================================
doraemon_episodes = [
    "https://hcdn3.hakunaymatata.com/resource/57088eff1fe9c788414dd59ca06eb898.mp4?sign=9d3699cf0cd3d59ecca25d1f762d5358&t=1779603649", # এপিসোড ১
    "", # এপিসোড ২
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
# ৪. FFmpeg এর জন্য প্লেলিস্ট ফাইল তৈরি করা
# ==========================================
def generate_ffmpeg_playlist():
    valid_eps = [ep for ep in doraemon_episodes if ep.strip()]
    if not valid_eps:
        print("Error: কোনো ডোরেমন লিংক খুঁজে পাওয়া যায়নি!")
        return False
        
    with open("ffmpeg_list.txt", "w", encoding="utf-8") as f:
        for ep in valid_eps:
            f.write(f"file '{ep}'\n")
    return True

# ==========================================
# ৫. আপডেটেড লাইভ স্ট্রিমিং রুট (ব্লক লস মুক্ত)
# ==========================================
@app.route('/doraemon_live.ts') # .mp4 থেকে .ts (MPEG-TS) করা হয়েছে লাইভ স্ট্রিমিং স্মুথ করার জন্য
def doraemon_live():
    valid_eps = [ep for ep in doraemon_episodes if ep.strip()]
    if not valid_eps:
        return "No episodes configured", 404

    # অপ্টিমাইজড FFmpeg কমান্ড (অনলাইন লিংকের বাফারিং ও ব্লক লস ফিক্সড)
    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-protocol_whitelist', 'file,http,https,tcp,tls',
        '-loop', '1',                      # লুপ চালু থাকবে
        '-probesize', '32k',               # দ্রুত স্টার্ট হওয়ার জন্য প্রোব সাইজ কমানো হয়েছে
        '-max_delay', '500000',            # বাফার লাইভ ডিলে ম্যানেজমেন্ট
        '-i', 'ffmpeg_list.txt',
        '-c:v', 'copy',                    # ভিডিও নো-এনকোড কপি
        '-c:a', 'copy',                    # অডিও নো-এনকোড কপি
        '-f', 'mpegts',                    # লাইভ টিভির জন্য সবচেয়ে স্টেবল ফরম্যাট
        'pipe:1'
    ]
    
    def generate_stream():
        # বড় বাফার সাইজ (bufsize) দিয়ে প্রসেস ওপেন করা যাতে ব্লক লস না হয়
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=10**6)
        try:
            while True:
                data = process.stdout.read(8192) #Chunk সাইজ ৪১৮২ থেকে ৮১৯২ করা হয়েছে
                if not data:
                    break
                yield data
        except GeneratorExit:
            process.terminate()
        finally:
            process.kill()

    # মিম-টাইপ mpegts দেওয়া হয়েছে যাতে প্লেয়ার বাফারিং না করে সরাসরি লাইভ ট্রিট করে
    return Response(generate_stream(), mimetype='video/mpegts')

# ==========================================
# ৬. বাহ্যিক প্লেলিস্ট এবং M3U জেনারেটর
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

def create_playlist():
    print("M3U Playlist ফাইল তৈরি হচ্ছে...")
    
    special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Noor Isp
{LIVE_CHANNEL_1_URL}
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Noor Isp
{LIVE_CHANNEL_2_URL}
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Doraemon 24/7 (Live TV Mode)
http://localhost:5000/doraemon_live.ts
"""
    final_data = special_channels_content
    
    for name, url in external_playlists.items():
        if not url: continue
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            r = requests.get(url, headers=headers, timeout=30)
            if r.status_code == 200:
                processed = clean_and_group(r.text, name)
                final_data += "\n" + processed
            else:
                print(f"লিঙ্ক থেকে ডাটা পাওয়া যায়নি। কোড: {r.status_code}")
        except Exception as e:
            print(f"বাহ্যিক প্লেলিস্ট আনতে সমস্যা: {e}")
            
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    print("playlist.m3u সফলভাবে তৈরি হয়েছে!")

if __name__ == "__main__":
    if generate_ffmpeg_playlist():
        create_playlist()
        print("\n📺 ফিক্সড লাইভ টিভি মোডে ডোরেমন চ্যানেল ব্যাকগ্রাউন্ডে চালু হচ্ছে...")
        print("আপনার প্লেয়ার বা টিভিতে ৩ নম্বর চ্যানেলটি চালু করে টেস্ট করুন।")
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
