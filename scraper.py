import requests
import re

def get_link():
    try:
        url = "http://redforce.live:8082" 
        r = requests.get(url, timeout=20)
        # লিঙ্ক খুঁজে বের করা
        matches = re.findall(r'http[s]?://[^\s"\'<>]+m3u8[^\s"\'<>]*', r.text)
        if matches:
            with open("mysports.m3u", "w") as f:
                f.write(f"#EXTM3U\n#EXTINF:-1,SSC Sports 5\n{matches[0]}")
            print("Update Success!")
    except:
        print("Failed")

if __name__ == "__main__":
    get_link()
