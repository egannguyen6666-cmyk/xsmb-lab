# Lấy kết quả Keno mới nhất từ bảng kết quả công khai (minhchinh.com) và ghi vào vietlott_keno.csv.
# Usage: python3 tools/fetch_keno.py
# Chỉ lấy các trang cần thiết (15 kỳ/trang), nghỉ 3 giây giữa các yêu cầu; kiểm tra đủ 20 số khác nhau trong 1–80.
import datetime, os, re, time, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "vietlott_keno.csv")
URL = "https://www.minhchinh.com/xo-so-dien-toan-keno.html"
UA = {"User-Agent": "Mozilla/5.0 (xs-lab keno updater)"}
ROW = re.compile(r'kn-ky">#(\d+)</div>.*?kn-date">(\d{2})/(\d{2})/(\d{4})</div>.*?kn-balls">(.*?)</div>', re.S)


def page(date, n):
    data = urllib.parse.urlencode({"date": date.strftime("%d-%m-%Y"), "page": n, "ky": "", "number": ""}).encode()
    with urllib.request.urlopen(urllib.request.Request(URL, data=data, headers=UA), timeout=30) as r:
        t = r.read().decode("utf-8", "replace")
    out = []
    for ky, d, m, y, balls in ROW.findall(t):
        nums = [int(x) for x in re.findall(r'kn-ball">(\d+)<', balls)]
        if len(nums) == 20 and len(set(nums)) == 20 and all(1 <= x <= 80 for x in nums):
            out.append((int(ky), f"{y}-{m}-{d}", sorted(nums)))
    return out


rows = {}
if os.path.exists(PATH):
    for line in open(PATH).read().strip().split("\n")[1:]:
        if line: rows[int(line.split(",")[0])] = line
known = max(rows) if rows else 0
vn = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=7)
added = 0
for day in (vn.date() - datetime.timedelta(days=1), vn.date()):
    for n in range(1, 10):
        try:
            got = page(day, n)
        except Exception as e:
            print(day, "trang", n, "lỗi", e); break
        time.sleep(3)
        if not got: break
        for ky, date, nums in got:
            if ky not in rows:
                rows[ky] = f"{ky},{date}," + " ".join(map(str, nums)); added += 1
        if min(k for k, _, _ in got) <= known: break
out = [rows[k] for k in sorted(rows)][-6000:]
open(PATH, "w").write("ky,date,nums\n" + "\n".join(out) + "\n")
print("keno: thêm", added, "kỳ · kỳ cuối", out[-1][:24] if out else "-")
