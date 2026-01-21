import requests
import re
import sys

def fetch_token():
    url = "http://redforce.live/"
    # ব্রাউজারের মতো ছদ্মবেশ
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        print("সাইটে ঢোকার চেষ্টা করছি...")
        response = requests.get(url, headers=headers, timeout=30)
        
        # সাইটটি ঠিকঠাক লোড হয়েছে কি না চেক করা
        if response.status_code != 200:
            print(f"ভুল: সাইট লোড হয়নি। স্ট্যাটাস কোড: {response.status_code}")
            return None

        # টোকেন খোঁজার পদ্ধতি
        # আপনার দেওয়া লিঙ্ক অনুযায়ী টোকেনটি বেশ লম্বা হয়, তাই এই প্যাটার্নটি ব্যবহার করছি
        token_match = re.search(r'token=([a-zA-Z0-9.-]{30,})', response.text)
        
        if token_match:
            return token_match.group(1)
        
        # বিকল্প পদ্ধতি যদি সরাসরি না পাওয়া যায়
        token_match_alt = re.search(r'["\']?token["\']?\s*[:=]\s*["\']?([a-zA-Z0-9.-]{30,})["\']?', response.text)
        if token_match_alt:
            return token_match_alt.group(1)

        print("Error: সাইটের কোডের ভেতরে টোকেন খুঁজে পাওয়া যায়নি।")
        return None

    except Exception as e:
        print(f"Error: কানেকশনে সমস্যা হয়েছে - {e}")
        return None

def main():
    token = fetch_token()
    
    if token:
        print(f"টোকেন পাওয়া গেছে: {token[:15]}...")
        # নতুন ফাইল তৈরি
        m3u_content = f"#EXTM3U\n#EXTINF:-1, Star Sports 1 HD\nhttp://redforce.live:8082/STAR.SPORTS1.HD/index.m3u8?token={token}&remote=no_check_ip\n"
        
        with open("my_channels.m3u", "w") as f:
            f.write(m3u_content)
        print("my_channels.m3u ফাইলটি আপডেট করা হয়েছে।")
    else:
        # টোকেন না পেলে স্ক্রিপ্ট ফেইল করাবে যাতে আমরা কারণ বুঝতে পারি
        sys.exit(1)

if __name__ == "__main__":
    main()
