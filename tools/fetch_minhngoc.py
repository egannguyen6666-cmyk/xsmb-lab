# Lấy kết quả vừa quay từ widget công khai của Minh Ngọc và ghi vào dữ liệu (có kiểm tra).
# Usage: python3 tools/fetch_minhngoc.py mb|mn|mt [YYYY-MM-DD]
#   mb: mien-bac -> xsmb.csv + recent.json (qua tools/add_day.py)
#   mn/mt: các đài quay hôm nay (suy ra từ lịch 4 tuần gần nhất trong csv) -> add_day_mn.py
# Mỗi yêu cầu cách nhau >= 5 giây. Kết quả chưa quay xong (ô trống) thì bỏ qua, lần chạy sau sẽ lấy.
import datetime, html, os, re, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
UA = {"User-Agent": "Mozilla/5.0 (xs-lab data updater)"}
MB_SPEC = [("giaidb", 1, 5), ("giai1", 1, 5), ("giai2", 2, 5), ("giai3", 6, 5), ("giai4", 4, 4), ("giai5", 6, 4), ("giai6", 3, 3), ("giai7", 4, 2)]
MN_SPEC = [("giaidb", 1, 6), ("giai1", 1, 5), ("giai2", 1, 5), ("giai3", 2, 5), ("giai4", 7, 5), ("giai5", 1, 4), ("giai6", 3, 4), ("giai7", 1, 3), ("giai8", 1, 2)]
_last = [0.0]


def get(slug):
    wait = 5 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    _last[0] = time.time()
    url = f"https://www.minhngoc.net.vn/getkqxs/{slug}.js"
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(js, spec):
    txt = html.unescape(js.replace("\\\"", "\"").replace("\\/", "/"))
    m = re.search(r'selected="selected"\s*>\s*(\d{2})/(\d{2})/(\d{4})', txt) or re.search(r"Ngày:\s*(\d{2})/(\d{2})/(\d{4})", txt)
    if not m:
        return None, "không thấy ngày"
    date = f"{m.group(3)}-{m.group(2)}-{m.group(1)}"
    nums = []
    for cls, n, w in spec:
        c = re.search(r'class="' + cls + r'"\s*>(.*?)</td>', txt, re.S)
        if not c:
            return date, f"thiếu {cls}"
        v = re.findall(r"\d+", re.sub(r"<[^>]+>", " ", c.group(1)))
        if len(v) != n or any(len(x) != w for x in v):
            return date, f"{cls} chưa đủ ({' '.join(v) or 'trống'})"
        nums += v
    return date, nums


def run(args):
    r = subprocess.run([sys.executable, os.path.join(HERE, args[0])] + args[1:], cwd=ROOT, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip())


def todays_stations(csv_path, day):
    want = {(day - datetime.timedelta(days=7 * k)).isoformat() for k in range(1, 5)}
    st = set()
    for line in open(os.path.join(ROOT, csv_path)):
        p = line.split(",")
        if len(p) >= 2 and p[0] in want:
            st.add(p[1])
    return sorted(st)


def main():
    reg = sys.argv[1]
    vn = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None) + datetime.timedelta(hours=7)
    day = datetime.date.fromisoformat(sys.argv[2]) if len(sys.argv) > 2 else vn.date()
    if reg == "mb":
        try:
            date, res = parse(get("mien-bac"), MB_SPEC)
        except Exception as e:
            print("mien-bac: lỗi tải", e); return
        if isinstance(res, str):
            print("mien-bac:", date, res); return
        run(["add_day.py", "xsmb.csv", "recent.json", date, " ".join(res)])
        return
    csv_path, rec_path = ("xsmn.csv", "recent_mn.json") if reg == "mn" else ("xsmt.csv", "recent_mt.json")
    for slug in todays_stations(csv_path, day):
        try:
            date, res = parse(get(slug), MN_SPEC)
        except Exception as e:
            print(slug, ": lỗi tải", e); continue
        if isinstance(res, str):
            print(slug, ":", date, res); continue
        if date != day.isoformat():
            print(slug, ": widget đang hiện ngày", date, "(chưa có kỳ", day.isoformat() + ")")
        run(["add_day_mn.py", csv_path, rec_path, date, slug, " ".join(res)])


if __name__ == "__main__":
    main()
