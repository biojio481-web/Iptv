import requests
import re

def fetch_link():
    url = "http://redforce.live/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        # রেডফোর্স সাইটে টোকেন অনেক সময় ভ্যারিয়েবলের ভেতর থাকে
        # এই রেগুলার এক্সপ্রেশনটি আরও শক্তিশালী
        token_match = re.search(r'token\s*[:=]\s*["\']?([a-zA-Z0-9.-]+)["\']?', response.text)
        
        if token_match:
            token = token_match.group(1)
            # আপনার মেইন প্লেলিস্ট লিঙ্ক তৈরি
            new_link = f"http://redforce.live:8082/STAR.SPORTS1.HD/index.m3u8?token={token}&remote=no_check_ip"
            
            with open("my_channels.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write(f"#EXTINF:-1, Star Sports 1 HD\n{new_link}\n")
            print(f"Success! Token found: {token}")
        else:
            # যদি টোকেন না পায়, তবে সোর্স কোড চেক করার জন্য প্রিন্ট করবে
            print("Error: Token not found on page.")
            raise Exception("Token fetch failed") # এটি দিলে Actions এ লাল চিহ্ন দেখাবে যদি ব্যর্থ হয়
            
    except Exception as e:
        print(f"Detailed Error: {e}")
        exit(1) # এটি গিটহাবকে জানাবে যে স্ক্রিপ্টটি ফেইল করেছে

if __name__ == "__main__":
    fetch_link()
