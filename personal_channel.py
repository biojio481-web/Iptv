import datetime
import pytz

def create_channel():
    bd_tz = pytz.timezone('Asia/Dhaka')
    now = datetime.datetime.now(bd_tz)
    current_total_minutes = (now.hour * 60) + now.minute

    # --- আপনার তথ্যগুলো এখানে দিন ---
    channel_name = "Star Tv HD"
    logo = "https://i.ibb.co/BV07dhKk/Gemini-Generated-Image-3j1njw3j1njw3j1n.png"
    
    movie_link = "http://172.16.29.2:8090/hls/tsportshd.m3u8"
    sports_link = "http://103.182.170.32:8888/play/a04g"
    series_link = "http://172.16.29.2:8090/hls/tsportshd.m3u8"
    # ---------------------------------------

    if 600 <= current_total_minutes < 900:
        stream_url = movie_link
        mode = "Movie Special"
    elif 900 <= current_total_minutes < 1440:
        stream_url = sports_link
        mode = "Sports Live"
    else:
        stream_url = series_link
        mode = "Series Night"

    content = f'#EXTM3U\n#EXTINF:-1 tvg-id="StarTvHD" tvg-name="Star Tv HD" tvg-logo="{logo}" group-title="{mode}", {channel_name} ({mode})\n{stream_url}'
    
    with open("my_stream.m3u8", "w", encoding="utf-8") as f:
        f.write(content)

if __name__ == "__main__":
    create_channel()
