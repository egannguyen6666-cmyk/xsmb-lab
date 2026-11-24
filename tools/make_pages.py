# Tạo trang tĩnh cho SEO: kết quả theo ngày, theo đài, theo thứ + sitemap.xml.
# Usage: python3 tools/make_pages.py   (chạy ở thư mục gốc của kho, sau khi dữ liệu đã cập nhật)
# Trang theo ngày được giữ lại vĩnh viễn (không xoá), nên kho lưu trữ lớn dần mỗi ngày.
import csv, datetime, html, json, os, re

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
@media(max-width:600px){table.mn{table-layout:fixed}table.mn td span{display:block;margin:1px 0;font-size:15px;letter-spacing:-.2px}table.mn tr.db td span,table.mn tr.g8 td span{font-size:16px}table.mn th{font-size:12px;padding:6px 2px}table.mn td{padding:5px 1px}table.mn td.l{width:30px;font-size:11px}td span{margin:2px 5px;font-size:16px}h1{font-size:22px}}"""


def vn(d): return f"{d[8:10]}/{d[5:7]}/{d[:4]}"
def slug_d(d): return f"{d[8:10]}-{d[5:7]}-{d[:4]}"
def wdi(d): return datetime.date.fromisoformat(d).weekday()
def esc(s): return html.escape(s, quote=True)


def page(path, title, desc, crumbs, h1, body):
    url = BASE + path
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate([("XS Lab", "")] + crumbs)]}
    depth = path.count("/")
    up = "../" * depth
    out = f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} | XS Lab</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="XS Lab"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}icon-512.png">
<link rel="icon" type="image/png" href="{up}icon-192.png"><link rel="alternate" type="application/rss+xml" href="{up}rss.xml"><meta name="theme-color" content="#16151b">
<script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script><style>{CSS}</style></head><body>
<header><nav class="q"><a class="b" href="{up}">XS Lab</a><a href="{up}xsmb/">XSMB</a><a href="{up}xsmn/">XSMN</a><a href="{up}xsmt/">XSMT</a><a href="{up}truc-tiep/">Trực tiếp</a><a href="{up}do-ve/">Dò vé</a><a href="{up}vietlott/">Vietlott</a><a href="{up}thong-ke/">Thống kê</a></nav></header>
<main><div class="bc"><a href="{up}">XS Lab</a>{''.join(f' › <a href="{up}{u}">{esc(n)}</a>' for n, u in crumbs[:-1])} › {esc(crumbs[-1][0])}</div>
<h1>{esc(h1)}</h1>{body}</main>
<footer><p><b>Thông tin nguồn.</b> {NOTICE}</p><p>XS Lab chỉ trình bày kết quả và thống kê dữ liệu đã quay, không đưa ra dự đoán kết quả. <a href="{up}hoi-dap/">Hỏi đáp</a> · <a href="{up}mien-tru-trach-nhiem/">Miễn trừ trách nhiệm</a> · <a href="{up}chinh-sach-bao-mat/">Bảo mật</a></p></footer></body></html>"""
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

# ---------- sitemap ----------
spa = [x.strip() for x in open(os.path.join(ROOT, "tools", "spa_pages.txt")).read().split() if x.strip()]
urls = [(BASE, "1.0")] + [(BASE + s + "/", "0.9" if s in ("xsmb", "xsmn", "xsmt") else "0.7") for s in spa]
for reg in REG:
    for x in sorted(os.listdir(os.path.join(ROOT, reg))):
        if os.path.isfile(os.path.join(ROOT, reg, x, "index.html")):
            urls.append((f"{BASE}{reg}/{x}/", "0.6"))
today = datetime.date.today().isoformat()
open(os.path.join(ROOT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f' <url><loc>{u}</loc><lastmod>{today}</lastmod><priority>{p}</priority></url>\n' for u, p in urls) + '</urlset>\n')
print("sitemap:", len(urls), "URL")
