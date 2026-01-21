import requests
import re

def fetch_link():
    url = "http://redforce.live/"
    # ব্রাউজারের মতো ছদ্মবেশ ধরার জন্য হেডার
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    }
    
    try:
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=20)
        
        # সোর্স কোড থেকে টোকেন খোঁজা
        token_match = re.search(r'token=([a-zA-Z0-9.-]+)', response.text)
        
        if token_match:
            token = token_match.group(1)
            new_link = f"http://redforce.live:8082/STAR.SPORTS1.HD/index.m3u8?token={token}&remote=no_check_ip"
            
            with open("my_channels.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write("#EXTINF:-1, Star Sports 1 HD\n")
                f.write(new_link)
            print("লিঙ্ক সফলভাবে আপডেট হয়েছে!")
        else:
            print("টোকেন পাওয়া যায়নি। সাইটের ডিজাইন হয়তো বদলে গেছে।")
            # ডিবাগ করার জন্য সোর্স কোড প্রিন্ট করা
            print(response.text[:500]) 
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_link()
