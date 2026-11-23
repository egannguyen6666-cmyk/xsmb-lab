# Usage: python3 tools/add_day.py xsmb.csv recent.json 2026-11-23 "94495 61045 37123 28361 65151 ... 50 51 52 57"
#   (27 số theo thứ tự ĐB, G1, G2×2, G3×6, G4×4, G5×6, G6×3, G7×4, cách nhau bằng dấu cách/phẩy/xuống dòng)
#   hoặc kiểu cũ: python3 tools/add_day.py xsmb.csv recent.json '{"date":...,"db":[...],...}'
# Validates a full draw (27 prizes, correct digit counts) and appends it to both files. Refuses duplicates or out-of-order dates.
import json, sys, datetime
import re
csv_path, rec_path = sys.argv[1], sys.argv[2]
spec = [("db",1,5),("g1",1,5),("g2",2,5),("g3",6,5),("g4",4,4),("g5",6,4),("g6",3,3),("g7",4,2)]
if len(sys.argv) >= 5:
    toks = re.findall(r"\d+", sys.argv[4])
    assert len(toks) == 27, f"cần đúng 27 số, đang có {len(toks)}"
    d, j = {"date": sys.argv[3].strip()}, 0
    for g, n, w in spec: d[g] = toks[j:j+n]; j += n
else:
    d = json.loads(sys.argv[3])
_d = datetime.date.fromisoformat(d["date"])
TET = {2026:"2026-02-17",2027:"2027-02-06",2028:"2028-01-26",2029:"2029-02-13",2030:"2030-02-03",2031:"2031-01-23",2032:"2032-02-11",2033:"2033-01-31",2034:"2034-02-19",2035:"2035-02-08",2036:"2036-01-28",2037:"2037-02-15",2038:"2038-02-04",2039:"2039-01-24",2040:"2040-02-12"}
for _y in (_d.year, _d.year + 1):
    if _y in TET and -1 <= (_d - datetime.date.fromisoformat(TET[_y])).days <= 2:
        print("SKIP: ngày nghỉ Tết, XSMB không quay"); sys.exit(0)
nums = []
for g, n, w in spec:
    v = [str(x).strip() for x in d[g]]
    assert len(v) == n, f"{g}: cần {n} số, có {len(v)}"
    for x in v: assert x.isdigit() and len(x) == w, f"{g}: '{x}' phải có {w} chữ số"
    d[g] = v; nums += v
assert len(nums) == 27
lines = open(csv_path).read().strip().split("\n")
last = lines[-1].split(",")[0]
if d["date"] <= last:
    print("SKIP: đã có ngày", d["date"], "hoặc ngày cũ hơn", last); sys.exit(0)
lines.append(d["date"] + "," + "".join(x[-2:] for x in nums))
open(csv_path, "w").write("\n".join(lines) + "\n")
rec = [r for r in json.load(open(rec_path)) if r.get("date") != d["date"]]; rec.append({k: d[k] for k in ["date"] + [g for g, _, _ in spec]}); rec = rec[-60:]
open(rec_path, "w").write(json.dumps(rec, separators=(",", ":")))
print("added", d["date"], lines[-1])
