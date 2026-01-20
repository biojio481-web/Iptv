import requests
import re

def get_link():
    try:
        url = "http://redforce.live:8082"
        r = requests.get(url, timeout=20)
        # সব m3u8 লিঙ্ক খুঁজে বের করা
        matches = re.findall(r'http[s]?://[^\s"\'<>]+m3u8[^\s"\'<>]*', r.text)
        if matches:
            with open("mysports.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write("#EXTINF:-1,SSC Sports 5\n")
                f.write(matches[0])
            print("Update Done!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_link()
