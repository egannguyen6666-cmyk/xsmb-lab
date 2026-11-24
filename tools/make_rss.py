# Tạo rss.xml: kết quả XSMB, XSMN, XSMT và Vietlott các kỳ gần nhất.
# Usage: python3 tools/make_rss.py   (chạy trong thư mục gốc của kho)
import csv, datetime, json, os
from email.utils import format_datetime
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = ("https://" + open(os.path.join(ROOT, "CNAME")).read().strip() + "/") if os.path.exists(os.path.join(ROOT, "CNAME")) else "https://egannguyen6666-cmyk.github.io/xsmb-lab/"
TZ = datetime.timezone(datetime.timedelta(hours=7))
ST = {'an-giang':'An Giang','bac-lieu':'Bạc Liêu','ben-tre':'Bến Tre','binh-duong':'Bình Dương','binh-phuoc':'Bình Phước','binh-thuan':'Bình Thuận','ca-mau':'Cà Mau','can-tho':'Cần Thơ','da-lat':'Đà Lạt','dong-nai':'Đồng Nai','dong-thap':'Đồng Tháp','hau-giang':'Hậu Giang','kien-giang':'Kiên Giang','long-an':'Long An','soc-trang':'Sóc Trăng','tay-ninh':'Tây Ninh','tien-giang':'Tiền Giang','tra-vinh':'Trà Vinh','vinh-long':'Vĩnh Long','vung-tau':'Vũng Tàu','tp-hcm':'TP.HCM','binh-dinh':'Bình Định','da-nang':'Đà Nẵng','dak-lak':'Đắk Lắk','dak-nong':'Đắk Nông','gia-lai':'Gia Lai','khanh-hoa':'Khánh Hòa','kon-tum':'Kon Tum','ninh-thuan':'Ninh Thuận','phu-yen':'Phú Yên','quang-binh':'Quảng Bình','quang-nam':'Quảng Nam','quang-ngai':'Quảng Ngãi','quang-tri':'Quảng Trị','thua-thien-hue':'Thừa Thiên Huế'}
NOTE = " Thông tin chỉ mang tính chất tham khảo; vui lòng kiểm tra lại kết quả chính thức được công bố bởi các công ty xổ số."


def vn(d): return f"{d[8:10]}/{d[5:7]}/{d[:4]}"
def when(d, hm): return datetime.datetime.fromisoformat(d + "T" + hm).replace(tzinfo=TZ)
def load(f, default):
    p = os.path.join(ROOT, f)
    return json.load(open(p)) if os.path.exists(p) else default


items = []
for r in load("recent.json", [])[-7:]:
    lo = sorted(x[-2:] for g in ["db", "g1", "g2", "g3", "g4", "g5", "g6", "g7"] for x in r[g])
    items.append((when(r["date"], "18:40"), f"Kết quả XSMB {vn(r['date'])}", f"Giải Đặc biệt {r['db'][0]} · Giải Nhất {r['g1'][0]} · Lô tô: {' '.join(lo)}.", BASE + "xsmb/", "xsmb-" + r["date"]))
for fn, lab, slug, hm in (("recent_mn.json", "XSMN", "xsmn/", "16:40"), ("recent_mt.json", "XSMT", "xsmt/", "17:40")):
    rec = load(fn, []); by = {}
    for r in rec: by.setdefault(r["date"], []).append(r)
    for d in sorted(by)[-7:]:
        desc = " · ".join(f"{ST.get(r['station'], r['station'])}: ĐB {r['db'][0]}, G8 {r['g8'][0]}" for r in sorted(by[d], key=lambda x: x["station"]))
        items.append((when(d, hm), f"Kết quả {lab} {vn(d)}", desc + ".", BASE + slug, lab.lower() + "-" + d))
for fn, nm, slug, fmt in (("vietlott_645.csv", "Mega 6/45", "mega-645/", "6"), ("vietlott_655.csv", "Power 6/55", "power-655/", "7"), ("vietlott_3d.csv", "Max 3D", "max-3d/", "3"), ("vietlott_3dpro.csv", "Max 3D Pro", "max-3d-pro/", "3")):
    p = os.path.join(ROOT, fn)
    if not os.path.exists(p): continue
    rows = list(csv.reader(open(p)))[1:][-3:]
    for r in rows:
        if fmt == "6": desc = "Bộ số: " + " ".join(x.zfill(2) for x in r[2:8])
        elif fmt == "7": desc = "Bộ số: " + " ".join(x.zfill(2) for x in r[2:8]) + (f" · số đặc biệt {r[8].zfill(2)}" if len(r) > 8 and r[8] else "")
        else: desc = f"Giải Đặc biệt: {r[2]} · Giải Nhất: {r[3]}"
        items.append((when(r[1], "18:30"), f"Kết quả Vietlott {nm} kỳ #{r[0].zfill(5)} ngày {vn(r[1])}", desc + ".", BASE + slug, slug.strip("/") + "-" + r[0]))
items.sort(key=lambda x: x[0], reverse=True)
items = items[:50]
now = datetime.datetime.now(TZ)
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">', '<channel>',
       '<title>XS Lab – Kết quả xổ số XSMB, XSMN, XSMT và Vietlott</title>', f'<link>{BASE}</link>',
       f'<atom:link href="{BASE}rss.xml" rel="self" type="application/rss+xml"/>',
       '<description>Kết quả xổ số các kỳ gần nhất, cập nhật từ nguồn công khai và chỉ mang tính chất tham khảo.</description>',
       '<language>vi</language>', f'<lastBuildDate>{format_datetime(now)}</lastBuildDate>']
for dt, title, desc, link, guid in items:
    out.append(f'<item><title>{escape(title)}</title><link>{link}</link><guid isPermaLink="false">{guid}</guid><pubDate>{format_datetime(dt)}</pubDate><description>{escape(desc + NOTE)}</description></item>')
out += ['</channel>', '</rss>']
open(os.path.join(ROOT, "rss.xml"), "w").write("\n".join(out) + "\n")
print("rss.xml:", len(items), "mục")
