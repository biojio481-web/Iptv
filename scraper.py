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
# ২. স্পেশাল লাইভ চ্যানেল আপডেট (এখানে লিংক পরিবর্তন করবেন)
# ==========================================
# ১ নম্বর এবং ২ নম্বর চ্যানেলের লিংক নিচে দেওয়া আছে। যখনই লিংক পরিবর্তন করতে চান, 
# শুধু "https://..." অংশটি মুছে আপনার নতুন লিংকটি বসিয়ে দিবেন।
LIVE_CHANNEL_1_URL = "https://tvsen7.aynaott.com/sspts1/index.m3u8" # ১ নম্বর চ্যানেলের লিংক
LIVE_CHANNEL_2_URL = "https://tvsen7.aynaott.com/tsports-hd/index.m3u8" # ২ নম্বর চ্যানেলের লিংক

# ==========================================
# ৩. ডোরেমন ২৪/৭ পর্বের তালিকা (এখানে আপনার ২০টি পর্বের জায়গা রয়েছে)
# ==========================================
# আপনার দেওয়া ১ম লিংকটি নিচে বসানো আছে। বাকি খালি জায়গাগুলোতে পরে নতুন লিংক বসাবেন।
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
# ৪. FFmpeg এর জন্য প্লেলিস্ট ফাইল তৈরি করার ফাংশন
# ==========================================
def generate_ffmpeg_playlist():
    valid_eps = [ep for ep in doraemon_episodes if ep.strip()]
    if not valid_eps:
        print("Error: কোনো ডোরেমন লিংক খুঁজে পাওয়া যায়নি! দয়া করে অন্তত ১টি লিংক রাখুন।")
        return False
        
    with open("ffmpeg_list.txt", "w", encoding="utf-8") as f:
        for ep in valid_eps:
            f.write(f"file '{ep}'\n")
    return True

# ==========================================
# ৫. লাইভ স্ট্রিমিং রুট (যা আসল টিভির মতো ডাটা স্ট্রিম করবে)
# ==========================================
@app.route('/doraemon_live.mp4')
def doraemon_live():
    valid_eps = [ep for ep in doraemon_episodes if ep.strip()]
    if not valid_eps:
        return "No episodes configured", 404

    # FFmpeg কমান্ড: রিয়েল-টাইমে নিরবচ্ছিন্ন লুপ লাইভ স্ট্রিম তৈরি করার জন্য
    ffmpeg_cmd = [
        'ffmpeg',
        '-re',                             # রিয়াল-টাইম স্পিডে রিড করবে (লাইভ টিভি মোড)
        '-f', 'concat',                    # সব ভিডিও একসাথে জোড়া দেবে
        '-safe', '0',
        '-protocol_whitelist', 'file,http,https,tcp,tls',
        '-loop', '1',                      # পুরো লিস্টের শেষ পর্ব শেষ হলে আবার ১ম পর্ব থেকে লুপ করবে
        '-i', 'ffmpeg_list.txt',
        '-c', 'copy',                      # সোর্স ফরম্যাট ডিরেক্ট কপি করবে
        '-f', 'mp4',                       # আউটপুট ভিডিও ফরম্যাট
        '-movflags', 'frag_keyframe+empty_moov', # লাইভ স্ট্রিম সচল রাখার জন্য জরুরি ফ্ল্যাগ
        'pipe:1'                           # আউটপুট সরাসরি পাইথন সার্ভারে পাঠাবে
    ]
    
    def generate_stream():
        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        try:
            while True:
                data = process.stdout.read(4096)
                if not data:
                    break
                yield data
        except GeneratorExit:
            process.terminate()
        finally:
            process.kill()

    return Response(generate_stream(), mimetype='video/mp4')

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
    
    # ডাইনামিক লিংক ব্যবহার করে ১ ও ২ নম্বর চ্যানেল জেনারেট করা
    special_channels_content = f"""#EXTM3U
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-1-Noor Isp
{LIVE_CHANNEL_1_URL}
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-2-Noor Isp
{LIVE_CHANNEL_2_URL}
#EXTINF:-1 tvg-logo="{SPECIAL_LOGO_URL}" logo="{SPECIAL_LOGO_URL}" group-title="{SPECIAL_GROUP}",Live-3-Doraemon 24/7 (Live TV Mode)
http://localhost:5000/doraemon_live.mp4
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
        print("\n📺 আসল লাইভ টিভি মোডে ডোরেমন চ্যানেল ব্যাকগ্রাউন্ডে চালু হচ্ছে...")
        print("আপনার টিভিতে বা প্লেয়ারে ৩ নম্বর চ্যানেলটি অন করুন।")
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
