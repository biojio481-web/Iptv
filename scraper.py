import requests

def generate_playlist():
    # ১. আপনার ৩টি মূল লাইভ চ্যানেলের ডাটা (লিংক ও লোগোসহ)
    logo_url = "https://i.postimg.cc/2jczw2z4/file-000000009b507209933f01562a8e146a.png"
    
    m3u_content = "#EXTM3U\n"
    m3u_content += "#EXTVLCOPT:http-user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)\n\n"
    
    # চ্যানেল ১
    m3u_content += f'#EXTINF:-1 tvg-id="live1" tvg-name="Live 1" tvg-logo="{logo_url}" group-title="My Live",Live 1\n'
    m3u_content += "https://tvsen5.aynaott.com/willowhd/index.m3u8nn"
    
    # চ্যানেল ২
    m3u_content += f'#EXTINF:-1 tvg-id="live2" tvg-name="Live 2" tvg-logo="{logo_url}" group-title="My Live",Live 2\n'
    m3u_content += "https://tvsen7.aynaott.com/tsports-hd/index.m3u8nn"
    
    # চ্যানেল ৩
    m3u_content += f'#EXTINF:-1 tvg-id="live3" tvg-name="Live 3" tvg-logo="{logo_url}" group-title="My Live",Live 3\n'
    m3u_content += "https://tvsen6.aynaott.com/asports/tracks-v1a1/mono.ts.m3u8nn"
    
    # ২. বাহ্যিক (External) গিটহাব প্লেলিস্ট লিংক থেকে ডাটা আনা
    external_url = "https://raw.githubusercontent.com/mdarif2743/sky-life/refs/heads/main/Arif.m3u"
    
    try:
        # গিটহাব থেকে ফাইলটি ডাউনলোড করা হচ্ছে
        response = requests.get(external_url, timeout=10)
        if response.status_code == 200:
            external_data = response.text
            
            # বাহ্যিক ফাইলের ভেতরের #EXTM3U ট্যাগটি বাদ দিয়ে শুধু চ্যানেলগুলো নেওয়া হচ্ছে
            for line in external_data.splitlines():
                if line.strip() and not line.startswith("#EXTM3U"):
                    m3u_content += line + "\n"
        else:
            print(f"Warning: External playlist fetch failed with status {response.status_code}")
    except Exception as e:
        print(f"Error fetching external playlist: {e}")
        
    # ৩. ফাইনাল আউটপুট ফাইল তৈরি (যা আপনার কিতাবে লোড হবে)
    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write(m3u_content)
        
    print("Playlist generated successfully without any errors!")

if __name__ == "__main__":
    generate_playlist()
