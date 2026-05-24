import subprocess
import time

# =========================================================================
# 📺 আপনার ভিডিও প্লেলিস্ট সেকশন (এখানে আপনার লিংকগুলো বসাবেন)
# =========================================================================

# ১. ডোরেমন সেকশন (আপনার দেওয়া টেস্ট লিংকটি ১ নম্বরে সেট করা হয়েছে)
DORAEMON_PLAYLIST = [
    "https://hcdn3.hakunaymatata.com/resource/57088eff1fe9c788414dd59ca06eb898.mp4?sign=9d3699cf0cd3d59ecca25d1f762d5358&t=1779603649",
    "", # ২ নম্বর ঘর (লিংক বসানোর জন্য খালি)
    "", # ৩ নম্বর ঘর
    "", # ৪ নম্বর ঘর
    "", # ৫ নম্বর ঘর
    "", # ৬ নম্বর ঘর
    "", # ৭ নম্বর ঘর
    "", # ৮ নম্বর ঘর
    "", # ৯ নম্বর ঘর
    "", # ১০ নম্বর ঘর
    "", # ১১ নম্বর ঘর
    "", # ১২ নম্বর ঘর
    "", # ১৩ নম্বর ঘর
    "", # ১৪ নম্বর ঘর
    "", # ১৫ নম্বর ঘর
    "", # ১৬ নম্বর ঘর
    "", # ১৭ নম্বর ঘর
    "", # ১৮ নম্বর ঘর
    "", # ১৯ নম্বর ঘর
    "", # ২০ নম্বর ঘর
]

# ২. পারম্যান সেকশন (সব ঘর খালি, লিংক পেলে অটো চালু হবে)
PERMAN_PLAYLIST = [
    "", # ১ নম্বর ঘর
    "", # ২ নম্বর ঘর
    "", # ৩ নম্বর ঘর
    "", # ৪ নম্বর ঘর
    "", # ۵ নম্বর ঘর
    "", # ৬ নম্বর ঘর
    "", # ৭ নম্বর ঘর
    "", # ৮ নম্বর ঘর
    "", # ৯ নম্বর ঘর
    "", # ১০ নম্বর ঘর
    "", # ১১ নম্বর ঘর
    "", # ১২ নম্বর ঘর
    "", # ১৩ নম্বর ঘর
    "", # ১৪ নম্বর ঘর
    "", # ১৫ নম্বর ঘর
    "", # ১৬ নম্বর ঘর
    "", # ১৭ নম্বর ঘর
    "", # ১৮ নম্বর ঘর
    "", # ১৯ নম্বর ঘর
    "", # ২০ নম্বর ঘর
]


# =========================================================================
# 📡 লাইভ স্ট্রিমিং সার্ভার কনফিগারেশন
# =========================================================================
# আপনার ইউটিউব/ফেসবুক বা আইপিটিভি সার্ভারের RTMP URL এবং Stream Key এখানে দিন
STREAM_URL = "rtmp://your_streaming_server_url/live/stream_key"


def get_master_playlist():
    """খালি ঘরগুলো বাদ দিয়ে শুধুমাত্র আসল লিংকগুলোর একটি প্লেলিস্ট তৈরি করবে"""
    master_list = []
    
    # ডোরেমন লিংক চেক
    for link in DORAEMON_PLAYLIST:
        # লিংক যদি খালি না হয় এবং এতে http বা https থাকে
        if link and link.strip() and link.startswith("http"):
            master_list.append((link.strip(), "Doraemon"))
            
    # পারম্যান লিংক检查
    for link in PERMAN_PLAYLIST:
        if link and link.strip() and link.startswith("http"):
            master_list.append((link.strip(), "Perman"))
            
    return master_list


def start_streaming():
    print("🚀 ২৪/৭ কার্টুন লাইভ স্ট্রিমিং সিস্টেম চালু হচ্ছে...")
    
    while True:
        playlist = get_master_playlist()
        
        if not playlist:
            print("⚠️ প্লেলিস্টে কোনো ভিডিও লিংক পাওয়া যায়নি! অনুগ্রহ করে কোডে লিংক বসান।")
            time.sleep(10)
            continue
            
        total_videos = len(playlist)
        
        for index, (video_url, show_name) in enumerate(playlist, start=1):
            print(f"\n📺 [{show_name}] মোট {total_videos} টির মধ্যে {index} নম্বর ভিডিও চলছে...")
            print(f"🔗 লিংক: {video_url}")
            
            # FFmpeg কমান্ড (ভিডিও লাইভ স্ট্রিমিং ইঞ্জিন)
            ffmpeg_command = [
                'ffmpeg',
                '-re',
                '-i', video_url,
                '-c:v', 'libx264',
                '-preset', 'veryfast',
                '-b:v', '2000k',
                '-maxrate', '2500k',
                '-bufsize', '4000k',
                '-pix_fmt', 'yuv420p',
                '-g', '50',
                '-c:a', 'aac',
                '-b:a', '128k',
                '-ar', '44100',
                '-f', 'flv',
                STREAM_URL
            ]
            
            try:
                # স্ট্রিম চালু করা
                process = subprocess.Popen(ffmpeg_command)
                process.wait()  # ভিডিওটি শেষ হওয়া পর্যন্ত অপেক্ষা করবে
            except Exception as e:
                print(f"❌ এই লিংকটি চালাতে সমস্যা হয়েছে: {e}")
                time.sleep(5)
                
        print("\n🔄 প্লেলিস্টের শেষ ভিডিও শেষ হয়েছে। লুপ সিস্টেমের কারণে আবার ১ম ভিডিও থেকে শুরু হচ্ছে...")
        time.sleep(2)

if __name__ == "__main__":
    start_streaming()
