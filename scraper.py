import requests
import re

def get_link():
    # সোর্স সাইট (আপনার দেওয়া লিঙ্কের মূল ডোমেইন)
    url = "http://redforce.live:8082" 
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        # লিঙ্কের ভেতর m3u8 এবং টোকেন খোঁজা
        link = re.findall(r'http[s]?://[^\s"\'<>]+m3u8\?token=[^\s"\'<>]+', response.text)
        
        if link:
            with open("mysports.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write("#EXTINF:-1, SSC Sports 5 HD\n")
                f.write(link[0])
            print("লিঙ্ক আপডেট হয়েছে!")
        else:
            print("লিঙ্ক খুঁজে পাওয়া যায়নি।")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_link()
