import datetime
import pytz

# বাংলাদেশ সময় অনুযায়ী জোন সেট করা
tz = pytz.timezone('Asia/Dhaka')
now = datetime.datetime.now(tz)
hour = now.hour

# আপনার শিডিউল অনুযায়ী লিঙ্ক
if 10 <= hour < 18:  # সকাল ১০টা - সন্ধ্যা ৬টা (Cartoon)
    url = "https://ranapk.online/RANAPK33x/TVD/play.php?id=734308"
    title = "Cartoon 24/7"
elif 18 <= hour < 24: # সন্ধ্যা ৬টা - রাত ১২টা (Sports)
    url = "http://172.16.29.34/live/ontest1/ontest1/461.m3u8"
    title = "Sports 24/7"
else: # রাত ১২টা - সকাল ১০টা (Entertainment)
    url = "https://ranapk.online/RANAPK33x/TVD/play.php?id=734323"
    title = "Entertainment 24/7"

# প্লেলিস্ট ফাইল তৈরি করা
with open('main.m3u', 'w') as f:
    f.write(f'#EXTM3U\n#EXTINF:-1, {title}\n{url}')

print(f"Update done! Current: {title}")
