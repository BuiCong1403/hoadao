import requests
import re

SOURCE_URL = "https://raw.githubusercontent.com/nhanb2004798/watchfbfree/refs/heads/main/watchfrhd.m3u"


def load_m3u(url):
    items = []

    try:
        res = requests.get(url, timeout=15)
        text = res.text

        # nối các dòng bị xuống dòng giữa URL
        text = re.sub(r'\n(?!#)', '', text)

        lines = text.splitlines()

        title = "Unknown"
        logo = ""

        for line in lines:
            line = line.strip()

            if line.startswith("#EXTINF"):
                parts = line.split(",", 1)
                title = parts[1] if len(parts) > 1 else "Channel"

                m = re.search(r'tvg-logo="([^"]+)"', line)
                logo = m.group(1) if m else ""

            elif line.startswith("http"):
                stream = line

                # ❌ chỉ loại mấy cái chắc chắn không dùng
                if any(x in stream for x in ["udp://", "rtp://"]):
                    continue

                # ✅ KHÔNG lọc đuôi nữa → giữ hết
                items.append({
                    "title": title,
                    "logo": logo,
                    "url": stream
                })

    except Exception as e:
        print("Error:", e)

    return items


def remove_duplicate(data):
    seen = set()
    out = []

    for item in data:
        if item["url"] in seen:
            continue
        seen.add(item["url"])
        out.append(item)

    return out

def write_m3u(data):
    content = "#EXTM3U\n"

    for item in data:
        content += f'#EXTINF:-1 tvg-logo="{item["logo"]}",{item["title"]}\n'
        content += f'{item["url"]}\n\n'

    with open("hoadao.m3u", "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Done! {len(data)} channels")


if __name__ == "__main__":
    data = load_m3u(SOURCE_URL)

    print("Raw:", len(data))

    data = remove_duplicate(data)
    data = sort_streams(data)

    print("Final:", len(data))

    write_m3u(data)
