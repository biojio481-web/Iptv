import requests
import re

def fetch_link():
    # রেডফোর্স মেইন পেজ যেখান থেকে টোকেন স্ক্র্যাপ করা হবে
    url = "http://redforce.live/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # সোর্স কোড থেকে টোকেন খুঁজে বের করা
        token_match = re.search(r'token=([a-zA-Z0-9.-]+)', response.text)
        
        if token_match:
            token = token_match.group(1)
            # আপনার পছন্দের চ্যানেল লিঙ্ক (স্টার স্পোর্টস উদাহরণ হিসেবে)
            new_link = f"http://redforce.live:8082/STAR.SPORTS1.HD/index.m3u8?token={token}&remote=no_check_ip"
            
            # প্লেলিস্ট ফাইলে সেভ করা
            with open("live_tv.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write("#EXTINF:-1, Star Sports 1 HD\n")
                f.write(new_link)
            print("নতুন টোকেন দিয়ে লিঙ্ক আপডেট হয়েছে!")
        else:
            print("টোকেন পাওয়া যায়নি। সাইটটি হয়তো প্রোটেক্টেড।")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fetch_link()
