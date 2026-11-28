#!/usr/bin/env python3
"""Lấy ID các buổi phát trực tiếp hôm nay của kênh YouTube XS Lab (qua RSS công khai của kênh)
và ghi ra yt-live.json để trang Trực tiếp nhúng đúng buổi live của từng miền."""
import json, os, re, sys, urllib.request, datetime as dt
import xml.etree.ElementTree as ET
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CFG = os.path.join(ROOT, "tools", "yt_channel.txt")
OUT = os.path.join(ROOT, "yt-live.json")
cid = (open(CFG).read().strip() if os.path.exists(CFG) else "") or os.environ.get("YT_CHANNEL_ID", "")
if not re.fullmatch(r"UC[\w-]{22}", cid):
    print("Chưa có ID kênh YouTube (tools/yt_channel.txt), bỏ qua"); sys.exit(0)
today = (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=7)).date()
dmy = today.strftime("%d/%m/%Y")
try:
    req = urllib.request.Request(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}", headers={"User-Agent": "Mozilla/5.0 xslab-live"})
    xml = urllib.request.urlopen(req, timeout=20).read()
except Exception as e:
    print("Không đọc được RSS kênh:", e); sys.exit(0)
ns = {"a": "http://www.w3.org/2005/Atom", "yt": "http://www.youtube.com/xml/schemas/2015"}
found = {}
for en in ET.fromstring(xml).findall("a:entry", ns):
    vid = (en.findtext("yt:videoId", "", ns) or "").strip(); t = (en.findtext("a:title", "", ns) or "")
    if not vid or dmy not in t: continue
    if re.search(r"KQXS hôm nay|3 miền|XSMN, XSMT, XSMB", t, re.I): k = "tong"
    elif re.search(r"\bXSMB\b|Miền Bắc", t): k = "mb"
    elif re.search(r"\bXSMT\b|Miền Trung", t): k = "mt"
    elif re.search(r"\bXSMN\b|Miền Nam", t): k = "mn"
    else: continue
    found.setdefault(k, {"id": vid, "title": t})
old = {}
try: old = json.load(open(OUT))
except Exception: pass
new = {"date": today.isoformat(), **found}
if old.get("date") == new["date"]:
    for k in ("tong", "mn", "mt", "mb"):           # giữ ID đã thấy trước đó trong ngày
        if k not in new and k in old: new[k] = old[k]
if new != old:
    json.dump(new, open(OUT, "w"), ensure_ascii=False, separators=(",", ":"))
    print("Đã cập nhật yt-live.json:", ", ".join(f"{k}={v['id']}" for k, v in new.items() if k != "date") or "chưa có buổi nào")
else:
    print("Không có gì mới")
