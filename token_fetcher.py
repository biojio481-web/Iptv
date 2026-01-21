import requests
import re
import sys

def main():
    url = "http://redforce.live/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'http://redforce.live/'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        # রেডফোর্স সাইট থেকে টোকেন বের করার জন্য সঠিক প্যাটার্ন
        token_match = re.search(r'token=([a-zA-Z0-9.-]+)', response.text)
        
        if token_match:
            token = token_match.group(1)
            # লিঙ্কটি তৈরি করা হচ্ছে
            link = f"http://redforce.live:8082/STAR.SPORTS1.HD/index.m3u8?token={token}&remote=no_check_ip"
            
            # আপনার মেইন প্লেলিস্ট ফাইল
            with open("live_tv.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1, Star Sports 1 HD\n{link}\n")
            print("Successfully updated live_tv.m3u")
        else:
            print("Token not found on the page!")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
