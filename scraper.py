import requests

def merge_playlists():
    # আপনার সব প্লেলিস্ট লিঙ্ক (নতুনটিসহ মোট ৫টি)
    playlist_links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "https://raw.githubusercontent.com/BINOD-XD/Toffee-Auto-Update-Playlist/refs/heads/main/toffee_OTT_Navigator.m3u",
        "https://ranapk.short.gy/TG@RANAPKBDSx/tvd.m3u", # এই যে আপনার নতুন লিঙ্কটি
        
        # ভবিষ্যতে আরও লিঙ্ক যোগ করতে চাইলে নিচের কোটেশনের ভেতরে বসাবেন
        "" 
    ]
    
    combined_content = "#EXTM3U\n"
    
    print("চ্যানেলগুলো একত্রিত করা শুরু হচ্ছে...")

    for url in playlist_links:
        if not url.strip():
            continue
            
        try:
            # allow_redirects=True দেওয়া হয়েছে কারণ আপনার নতুন লিঙ্কটি একটি শর্ট লিঙ্ক
            r = requests.get(url, timeout=30, allow_redirects=True)
            if r.status_code == 200:
                data = r.text.replace("#EXTM3U", "").strip()
                if data:
                    combined_content += data + "\n"
                    print(f"সফল হয়েছে: {url}")
            else:
                print(f"লিঙ্কটি কাজ করছে না: {url}")
        except Exception as e:
            print(f"এরর: {url} | {e}")

    # ফাইনাল playlist.m3u ফাইল তৈরি
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())
    
    print("\nঅভিনন্দন! আপনার প্লেলিস্ট আপডেট হয়ে গেছে।")

if __name__ == "__main__":
    merge_playlists()
