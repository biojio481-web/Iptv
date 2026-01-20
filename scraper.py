import requests
import re

def get_live_link():
    # সোর্স ইউআরএল (যেখান থেকে লিঙ্কটি কালেক্ট করা হবে)
    # আপনি আপনার দেওয়া সাইটের মূল অংশটি এখানে ব্যবহার করতে পারেন
    source_url = "http://redforce.live:8082/SSC.SPORTS.5.HD/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1'
    }

    try:
        # সাইট থেকে ডেটা আনা
        response = requests.get(source_url, headers=headers, timeout=15)
        
        # রেগুলার এক্সপ্রেশন দিয়ে m3u8 এবং টোকেন খুঁজে বের করা
        # এটি স্বয়ংক্রিয়ভাবে নতুন টোকেনসহ লিঙ্কটি খুঁজবে
        pattern = r'(http.*?index\.m3u8\?token=[\w-]+)'
        matches = re.findall(pattern, response.text)

        if matches:
            final_link = matches[0]
            # playlist.m3u ফাইল তৈরি বা আপডেট করা
            with open("playlist.m3u", "w") as f:
                f.write("#EXTM3U\n")
                f.write("#EXTINF:-1, SSC Sports 5 HD (Auto-Updated)\n")
                f.write(f"{final_link}\n")
            print("Successfully updated the link!")
        else:
            print("Could not find a new token. Site might be protected.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    get_live_link()
