# Nhập tay kết quả một đài XSMN (có kiểm tra).
# Usage: python3 tools/add_day_mn.py xsmn.csv recent_mn.json 2026-11-23 tp-hcm "321463 33527 13225 42438 60051 73797 ... 061 35"
#   18 số theo thứ tự ĐB, G1, G2, G3(2), G4(7), G5, G6(3), G7, G8.  Mã đài: tp-hcm, dong-thap, ca-mau, ...
import json, re, sys, datetime
SL = ['an-giang','bac-lieu','ben-tre','binh-duong','binh-phuoc','binh-thuan','ca-mau','can-tho','da-lat','dong-nai','dong-thap','hau-giang','kien-giang','long-an','soc-trang','tay-ninh','tien-giang','tra-vinh','vinh-long','vung-tau','tp-hcm']
G = [("db",1,(5,6)),("g1",1,(5,)),("g2",1,(5,)),("g3",2,(5,)),("g4",7,(5,)),("g5",1,(4,)),("g6",3,(4,)),("g7",1,(3,)),("g8",1,(2,))]
csv_path, rec_path, date, st, raw = sys.argv[1:6]
datetime.date.fromisoformat(date)
assert st in SL, f"mã đài không hợp lệ: {st}"
toks = re.findall(r"\d+", raw); assert len(toks) == 18, f"cần 18 số, có {len(toks)}"
d, j = {"date": date, "station": st}, 0
for g, n, ws in G:
    v = toks[j:j+n]; j += n
    for x in v: assert len(x) in ws, f"{g}: '{x}' sai số chữ số"
    d[g] = v
lines = open(csv_path).read().strip().split("\n")
if any(l.startswith(f"{date},{st},") for l in lines[1:]):
    print("SKIP: đã có", date, st); sys.exit(0)
lines.append(f"{date},{st}," + "".join(x[-2:] for g, _, _ in G for x in d[g]))
head, body = lines[0], sorted(lines[1:])
open(csv_path, "w").write(head + "\n" + "\n".join(body) + "\n")
rec = [r for r in json.load(open(rec_path)) if not (r["date"] == date and r["station"] == st)] + [d]
dates = sorted({r["date"] for r in rec})[-60:]
rec = sorted([r for r in rec if r["date"] in dates], key=lambda r: (r["date"], r["station"]))
open(rec_path, "w").write(json.dumps(rec, separators=(",", ":"), ensure_ascii=False))
print("added", date, st)
