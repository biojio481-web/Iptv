import datetime
import pytz

# বাংলাদেশ সময় জোন
tz = pytz.timezone('Asia/Dhaka')
hour = datetime.datetime.now(tz).hour

# শিডিউল অনুযায়ী লিঙ্ক সেট করা
if 10 <= hour < 18:  # সকাল ১০টা - সন্ধ্যা ৬টা (Cartoon)
    url = "https://ranapk.online/RANAPK33x/TVD/play.php?id=734308"
    title = "Cartoon Live 24/7"
elif 18 <= hour < 24: # সন্ধ্যা ৬টা - রাত ১২টা (Sports)
    url = "http://172.16.29.34/live/ontest1/ontest1/461.m3u8"
    title = "Sports Live 24/7"
else: # রাত ১২টা - সকাল ১০টা (Entertainment)
    url = "https://ranapk.online/RANAPK33x/TVD/play.php?id=734323"
    title = "Entertainment Live 24/7"

# আপনার চ্যানেলের প্লেলিস্ট ফাইল তৈরি
with open('main.m3u', 'w') as f:
    f.write(f'#EXTM3U\n#EXTINF:-1, {title}\n{url}')

print(f"Updated! Now: {title}")
