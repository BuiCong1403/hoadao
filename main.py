import requests
import re
from datetime import datetime

SOURCE_URL = "https://raw.githubusercontent.com/nhanb2004798/watchfbfree/refs/heads/main/watchfrhd.m3u"

def load_m3u(url):
    items = []
    try:
        res = requests.get(url, timeout=15)
        lines = res.text.splitlines()

        title = ""
        logo = ""

        for line in lines:
            if line.startswith("#EXTINF"):
                parts = line.split(",", 1)
                title = parts[1] if len(parts) > 1 else "Channel"

                m = re.search(r'tvg-logo="([^"]+)"', line)
                logo = m.group(1) if m else ""

            elif line.startswith("http"):
                stream = line.strip()

                # ✅ lọc OTTPlayer: chỉ m3u8
                if ".m3u8" not in stream:
                    continue

                # ❌ loại link lỗi phổ biến
                if any(x in stream for x in ["udp://", "rtp://"]):
                    continue

                items.append({
                    "title": title,
                    "logo": logo,
                    "url": stream
                })

    except Exception as e:
        print("Error:", e)

    return items


def write_m3u(data):
    content = "#EXTM3U\n"

    seen = set()

    for item in data:
        if item["url"] in seen:
            continue
        seen.add(item["url"])

        content += f'#EXTINF:-1 tvg-logo="{item["logo"]}",{item["title"]}\n'
        content += f'{item["url"]}\n\n'

    with open("hoadao.m3u", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Done! {len(data)} channels")


if __name__ == "__main__":
    data = load_m3u(SOURCE_URL)
    write_m3u(data)
