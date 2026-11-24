# Tạo trang tĩnh cho SEO: kết quả theo ngày, theo đài, theo thứ + sitemap.xml.
# Usage: python3 tools/make_pages.py   (chạy ở thư mục gốc của kho, sau khi dữ liệu đã cập nhật)
# Trang theo ngày được giữ lại vĩnh viễn (không xoá), nên kho lưu trữ lớn dần mỗi ngày.
import csv, datetime, html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = ("https://" + open(os.path.join(ROOT, "CNAME")).read().strip() + "/") if os.path.exists(os.path.join(ROOT, "CNAME")) else "https://egannguyen6666-cmyk.github.io/xsmb-lab/"
ST = {'an-giang':'An Giang','bac-lieu':'Bạc Liêu','ben-tre':'Bến Tre','binh-duong':'Bình Dương','binh-phuoc':'Bình Phước','binh-thuan':'Bình Thuận','ca-mau':'Cà Mau','can-tho':'Cần Thơ','da-lat':'Đà Lạt','dong-nai':'Đồng Nai','dong-thap':'Đồng Tháp','hau-giang':'Hậu Giang','kien-giang':'Kiên Giang','long-an':'Long An','soc-trang':'Sóc Trăng','tay-ninh':'Tây Ninh','tien-giang':'Tiền Giang','tra-vinh':'Trà Vinh','vinh-long':'Vĩnh Long','vung-tau':'Vũng Tàu','tp-hcm':'TP.HCM','binh-dinh':'Bình Định','da-nang':'Đà Nẵng','dak-lak':'Đắk Lắk','dak-nong':'Đắk Nông','gia-lai':'Gia Lai','khanh-hoa':'Khánh Hòa','kon-tum':'Kon Tum','ninh-thuan':'Ninh Thuận','phu-yen':'Phú Yên','quang-binh':'Quảng Bình','quang-nam':'Quảng Nam','quang-ngai':'Quảng Ngãi','quang-tri':'Quảng Trị','thua-thien-hue':'Thừa Thiên Huế'}
WD = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
WDS = ['thu-2', 'thu-3', 'thu-4', 'thu-5', 'thu-6', 'thu-7', 'chu-nhat']
WDL = ['thứ Hai', 'thứ Ba', 'thứ Tư', 'thứ Năm', 'thứ Sáu', 'thứ Bảy', 'Chủ nhật']
REG = {'xsmb': ('XSMB', 'miền Bắc', '18:15'), 'xsmn': ('XSMN', 'miền Nam', '16:15'), 'xsmt': ('XSMT', 'miền Trung', '17:15')}
MB_G = [('ĐB', 'db'), ('G1', 'g1'), ('G2', 'g2'), ('G3', 'g3'), ('G4', 'g4'), ('G5', 'g5'), ('G6', 'g6'), ('G7', 'g7')]
MN_G = [('G8', 'g8'), ('G7', 'g7'), ('G6', 'g6'), ('G5', 'g5'), ('G4', 'g4'), ('G3', 'g3'), ('G2', 'g2'), ('G1', 'g1'), ('ĐB', 'db')]
NOTICE = 'Thông tin và kết quả xổ số trên XS Lab được chúng tôi cập nhật từ nguồn công khai và chỉ mang tính chất tham khảo. Vui lòng kiểm tra lại kết quả chính thức được công bố bởi các công ty xổ số kiến thiết.'
CSS = """:root{--bg:#f6f5f2;--p:#fff;--ink:#1b1a20;--mu:#6b6775;--ln:#e4e1db;--red:#c8102e;--band:#f1efea}
@media(prefers-color-scheme:dark){:root{--bg:#121116;--p:#1c1b22;--ink:#eceaf0;--mu:#a19cab;--ln:#2e2c36;--red:#ff5872;--band:#24222b}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--red)}header{background:#16151b;color:#fff;padding:10px 16px}header a{color:#fff;text-decoration:none;margin-right:14px;font-weight:600;font-size:14px;white-space:nowrap}header .b{font-size:18px;margin-right:18px}
nav.q{display:flex;flex-wrap:wrap;gap:4px 0;align-items:center}main{max-width:980px;margin:0 auto;padding:16px}
.bc{font-size:13px;color:var(--mu);margin:4px 0 8px}.bc a{color:var(--mu)}h1{font-size:26px;line-height:1.25;margin:4px 0 6px}h2{font-size:19px;margin:24px 0 8px}
.card{background:var(--p);border:1px solid var(--ln);border-radius:14px;padding:14px;margin:12px 0;overflow-x:auto}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{border:1px solid var(--ln);padding:7px 6px;text-align:center}th{background:var(--band);font-size:14px}
td.l{width:48px;color:var(--mu);font-weight:600;background:var(--band);font-size:13px}td span{display:inline-block;margin:2px 8px;font-size:18px}td b{color:var(--red)}
tr.db td span{font-size:22px;font-weight:700;color:var(--red)}tr.g8 td span{font-size:22px;font-weight:700;color:var(--red)}
.lt td{text-align:left}.lt td:first-child{width:44px;text-align:center;color:var(--red);font-weight:700}
.pn{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin:10px 0}.pn a{text-decoration:none;font-weight:600}
.cta{display:inline-block;background:#c8102e;color:#fff!important;text-decoration:none;padding:9px 14px;border-radius:999px;font-weight:600;margin:4px 6px 4px 0}
ul.ls{columns:2;padding-left:18px}@media(min-width:700px){ul.ls{columns:4}}footer{color:var(--mu);font-size:13px;max-width:980px;margin:20px auto;padding:0 16px 30px}
.note{color:var(--mu);font-size:14px}
table.wk td i{font-style:normal}table.wk b{color:var(--red)}@media(max-width:600px){table.wk i{display:none}table.wk td,table.wk th{font-size:13px;padding:5px 2px}table.sm td,table.sm th{font-size:12px;padding:5px 1px}}
.g100 td{padding:5px 2px;font-size:15px;line-height:1.2}.g100 small{color:var(--mu);font-size:12px}
@media(max-width:600px){table.mn{table-layout:fixed}table.mn td span{display:block;margin:1px 0;font-size:15px;letter-spacing:-.2px}table.mn tr.db td span,table.mn tr.g8 td span{font-size:16px}table.mn th{font-size:12px;padding:6px 2px}table.mn td{padding:5px 1px}table.mn td.l{width:30px;font-size:11px}td span{margin:2px 5px;font-size:16px}h1{font-size:22px}}"""


def vn(d): return f"{d[8:10]}/{d[5:7]}/{d[:4]}"
def slug_d(d): return f"{d[8:10]}-{d[5:7]}-{d[:4]}"
def wdi(d): return datetime.date.fromisoformat(d).weekday()
def esc(s): return html.escape(s, quote=True)


def page(path, title, desc, crumbs, h1, body, ld=None):
    url = BASE + path
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate([("XS Lab", "")] + crumbs)]}
    depth = path.count("/")
    up = "../" * depth
    out = f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | XS Lab</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="XS Lab"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}icon-512.png">
<link rel="icon" type="image/png" href="{up}icon-192.png"><link rel="apple-touch-icon" href="{up}icon-180.png"><link rel="manifest" href="{up}manifest.webmanifest"><link rel="alternate" type="application/rss+xml" href="{up}rss.xml"><meta name="theme-color" content="#16151b">
{shell.THEME_HEAD}<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>{"".join(f'<script type="application/ld+json">{x}</script>' for x in (ld or []))}<style>{shell.STATIC_CSS}{shell.MENU_CSS}</style></head><body class="static">{shell.SPRITE}
<div class="app">{shell.side_html(up, path)}<main class="main">{shell.mhead(up)}{shell.menu_html(up, path)}
<nav class="bc" aria-label="Đường dẫn"><a href="{up}./">XS Lab</a>{''.join(f' › <a href="{up}{u}">{esc(n)}</a>' for n, u in crumbs[:-1])} › {esc(crumbs[-1][0])}</nav>
<h1>{esc(h1)}</h1>{body}
{shell.footer_html(up)}</main></div>{shell.tab_html(up, path)}<script>{shell.MENU_JS}</script></body></html>"""
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)


def cells(vals): return ''.join(f'<span>{v[:-2]}<b>{v[-2:]}</b></span>' for v in vals)
def mb_table(r): return '<table>' + ''.join(f'<tr class="{g}"><td class="l">{lb}</td><td>{cells(r[g])}</td></tr>' for lb, g in MB_G) + '</table>'


def mn_table(recs):
    head = '<tr><th>Giải</th>' + ''.join(f'<th>{ST.get(r["station"], r["station"])}</th>' for r in recs) + '</tr>'
    return '<table class="mn">' + head + ''.join(f'<tr class="{g}"><td class="l">{lb}</td>' + ''.join(f'<td>{cells(r[g])}</td>' for r in recs) + '</tr>' for lb, g in MN_G) + '</table>'


def lotos(r, G): return sorted(int(v[-2:]) for _, g in G for v in r[g])


def loto_table(lo):
    h = [[] for _ in range(10)]
    for k in lo: h[k // 10].append(str(k % 10))
    return '<table class="lt"><tr><th>Đầu</th><th>Đuôi</th></tr>' + ''.join(f'<tr><td>{i}</td><td>{", ".join(x) or "–"}</td></tr>' for i, x in enumerate(h)) + '</table>'


def facts(lo):
    from collections import Counter
    c = Counter(lo); multi = [f"{k:02d} ×{n}" for k, n in sorted(c.items()) if n > 1]
    heads = {k // 10 for k in lo}; tails = {k % 10 for k in lo}
    dh = [str(d) for d in range(10) if d not in heads]; dt = [str(d) for d in range(10) if d not in tails]
    kep = [f"{k:02d}" for k in sorted(set(lo)) if k % 11 == 0]
    return f'<ul><li>Lô về nhiều nháy: {", ".join(multi) or "không có"}.</li><li>Đầu câm: {", ".join(dh) or "không có"}; đuôi câm: {", ".join(dt) or "không có"}.</li><li>Lô kép: {", ".join(kep) or "không có"}.</li><li>{len(set(lo))} lô khác nhau trên {len(lo)} giải.</li></ul>'


made = []
# ---------- XSMB theo ngày ----------
mb = json.load(open(os.path.join(ROOT, "recent.json")))
mb_dates = sorted(r["date"] for r in mb)
existing = lambda reg: sorted(m.group(1) for m in (re.match(r"(\d{2}-\d{2}-\d{4})$", x) for x in (os.listdir(os.path.join(ROOT, reg)) if os.path.isdir(os.path.join(ROOT, reg)) else [])) if m)
def iso(s): return f"{s[6:]}-{s[3:5]}-{s[:2]}"
all_mb = sorted(set(mb_dates) | {iso(x) for x in existing("xsmb")})
for r in mb:
    d = r["date"]; i = all_mb.index(d); prv = all_mb[i - 1] if i else None; nxt = all_mb[i + 1] if i + 1 < len(all_mb) else None
    lo = lotos(r, MB_G); w = wdi(d)
    body = f'''<p>Kết quả xổ số miền Bắc (XSMB) {WDL[w]} ngày {vn(d)}, quay lúc 18:15: giải Đặc biệt <b>{r["db"][0]}</b>, giải Nhất {r["g1"][0]}. Bảng đủ 27 giải và lô tô theo đầu bên dưới.</p>
<div class="card">{mb_table(r)}</div><h2>Lô tô XSMB {vn(d)}</h2><div class="card">{loto_table(lo)}</div><h2>Thống kê nhanh</h2>{facts(lo)}
<div class="pn">{f'<a href="../{slug_d(prv)}/">‹ XSMB {vn(prv)}</a>' if prv else '<span></span>'}{f'<a href="../{slug_d(nxt)}/">XSMB {vn(nxt)} ›</a>' if nxt else '<span></span>'}</div>
<p><a class="cta" href="../">XSMB hôm nay</a><a class="cta" href="../{WDS[w]}/">XSMB {WD[w]}</a><a class="cta" href="../../xsmb-30-ngay/">XSMB 30 ngày</a><a class="cta" href="../../do-ve/">Dò vé số</a></p>'''
    p = f"xsmb/{slug_d(d)}/"
    page(p, f"XSMB {vn(d)} – Kết quả xổ số miền Bắc {WDL[w]} ngày {vn(d)}", f"XSMB {vn(d)}: kết quả xổ số miền Bắc {WDL[w]} ngày {vn(d)}, giải Đặc biệt {r['db'][0]}, đủ 27 giải và lô tô. Không quảng cáo.", [("XSMB", "xsmb/"), (f"XSMB {vn(d)}", p)], f"XSMB {vn(d)} – Kết quả xổ số miền Bắc {WDL[w]} {vn(d)}", body)

# ---------- XSMN, XSMT theo ngày ----------
for reg, fn in (("xsmn", "recent_mn.json"), ("xsmt", "recent_mt.json")):
    lab, name, tm = REG[reg]
    rec = json.load(open(os.path.join(ROOT, fn))); by = {}
    for r in rec: by.setdefault(r["date"], []).append(r)
    all_d = sorted(set(by) | {iso(x) for x in existing(reg)})
    for d, rs in by.items():
        rs = sorted(rs, key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], "")))
        i = all_d.index(d); prv = all_d[i - 1] if i else None; nxt = all_d[i + 1] if i + 1 < len(all_d) else None; w = wdi(d)
        names = ", ".join(ST.get(r["station"], r["station"]) for r in rs)
        body = f'''<p>Kết quả xổ số {name} ({lab}) {WDL[w]} ngày {vn(d)}, quay lúc {tm}, gồm {len(rs)} đài: {names}. Giải Đặc biệt: {"; ".join(f"{ST.get(r['station'], r['station'])} <b>{r['db'][0]}</b>" for r in rs)}.</p>
<div class="card">{mn_table(rs)}</div>
{''.join(f'<h2>Lô tô {ST.get(r["station"], r["station"])} {vn(d)}</h2><div class="card">{loto_table(lotos(r, MN_G))}</div><p class="note">Xem các kỳ khác của đài: <a href="../{r["station"]}/">Xổ số {ST.get(r["station"], r["station"])}</a></p>' for r in rs)}
<div class="pn">{f'<a href="../{slug_d(prv)}/">‹ {lab} {vn(prv)}</a>' if prv else '<span></span>'}{f'<a href="../{slug_d(nxt)}/">{lab} {vn(nxt)} ›</a>' if nxt else '<span></span>'}</div>
<p><a class="cta" href="../">{lab} hôm nay</a><a class="cta" href="../{WDS[w]}/">{lab} {WD[w]}</a><a class="cta" href="../../{reg}-30-ngay/">{lab} 30 ngày</a><a class="cta" href="../../do-ve/">Dò vé số</a></p>'''
        p = f"{reg}/{slug_d(d)}/"
        page(p, f"{lab} {vn(d)} – Kết quả xổ số {name} {WDL[w]} ngày {vn(d)}", f"{lab} {vn(d)}: kết quả xổ số {name} {WDL[w]} ngày {vn(d)} các đài {names}, đủ 18 giải mỗi đài và lô tô. Không quảng cáo.", [(lab, reg + "/"), (f"{lab} {vn(d)}", p)], f"{lab} {vn(d)} – Kết quả xổ số {name} {WDL[w]} {vn(d)}", body)

    # ---------- trang từng đài ----------
    rows = list(csv.reader(open(os.path.join(ROOT, reg + ".csv"))))[1:]
    sts = sorted({r["station"] for r in rec})
    for st in sts:
        nm = ST.get(st, st); hist = sorted([r for r in rows if r[1] == st], key=lambda r: r[0])
        mine = sorted([r for r in rec if r["station"] == st], key=lambda r: r["date"], reverse=True)
        days = sorted({wdi(r["date"]) for r in mine})
        last = {}; cnt = {k: 0 for k in range(100)}; N = len(hist); win = hist[-52:]
        for i, r in enumerate(hist):
            for j in range(0, 36, 2): last[int(r[2][j:j + 2])] = i
        for r in win:
            for j in range(0, 36, 2): cnt[int(r[2][j:j + 2])] += 1
        gan = sorted(range(100), key=lambda k: -(N - 1 - last.get(k, -1)))[:10]
        hot = sorted(range(100), key=lambda k: (-cnt[k], k))[:10]
        res = ''.join(f'<h2>Xổ số {nm} {WDL[wdi(r["date"])]} {vn(r["date"])}</h2><div class="card">{mn_table([r])}</div><p class="note"><a href="../{slug_d(r["date"])}/">Xem cả các đài {lab} ngày {vn(r["date"])}</a></p>' for r in mine[:6])
        body = f'''<p>Xổ số {nm} thuộc {lab}, quay {", ".join(WDL[x] for x in days)} hằng tuần lúc khoảng {tm}. Mỗi kỳ có 18 giải, vé 6 chữ số. Dữ liệu XS Lab có {N:,} kỳ của đài {nm} (từ {vn(hist[0][0])}).</p>{res}
<h2>Lô gan {nm}</h2><p>10 lô lâu chưa về nhất tính đến kỳ {vn(hist[-1][0])}:</p><div class="card"><table><tr><th>Lô</th><th>Số kỳ chưa về</th></tr>{''.join(f'<tr><td><b>{k:02d}</b></td><td>{N - 1 - last.get(k, -1)}</td></tr>' for k in gan)}</table></div>
<h2>Lô về nhiều nhất 52 kỳ gần nhất</h2><div class="card"><table><tr><th>Lô</th><th>Số lần</th></tr>{''.join(f'<tr><td><b>{k:02d}</b></td><td>{cnt[k]}</td></tr>' for k in hot)}</table></div>
<p class="note">Theo xác suất, mỗi lô có khoảng 16,55% khả năng xuất hiện trong một kỳ của đài (18 giải). Các bảng trên là thống kê dữ liệu đã quay, không phải dự đoán.</p>
<p><a class="cta" href="../">{lab} hôm nay</a><a class="cta" href="../../thong-ke/">Thống kê lô tô</a><a class="cta" href="../../do-ve/">Dò vé {nm}</a></p>'''
        p = f"{reg}/{st}/"
        page(p, f"Xổ số {nm} – Kết quả XS {nm} hôm nay, lô gan {nm}", f"Kết quả xổ số {nm} ({lab}) các kỳ gần nhất, đủ 18 giải, lịch quay {', '.join(WDL[x] for x in days)}, lô gan và lô về nhiều của đài {nm}. Không quảng cáo.", [(lab, reg + "/"), (f"Xổ số {nm}", p)], f"Xổ số {nm} – kết quả {lab} đài {nm}", body)

    # ---------- theo thứ ----------
    for w in range(7):
        ds = sorted([d for d in by if wdi(d) == w], reverse=True)
        if not ds: continue
        body = f'<p>Kết quả {lab} {WDL[w]} các tuần gần nhất. Các đài quay {WDL[w]}: {", ".join(ST.get(s, s) for s in sorted({r["station"] for r in by[ds[0]]}))}.</p>' + ''.join(f'<h2>{lab} {WDL[w]} {vn(d)}</h2><div class="card">{mn_table(sorted(by[d], key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], ""))))}</div><p class="note"><a href="../{slug_d(d)}/">Lô tô và thống kê {lab} {vn(d)}</a></p>' for d in ds[:6])
        p = f"{reg}/{WDS[w]}/"
        page(p, f"{lab} {WD[w]} – Kết quả xổ số {name} {WDL[w]} hằng tuần", f"{lab} {WD[w]}: kết quả xổ số {name} {WDL[w]} các tuần gần nhất, các đài quay {WDL[w]}, đủ 18 giải. Không quảng cáo.", [(lab, reg + "/"), (f"{lab} {WD[w]}", p)], f"{lab} {WD[w]} – kết quả xổ số {name} {WDL[w]}", body)

for w in range(7):
    rs = sorted([r for r in mb if wdi(r["date"]) == w], key=lambda r: r["date"], reverse=True)
    if not rs: continue
    body = f'<p>Kết quả XSMB {WDL[w]} các tuần gần nhất, quay lúc 18:15.</p>' + ''.join(f'<h2>XSMB {WDL[w]} {vn(r["date"])}</h2><div class="card">{mb_table(r)}</div><p class="note"><a href="../{slug_d(r["date"])}/">Lô tô và thống kê XSMB {vn(r["date"])}</a></p>' for r in rs[:6])
    p = f"xsmb/{WDS[w]}/"
    page(p, f"XSMB {WD[w]} – Kết quả xổ số miền Bắc {WDL[w]} hằng tuần", f"XSMB {WD[w]}: kết quả xổ số miền Bắc {WDL[w]} các tuần gần nhất, đủ 27 giải. Không quảng cáo.", [("XSMB", "xsmb/"), (f"XSMB {WD[w]}", p)], f"XSMB {WD[w]} – kết quả xổ số miền Bắc {WDL[w]}", body)

# ---------- trang lưu trữ (mục lục) ----------
for reg in REG:
    lab, name, _ = REG[reg]
    ds = sorted({iso(x) for x in existing(reg)}, reverse=True)
    sts = sorted([x for x in os.listdir(os.path.join(ROOT, reg)) if x in ST]) if reg != "xsmb" else []
    body = f'<p>Toàn bộ trang kết quả {lab} theo ngày trên XS Lab ({len(ds)} ngày), mới nhất ở trên.</p><h2>Theo thứ</h2><ul class="ls">' + ''.join(f'<li><a href="../{WDS[w]}/">{lab} {WD[w]}</a></li>' for w in range(7) if os.path.isdir(os.path.join(ROOT, reg, WDS[w]))) + '</ul>'
    if sts: body += '<h2>Theo đài</h2><ul class="ls">' + ''.join(f'<li><a href="../{s}/">Xổ số {ST[s]}</a></li>' for s in sorted(sts, key=lambda s: ST[s])) + '</ul>'
    body += '<h2>Theo ngày</h2><ul class="ls">' + ''.join(f'<li><a href="../{slug_d(d)}/">{lab} {vn(d)}</a></li>' for d in ds) + '</ul>'
    p = f"{reg}/so-ket-qua/"
    page(p, f"Sổ kết quả {lab} – lưu trữ kết quả xổ số {name} theo ngày", f"Lưu trữ kết quả {lab} theo ngày, theo thứ{', theo đài' if sts else ''}. Không quảng cáo.", [(lab, reg + "/"), (f"Sổ kết quả {lab}", p)], f"Sổ kết quả {lab} theo ngày", body)


# ---------- trang thống kê (dữ liệu đã quay, không dự đoán) ----------
from collections import Counter
def grid100(c, title):
    mx = max(c.values()) or 1
    return f'<table class="g100"><caption class="note" style="caption-side:top;text-align:left;padding:4px 0">{title}</caption>' + ''.join('<tr>' + ''.join(f'<td style="background:rgba(200,16,46,{0.08 + 0.5 * c.get(r * 10 + k, 0) / mx:.2f})"><b>{r * 10 + k:02d}</b><br><small>{c.get(r * 10 + k, 0)}</small></td>' for k in range(10)) + '</tr>' for r in range(10)) + '</table>'
def tbl(head, rows): return '<table><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def card(x): return f'<div class="card">{x}</div>'
STATP = []
def spage(slug, title, desc, h1, intro, body):
    p = f"thong-ke/{slug}/"; STATP.append((slug, h1))
    page(p, title, desc, [("Thống kê", "thong-ke/"), (h1, p)], h1, f'<p>{intro}</p>{body}<p class="note">Các bảng trên là thống kê kết quả đã quay, cập nhật mỗi ngày; không phải dự đoán. Mỗi kỳ quay độc lập.</p><p><a class="cta" href="../">Thống kê lô tô</a><a class="cta" href="../bang-thong-ke/">Tất cả bảng thống kê</a><a class="cta" href="../../thong-ke-dan/">Tra cứu dàn, 3 càng</a></p>')

two = [l.split(",") for l in open(os.path.join(ROOT, "xsmb.csv")).read().strip().split("\n")[1:]]
fullmb = [(l.split(",")[0], l.split(",")[1].split()) for l in open(os.path.join(ROOT, "xsmb_full.csv")).read().strip().split("\n")[1:]]
lastd = two[-1][0]; N = len(two)
lo = [[int(r[1][j:j + 2]) for j in range(0, len(r[1]), 2)] for r in two]
last = {}; rec = Counter(); prev = {}
for i, ks in enumerate(lo):
    for k in set(ks):
        rec[k] = max(rec[k], i - prev.get(k, -1) - 1); prev[k] = i
gan = sorted(range(100), key=lambda k: -(N - 1 - prev.get(k, -1)))
spage("lo-gan-xsmb", "Lô gan XSMB – thống kê lô lâu chưa về miền Bắc", f"Lô gan XSMB đến {vn(lastd)}: 30 lô lâu chưa về nhất, kỷ lục gan của từng lô từ 2005. Không quảng cáo.", "Lô gan XSMB",
      f"Lô gan là lô (2 số cuối của giải) đã nhiều kỳ liên tiếp chưa xuất hiện. Bảng tính đến kỳ {vn(lastd)} trên {N:,} kỳ XSMB từ {vn(two[0][0])}.",
      card(tbl(["Lô", "Số kỳ chưa về", "Lần về gần nhất", "Kỷ lục gan"], [(f"<b>{k:02d}</b>", N - 1 - prev[k], vn(two[prev[k]][0]), rec[k]) for k in gan[:30]])))
c30 = Counter(k for ks in lo[-30:] for k in ks); c90 = Counter(k for ks in lo[-90:] for k in ks)
spage("tan-suat-lo-to-xsmb", "Tần suất lô tô XSMB 30, 90 ngày – bảng 00–99", f"Tần suất lô tô XSMB 00–99 trong 30 và 90 kỳ gần nhất đến {vn(lastd)}. Không quảng cáo.", "Tần suất lô tô XSMB",
      f"Số lần mỗi lô từ 00 đến 99 xuất hiện. Mỗi kỳ XSMB có 27 lô, nên trong 30 kỳ trung bình mỗi lô về {30 * 27 / 100:.1f} lần.",
      card(grid100(c30, f"30 kỳ gần nhất ({vn(two[-30][0])} – {vn(lastd)})")) + card(grid100(c90, f"90 kỳ gần nhất ({vn(two[-90][0])} – {vn(lastd)})")))
dh = Counter(k // 10 for ks in lo[-30:] for k in ks); dt = Counter(k % 10 for ks in lo[-30:] for k in ks)
db = [(r[0], int(r[1][:2])) for r in two]
dbh = Counter(k // 10 for _, k in db[-100:]); dbt = Counter(k % 10 for _, k in db[-100:])
spage("dau-duoi-xsmb", "Thống kê đầu đuôi lô tô XSMB", f"Thống kê đầu đuôi lô tô và giải đặc biệt XSMB đến {vn(lastd)}. Không quảng cáo.", "Đầu đuôi lô tô XSMB",
      "Đầu là chữ số hàng chục, đuôi là chữ số hàng đơn vị của lô. Trung bình mỗi đầu (hoặc đuôi) chiếm 10% số lô.",
      card(tbl(["Chữ số", "Đầu lô (30 kỳ)", "Đuôi lô (30 kỳ)", "Đầu ĐB (100 kỳ)", "Đuôi ĐB (100 kỳ)"], [(d, dh[d], dt[d], dbh[d], dbt[d]) for d in range(10)])))
# đặc biệt theo tuần
fmap = dict(fullmb)
end = datetime.date.fromisoformat(lastd); start = end - datetime.timedelta(days=end.weekday() + 7 * 11)
rows = []
for w in range(12):
    row = []
    for k in range(7):
        d = (start + datetime.timedelta(days=7 * w + k)).isoformat()
        v = fmap.get(d); row.append(f'<i>{v[0][:-2]}</i><b>{v[0][-2:]}</b>' if v else ('' if d > lastd else '–'))
    rows.append([vn((start + datetime.timedelta(days=7 * w)).isoformat())] + row)
dbg = {}
for i, (d, k) in enumerate(db): dbg[k] = i
dgan = sorted(range(100), key=lambda k: -(N - 1 - dbg.get(k, -1)))[:15]
spage("giai-dac-biet-xsmb", "Thống kê giải đặc biệt XSMB – bảng đặc biệt tuần", f"Bảng giải đặc biệt XSMB theo tuần 12 tuần gần nhất, đầu đuôi và 2 số cuối giải đặc biệt lâu chưa về, đến {vn(lastd)}.", "Thống kê giải đặc biệt XSMB",
      "Bảng giải Đặc biệt XSMB theo tuần (2 số cuối tô đỏ) và các số chưa làm 2 số cuối giải Đặc biệt lâu nhất.",
      card(tbl(["Tuần từ"] + WD, rows[::-1]).replace("<table>", "<table class=\"wk\">", 1)) + "<h2>2 số cuối giải Đặc biệt lâu chưa về</h2>" + card(tbl(["Số", "Số kỳ chưa về", "Lần gần nhất"], [(f"<b>{k:02d}</b>", N - 1 - dbg[k], vn(db[dbg[k]][0])) for k in dgan])))
g1 = [(d, v[1]) for d, v in fullmb]; g1c = Counter(int(v[-2:]) for _, v in g1[-100:])
spage("giai-nhat-xsmb", "Thống kê giải nhất XSMB", f"Giải nhất XSMB 30 kỳ gần nhất và tần suất 2 số cuối giải nhất 100 kỳ, đến {vn(lastd)}.", "Thống kê giải nhất XSMB",
      "Giải Nhất XSMB gồm 5 chữ số. Bảng liệt kê 30 kỳ gần nhất và số lần mỗi cặp 2 số cuối xuất hiện ở giải Nhất trong 100 kỳ.",
      card(tbl(["Ngày", "Giải Nhất", "2 số cuối"], [(vn(d), v, f"<b>{v[-2:]}</b>") for d, v in g1[-30:][::-1]])) + card(grid100(g1c, "2 số cuối giải Nhất, 100 kỳ gần nhất")))
def cang(L, label, slug, minw):
    tails = [(d, v[0][-L:]) for d, v in fullmb if len(v[0]) >= L]
    allc = Counter(t for _, t in tails); M = len(tails)
    lastseen = {}
    for i, (_, t) in enumerate(tails): lastseen[t] = i
    rec30 = Counter(x[-L:] for _, v in fullmb[-30:] for x in v if len(x) >= minw)
    body = "<h2>" + label + " giải Đặc biệt 30 kỳ gần nhất</h2>" + card(tbl(["Ngày", "Giải Đặc biệt", label], [(vn(d), v[0], f"<b>{v[0][-L:]}</b>") for d, v in fullmb[-30:][::-1]]))
    top = [(t, n) for t, n in allc.most_common(20)]
    body += f"<h2>{label} giải Đặc biệt về nhiều lần nhất ({M:,} kỳ)</h2><p class='note'>Theo xác suất, mỗi số {label} trung bình về {M / 10 ** L:.2f} lần ở giải Đặc biệt trong {M:,} kỳ.</p>" + card(tbl([label, "Số lần", "Lần gần nhất"], [(f"<b>{t}</b>", n, vn(tails[lastseen[t]][0])) for t, n in top]))
    if L == 3:
        h = Counter(t[0] for _, t in tails[-365:])
        body += "<h2>Đầu 3 càng giải Đặc biệt (365 kỳ)</h2>" + card('<table class="sm">' + tbl(["Chữ số hàng trăm"] + [str(d) for d in range(10)], [["Số lần"] + [h[str(d)] for d in range(10)]])[7:])
        never = [f"{x:03d}" for x in range(1000) if f"{x:03d}" not in allc]
        gl = sorted(lastseen, key=lambda t: lastseen[t])[:15]
        body += f"<h2>3 càng giải Đặc biệt lâu chưa về</h2>" + card(tbl(["3 càng", "Số kỳ chưa về", "Lần gần nhất"], [(f"<b>{t}</b>", M - 1 - lastseen[t], vn(tails[lastseen[t]][0])) for t in gl])) + (f"<p class='note'>{len(never)} số 3 càng chưa từng làm 3 số cuối giải Đặc biệt.</p>" if never else "")
    body += f"<h2>{label} ở mọi giải, 30 kỳ gần nhất</h2><p class='note'>Tính {L} chữ số cuối của các giải có từ {minw} chữ số trở lên.</p>" + card(tbl([label, "Số lần"], [(f"<b>{t}</b>", n) for t, n in rec30.most_common(20)]))
    spage(slug, f"Thống kê {label} XSMB – {label} giải đặc biệt", f"Thống kê {label} XSMB đến {vn(lastd)}: {label} giải đặc biệt 30 kỳ, {label} về nhiều nhất, lâu chưa về và {label} ở mọi giải. Không quảng cáo.", f"Thống kê {label} XSMB",
          f"{label} là {L} chữ số cuối của giải (thường xét giải Đặc biệt). Dữ liệu đủ giải XSMB từ {vn(fullmb[0][0])} đến {vn(fullmb[-1][0])}.", body)
cang(3, "3 càng", "3-cang-xsmb", 3); cang(4, "4 càng", "4-cang-xsmb", 4)
for reg in ("xsmn", "xsmt"):
    lab, name, _ = REG[reg]
    F = [(l.split(",")[0], l.split(",")[1], l.split(",")[2].split()) for l in open(os.path.join(ROOT, reg + "_full.csv")).read().strip().split("\n")[1:]]
    ds = sorted({d for d, _, _ in F}); ld = ds[-1]; byd = {}
    for d, s, v in F: byd.setdefault(d, []).append((s, v))
    def recent_tbl(idx, L=None, n=14):
        rows = []
        for d in ds[-n:][::-1]:
            rows.append([vn(d), " · ".join(f"{ST.get(s, s)}: <b>{(v[idx][-L:] if L else v[idx])}</b>" for s, v in sorted(byd[d]))])
        return card(tbl(["Ngày", "Các đài"], rows))
    d90 = set(ds[-90:]); d180 = set(ds[-180:])
    g8c = Counter(int(v[17]) for d, s, v in F if d in d90)
    g8last = {}
    for i, d in enumerate(ds):
        for s, v in byd[d]: g8last[int(v[17])] = i
    g8g = sorted(range(100), key=lambda k: g8last.get(k, -1))[:15]
    spage(f"giai-8-{reg}", f"Thống kê giải tám {lab} – giải 8 {name}", f"Giải tám {lab} 14 ngày gần nhất theo đài, tần suất giải 8 trong 90 ngày và số lâu chưa về ở giải 8, đến {vn(ld)}.", f"Thống kê giải tám {lab}",
          f"Giải Tám {lab} là giải 2 chữ số, quay đầu tiên ở mỗi đài. Bảng tính trên tất cả các đài {name}.",
          "<h2>Giải tám 14 ngày gần nhất</h2>" + recent_tbl(17) + card(grid100(g8c, f"Tần suất giải tám, 90 ngày gần nhất (tất cả các đài)")) + "<h2>Số lâu chưa về ở giải tám</h2>" + card(tbl(["Số", "Số ngày chưa về", "Lần gần nhất"], [(f"<b>{k:02d}</b>", len(ds) - 1 - g8last[k], vn(ds[g8last[k]])) for k in g8g if k in g8last])))
    g1c = Counter(int(v[1][-2:]) for d, s, v in F if d in d90)
    spage(f"giai-nhat-{reg}", f"Thống kê giải nhất {lab}", f"Giải nhất {lab} 14 ngày gần nhất theo đài và tần suất 2 số cuối giải nhất 90 ngày, đến {vn(ld)}.", f"Thống kê giải nhất {lab}",
          f"Giải Nhất {lab} gồm 5 chữ số. Bảng liệt kê 14 ngày gần nhất và số lần mỗi cặp 2 số cuối xuất hiện ở giải Nhất.",
          "<h2>Giải nhất 14 ngày gần nhất</h2>" + recent_tbl(1) + card(grid100(g1c, "2 số cuối giải Nhất, 90 ngày gần nhất (tất cả các đài)")))
    dbc = Counter(int(v[0][-2:]) for d, s, v in F if d in d180)
    dlast = {}
    for i, d in enumerate(ds):
        for s, v in byd[d]: dlast[int(v[0][-2:])] = i
    dg = sorted(range(100), key=lambda k: dlast.get(k, -1))[:15]
    spage(f"giai-dac-biet-{reg}", f"Thống kê giải đặc biệt {lab}", f"Giải đặc biệt {lab} 14 ngày gần nhất theo đài, tần suất 2 số cuối giải đặc biệt 180 ngày và số lâu chưa về, đến {vn(ld)}.", f"Thống kê giải đặc biệt {lab}",
          f"Giải Đặc biệt {lab} gồm 6 chữ số (trước năm 2009 là 5 chữ số). Bảng tính trên tất cả các đài {name}.",
          "<h2>Giải đặc biệt 14 ngày gần nhất</h2>" + recent_tbl(0) + card(grid100(dbc, "2 số cuối giải Đặc biệt, 180 ngày gần nhất")) + "<h2>2 số cuối giải đặc biệt lâu chưa về</h2>" + card(tbl(["Số", "Số ngày chưa về", "Lần gần nhất"], [(f"<b>{k:02d}</b>", len(ds) - 1 - dlast[k], vn(ds[dlast[k]])) for k in dg if k in dlast])))
    d365 = set(ds[-365:]); c3 = Counter(v[0][-3:] for d, s, v in F if d in d365); h3 = Counter(v[0][-3] for d, s, v in F if d in d365); M3 = sum(c3.values())
    spage(f"3-cang-{reg}", f"Thống kê 3 càng {lab} – 3 càng giải đặc biệt", f"3 càng giải đặc biệt {lab} 14 ngày gần nhất theo đài, 3 càng về nhiều nhất và đầu 3 càng trong 365 ngày, đến {vn(ld)}.", f"Thống kê 3 càng {lab}",
          f"3 càng là 3 chữ số cuối của giải Đặc biệt. Trong 365 ngày gần nhất có {M3:,} giải Đặc biệt {lab}; mỗi số 3 càng trung bình về {M3 / 1000:.2f} lần.",
          "<h2>3 càng 14 ngày gần nhất</h2>" + recent_tbl(0, 3) + "<h2>3 càng về nhiều nhất (365 ngày)</h2>" + card(tbl(["3 càng", "Số lần"], [(f"<b>{t}</b>", n) for t, n in c3.most_common(20)])) + "<h2>Đầu 3 càng (365 ngày)</h2>" + card('<table class="sm">' + tbl(["Chữ số hàng trăm"] + [str(d) for d in range(10)], [["Số lần"] + [h3[str(d)] for d in range(10)]])[7:]))
hub = "<p>Các bảng thống kê kết quả XSMB, XSMN, XSMT được tạo lại mỗi ngày từ dữ liệu đã quay.</p>" + "".join(f"<h2>{REG[r][0]}</h2><ul class='ls'>" + "".join(f'<li><a href="../{s}/">{h}</a></li>' for s, h in STATP if s.endswith(r)) + "</ul>" for r in REG)
page("thong-ke/bang-thong-ke/", "Bảng thống kê xổ số XSMB, XSMN, XSMT – lô gan, 3 càng, giải đặc biệt", "Tổng hợp các bảng thống kê XSMB, XSMN, XSMT: lô gan, tần suất lô tô, đầu đuôi, giải đặc biệt, giải nhất, giải tám, 3 càng, 4 càng. Không quảng cáo.", [("Thống kê", "thong-ke/"), ("Bảng thống kê", "thong-ke/bang-thong-ke/")], "Bảng thống kê xổ số", hub)


# ---------- hiện sẵn bảng kết quả mới nhất trong trang ứng dụng (tải nhanh, không nhảy bố cục) ----------
WDV = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']
def heads(lo):
    h = [[] for _ in range(10)]
    for k in sorted(lo): h[k // 10].append(str(k % 10))
    return h
def pre_mb():
    r = mb[-1]; d = r["date"]
    b = '<div class="ticket">' + ''.join(f'<div class="row {"db" if g == "db" else ""}"><div class="lb">{lb}</div><div class="nums">' + ''.join(f'<span>{n[:-2]}<b>{n[-2:]}</b></span>' for n in r[g]) + '</div></div>' for lb, g in MB_G) + '</div>'
    b += '<div class="loto">' + ''.join(f'<div><b>{j}</b><span>{", ".join(a) or "–"}</span></div>' for j, a in enumerate(heads(lotos(r, MB_G)))) + '</div>'
    return f"XSMB {WDV[wdi(d)]}, {vn(d)}", b
def pre_mn(fn, lab, sel):
    rec = json.load(open(os.path.join(ROOT, fn))); d = max(r["date"] for r in rec)
    rs = sorted([r for r in rec if r["date"] == d], key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], "")))
    b = '<div class="mnb"><table><thead><tr><th>Giải</th>' + ''.join(f'<th class="{"sel" if r["station"] == sel else ""}">{ST.get(r["station"], r["station"])}</th>' for r in rs) + '</tr></thead><tbody>'
    b += ''.join(f'<tr class="{g}"><td>{lb}</td>' + ''.join('<td>' + ''.join(f'<span>{n[:-2]}<b>{n[-2:]}</b></span>' for n in r[g]) + '</td>' for r in rs) + '</tr>' for lb, g in MN_G) + '</tbody></table></div>'
    b += '<div class="lt">' + ''.join(f'<div><h4>{ST.get(r["station"], r["station"])}</h4>' + ''.join(f'<p><b>{j}</b><span>{", ".join(a) or "–"}</span></p>' for j, a in enumerate(heads(lotos(r, MN_G)))) + '</div>' for r in rs) + '</div>'
    return f"{lab} {WDV[wdi(d)]}, {vn(d)}", b
PRE = {"mb": pre_mb(), "mn": pre_mn("recent_mn.json", "XSMN", "tp-hcm"), "mt": pre_mn("recent_mt.json", "XSMT", "da-nang")}
for f, reg in (("index.html", "mb"), ("xsmb/index.html", "mb"), ("xsmb-30-ngay/index.html", "mb"), ("xsmn/index.html", "mn"), ("xsmn-30-ngay/index.html", "mn"), ("xsmt/index.html", "mt"), ("xsmt-30-ngay/index.html", "mt")):
    fp = os.path.join(ROOT, f)
    if not os.path.exists(fp): continue
    h = open(fp).read(); title, board = PRE[reg]
    h2 = re.sub(r'<div id="rsBoard">.*?</div><!--/rsb-->', lambda m: f'<div id="rsBoard">{board}</div><!--/rsb-->', h, count=1, flags=re.S)
    h2 = re.sub(r'<h2 id="rsT">[^<]*</h2>', f'<h2 id="rsT">{title}</h2>', h2, count=1)
    dlast = {'mb': mb[-1]['date']}.get(reg) or max(r['date'] for r in json.load(open(os.path.join(ROOT, 'recent_mn.json' if reg == 'mn' else 'recent_mt.json'))))
    h2 = re.sub(r'<input type="date" id="rsDate"[^>]*>', f'<input type="date" id="rsDate" aria-label="Chọn ngày" value="{dlast}">', h2, count=1)
    if h2 != h: open(fp, "w").write(h2)

# ---------- sitemap ----------

# ---------- Trang thông tin: giới thiệu, liên hệ, điều khoản ----------
GH = "https://github.com/egannguyen6666-cmyk/xsmb-lab"
ORG = shell.org_ld(BASE)
def webpage_ld(typ, path, name):
    return json.dumps({"@context": "https://schema.org", "@type": typ, "name": name, "url": BASE + path, "inLanguage": "vi", "isPartOf": {"@type": "WebSite", "name": "XS Lab", "url": BASE}, "publisher": {"@id": BASE + "#org"}}, ensure_ascii=False)
INFO_PAGES = [
 ("gioi-thieu/", "AboutPage", "Giới thiệu XS Lab – trang kết quả xổ số và thống kê dữ liệu không quảng cáo", "XS Lab là trang kết quả xổ số XSMB, XSMN, XSMT, Vietlott và thống kê dữ liệu quá khứ, không quảng cáo, không dự đoán. Nguồn dữ liệu, cách cập nhật và nguyên tắc biên tập.", "Giới thiệu", "Giới thiệu XS Lab", f"""<div class="card doc">
<p><b>XS Lab</b> là trang tra cứu kết quả xổ số và thống kê dữ liệu cho xổ số kiến thiết miền Bắc (XSMB), miền Nam (XSMN), miền Trung (XSMT) và các sản phẩm Vietlott. Trang được xây dựng như một công cụ đọc dữ liệu: gọn, nhanh, không quảng cáo, không cửa sổ bật lên và không theo dõi người dùng.</p>
<h2>XS Lab làm gì</h2><ul>
<li>Cập nhật kết quả XSMB, XSMN, XSMT mỗi ngày ngay sau giờ quay, kèm trang trực tiếp trong giờ quay và sổ kết quả theo ngày, theo đài, theo thứ.</li>
<li>Cập nhật kết quả Vietlott: Keno, Mega 6/45, Power 6/55, Max 3D, Max 3D Pro.</li>
<li>Trình bày dữ liệu thống kê từ kết quả đã quay: lô gan, tần suất, đầu đuôi, giải đặc biệt, 3 càng, 4 càng; công cụ dò vé và tra cứu dàn số.</li>
<li>Giải thích cơ cấu giải, cách dò vé, thời hạn và nơi lĩnh thưởng theo thể lệ đã công bố.</li></ul>
<h2>XS Lab không làm gì</h2><ul>
<li>Không đưa ra dự đoán, “soi cầu” hay gợi ý số. Mọi con số trên trang là thống kê kết quả đã quay; mỗi kỳ quay độc lập với các kỳ trước.</li>
<li>Không bán vé, không nhận đặt cược, không thu tiền dưới bất kỳ hình thức nào. Tin nhắn hay tài khoản mạng xã hội mời chào nhân danh XS Lab là giả mạo.</li>
<li>Không chạy quảng cáo và không thu thập dữ liệu cá nhân (xem <a href="../chinh-sach-bao-mat/">Chính sách bảo mật</a>).</li></ul>
<h2>Nguồn dữ liệu và cách cập nhật</h2>
<p>Kết quả được tổng hợp tự động từ các trang công bố kết quả công khai, sau đó đối chiếu chéo giữa các nguồn và với dữ liệu lưu trữ trước khi đăng. Lịch sử XSMB có từ năm 2005; XSMN, XSMT lưu theo từng đài. Toàn bộ dữ liệu được công khai dưới dạng tệp CSV để ai cũng kiểm tra được. Chi tiết tại <a href="../ve-du-lieu/">Về dữ liệu</a>.</p>
<p class="note">{NOTICE}</p>
<h2>Nguyên tắc biên tập</h2><ul>
<li>Chỉ viết những gì kiểm chứng được từ thể lệ của công ty xổ số kiến thiết và Vietlott, hoặc tính toán trực tiếp từ dữ liệu đã quay; khi thể lệ thay đổi, nội dung được sửa theo.</li>
<li>Xác suất và tỷ lệ trả thưởng được nêu rõ để người đọc hiểu đúng bản chất: kỳ vọng của mọi cách chơi xổ số đều âm.</li>
<li>Phát hiện sai sót sẽ được sửa ngay khi xác minh. Bạn có thể báo lỗi tại trang <a href="../lien-he/">Liên hệ</a>.</li></ul>
<h2>Chơi có trách nhiệm</h2>
<p>Xổ số là trò chơi có thưởng dành cho người từ đủ 18 tuổi. Hãy coi đây là hình thức giải trí, chỉ chi số tiền bạn sẵn sàng mất, và đừng tìm cách “gỡ” khi đã thua.</p></div>"""),
 ("lien-he/", "ContactPage", "Liên hệ XS Lab – góp ý, báo lỗi kết quả xổ số", "Liên hệ XS Lab để góp ý, báo lỗi kết quả XSMB, XSMN, XSMT, Vietlott hoặc đề xuất tính năng.", "Liên hệ", "Liên hệ XS Lab", f"""<div class="card doc">
<p>XS Lab luôn muốn nghe góp ý của người đọc. Nếu bạn thấy kết quả nào chưa khớp với kết quả chính thức, một trang hiển thị lỗi hay muốn đề xuất tính năng mới, hãy liên hệ qua kênh dưới đây.</p>
<h2>Kênh liên hệ</h2><ul>
<li><b>Email:</b> <a href="mailto:{shell.EMAIL}">{shell.EMAIL}</a> – góp ý, báo lỗi kết quả, đề xuất tính năng.</li>
<li><b>Website:</b> <a href="{BASE}">xslab.live</a></li></ul>
<h2>Khi báo lỗi kết quả</h2>
<p>Để sửa nhanh, vui lòng ghi rõ: miền hoặc đài (ví dụ XSMB, Vĩnh Long), ngày quay, giải bị sai, con số đang hiển thị và con số đúng kèm nguồn (trang của công ty xổ số kiến thiết hoặc Vietlott).</p>
<h2>Lưu ý</h2><ul>
<li>XS Lab không bán vé, không nhận đặt cược, không cung cấp số dự đoán và không bao giờ yêu cầu chuyển tiền. Mọi lời mời chào như vậy nhân danh XS Lab đều là giả mạo.</li>
<li>Về lĩnh thưởng, vé trúng hay tranh chấp liên quan đến vé, vui lòng liên hệ trực tiếp công ty xổ số kiến thiết phát hành vé hoặc Vietlott.</li></ul>
<p class="note">{NOTICE}</p></div>"""),
 ("dieu-khoan-su-dung/", "WebPage", "Điều khoản sử dụng XS Lab", "Điều khoản sử dụng trang XS Lab: tính chất thông tin, giới hạn trách nhiệm, sử dụng dữ liệu và độ tuổi.", "Điều khoản sử dụng", "Điều khoản sử dụng", f"""<div class="card doc">
<p>Khi truy cập và sử dụng XS Lab ({BASE}), bạn đồng ý với các điều khoản dưới đây. Nếu không đồng ý, vui lòng ngừng sử dụng trang.</p>
<h2>1. Tính chất thông tin</h2><p>{NOTICE} Dữ liệu thống kê trên XS Lab mô tả các kết quả đã quay, không phải dự đoán và không phải lời khuyên tham gia xổ số.</p>
<h2>2. Giới hạn trách nhiệm</h2><p>XS Lab nỗ lực bảo đảm thông tin chính xác và kịp thời nhưng không bảo đảm tuyệt đối. XS Lab không chịu trách nhiệm cho bất kỳ thiệt hại nào phát sinh từ việc sử dụng thông tin trên trang, kể cả việc dò vé, mua vé hay lĩnh thưởng dựa trên thông tin này. Kết quả chính thức để lĩnh thưởng là kết quả do công ty xổ số kiến thiết và Vietlott công bố.</p>
<h2>3. Độ tuổi</h2><p>Xổ số là trò chơi có thưởng dành cho người từ đủ 18 tuổi theo quy định của pháp luật Việt Nam.</p>
<h2>4. Sử dụng hợp pháp</h2><p>Bạn không được dùng nội dung hoặc dữ liệu của XS Lab cho hoạt động cá cược, số đề hay bất kỳ hoạt động nào trái pháp luật; không được dùng công cụ tự động gây quá tải cho trang.</p>
<h2>5. Dữ liệu và nội dung</h2><p>Các tệp dữ liệu CSV được cung cấp miễn phí cho mục đích tra cứu, học tập và nghiên cứu; khi sử dụng lại, vui lòng ghi nguồn XS Lab. Kết quả xổ số là thông tin công khai của các đơn vị phát hành.</p>
<h2>6. Liên kết bên ngoài</h2><p>Trang có thể dẫn đến website khác; XS Lab không chịu trách nhiệm về nội dung của các website đó.</p>
<h2>7. Quyền riêng tư</h2><p>Xem <a href="../chinh-sach-bao-mat/">Chính sách bảo mật</a> và <a href="../cookies/">Chính sách cookie</a>.</p>
<h2>8. Thay đổi điều khoản</h2><p>XS Lab có thể cập nhật điều khoản khi cần; phiên bản đăng trên trang này là phiên bản có hiệu lực. Mọi thắc mắc xin gửi qua trang <a href="../lien-he/">Liên hệ</a>.</p>
<p class="note">Cập nhật lần cuối: 24/11/2026.</p></div>"""),
]
for path, typ, title, desc, crumb, h1, body in INFO_PAGES:
    page(path, title, desc, [(crumb, path)], h1, body, ld=[ORG, webpage_ld(typ, path, h1)])

spa = [x.strip() for x in open(os.path.join(ROOT, "tools", "spa_pages.txt")).read().split() if x.strip()]
urls = [(BASE, "1.0")] + [(BASE + s + "/", "0.9" if s in ("xsmb", "xsmn", "xsmt") else "0.7") for s in spa] + [(BASE + x[0], "0.5") for x in INFO_PAGES]
for reg in list(REG) + ["thong-ke"]:
    for x in sorted(os.listdir(os.path.join(ROOT, reg))):
        if os.path.isfile(os.path.join(ROOT, reg, x, "index.html")):
            urls.append((f"{BASE}{reg}/{x}/", "0.6"))
today = datetime.date.today().isoformat()
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f' <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n' for u, p in urls) + '</urlset>\n')
print("sitemap:", len(urls), "URL")
