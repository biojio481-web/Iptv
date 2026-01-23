import requests

def merge_playlists():
    # আপনার সব প্লেলিস্ট লিঙ্ক
    playlist_links = [
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/Specialbdix.m3u",
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/playlist_ontest1_plus%20(1).m3u",
        "https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u",
        "https://raw.githubusercontent.com/biojio481-web/Iptv/refs/heads/main/main.m3u",
        "https://iptv-scraper-zilla.pages.dev/CricHD.m3u",
        
        # ভবিষ্যতে আরও লিঙ্ক এখানে দিতে পারবেন
        "" 
    ]
    
    combined_content = "#EXTM3U\n"
    
    # ব্রাউজার হিসেবে পরিচয় দেওয়ার জন্য Headers (এটি দিলে লিঙ্ক ব্লক করবে না)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("চ্যানেলগুলো একত্রিত করা শুরু হচ্ছে...")

    for url in playlist_links:
        if not url.strip():
            continue
            
        try:
            # timeout বাড়িয়ে ৬০ সেকেন্ড করা হয়েছে এবং headers যোগ করা হয়েছে
            r = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
            
            if r.status_code == 200:
                # মেইন হেডার বাদ দিয়ে শুধু কন্টেন্ট নেওয়া
                content = r.text
                if "#EXTM3U" in content:
                    data = content.replace("#EXTM3U", "").strip()
                    if data:
                        combined_content += data + "\n"
                        print(f"সফল হয়েছে: {url}")
                else:
                    # যদি লিঙ্কে সরাসরি চ্যানেল থাকে (হেডার ছাড়া)
                    combined_content += content.strip() + "\n"
                    print(f"সফল হয়েছে (Raw): {url}")
            else:
                print(f"লিঙ্কটি কাজ করছে না (Status: {r.status_code}): {url}")
        except Exception as e:
            print(f"এরর: {url} | {e}")

    # ফাইনাল playlist.m3u ফাইল তৈরি
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(combined_content.strip())
    
    print("\nঅভিনন্দন! প্লেলিস্ট আপডেট সম্পন্ন হয়েছে।")

if __name__ == "__main__":
    merge_playlists()
