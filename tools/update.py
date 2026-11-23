# Cập nhật dữ liệu XSMB từ nhiều bộ dữ liệu mở trên GitHub, lấy bộ mới nhất, gộp với dữ liệu đang có.
# Usage: python3 tools/update.py xsmb.csv   (ghi xsmb.csv và recent.json cùng thư mục)
import csv, io, json, os, sys, urllib.request
MIRRORS = [
    "https://raw.githubusercontent.com/kina2711/vietnam-lottery-xsmb/refs/heads/main/data/xsmb.csv",
    "https://raw.githubusercontent.com/khiemdoan/vietnam-lottery-xsmb-analysis/refs/heads/main/data/xsmb.csv",
    "https://raw.githubusercontent.com/daiduong-eth/vietnam-lottery-xsmb/refs/heads/main/data/xsmb.csv",
    "https://raw.githubusercontent.com/xmanzero/xsmb-dashboard/refs/heads/main/data/xsmb.csv",
]
SKIP = {"2009-02-13"}  # dòng bị trùng trong nguồn
GROUPS = [("db",1,5),("g1",1,5),("g2",2,5),("g3",6,5),("g4",4,4),("g5",6,4),("g6",3,3),("g7",4,2)]
def load(url):
    raw = urllib.request.urlopen(url, timeout=60).read().decode("utf-8")
    rows = list(csv.reader(io.StringIO(raw)))[1:]
    out = []
    for r in rows:
        if len(r) != 28 or r[0] in SKIP or any(x.strip() == "" for x in r): continue
        nums, j, full = [], 1, {"date": r[0]}
        for g, n, w in GROUPS:
            full[g] = [str(int(x)).zfill(w) for x in r[j:j+n]]; j += n
        out.append(full)
    return out
best = []
for u in MIRRORS:
    try:
        d = load(u)
        print("nguồn", u.split("/")[3], "đến", d[-1]["date"])
        if d and (not best or d[-1]["date"] > best[-1]["date"]): best = d
    except Exception as e:
        print("lỗi nguồn", u.split("/")[3], e)
path = sys.argv[1]; rp = os.path.join(os.path.dirname(os.path.abspath(path)), "recent.json")
old = open(path).read().strip().split("\n")[1:] if os.path.exists(path) else []
old_rec = json.load(open(rp)) if os.path.exists(rp) else []
if not best:
    print("Không tải được nguồn nào, giữ nguyên dữ liệu cũ."); sys.exit(0)
two = lambda f: f["date"] + "," + "".join(x[-2:] for g, _, _ in GROUPS for x in f[g])
lines = ["date,two_digits"] + [two(f) for f in best]
extra = [l for l in old if l[:10] > best[-1]["date"]]
lines += extra
if len(lines) - 1 < len(old):
    print("Dữ liệu mới ít hơn dữ liệu cũ, không ghi đè."); sys.exit(0)
open(path, "w").write("\n".join(lines) + "\n")
rec = best[-60:] + [r for r in old_rec if r.get("date", "") > best[-1]["date"]]
open(rp, "w").write(json.dumps(rec[-60:], separators=(",", ":")))
print("xsmb.csv:", len(lines) - 1, "kỳ, đến", lines[-1][:10], "| giữ thêm:", [l[:10] for l in extra])
