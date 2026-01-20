import os

def create_playlist():
    # এখানে আপনার সংগৃহীত লিঙ্কটি দিন
    channel_name = "SSC Sports 5 HD"
    stream_url = "http://redforce.live:8082/SSC.SPORTS.5.HD/index.m3u8?token=YOUR_TOKEN_HERE" 
    
    # ফাইল তৈরি করা
    try:
        with open("mysports.m3u", "w") as f:
            f.write("#EXTM3U\n")
            f.write(f"#EXTINF:-1, {channel_name}\n")
            f.write(stream_url)
        print("Success: File updated!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_playlist()
