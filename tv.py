import datetime
import pytz

# Bangladesh er timezone set kora
tz = pytz.timezone('Asia/Dhaka')
now = datetime.datetime.now(tz)
hour = now.hour

# Schedule logic
if 10 <= hour < 18:  # Shokal 10ta theke Shondha 6ta
    url = "https://ranapk.online/RANAPK33x/TVD/play.php?id=734308"
    title = "Cartoon Live 24/7"
elif 18 <= hour < 24: # Shondha 6ta theke Raat 12ta
    url = "http://172.16.29.34/live/ontest1/ontest1/461.m3u8"
    title = "Sports Live 24/7"
else: # Raat 12ta theke Shokal 10ta
    url = "https://ranapk.online/RANAPK33x/TVD/play.php?id=734323"
    title = "Entertainment Live 24/7"

# File update kora
with open('main.m3u', 'w') as f:
    f.write(f'#EXTM3U\n#EXTINF:-1, {title}\n{url}')

print(f"Update done! Current Bangladesh Hour: {hour}, Playing: {title}")
