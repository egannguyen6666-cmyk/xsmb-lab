# Dữ liệu đủ giải (để thống kê 3 càng, 4 càng, giải nhất, giải tám):
#   xsmb_full.csv : date,27 số (ĐB,G1,G2×2,G3×6,G4×4,G5×6,G6×3,G7×4) cách nhau bằng dấu cách
#   xsmn_full.csv, xsmt_full.csv : date,station,18 số (ĐB,G1,G2,G3×2,G4×7,G5,G6×3,G7,G8)  (do update_mn.py ghi)
# Script này tải XSMB đủ giải từ bộ dữ liệu mở và gộp thêm các kỳ mới trong recent*.json cho cả 3 miền.
# Usage: python3 tools/update_full.py
import csv, io, json, os, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W = [5] + [5] + [5] * 2 + [5] * 6 + [4] * 4 + [4] * 6 + [3] * 3 + [2] * 4
COLS = ["special", "prize1", "prize2_1", "prize2_2"] + [f"prize3_{i}" for i in range(1, 7)] + [f"prize4_{i}" for i in range(1, 5)] + [f"prize5_{i}" for i in range(1, 7)] + [f"prize6_{i}" for i in range(1, 4)] + [f"prize7_{i}" for i in range(1, 5)]
MBG = [("db", 1), ("g1", 1), ("g2", 2), ("g3", 6), ("g4", 4), ("g5", 6), ("g6", 3), ("g7", 4)]
MNG = ["db", "g1", "g2", "g3", "g4", "g5", "g6", "g7", "g8"]


def load(p, key):
    out = {}
    if os.path.exists(p):
        for line in open(p).read().strip().split("\n")[1:]:
            if line: out[key(line)] = line
    return out


p = os.path.join(ROOT, "xsmb_full.csv")
rows = load(p, lambda l: l.split(",")[0])
try:
    txt = urllib.request.urlopen("https://raw.githubusercontent.com/khiemdoan/vietnam-lottery-xsmb-analysis/refs/heads/main/data/xsmb.csv", timeout=90).read().decode()
    for r in csv.DictReader(io.StringIO(txt)):
        try:
            v = [str(int(float(r[c]))).zfill(w) for c, w in zip(COLS, W)]
        except Exception:
            continue
        if all(len(x) == w for x, w in zip(v, W)): rows.setdefault(r["date"][:10], f"{r['date'][:10]}," + " ".join(v))
except Exception as e:
    print("xsmb full: lỗi tải", e)
for r in json.load(open(os.path.join(ROOT, "recent.json"))):
    v = [x for g, n in MBG for x in r[g]]
    if len(v) == 27: rows[r["date"]] = f"{r['date']}," + " ".join(v)
two = {l.split(",")[0]: l.split(",")[1] for l in open(os.path.join(ROOT, "xsmb.csv")).read().strip().split("\n")[1:]}
bad = [d for d, l in rows.items() if d in two and "".join(x[-2:] for x in l.split(",")[1].split()) != two[d]]
for d in bad: rows.pop(d)
open(p, "w").write("date,nums\n" + "\n".join(rows[k] for k in sorted(rows)) + "\n")
print("xsmb_full.csv:", len(rows), "kỳ; bỏ", len(bad), "kỳ lệch với xsmb.csv")
for reg, rf in (("xsmn", "recent_mn.json"), ("xsmt", "recent_mt.json")):
    p = os.path.join(ROOT, reg + "_full.csv")
    rows = load(p, lambda l: tuple(l.split(",")[:2]))
    for r in json.load(open(os.path.join(ROOT, rf))):
        v = [x for g in MNG for x in r[g]]
        if len(v) == 18: rows[(r["date"], r["station"])] = f"{r['date']},{r['station']}," + " ".join(v)
    open(p, "w").write("date,station,nums\n" + "\n".join(rows[k] for k in sorted(rows)) + "\n")
    print(reg + "_full.csv:", len(rows))
