# Cập nhật kết quả Vietlott Mega 6/45 và Power 6/55 từ bộ dữ liệu mở vietvudanh/vietlott-data.
# Usage: python3 tools/update_vietlott.py
# Ghi vietlott_645.csv (ky,date,6 số) và vietlott_655.csv (ky,date,6 số,số đặc biệt). Giữ các kỳ đã có, kiểm tra trước khi ghi.
import json, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = "https://raw.githubusercontent.com/vietvudanh/vietlott-data/master/data/{}.jsonl"
GAMES = {"645": (45, 6, "vietlott_645.csv", "ky,date,n1,n2,n3,n4,n5,n6"), "655": (55, 7, "vietlott_655.csv", "ky,date,n1,n2,n3,n4,n5,n6,db")}


def load(path):
    rows = {}
    if os.path.exists(path):
        for line in open(path).read().strip().split("\n")[1:]:
            if line:
                rows[int(line.split(",")[0])] = line
    return rows


for game, (mx, n, fname, head) in GAMES.items():
    path = os.path.join(ROOT, fname)
    rows = load(path)
    try:
        with urllib.request.urlopen(urllib.request.Request(SRC.format("power" + game), headers={"User-Agent": "xs-lab"}), timeout=60) as r:
            text = r.read().decode("utf-8")
    except Exception as e:
        print(game, "lỗi tải", e); continue
    added = 0
    for line in text.splitlines():
        try:
            d = json.loads(line)
            ky, date, res = int(d["id"]), d["date"], [int(x) for x in d["result"]]
        except Exception:
            continue
        main = res[:6]
        if not (len(res) == n or (game == "655" and len(res) == 6)) or len(set(main)) != 6 or any(not 1 <= x <= mx for x in res) or len(date) != 10:
            continue
        if game == "655" and len(res) == 7 and res[6] in main:
            continue
        line2 = f"{ky},{date}," + ",".join(str(x) for x in sorted(main)) + ((f",{res[6]}" if len(res) == 7 else ",") if game == "655" else "")
        if ky not in rows:
            added += 1
        rows.setdefault(ky, line2)
    out = [rows[k] for k in sorted(rows)]
    open(path, "w").write(head + "\n" + "\n".join(out) + "\n")
    print(game, "tổng", len(out), "kỳ, thêm", added, "· kỳ cuối", out[-1] if out else "-")


def fetch(name):
    with urllib.request.urlopen(urllib.request.Request(SRC.format(name), headers={"User-Agent": "xs-lab"}), timeout=120) as r:
        return r.read().decode("utf-8")


# Max 3D và Max 3D Pro: 20 bộ ba số mỗi kỳ (ĐB 2, Nhất 4, Nhì 6, Ba 8)
for src, fname in (("3d", "vietlott_3d.csv"), ("3d_pro", "vietlott_3dpro.csv")):
    path = os.path.join(ROOT, fname); rows = load(path); added = 0
    try:
        text = fetch(src)
    except Exception as e:
        print(src, "lỗi tải", e); continue
    for line in text.splitlines():
        try:
            d = json.loads(line); res = d["result"]; ky = int(d["id"]); date = d["date"]
            groups = [res["Giải Đặc biệt"], res["Giải Nhất"], res["Giải Nhì"], res["Giải ba"]]
        except Exception:
            continue
        if [len(g) for g in groups] != [2, 4, 6, 8] or any(not (len(x) == 3 and x.isdigit()) for g in groups for x in g) or len(date) != 10:
            continue
        if ky not in rows: added += 1
        rows.setdefault(ky, f"{ky},{date}," + ",".join(" ".join(g) for g in groups))
    out = [rows[k] for k in sorted(rows)]
    open(path, "w").write("ky,date,db,g1,g2,g3\n" + "\n".join(out) + "\n")
    print(src, "tổng", len(out), "kỳ, thêm", added, "· kỳ cuối", out[-1][:40] if out else "-")

# Keno: 20 số từ 1-80 mỗi kỳ; chỉ giữ 6.000 kỳ gần nhất cho nhẹ trang
path = os.path.join(ROOT, "vietlott_keno.csv"); rows = load(path); added = 0
try:
    text = fetch("keno")
    for line in text.splitlines():
        try:
            d = json.loads(line); ky = int(str(d["id"]).lstrip("#")); res = [int(x) for x in d["result"]]; date = d["date"]
        except Exception:
            continue
        if len(res) != 20 or len(set(res)) != 20 or any(not 1 <= x <= 80 for x in res) or len(date) != 10:
            continue
        if ky not in rows: added += 1
        rows.setdefault(ky, f"{ky},{date}," + " ".join(str(x) for x in sorted(res)))
    out = [rows[k] for k in sorted(rows)][-6000:]
    open(path, "w").write("ky,date,nums\n" + "\n".join(out) + "\n")
    print("keno tổng", len(out), "kỳ, thêm", added, "· kỳ cuối", out[-1][:30] if out else "-")
except Exception as e:
    print("keno lỗi tải", e)
