import requests
import re
import sys

def fetch_link():
    # সরাসরি মেইন সাইটে রিকোয়েস্ট পাঠানো
    url = "http://redforce.live/"
    
    # ব্রাউজারের মতো ছদ্মবেশ ধরার জন্য উন্নত হেডার
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://redforce.live/',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    
    try:
        print("Connecting to Redforce...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status() # যদি সাইট ডাউন থাকে তবে এরর দিবে
        
        # সোর্স কোড থেকে টোকেন খোঁজার কয়েকটি পদ্ধতি (Pattern)
        patterns = [
            r'token=([a-zA-Z0-9.-]+)',
            r'token\s*[:=]\s*["\']?([a-zA-Z0-9.-]{20,})["\']?', # ২০ অক্ষরের বেশি টোকেন
            r'index\.m3u8\?token=([a-zA-Z0-9.-]+)'
        ]
        
        token = None
        for pattern in patterns:
            match = re.search(pattern, response.text)
            if match:
                token = match.group(1)
                break
        
        if token:
            print(f"Token found: {token[:10]}...")
            # নতুন প্লেলিস্ট কন্টেন্ট
            m3u_content = f"#EXTM3U\n#EXTINF:-1, Star Sports 1 HD\nhttp://redforce.live:8082/STAR.SPORTS1.HD/index.m3u8?token={token}&remote=no_check_ip\n"
            
            with open("my_channels.m3u", "w") as f:
                f.write(m3u_content)
            print("my_channels.m3u file updated!")
        else:
            print("Error: Could not find token in source code.")
            # সাইট যদি রেসপন্স দেয় কিন্তু টোকেন না থাকে, তবে সেটি ডিবাগ করতে সাহায্য করবে
            sys.exit(1) 

    except Exception as e:
        print(f"Network or Script Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_link()
