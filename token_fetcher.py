import requests
import re
import sys

def main():
    # মেইন ইউআরএল যেখান থেকে টোকেন আসে
    url = "http://redforce.live/"
    
    # ব্রাউজার হিসেবে ছদ্মবেশ নিতে উন্নত হেডার
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'http://redforce.live/',
        'Connection': 'keep-alive'
    }
    
    try:
        print("Connecting to Redforce site...")
        response = requests.get(url, headers=headers, timeout=30)
        
        # সোর্স কোডে টোকেন খোঁজার জন্য একাধিক প্যাটার্ন
        # প্যাটার্ন ১: সরাসরি token=
        # প্যাটার্ন ২: কোটেশনের ভেতরে টোকেন
        token = None
        
        patterns = [
            r'token=([a-zA-Z0-9\.-]+)',
            r'["\']token["\']\s*[:=]\s*["\']([a-zA-Z0-9\.-]+)["\']',
            r'index\.m3u8\?token=([a-zA-Z0-9\.-]+)'
        ]

        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                token = match.group(1)
                break
        
        if token:
            print(f"Token Found: {token[:10]}...")
            # আপনার পার্মানেন্ট লিঙ্কের ফরম্যাট
            link = f"http://redforce.live:8082/STAR.SPORTS1.HD/index.m3u8?token={token}&remote=no_check_ip"
            
            with open("live_tv.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1, Star Sports 1 HD\n{link}\n")
            print("Successfully updated live_tv.m3u")
        else:
            print("Error: সাইটে টোকেন খুঁজে পাওয়া যায়নি!")
            # ডিবাগ করার জন্য সাইটের কিছু অংশ প্রিন্ট করছি
            print("Site Content Snippet:", response.text[:500])
            sys.exit(1)
            
    except Exception as e:
        print(f"Connection Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
