# Cập nhật dữ liệu XSMN từ 2 bộ dữ liệu mở (gộp, đối chiếu), giữ các kết quả mới hơn đã có.
# Usage: python3 tools/update_mn.py xsmn.csv   hoặc   python3 tools/update_mn.py xsmt.csv
# (ghi file csv và recent_mn.json / recent_mt.json cùng thư mục)
# xsmn.csv: date,station,two_digits  (36 ký tự = 2 số cuối 18 giải theo thứ tự ĐB,G1,G2,G3×2,G4×7,G5,G6×3,G7,G8)
import csv, io, json, os, sys, urllib.request
MT = {'binh-dinh':'Bình Định','da-nang':'Đà Nẵng','dak-lak':'Đắk Lắk','dak-nong':'Đắk Nông','gia-lai':'Gia Lai','khanh-hoa':'Khánh Hòa','kon-tum':'Kon Tum','ninh-thuan':'Ninh Thuận','phu-yen':'Phú Yên','quang-binh':'Quảng Bình','quang-nam':'Quảng Nam','quang-ngai':'Quảng Ngãi','quang-tri':'Quảng Trị','thua-thien-hue':'Thừa Thiên Huế'}
SL = {'an-giang':'An Giang','bac-lieu':'Bạc Liêu','ben-tre':'Bến Tre','binh-duong':'Bình Dương','binh-phuoc':'Bình Phước','binh-thuan':'Bình Thuận','ca-mau':'Cà Mau','can-tho':'Cần Thơ','da-lat':'Đà Lạt','dong-nai':'Đồng Nai','dong-thap':'Đồng Tháp','hau-giang':'Hậu Giang','kien-giang':'Kiên Giang','long-an':'Long An','soc-trang':'Sóc Trăng','tay-ninh':'Tây Ninh','tien-giang':'Tiền Giang','tra-vinh':'Trà Vinh','vinh-long':'Vĩnh Long','vung-tau':'Vũng Tàu','tp-hcm':'Hồ Chí Minh'}
IS_MT = 'xsmt' in os.path.basename(sys.argv[1])
if IS_MT: SL = MT
NAME2SLUG = {v: k for k, v in SL.items()}
NAME2SLUG.update({'Huế': 'thua-thien-hue', 'Đắc Lắc': 'dak-lak', 'Đắc Nông': 'dak-nong'} if IS_MT else {})
G = [("db",1,6),("g1",1,5),("g2",1,5),("g3",2,5),("g4",7,5),("g5",1,4),("g6",3,4),("g7",1,3),("g8",1,2)]
def get(url):
    return urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
def norm(vals):
    out, j = {}, 0
    for g, n, w in G:
        v = [x.strip() for x in vals[j:j+n]]; j += n
        if g == "db": v = [x.zfill(5) if len(x) <= 5 else x for x in v]
        else: v = [x.zfill(w) for x in v]
        out[g] = v
    return out
def valid(f):
    return all(len(f[g]) == n and all(x.isdigit() for x in f[g]) for g, n, w in G)
data, src = {}, {}
try:
    for r in csv.DictReader(io.StringIO(get("https://raw.githubusercontent.com/tuanseo5t-alt/xosomn-xosomt/main/data/" + ("xsmt/xsmt.csv" if IS_MT else "xsmn/xsmn.csv")))):
        s = NAME2SLUG.get(r["station"]);
        if not s: continue
        sp = lambda c: [x for x in r[c].split(",")]
        f = norm([r["special"], r["first"], r["second"]] + sp("third") + sp("fourth") + [r["fifth"]] + sp("sixth") + [r["seventh"], r["eighth"]])
        if valid(f): data[(r["date"], s)] = f; src[(r["date"], s)] = "A"
    print("nguồn A:", len(data))
except Exception as e: print("lỗi nguồn A", e)
nb = 0; conflicts = 0
for s in ([] if IS_MT else SL):
    try:
        for r in csv.DictReader(io.StringIO(get(f"https://raw.githubusercontent.com/Hpbt/xsmn-thong-ke/refs/heads/main/data/{s}.csv"))):
            f = norm([r["DB"], r["G1"], r["G2"]] + r["G3"].split() + r["G4"].split() + [r["G5"]] + r["G6"].split() + [r["G7"], r["G8"]])
            if not valid(f): continue
            k = (r["date"], s); nb += 1
            if k in data:
                if data[k] != f: conflicts += 1
            else: data[k] = f
    except Exception as e: print("lỗi nguồn B", s, e)
print("nguồn B:", nb, "| khác nhau:", conflicts)
path = sys.argv[1]; rp = os.path.join(os.path.dirname(os.path.abspath(path)), "recent_mt.json" if IS_MT else "recent_mn.json")
old = open(path).read().strip().split("\n")[1:] if os.path.exists(path) else []
old_rec = json.load(open(rp)) if os.path.exists(rp) else []
if not data:
    print("Không tải được nguồn nào, giữ nguyên."); sys.exit(0)
two = lambda f: "".join(x[-2:] for g, _, _ in G for x in f[g])
lines = {(d, s): f"{d},{s},{two(f)}" for (d, s), f in data.items()}
last = max(d for d, _ in data)
for l in old:
    d, s, _ = l.split(",")
    if (d, s) not in lines and d > last: lines[(d, s)] = l
if len(lines) < len(old):
    print("Dữ liệu mới ít hơn cũ, không ghi đè."); sys.exit(0)
keys = sorted(lines)
open(path, "w").write("date,station,two_digits\n" + "\n".join(lines[k] for k in keys) + "\n")
fp = path.replace(".csv", "_full.csv"); full = {}
if os.path.exists(fp):
    for l in open(fp).read().strip().split("\n")[1:]:
        if l: full[tuple(l.split(",")[:2])] = l
for (d, s), f in data.items(): full[(d, s)] = f"{d},{s}," + " ".join(x for g, _, _ in G for x in f[g])
open(fp, "w").write("date,station,nums\n" + "\n".join(full[k] for k in sorted(full)) + "\n")
print(os.path.basename(fp) + ":", len(full))
dates = sorted({d for d, _ in keys})[-60:]
rec = [{"date": d, "station": s, **data[(d, s)]} for d, s in keys if d in dates and (d, s) in data]
have = {(r["date"], r["station"]) for r in rec}
rec += [r for r in old_rec if r.get("date") in dates and (r["date"], r["station"]) not in have]
rec.sort(key=lambda r: (r["date"], r["station"]))
open(rp, "w").write(json.dumps(rec, separators=(",", ":"), ensure_ascii=False))
print("xsmn.csv:", len(keys), "kết quả đài, đến", keys[-1][0])
