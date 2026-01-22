import requests

def merge_playlists():
    # আপনার দেওয়া ৪টি এবং ভবিষ্যতে যোগ করার জন্য ২টির জায়গা রাখা হয়েছে
    playlist_links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_OTT_Navigator.m3u",
        
        # ভবিষ্যতে নতুন লিঙ্ক যোগ করতে চাইলে নিচের উদ্ধৃতি চিহ্নের (" ") ভেতরে বসাবেন
        "", # এখানে ৫ নম্বর লিঙ্ক দিতে পারবেন
        ""  # এখানে ৬ নম্বর লিঙ্ক দিতে পারবেন
    ]
    
    combined_content = "#EXTM3U\n"
    
    print("প্লেলিস্ট মার্জ করা শুরু হচ্ছে...")

    for url in playlist_links:
        # লিঙ্কটি খালি থাকলে তা স্কিপ করবে
        if not url.strip():
            continue
            
        try:
            # লিঙ্ক থেকে ডাটা নিয়ে আসা
            r = requests.get(url, timeout=30)
            if r.status_code == 200:
                # মেইন হেডার বাদ দিয়ে শুধু চ্যানেলের তথ্য নেওয়া
                data = r.text.replace("#EXTM3U", "").strip()
                if data:
                    combined_content += data + "\n"
                    print(f"সফলভাবে যোগ হয়েছে: {url}")
            else:
                print(f"লিঙ্কটি কাজ করছে না: {url}")
        except Exception as e:
            print(f"এরর: {url} | {e}")

    # নতুন playlist.m3u ফাইলটি তৈরি করা
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())
    
    print("\nঅভিনন্দন! আপনার playlist.m3u ফাইলটি তৈরি হয়ে গেছে।")

if __name__ == "__main__":
    merge_playlists()
