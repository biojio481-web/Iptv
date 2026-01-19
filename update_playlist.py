import requests

# ১. আপনার নিজের চ্যানেলের লিস্ট (ঐচ্ছিক)
# যদি নিজের কিছু না থাকে তবে এটি খালি রাখতে পারেন
MY_CHANNELS = """#EXTM3U
#EXTINF:-1, My Custom Channel
https://example.com/stream.m3u8
"""

# ২. অন্য যাদের প্লেলিস্ট অ্যাড করতে চান তাদের RAW লিংক এখানে দিন
# আপনি চাইলে একাধিক লিংক লিস্টে রাখতে পারেন
OTHER_PLAYLIST_URLS = [
    "https://raw.githubusercontent.com/username/repo/master/playlist.m3u8",
    "https://example.com/another_playlist.m3u8"
]

def update_playlist():
    final_content = MY_CHANNELS.strip()

    for url in OTHER_PLAYLIST_URLS:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                # #EXTM3U হেডার বাদ দিয়ে শুধু চ্যানেলগুলো নেওয়া হচ্ছে
                content = response.text.replace("#EXTM3U", "").strip()
                if content:
                    final_content += "\n" + content
                print(f"Successfully fetched: {url}")
            else:
                print(f"Failed to fetch {url}: Status {response.status_code}")
        except Exception as e:
            print(f"Error fetching {url}: {e}")

    # ৩. সব মিলিয়ে নতুন ফাইলটি সেভ করা
    with open("playlist.m3u8", "w", encoding="utf-8") as f:
        f.write(final_content)
        print("Playlist updated successfully!")

if __name__ == "__main__":
    update_playlist()
