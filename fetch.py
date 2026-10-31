"""把 ziyuanzhan 的在线站点列表转成 LibreTV 订阅格式（sources[].url）。"""

import json
import urllib.request

SRC = "https://mylazily.github.io/ziyuanzhan/data/online.json"
OUT = "d7f.json"

data = json.load(urllib.request.urlopen(SRC, timeout=30))

seen, sources = set(), []
for site in data["data"]:
    url = (site.get("api") or "").strip().rstrip("/")
    if not url.startswith("http") or url in seen:
        continue
    seen.add(url)
    sources.append({"name": site["name"], "url": url})

if len(sources) < 10:
    raise SystemExit(f"只拿到 {len(sources)} 条源，疑似上游异常，不覆盖")

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(
        {"name": "资源站监测（自动同步）", "sources": sources, "liveSources": []},
        f,
        ensure_ascii=False,
        indent=2,
    )
print(f"{len(sources)} sources")
