# Tạo trang tĩnh cho SEO: kết quả theo ngày, theo đài, theo thứ + sitemap.xml.
# Usage: python3 tools/make_pages.py   (chạy ở thư mục gốc của kho, sau khi dữ liệu đã cập nhật)
# Trang theo ngày được giữ lại vĩnh viễn (không xoá), nên kho lưu trữ lớn dần mỗi ngày.
import csv, datetime, html, json, os, re, sys
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shell

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = ("https://" + open(os.path.join(ROOT, "CNAME")).read().strip() + "/") if os.path.exists(os.path.join(ROOT, "CNAME")) else "https://egannguyen6666-cmyk.github.io/xsmb-lab/"
ST = {'an-giang':'An Giang','bac-lieu':'Bạc Liêu','ben-tre':'Bến Tre','binh-duong':'Bình Dương','binh-phuoc':'Bình Phước','binh-thuan':'Bình Thuận','ca-mau':'Cà Mau','can-tho':'Cần Thơ','da-lat':'Đà Lạt','dong-nai':'Đồng Nai','dong-thap':'Đồng Tháp','hau-giang':'Hậu Giang','kien-giang':'Kiên Giang','long-an':'Long An','soc-trang':'Sóc Trăng','tay-ninh':'Tây Ninh','tien-giang':'Tiền Giang','tra-vinh':'Trà Vinh','vinh-long':'Vĩnh Long','vung-tau':'Vũng Tàu','tp-hcm':'TP.HCM','binh-dinh':'Bình Định','da-nang':'Đà Nẵng','dak-lak':'Đắk Lắk','dak-nong':'Đắk Nông','gia-lai':'Gia Lai','khanh-hoa':'Khánh Hòa','kon-tum':'Kon Tum','ninh-thuan':'Ninh Thuận','phu-yen':'Phú Yên','quang-binh':'Quảng Bình','quang-nam':'Quảng Nam','quang-ngai':'Quảng Ngãi','quang-tri':'Quảng Trị','thua-thien-hue':'Thừa Thiên Huế'}
AB2 = {'ben-tre': 'XSBTR', 'tp-hcm': 'XSTP', 'da-nang': 'XSDNA', 'da-lat': 'XSLD', 'thua-thien-hue': 'XSHUE', 'quang-nam': 'XSQNA'}
STATION_SM = {'xsmn': [], 'xsmt': []}
AB = {'an-giang':'XSAG','bac-lieu':'XSBL','ben-tre':'XSBT','binh-duong':'XSBD','binh-phuoc':'XSBP','binh-thuan':'XSBTH','ca-mau':'XSCM','can-tho':'XSCT','da-lat':'XSDL','dong-nai':'XSDN','dong-thap':'XSDT','hau-giang':'XSHG','kien-giang':'XSKG','long-an':'XSLA','soc-trang':'XSST','tay-ninh':'XSTN','tien-giang':'XSTG','tra-vinh':'XSTV','vinh-long':'XSVL','vung-tau':'XSVT','tp-hcm':'XSHCM','binh-dinh':'XSBDI','da-nang':'XSDNG','dak-lak':'XSDLK','dak-nong':'XSDNO','gia-lai':'XSGL','khanh-hoa':'XSKH','kon-tum':'XSKT','ninh-thuan':'XSNT','phu-yen':'XSPY','quang-binh':'XSQB','quang-nam':'XSQNM','quang-ngai':'XSQNG','quang-tri':'XSQT','thua-thien-hue':'XSTTH'}
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


def dec(x, k): return f'{x:.{k}f}'.replace('.', ',')
def fm(n): return f'{n:,}'.replace(',', '.')
def vn(d): return f"{d[8:10]}/{d[5:7]}/{d[:4]}"
def slug_d(d): return f"{d[8:10]}-{d[5:7]}-{d[:4]}"
def wdi(d): return datetime.date.fromisoformat(d).weekday()
def esc(s): return html.escape(s, quote=True)

# Cấu hình sửa từ trang quản trị (site-config.json): tiêu đề SEO từng trang và mẫu cho nhóm trang.
try: CFG = json.load(open(os.path.join(ROOT, "site-config.json"), encoding="utf-8"))
except Exception: CFG = {}
SEO_DEF = {}
def _tpl(t, v):
    for k, x in v.items(): t = t.replace("{" + k + "}", str(x))
    return t
def seo_apply(path, title, desc, fam=None):
    if fam:
        m = (CFG.get("seo_mau") or {}).get(fam[0]) or {}
        if str(m.get("title", "")).strip(): title = _tpl(m["title"].strip(), fam[1])
        if str(m.get("desc", "")).strip(): desc = _tpl(m["desc"].strip(), fam[1])
        return title, desc
    SEO_DEF[path] = (title, desc)
    o = (CFG.get("seo_trang") or {}).get(path) or {}
    return (str(o.get("title", "")).strip() or title), (str(o.get("desc", "")).strip() or desc)


# ---------- tệp giao diện dùng chung cho mọi trang tĩnh (mỗi trang nhẹ hơn, trình duyệt lưu đệm) ----------
import hashlib
EXTRA_CSS = """@view-transition{navigation:auto}::view-transition-old(root),::view-transition-new(root){animation-duration:.14s}:where(tbody tr:nth-child(even))>td{background-color:light-dark(#f7f6f2,#211f28)}.ngrid a:is(:nth-child(20n+11),:nth-child(20n+12),:nth-child(20n+13),:nth-child(20n+14),:nth-child(20n+15),:nth-child(20n+16),:nth-child(20n+17),:nth-child(20n+18),:nth-child(20n+19),:nth-child(20n+20)):not([aria-current]){background:light-dark(#f3f1ec,#24222c)}.mnb tbody tr:nth-child(even) td:not(:first-child),.ticket .row:nth-child(even) .nums{background:light-dark(#f7f6f2,#211f28)}.mnb tbody tr:nth-child(even) td:first-child,.ticket .row:nth-child(even) .lb{background:light-dark(#e8e5df,#2c2a34)}.mnb td:not(:first-child){transition:background .2s}a.sl{color:inherit;text-decoration:none}a.sl:hover,a.sl:focus-visible{color:var(--red,#d01f3c);text-decoration:underline}.c30 a.sl,.lt a.sl{color:inherit}.qttabs{display:flex;gap:8px;flex-wrap:wrap}.qttabs a{padding:7px 12px;border:1px solid var(--line);border-radius:999px;background:var(--panel);color:var(--ink);text-decoration:none;font-weight:600;font-size:14px}.qttabs a[aria-current=page]{background:#d01f3c;border-color:#d01f3c;color:#fff}.qtbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px}.qtbar label{display:flex;gap:6px;align-items:center;font-size:14px}.qtbar select{min-height:40px;border:1px solid var(--line);border-radius:10px;background:var(--panel);color:var(--ink);font:inherit;font-size:14px;padding:0 8px;max-width:100%}.qtgo{min-height:44px;border:0;border-radius:12px;background:#d01f3c;color:#fff;font:inherit;font-weight:800;font-size:17px;padding:0 22px;cursor:pointer}.qtre{min-height:44px;border:1px solid var(--line);border-radius:12px;background:var(--panel);color:var(--ink);font:inherit;font-weight:600;padding:0 14px;cursor:pointer}.qroll{color:#d01f3c;opacity:.75}.qpend{color:var(--mute);letter-spacing:2px}#qtLo mark{background:#d01f3c;color:#fff;border-radius:4px;padding:0 3px}.g30{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0}.c30{display:flex;flex-direction:column;align-items:center;min-width:54px;padding:6px 8px;border:1px solid var(--line);border-radius:10px;background:var(--panel);text-decoration:none;color:var(--ink)}.c30 b{font-size:18px;color:#d01f3c}.c30 small{font-size:11.5px;color:var(--mute)}.dd30{width:100%;text-align:center;font-variant-numeric:tabular-nums}.dd30 td:first-child,.dd30 th:first-child{text-align:left;white-space:nowrap}.t30w{overflow-x:auto}.t30{width:100%;font-variant-numeric:tabular-nums}.t30 td{vertical-align:top}.t30 td small{display:block;color:var(--mute);font-size:11.5px}.t30 .db{color:#d01f3c;font-weight:700;white-space:nowrap}.t30 .lo{font-size:13.5px;line-height:1.7;word-spacing:2px}.t30 .st{white-space:nowrap}.ltg{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin:8px 0 14px}.ltg>div{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px}.ltg h3{font-size:15px;margin:0 0 6px}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid #d01f3c;border-radius:12px;padding:12px 14px;line-height:1.6}.vb{display:inline-grid;place-items:center;width:44px;height:44px;border-radius:50%;background:radial-gradient(circle at 32% 28%,#ff8a9b,#d01f3c 55%,#8f1027);color:#fff;font-weight:700;font-size:18px;margin:3px;font-variant-numeric:tabular-nums}.vb.y{background:radial-gradient(circle at 32% 28%,#fff6c2,#f2c200 55%,#a07800);color:#1b1a20}
.mgrid{display:grid;grid-template-columns:repeat(12,minmax(0,1fr));gap:4px}.mgrid a,.mgrid span{display:block;text-align:center;padding:6px 0;border:1px solid var(--line);border-radius:8px;text-decoration:none;font-size:13px;color:var(--ink);background:var(--panel)}.mgrid span{color:var(--mute);opacity:.5}.mgrid a:hover{border-color:#d01f3c;color:var(--red)}
.yr{display:grid;grid-template-columns:64px minmax(0,1fr);gap:8px;align-items:center;margin:0 0 6px}.yr b{font-variant-numeric:tabular-nums}
@media(max-width:600px){.mgrid{grid-template-columns:repeat(6,minmax(0,1fr))}.yr{grid-template-columns:1fr}.vb{width:38px;height:38px;font-size:16px}}
.facts li{margin-bottom:4px}"""
_css = shell.STATIC_CSS + shell.MENU_CSS + EXTRA_CSS
_svg = shell.SPRITE.replace('<svg width="0" height="0" style="position:absolute" aria-hidden="true">', '<svg xmlns="http://www.w3.org/2000/svg">')
os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
def _wr(fn, data):
    fp = os.path.join(ROOT, "assets", fn)
    if not os.path.exists(fp) or open(fp).read() != data: open(fp, "w").write(data)
_wr("s.css", _css); _wr("i.svg", _svg); _wr("m.js", shell.MENU_JS)
AV = hashlib.md5((_css + _svg + shell.MENU_JS).encode()).hexdigest()[:8]
WROTE = [0, 0]


def page(path, title, desc, crumbs, h1, body, ld=None, fam=None):
    title, desc = seo_apply(path, title, desc, fam)
    url = BASE + path
    bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate([("XS Lab", "")] + crumbs)]}
    depth = path.count("/")
    up = "../" * depth
    ic = f"{up}assets/i.svg?v={AV}#"
    out = f"""<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com https://www.googletagmanager.com; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob: https://*.google-analytics.com https://*.googletagmanager.com; font-src 'self' data:; connect-src 'self' https://cloudflareinsights.com https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com; frame-src 'self'; manifest-src 'self'; worker-src 'self'; media-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'"><meta name="referrer" content="strict-origin-when-cross-origin"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{esc(title)} | XS Lab</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:locale" content="vi_VN"><meta property="og:site_name" content="XS Lab"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}icon-512.png">
<link rel="icon" type="image/png" href="{up}icon-192.png"><link rel="apple-touch-icon" href="{up}icon-180.png"><link rel="manifest" href="{up}manifest.webmanifest"><link rel="alternate" type="application/rss+xml" href="{up}rss.xml"><meta name="theme-color" content="#16151b">
{shell.THEME_HEAD}<link rel="stylesheet" href="{up}assets/s.css?v={AV}"><script type="speculationrules">{{"prerender":[{{"where":{{"and":[{{"href_matches":"/*"}},{{"not":{{"href_matches":"/admin*"}}}},{{"not":{{"selector_matches":"[download],[target=_blank]"}}}}]}},"eagerness":"moderate"}}]}}</script><script type="application/ld+json">{json.dumps(bc, ensure_ascii=False)}</script>{"".join(f'<script type="application/ld+json">{x}</script>' for x in (ld or []))}</head><body class="static">
<div class="app">{shell.side_html(up, path, ic)}<main class="main">{shell.mhead(up, ic)}{shell.menu_html(up, path)}{(shell.subnav_html(path.split('/')[0], up, path if path.count('/')==2 and path.split('/')[1] in ('so-ket-qua','thu-2','thu-3','thu-4','thu-5','thu-6','thu-7','chu-nhat') else '') if path.split('/')[0] in ('xsmb','xsmn','xsmt') else '')}
<nav class="bc" aria-label="Đường dẫn"><a href="{up}./">XS Lab</a>{''.join(f' › <a href="{up}{u}">{esc(n)}</a>' for n, u in crumbs[:-1])} › {esc(crumbs[-1][0])}</nav>
<h1>{esc(h1)}</h1>{body}
{shell.footer_html(up)}</main></div>{shell.tab_html(up, path, ic)}<script src="{up}assets/m.js?v={AV}" defer></script><script type="module" src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "d84c5ca70d434fb8b09440653ffd5b77"}}'></script>{shell.GA_HTML}</body></html>"""
    lg = f'<img src="{up}icon-192.png" width="38" height="38" alt="" style="border-radius:10px">'
    out = out.replace(shell.LOGO, lg).replace(shell.LOGO.replace("lg1", "mg1").replace("lg2", "mg2"), lg.replace('width="38" height="38"', 'width="32" height="32"'))
    d = os.path.join(ROOT, path)
    os.makedirs(d, exist_ok=True)
    fp = os.path.join(d, "index.html")
    if os.path.exists(fp) and open(fp).read() == out: WROTE[1] += 1; return
    open(fp, "w").write(out); WROTE[0] += 1


def tbl(head, rows): return '<table><tr>' + ''.join(f'<th>{h}</th>' for h in head) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rows) + '</table>'
def card(x): return f'<div class="card">{x}</div>'
def cells(vals): return ''.join(f'<span>{v[:-2]}<b>{v[-2:]}</b></span>' for v in vals)
def mb_table(r): return '<table>' + ''.join(f'<tr class="{g}"><td class="l">{lb}</td><td>{cells(r[g])}</td></tr>' for lb, g in MB_G) + '</table>'


def mn_table(recs):
    head = '<tr><th>Giải</th>' + ''.join(f'<th>{ST.get(r["station"], r["station"])}</th>' for r in recs) + '</tr>'
    return '<table class="mn">' + head + ''.join(f'<tr class="{g}"><td class="l">{lb}</td>' + ''.join(f'<td>{cells(r[g])}</td>' for r in recs) + '</tr>' for lb, g in MN_G) + '</table>'


def diemtin(lab, d, recs, G, lots_list, gaps):
    from collections import Counter
    allo = [k for lo in lots_list for k in lo]; c = Counter(allo)
    mx = max(c.values()) if c else 0
    top = [f"{k:02d}" for k, n in sorted(c.items()) if n == mx and n > 1][:4]
    kep = sorted({k for k in allo if k % 11 == 0})
    dbs = "; ".join((ST.get(r["station"], "") + " " if r.get("station") else "") + r["db"][0] for r in recs)
    g = sorted(gaps, reverse=True)[:1]
    parts = [f"giải Đặc biệt {dbs}", f"{len(set(allo))} lô khác nhau trên {len(allo)} giải"]
    if top: parts.append(f"lô về nhiều nháy nhất là {', '.join(top)} ({mx} nháy)")
    parts.append(f"{len(kep)} lô kép" + (f" ({', '.join(f'{k:02d}' for k in kep)})" if kep else ""))
    if g: parts.append(f"số về lại sau thời gian vắng lâu nhất là {g[0][1]:02d} ({g[0][0]} kỳ chưa về)")
    return f'<p class="lead"><b>Điểm tin {lab} {vn(d)}:</b> ' + "; ".join(parts) + ".</p>"
def lotos(r, G): return sorted(int(v[-2:]) for _, g in G for v in r[g])
def SL(k, t=None): return f'<a class="sl" href="/so/{k:02d}/">{t if t is not None else f"{k:02d}"}</a>'


def loto_table(lo):
    H = [[] for _ in range(10)]; T = [[] for _ in range(10)]
    for k in sorted(lo): H[k // 10].append(SL(k, k % 10)); T[k % 10].append(SL(k, k // 10))
    return '<table class="lt"><tr><th>Đầu</th><th>Đuôi</th><th>Đầu</th><th>Đuôi</th></tr>' + ''.join(f'<tr><td>{i}</td><td>{", ".join(H[i]) or "–"}</td><td class="r">{", ".join(T[i]) or "–"}</td><td class="k">{i}</td></tr>' for i in range(10)) + '</table>'


def loto_list(lo):
    H = [[] for _ in range(10)]
    for k in sorted(lo): H[k // 10].append(SL(k))
    return '<table class="lt"><tr><th>Đầu</th><th>Lô tô</th></tr>' + ''.join(f'<tr><td class="k">{i}</td><td>{", ".join(H[i]) or "–"}</td></tr>' for i in range(10)) + '</table>'


def sameday(d, cur):
    out = []
    for r, lab in (("xsmb", "XSMB"), ("xsmn", "XSMN"), ("xsmt", "XSMT")):
        if r != cur and os.path.isdir(os.path.join(ROOT, r, slug_d(d))):
            out.append(f'<a href="../../{r}/{slug_d(d)}/">{lab} {vn(d)}</a>')
    return f'<p class="note">Cùng ngày ở miền khác: {" · ".join(out)}</p>' if out else ''

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
MBS = [("db", 0, 1), ("g1", 1, 2), ("g2", 2, 4), ("g3", 4, 10), ("g4", 10, 14), ("g5", 14, 20), ("g6", 20, 23), ("g7", 23, 27)]
MNS = [("db", 0, 1), ("g1", 1, 2), ("g2", 2, 3), ("g3", 3, 5), ("g4", 5, 12), ("g5", 12, 13), ("g6", 13, 16), ("g7", 16, 17), ("g8", 17, 18)]
def fullrecs(reg):
    R = {}
    if reg == "xsmb":
        for l in open(os.path.join(ROOT, "xsmb_full.csv")).read().strip().split("\n")[1:]:
            d, v = l.split(","); v = v.split()
            if len(v) == 27: R[(d, "")] = dict({"date": d, "station": ""}, **{g: v[a:b] for g, a, b in MBS})
        for r in mb: R[(r["date"], "")] = dict(r, station="")
    else:
        for l in open(os.path.join(ROOT, reg + "_full.csv")).read().strip().split("\n")[1:]:
            d, st, v = l.split(","); v = v.split()
            if len(v) == 18: R[(d, st)] = dict({"date": d, "station": st}, **{g: v[a:b] for g, a, b in MNS})
        for r in json.load(open(os.path.join(ROOT, "recent_mn.json" if reg == "xsmn" else "recent_mt.json"))): R[(r["date"], r["station"])] = r
    return R

# ---------- XSMN, XSMT theo ngày ----------
for reg, fn in (("xsmn", "recent_mn.json"), ("xsmt", "recent_mt.json")):
    lab, name, tm = REG[reg]
    rec = json.load(open(os.path.join(ROOT, fn))); by = {}
    for r in rec: by.setdefault(r["date"], []).append(r)
    # ---------- trang từng đài ----------
    FR = fullrecs(reg)
    rows = list(csv.reader(open(os.path.join(ROOT, reg + ".csv"))))[1:]
    sts = sorted({r["station"] for r in rec})
    for st in sts:
        nm = ST.get(st, st); ab = AB.get(st, ''); hist = sorted([r for r in rows if r[1] == st], key=lambda r: r[0])
        mine = sorted([r for r in rec if r["station"] == st], key=lambda r: r["date"], reverse=True)
        days = sorted({wdi(r["date"]) for r in mine})
        last = {}; cnt = {k: 0 for k in range(100)}; N = len(hist); win = hist[-52:]
        for i, r in enumerate(hist):
            for j in range(0, 36, 2): last[int(r[2][j:j + 2])] = i
        for r in win:
            for j in range(0, 36, 2): cnt[int(r[2][j:j + 2])] += 1
        gan = sorted(range(100), key=lambda k: -(N - 1 - last.get(k, -1)))[:10]
        hot = sorted(range(100), key=lambda k: (-cnt[k], k))[:10]
        # --- trang từng đài theo ngày (12 tháng gần nhất) ---
        alt = f" (còn gọi {AB2[st]})" if st in AB2 else ""
        cutoff = (datetime.date.fromisoformat(max(rr[0] for rr in rows)) - datetime.timedelta(days=365)).isoformat()
        seen = {}; made = set()
        def _sdl(dd): return f"../{slug_d(dd)}/" if (dd >= cutoff and FR.get((dd, st))) else f"../../{slug_d(dd)}/"
        for i, hr in enumerate(hist):
            d = hr[0]; lo2 = [int(hr[2][j:j + 2]) for j in range(0, 36, 2)]
            fr = FR.get((d, st))
            if d >= cutoff and fr:
                gaps = [(i - 1 - seen[k], k) for k in set(lo2) if k in seen]
                after = dict(seen); after.update({k: i for k in lo2})
                gan_d = sorted(range(100), key=lambda k: (-(i - after.get(k, -1)), k))[:10]
                prevs = [FR.get((hist[j][0], st)) for j in range(i - 1, max(-1, i - 11), -1)]
                prevs = [x for x in prevs if x]
                others = sorted([k2 for k2 in FR if k2[0] == d and k2[1] != st], key=lambda k2: ST.get(k2[1], ""))
                w = wdi(d); pth = f"{reg}/{st}/{slug_d(d)}/"
                nav = []
                if i > 0: nav.append(f'<a class="cta" href="{_sdl(hist[i - 1][0])}">‹ {ab} {vn(hist[i - 1][0])}</a>')
                if i + 1 < len(hist): nav.append(f'<a class="cta" href="{_sdl(hist[i + 1][0])}">{ab} {vn(hist[i + 1][0])} ›</a>')
                body = (diemtin(ab, d, [fr], MN_G, [lotos(fr, MN_G)], gaps)
                    + f'<p>Kết quả xổ số {nm} ({ab}){alt} {WDL[w]} ngày {vn(d)}, quay lúc {tm} cùng các đài {lab}: giải Đặc biệt <b>{fr["db"][0]}</b>, giải Nhất {fr["g1"][0]}.</p>'
                    + f'<div class="card">{mn_table([fr])}</div>'
                    + f'<h2>Lô tô {nm} {vn(d)}</h2><div class="card">{loto_list(lotos(fr, MN_G))}</div>'
                    + (f'<h2>Giải Đặc biệt {nm} 10 kỳ trước</h2><div class="card"><table><tr><th>Ngày</th><th>Đặc biệt</th></tr>' + ''.join(f'<tr><td><a href="{_sdl(x["date"])}">{vn(x["date"])}</a></td><td><b>{x["db"][0]}</b></td></tr>' for x in prevs) + '</table></div>' if prevs else '')
                    + f'<h2>Lô gan {nm} tính đến {vn(d)}</h2><div class="g30">' + ''.join(f'<a class="c30" href="../../../so/{k:02d}/"><b>{k:02d}</b><small>{i - after.get(k, -1)} kỳ</small></a>' for k in gan_d) + '</div>'
                    + '<p class="note">Số liệu là thống kê các kỳ đã quay của đài, không phải dự đoán.</p>'
                    + (f'<p>Cùng ngày: ' + ' · '.join(f'<a href="../../{k2[1]}/{slug_d(d)}/">{AB.get(k2[1], "")} {ST.get(k2[1], "")}</a>' for k2 in others) + f' · <a href="../../{slug_d(d)}/">Cả {lab} {vn(d)}</a></p>' if others else '')
                    + f'<p>{"".join(nav)}<a class="cta" href="../">Xổ số {nm}</a><a class="cta" href="../../../do-ve/">Dò vé số</a></p>')
                page(pth, f"{ab} {vn(d)[:5]}, Xổ số {nm} {vn(d)} – Kết quả {ab} {WDL[w]}", f"{ab} {vn(d)}: kết quả xổ số {nm}{alt} {WDL[w]} ngày {vn(d)} đủ 18 giải, lô tô, giải Đặc biệt 10 kỳ trước và lô gan đài {nm}. Không quảng cáo.", [(lab, reg + "/"), (f"Xổ số {nm}", f"{reg}/{st}/"), (f"{ab} {vn(d)}", pth)], f"{ab} {vn(d)} – Xổ số {nm} {WDL[w]}", body, fam=("ngay_dai", {"dai": nm, "dai_ma": ab, "mien_ma": lab, "ngay": vn(d), "ngay_ngan": vn(d)[:5], "thu": WDL[w]}))
                STATION_SM[reg].append((BASE + pth, d)); made.add(d)
            for k in lo2: seen[k] = i
        res = ''.join(f'<h2>{ab} {vn(r["date"])} – Xổ số {nm} {WDL[wdi(r["date"])]}</h2><div class="card">{mn_table([r])}</div><p class="note">' + (f'<a href="{slug_d(r["date"])}/">{ab} {vn(r["date"])}: lô tô, lô gan, Đặc biệt 10 kỳ</a> · ' if r["date"] in made else '') + f'<a href="../{slug_d(r["date"])}/">Xem cả các đài {lab} ngày {vn(r["date"])}</a></p>' for r in mine[:6])
        body = f'''<p class="favrow"><button type="button" class="favst" data-reg="{reg[2:]}" data-st="{st}" data-nm="{nm}">☆ Thêm {nm} vào đài mặc định</button></p><p>Xổ số {nm} ({ab}) thuộc {lab}, quay {", ".join(WDL[x] for x in days)} hằng tuần lúc khoảng {tm}. Mỗi kỳ có 18 giải, vé 6 chữ số. Dữ liệu XS Lab có {fm(N)} kỳ của đài {nm} (từ {vn(hist[0][0])}).</p>{res}
<h2>Lô gan {nm}</h2><p>10 lô lâu chưa về nhất tính đến kỳ {vn(hist[-1][0])}:</p><div class="card"><table><tr><th>Lô</th><th>Số kỳ chưa về</th></tr>{''.join(f'<tr><td><b>{SL(k)}</b></td><td>{N - 1 - last.get(k, -1)}</td></tr>' for k in gan)}</table></div>
<h2>Lô về nhiều nhất 52 kỳ gần nhất</h2><div class="card"><table><tr><th>Lô</th><th>Số lần</th></tr>{''.join(f'<tr><td><b>{SL(k)}</b></td><td>{cnt[k]}</td></tr>' for k in hot)}</table></div>
<p class="note">Theo xác suất, mỗi lô có khoảng 16,55% khả năng xuất hiện trong một kỳ của đài (18 giải). Các bảng trên là thống kê dữ liệu đã quay, không phải dự đoán.</p>
<p><a class="cta" href="../">{lab} hôm nay</a><a class="cta" href="../../thong-ke/">Thống kê lô tô</a><a class="cta" href="../../do-ve/">Dò vé {nm}</a></p>'''
        p = f"{reg}/{st}/"
        page(p, f"Xổ số {nm} ({ab}) – Kết quả {ab} hôm nay, lô gan {nm}", f"{ab}{alt}: kết quả xổ số {nm} ({lab}) các kỳ gần nhất, đủ 18 giải, lịch quay {', '.join(WDL[x] for x in days)}, lô gan và lô về nhiều của đài {nm}. Không quảng cáo.", [(lab, reg + "/"), (f"Xổ số {nm}", p)], f"Xổ số {nm} ({ab}) – kết quả {lab} đài {nm}", body)

    # ---------- theo thứ ----------
    for w in range(7):
        ds = sorted([d for d in by if wdi(d) == w], reverse=True)
        if not ds: continue
        body = f'<p>Kết quả {lab} {WDL[w]} các tuần gần nhất. Các đài quay {WDL[w]}: {", ".join(ST.get(s, s) for s in sorted({r["station"] for r in by[ds[0]]}))}.</p>' + ''.join(f'<h2>{lab} {WDL[w]} {vn(d)}</h2><div class="card">{mn_table(sorted(by[d], key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], ""))))}</div><p class="note"><a href="../{slug_d(d)}/">Lô tô và thống kê {lab} {vn(d)}</a></p>' + (('<div class="ltg">' + ''.join(f'<div><h3>Lô tô {ST.get(r["station"], "")} {WD[w]}, {vn(d)}</h3>{loto_list(lotos(r, MN_G))}</div>' for r in sorted(by[d], key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], "")))) + '</div>') if d == ds[0] else '') + sameday(d, reg) for d in ds[:6])
        p = f"{reg}/{WDS[w]}/"
        page(p, f"{lab} {WD[w]} – Kết quả xổ số {name} {WDL[w]} hằng tuần", f"{lab} {WD[w]}: kết quả xổ số {name} {WDL[w]} các tuần gần nhất, các đài quay {WDL[w]}, đủ 18 giải. Không quảng cáo.", [(lab, reg + "/"), (f"{lab} {WD[w]}", p)], f"{lab} {WD[w]} – kết quả xổ số {name} {WDL[w]}", body)

for w in range(7):
    rs = sorted([r for r in mb if wdi(r["date"]) == w], key=lambda r: r["date"], reverse=True)
    if not rs: continue
    body = f'<p>Kết quả XSMB {WDL[w]} các tuần gần nhất, quay lúc 18:15.</p>' + ''.join(f'<h2>XSMB {WDL[w]} {vn(r["date"])}</h2><div class="card">{mb_table(r)}</div><p class="note"><a href="../{slug_d(r["date"])}/">Lô tô và thống kê XSMB {vn(r["date"])}</a></p>' + (f'<h3>Lô tô XSMB {WD[w]}, {vn(r["date"])}</h3><div class="card">{loto_list(lotos(r, MB_G))}</div>' if r is rs[0] else '') + sameday(r["date"], "xsmb") for r in rs[:6])
    p = f"xsmb/{WDS[w]}/"
    page(p, f"XSMB {WD[w]} – Kết quả xổ số miền Bắc {WDL[w]} hằng tuần", f"XSMB {WD[w]}: kết quả xổ số miền Bắc {WDL[w]} các tuần gần nhất, đủ 27 giải. Không quảng cáo.", [("XSMB", "xsmb/"), (f"XSMB {WD[w]}", p)], f"XSMB {WD[w]} – kết quả xổ số miền Bắc {WDL[w]}", body)

# ---------- KHO LƯU TRỮ: trang kết quả theo ngày cho toàn bộ lịch sử, trang theo tháng, sổ kết quả ----------
# Trang ngày cũ chỉ được ghi lại khi nội dung đổi (page() so sánh trước khi ghi), nên kho mã không phình mỗi ngày.
MONTHS = {}
SITEMAP_ARCH = {}
for reg in REG:
    lab, name, tm = REG[reg]
    R = fullrecs(reg); G = MB_G if reg == "xsmb" else MN_G
    byd = {}
    for (d, st), r in R.items(): byd.setdefault(d, []).append(r)
    ds = sorted(byd)
    # lịch sử 2 số cuối để tính "về lại sau bao nhiêu kỳ" (chỉ dùng dữ liệu trước ngày đó, nên nội dung trang cũ không đổi)
    hist = [l.split(",") for l in open(os.path.join(ROOT, reg + ".csv")).read().strip().split("\n")[1:]]
    pv = {}; idx = {}; gapinfo = {}
    if reg == "xsmb":
        for i, (d, t) in enumerate(hist):
            ks = [int(t[j:j + 2]) for j in range(0, len(t), 2)]
            gapinfo[(d, "")] = sorted(((i - 1 - pv[k], k) for k in set(ks) if k in pv), reverse=True)[:3]
            for k in ks: pv[k] = i
    else:
        cnt = {}
        for d, st, t in hist:
            ks = [int(t[j:j + 2]) for j in range(0, len(t), 2)]; n = cnt.get(st, 0); P = pv.setdefault(st, {})
            gapinfo[(d, st)] = sorted(((n - 1 - P[k], k) for k in set(ks) if k in P), reverse=True)[:2]
            for k in ks: P[k] = n
            cnt[st] = n + 1
    dbl = {}; dbprev = {}
    for d in ds:
        for r in byd[d]:
            t = r["db"][0][-2:]; key = (r["station"], t)
            dbprev[(d, r["station"])] = dbl.get(key); dbl[key] = d
    SITEMAP_ARCH[reg] = []
    for i, d in enumerate(ds):
        rs = sorted(byd[d], key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], "")))
        prv = ds[i - 1] if i else None; nxt = ds[i + 1] if i + 1 < len(ds) else None; w = wdi(d); ym = d[:7]
        MONTHS.setdefault(reg, {}).setdefault(ym, []).append(d)
        mlink = f'../thang-{d[5:7]}-{d[:4]}/'
        def gtxt(key, unit):
            g = gapinfo.get(key) or []
            return ", ".join(f"<b>{SL(k)}</b> ({n} {unit})" for n, k in g) if g else "không có số nào"
        def dbtxt(r):
            pd = dbprev.get((d, r["station"]))
            return f"2 số cuối giải Đặc biệt <b>{r['db'][0][-2:]}</b> lần trước làm 2 số cuối giải Đặc biệt{' của đài' if r['station'] else ''} ngày {vn(pd)}" if pd else f"2 số cuối giải Đặc biệt <b>{r['db'][0][-2:]}</b> lần đầu xuất hiện ở giải Đặc biệt{' của đài' if r['station'] else ''} trong dữ liệu"
        nav = f'<div class="pn">{f"<a href='../{slug_d(prv)}/'>‹ {lab} {vn(prv)}</a>" if prv else "<span></span>"}{f"<a href='../{slug_d(nxt)}/'>{lab} {vn(nxt)} ›</a>" if nxt else "<span></span>"}</div>'
        links = f'<p><a class="cta" href="../../thong-ke/30-ky-{reg}/">Thống kê {lab} 30 kỳ</a><a class="cta" href="{mlink}">{lab} tháng {d[5:7]}/{d[:4]}</a><a class="cta" href="../{WDS[w]}/">{lab} {WD[w]}</a><a class="cta" href="../so-ket-qua/">Sổ kết quả {lab}</a><a class="cta" href="../">{lab} hôm nay</a></p>'
        if reg == "xsmb":
            r = rs[0]; lo = lotos(r, MB_G)
            body = (diemtin(lab, d, [r], MB_G, [lo], gapinfo.get((d, "")) or []) + f'<p>Kết quả xổ số miền Bắc (XSMB) {WDL[w]} ngày {vn(d)}, quay lúc 18:15: giải Đặc biệt <b>{r["db"][0]}</b>, giải Nhất {r["g1"][0]}. Bảng đủ 27 giải và lô tô đầu – đuôi bên dưới.</p>'
                    f'<div class="card">{mb_table(r)}</div><h2>Lô tô XSMB {vn(d)}</h2><div class="card">{loto_table(lo)}</div>'
                    f'<h2>Thống kê kỳ {vn(d)}</h2>{facts(lo)[:-5]}<li>Về lại sau thời gian dài nhất (so với các kỳ trước): {gtxt((d, ""), "kỳ")}.</li><li>{dbtxt(r)}.</li></ul>{nav}{links}')
            desc = f"XSMB {vn(d)}: kết quả xổ số miền Bắc {WDL[w]} ngày {vn(d)}, giải Đặc biệt {r['db'][0]}, đủ 27 giải, lô tô đầu đuôi và thống kê kỳ quay."
        else:
            names = ", ".join(ST.get(r["station"], r["station"]) for r in rs)
            body = (diemtin(lab, d, rs, MN_G, [lotos(x, MN_G) for x in rs], [gg for x in rs for gg in (gapinfo.get((d, x["station"])) or [])]) + f'<p>Kết quả xổ số {name} ({lab}) {WDL[w]} ngày {vn(d)}, quay lúc {tm}, gồm {len(rs)} đài: {names}. Giải Đặc biệt: {"; ".join(ST.get(r["station"], r["station"]) + " <b>" + r["db"][0] + "</b>" for r in rs)}.</p>'
                    f'<div class="card">{mn_table(rs)}</div>' +
                    ''.join(f'<h2>Lô tô {ST.get(r["station"], r["station"])} {vn(d)} ({AB.get(r["station"], "")})</h2>' + (f'<p class="note"><a href="../{r["station"]}/{slug_d(d)}/">Trang riêng {AB.get(r["station"], "")} {vn(d)}: lô gan, Đặc biệt 10 kỳ của đài</a></p>' if os.path.isdir(os.path.join(ROOT, reg, r["station"], slug_d(d))) else '') + f'<div class="card">{loto_table(lotos(r, MN_G))}</div><ul class="facts"><li>Về lại sau thời gian dài nhất (so với các kỳ trước của đài): {gtxt((d, r["station"]), "kỳ")}.</li><li>{dbtxt(r)}.</li><li>Xem các kỳ khác: <a href="../{r["station"]}/">Xổ số {ST.get(r["station"], r["station"])}</a></li></ul>' for r in rs) + nav + links)
            desc = f"{lab} {vn(d)}: kết quả xổ số {name} {WDL[w]} ngày {vn(d)} các đài {names} ({', '.join(AB.get(r['station'], '') for r in rs)}), đủ 18 giải mỗi đài, lô tô đầu đuôi và thống kê kỳ quay."
        p = f"{reg}/{slug_d(d)}/"
        page(p, f"{lab} {vn(d)} – Kết quả xổ số {name} {WDL[w]} ngày {vn(d)}", desc, [(lab, reg + "/"), (f"Sổ kết quả", reg + "/so-ket-qua/"), (f"{lab} {vn(d)}", p)], f"{lab} {vn(d)} – Kết quả xổ số {name} {WDL[w]} {vn(d)}", body, fam=("ngay_mien", {"mien_ma": lab, "mien": name, "ngay": vn(d), "ngay_ngan": vn(d)[:5], "thu": WDL[w]}))
        SITEMAP_ARCH[reg].append((BASE + p, d))
    # trang theo tháng
    yms = sorted(MONTHS[reg])
    for j, ym in enumerate(yms):
        y, m = ym[:4], ym[5:7]; dd = MONTHS[reg][ym]
        if reg == "xsmb":
            rows = [(f'<a href="../{slug_d(d)}/">{vn(d)}</a>', WD[wdi(d)], f'<b>{byd[d][0]["db"][0]}</b>', byd[d][0]["g1"][0]) for d in dd[::-1]]
            t = tbl(["Ngày", "Thứ", "Giải Đặc biệt", "Giải Nhất"], rows)
            tails = Counter(int(byd[d][0]["db"][0][-2:]) for d in dd)
        else:
            rows = [(f'<a href="../{slug_d(d)}/">{vn(d)}</a>', WD[wdi(d)], " · ".join(f'{ST.get(r["station"], r["station"])} <b>{r["db"][0]}</b>' for r in sorted(byd[d], key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], ""))))) for d in dd[::-1]]
            t = tbl(["Ngày", "Thứ", "Giải Đặc biệt các đài"], rows)
            tails = Counter(int(r["db"][0][-2:]) for d in dd for r in byd[d])
        rep = [f"{k:02d} ({n} lần)" for k, n in tails.most_common() if n > 1][:5]
        mp = f'<div class="pn">{f"<a href='../thang-{yms[j-1][5:7]}-{yms[j-1][:4]}/'>‹ Tháng {yms[j-1][5:7]}/{yms[j-1][:4]}</a>" if j else "<span></span>"}{f"<a href='../thang-{yms[j+1][5:7]}-{yms[j+1][:4]}/'>Tháng {yms[j+1][5:7]}/{yms[j+1][:4]} ›</a>" if j + 1 < len(yms) else "<span></span>"}</div>'
        body = (f'<p>Sổ kết quả {lab} tháng {m}/{y}: {len(dd)} ngày quay, từ {vn(dd[0])} đến {vn(dd[-1])}. Bấm vào ngày để xem đủ các giải và lô tô.</p>' + card(t) +
                f'<p class="note">2 số cuối giải Đặc biệt về nhiều lần trong tháng: {", ".join(rep) or "không có số nào về quá 1 lần"}.</p>' + mp +
                f'<p><a class="cta" href="../so-ket-qua/">Sổ kết quả {lab} các năm</a><a class="cta" href="../">{lab} hôm nay</a></p>')
        p = f"{reg}/thang-{m}-{y}/"
        page(p, f"{lab} tháng {m}/{y} – Sổ kết quả xổ số {name} tháng {m} năm {y}", f"Sổ kết quả {lab} tháng {m}/{y}: giải Đặc biệt{' và giải Nhất' if reg == 'xsmb' else ' các đài'} từng ngày, {len(dd)} kỳ quay, liên kết tới kết quả đủ giải.", [(lab, reg + "/"), ("Sổ kết quả", reg + "/so-ket-qua/"), (f"Tháng {m}/{y}", p)], f"Sổ kết quả {lab} tháng {m}/{y}", body)
        SITEMAP_ARCH[reg].append((BASE + p, dd[-1]))
    # sổ kết quả: lưới năm × tháng, 30 ngày gần nhất, theo thứ, theo đài
    years = sorted({ym[:4] for ym in yms}, reverse=True)
    grid = ''.join(f'<div class="yr"><b>{y}</b><div class="mgrid">' + ''.join((f'<a href="../thang-{m:02d}-{y}/">T{m}</a>' if f"{y}-{m:02d}" in MONTHS[reg] else f'<span>T{m}</span>') for m in range(1, 13)) + '</div></div>' for y in years)
    sts = sorted([x for x in os.listdir(os.path.join(ROOT, reg)) if x in ST]) if reg != "xsmb" else []
    body = (f'<p>Lưu trữ kết quả {lab} đủ giải từ {vn(ds[0])} đến {vn(ds[-1])}: {fm(len(ds))} ngày quay. Chọn tháng để xem giải Đặc biệt từng ngày, hoặc chọn ngày để xem đủ các giải.</p>'
            f'<h2>Theo tháng</h2>{card(grid)}<h2>30 ngày gần nhất</h2><ul class="ls">' + ''.join(f'<li><a href="../{slug_d(d)}/">{lab} {vn(d)}</a></li>' for d in ds[::-1][:30]) + '</ul>'
            '<h2>Theo thứ</h2><ul class="ls">' + ''.join(f'<li><a href="../{WDS[w]}/">{lab} {WD[w]}</a></li>' for w in range(7) if os.path.isdir(os.path.join(ROOT, reg, WDS[w]))) + '</ul>')
    if sts: body += '<h2>Theo đài</h2><ul class="ls">' + ''.join(f'<li><a href="../{s}/">Xổ số {ST[s]}</a></li>' for s in sorted(sts, key=lambda s: ST[s])) + '</ul>'
    p = f"{reg}/so-ket-qua/"
    page(p, f"Sổ kết quả {lab} – lưu trữ kết quả xổ số {name} từ {ds[0][:4]}", f"Sổ kết quả {lab}: lưu trữ kết quả xổ số {name} đủ giải từ {vn(ds[0])}, theo năm, tháng, ngày, theo thứ{', theo đài' if sts else ''}. Không quảng cáo.", [(lab, reg + "/"), (f"Sổ kết quả {lab}", p)], f"Sổ kết quả {lab} – lưu trữ từ {ds[0][:4]}", body)
    print(reg, "ngày:", len(ds), "tháng:", len(yms))

# ---------- trang thống kê (dữ liệu đã quay, không dự đoán) ----------
from collections import Counter
def grid100(c, title):
    mx = max(c.values()) or 1
    return f'<table class="g100"><caption class="note" style="caption-side:top;text-align:left;padding:4px 0">{title}</caption>' + ''.join('<tr>' + ''.join(f'<td style="background:rgba(200,16,46,{0.08 + 0.5 * c.get(r * 10 + k, 0) / mx:.2f})"><b>{r * 10 + k:02d}</b><br><small>{c.get(r * 10 + k, 0)}</small></td>' for k in range(10)) + '</tr>' for r in range(10)) + '</table>'
STATP = []
def spage(slug, title, desc, h1, intro, body):
    p = f"thong-ke/{slug}/"; STATP.append((slug, h1))
    page(p, title, desc, [("Thống kê", "thong-ke/"), (h1, p)], h1, f'<p>{intro}</p>{body}<p class="note">Các bảng trên là thống kê kết quả đã quay, cập nhật mỗi ngày; không phải dự đoán. Mỗi kỳ quay độc lập.</p><p><a class="cta" href="../">Thống kê lô tô</a><a class="cta" href="../bang-thong-ke/">Tất cả bảng thống kê</a><a class="cta" href="../../thong-ke-dan/">Tra cứu nhóm, 3 càng</a></p>')

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
      f"Lô gan là lô (2 số cuối của giải) đã nhiều kỳ liên tiếp chưa xuất hiện. Bảng tính đến kỳ {vn(lastd)} trên {fm(N)} kỳ XSMB từ {vn(two[0][0])}.",
      card(tbl(["Lô", "Số kỳ chưa về", "Lần về gần nhất", "Kỷ lục gan"], [(f"<b>{SL(k)}</b>", N - 1 - prev[k], vn(two[prev[k]][0]), rec[k]) for k in gan[:30]])))
c30 = Counter(k for ks in lo[-30:] for k in ks); c90 = Counter(k for ks in lo[-90:] for k in ks)
spage("tan-suat-lo-to-xsmb", "Tần suất lô tô XSMB 30, 90 ngày – bảng 00–99", f"Tần suất lô tô XSMB 00–99 trong 30 và 90 kỳ gần nhất đến {vn(lastd)}. Không quảng cáo.", "Tần suất lô tô XSMB",
      f"Số lần mỗi lô từ 00 đến 99 xuất hiện. Mỗi kỳ XSMB có 27 lô, nên trong 30 kỳ trung bình mỗi lô về {dec(30 * 27 / 100,1)} lần.",
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
      card(tbl(["Tuần từ"] + WD, rows[::-1]).replace("<table>", "<table class=\"wk\">", 1)) + "<h2>2 số cuối giải Đặc biệt lâu chưa về</h2>" + card(tbl(["Số", "Số kỳ chưa về", "Lần gần nhất"], [(f"<b>{SL(k)}</b>", N - 1 - dbg[k], vn(db[dbg[k]][0])) for k in dgan])))
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
    body += f"<h2>{label} giải Đặc biệt về nhiều lần nhất ({fm(M)} kỳ)</h2><p class='note'>Theo xác suất, mỗi số {label} trung bình về {dec(M / 10 ** L,2)} lần ở giải Đặc biệt trong {fm(M)} kỳ.</p>" + card(tbl([label, "Số lần", "Lần gần nhất"], [(f"<b>{t}</b>", n, vn(tails[lastseen[t]][0])) for t, n in top]))
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
          "<h2>Giải tám 14 ngày gần nhất</h2>" + recent_tbl(17) + card(grid100(g8c, f"Tần suất giải tám, 90 ngày gần nhất (tất cả các đài)")) + "<h2>Số lâu chưa về ở giải tám</h2>" + card(tbl(["Số", "Số ngày chưa về", "Lần gần nhất"], [(f"<b>{SL(k)}</b>", len(ds) - 1 - g8last[k], vn(ds[g8last[k]])) for k in g8g if k in g8last])))
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
          "<h2>Giải đặc biệt 14 ngày gần nhất</h2>" + recent_tbl(0) + card(grid100(dbc, "2 số cuối giải Đặc biệt, 180 ngày gần nhất")) + "<h2>2 số cuối giải đặc biệt lâu chưa về</h2>" + card(tbl(["Số", "Số ngày chưa về", "Lần gần nhất"], [(f"<b>{SL(k)}</b>", len(ds) - 1 - dlast[k], vn(ds[dlast[k]])) for k in dg if k in dlast])))
    d365 = set(ds[-365:]); c3 = Counter(v[0][-3:] for d, s, v in F if d in d365); h3 = Counter(v[0][-3] for d, s, v in F if d in d365); M3 = sum(c3.values())
    spage(f"3-cang-{reg}", f"Thống kê 3 càng {lab} – 3 càng giải đặc biệt", f"3 càng giải đặc biệt {lab} 14 ngày gần nhất theo đài, 3 càng về nhiều nhất và đầu 3 càng trong 365 ngày, đến {vn(ld)}.", f"Thống kê 3 càng {lab}",
          f"3 càng là 3 chữ số cuối của giải Đặc biệt. Trong 365 ngày gần nhất có {fm(M3)} giải Đặc biệt {lab}; mỗi số 3 càng trung bình về {dec(M3 / 1000,2)} lần.",
          "<h2>3 càng 14 ngày gần nhất</h2>" + recent_tbl(0, 3) + "<h2>3 càng về nhiều nhất (365 ngày)</h2>" + card(tbl(["3 càng", "Số lần"], [(f"<b>{t}</b>", n) for t, n in c3.most_common(20)])) + "<h2>Đầu 3 càng (365 ngày)</h2>" + card('<table class="sm">' + tbl(["Chữ số hàng trăm"] + [str(d) for d in range(10)], [["Số lần"] + [h3[str(d)] for d in range(10)]])[7:]))

# ---------- lô kép, số đảo, số gánh, tổng và chẵn lẻ giải đặc biệt (XSMB) ----------
def lastidx(pred):
    li = -1
    for i, ks in enumerate(lo):
        if pred(ks): li = i
    return li
def maxgap(pred):
    m = 0; pv = -1
    for i, ks in enumerate(lo):
        if pred(ks): m = max(m, i - pv - 1); pv = i
    return m
KEP = [11 * d for d in range(10)]; KL = [10 * a + (a + 5) % 10 for a in range(10)]
def kep_rows(L):
    out = []
    for k in L:
        li = lastidx(lambda ks, k=k: k in ks)
        out.append((f"<b>{SL(k)}</b>", c30[k], c90[k], N - 1 - li, vn(two[li][0]), rec[k]))
    return out
kday = [i for i in range(N - 30, N) if any(k in KEP for k in lo[i])]
spage("lo-kep-xsmb", "Thống kê lô kép XSMB – kép bằng, kép lệch", f"Thống kê lô kép XSMB đến {vn(lastd)}: số lần về 30, 90 kỳ, số kỳ chưa về và kỷ lục gan của từng lô kép bằng, kép lệch. Không quảng cáo.", "Thống kê lô kép XSMB",
      f"Lô kép bằng là lô có hai chữ số giống nhau (00, 11, …, 99); kép lệch là cặp chữ số cách nhau 5 (05, 50, 16, 61, …). Trong 30 kỳ gần nhất có {len(kday)}/30 kỳ XSMB về ít nhất một lô kép bằng; theo xác suất, khoảng 93% số kỳ có ít nhất một lô kép bằng.",
      "<h2>Lô kép bằng</h2>" + card(tbl(["Lô", "30 kỳ", "90 kỳ", "Số kỳ chưa về", "Lần về gần nhất", "Kỷ lục gan"], kep_rows(KEP))) +
      "<h2>Lô kép lệch</h2>" + card(tbl(["Lô", "30 kỳ", "90 kỳ", "Số kỳ chưa về", "Lần về gần nhất", "Kỷ lục gan"], kep_rows(KL))) +
      "<h2>Lô kép 14 kỳ gần nhất</h2>" + card(tbl(["Ngày", "Lô kép bằng đã về"], [(vn(two[i][0]), ", ".join(f"{k:02d}" + (f" ({lo[i].count(k)} nháy)" if lo[i].count(k) > 1 else "") for k in sorted(set(lo[i])) if k in KEP) or "–") for i in range(N - 1, N - 15, -1)])) +
      "<p class='note'>Mỗi lô trung bình về 8,1 lần trong 30 kỳ và 24,3 lần trong 90 kỳ (27 lô mỗi kỳ trên 100 số).</p>")
PAIRS = [(a, b) for a in range(10) for b in range(a + 1, 10)]
def drow(a, b):
    x, y = 10 * a + b, 10 * b + a
    both = lambda ks: x in ks and y in ks
    li = lastidx(both); n90 = sum(1 for ks in lo[-90:] if both(ks)); n365 = sum(1 for ks in lo[-365:] if both(ks))
    return (f"<b>{x:02d} – {y:02d}</b>", n90, n365, (N - 1 - li) if li >= 0 else "–", vn(two[li][0]) if li >= 0 else "–", maxgap(both))
DR = [drow(a, b) for a, b in PAIRS]
today_d = [f"{10 * a + b:02d} – {10 * b + a:02d}" for a, b in PAIRS if 10 * a + b in lo[-1] and 10 * b + a in lo[-1]]
spage("so-dao-xsmb", "Thống kê số đảo XSMB – lô đảo về cùng kỳ", f"Thống kê 45 cặp số đảo XSMB (12 – 21, 36 – 63…) đến {vn(lastd)}: số kỳ cùng về trong 90, 365 kỳ, số kỳ chưa cùng về và kỷ lục. Không quảng cáo.", "Thống kê số đảo XSMB",
      f"Số đảo là hai lô có chữ số đổi chỗ cho nhau, ví dụ 12 và 21. Bảng dưới đếm số kỳ XSMB mà cả hai lô của một cặp cùng xuất hiện. Kỳ {vn(lastd)}: " + (", ".join(today_d) if today_d else "không có cặp số đảo nào cùng về") + ". Theo xác suất, mỗi cặp cùng về trong khoảng 5–6% số kỳ, tức 5 lần trên 90 kỳ.",
      card(tbl(["Cặp số đảo", "Cùng về (90 kỳ)", "Cùng về (365 kỳ)", "Số kỳ chưa cùng về", "Lần gần nhất", "Kỷ lục chưa cùng về"], DR)) +
      "<h2>Các cặp lâu chưa cùng về nhất</h2>" + card(tbl(["Cặp số đảo", "Số kỳ chưa cùng về", "Lần gần nhất"], [(r[0], r[3], r[4]) for r in sorted(DR, key=lambda r: -(r[3] if isinstance(r[3], int) else 10 ** 6))[:10]])))
tails3 = [(d, v[0][-3:]) for d, v in fullmb if len(v[0]) >= 3]
isg = lambda t: t[0] == t[2]
gi = [i for i, (_, t) in enumerate(tails3) if isg(t)]
M3 = len(tails3); g365 = sum(1 for _, t in tails3[-365:] if isg(t)); gg = M3 - 1 - gi[-1]
gmax = max(b - a - 1 for a, b in zip([-1] + gi, gi))
gall30 = Counter(x[-3:] for _, v in fullmb[-30:] for x in v if len(x) >= 3 and isg(x[-3:]))
n3 = sum(1 for _, v in fullmb[-30:] for x in v if len(x) >= 3)
spage("so-ganh-xsmb", "Thống kê số gánh XSMB – 3 càng gánh giải đặc biệt", f"Thống kê số gánh XSMB đến {vn(lastd)}: giải đặc biệt có 3 số cuối dạng gánh (121, 353…), tần suất, số kỳ chưa về và số gánh ở mọi giải. Không quảng cáo.", "Thống kê số gánh XSMB",
      f"Số gánh là số 3 chữ số có chữ số đầu và cuối giống nhau (dạng ABA, ví dụ 121, 505, 989). Có 100 số gánh trong 1.000 số từ 000 đến 999, nên theo xác suất khoảng 10% kỳ có 3 số cuối giải Đặc biệt là số gánh.",
      card(tbl(["Chỉ số", "Giá trị"], [("Giải Đặc biệt gánh trong 365 kỳ gần nhất", f"{g365} kỳ ({dec(g365 / 3.65,1)}%)"), ("Số kỳ chưa có giải Đặc biệt gánh", gg), ("Lần gần nhất", f"{vn(tails3[gi[-1]][0])} – {fmap[tails3[gi[-1]][0]][0]}"), ("Kỷ lục số kỳ liên tiếp không có", gmax), ("Dữ liệu", f"{fm(M3)} kỳ từ {vn(tails3[0][0])}")])) +
      "<h2>20 lần giải Đặc biệt gánh gần nhất</h2>" + card(tbl(["Ngày", "Giải Đặc biệt", "Số gánh"], [(vn(tails3[i][0]), fmap[tails3[i][0]][0], f"<b>{tails3[i][1]}</b>") for i in gi[::-1][:20]])) +
      f"<h2>Số gánh ở mọi giải, 30 kỳ gần nhất</h2><p class='note'>Tính 3 chữ số cuối của {fm(n3)} giải có từ 3 chữ số trở lên; có {sum(gall30.values())} lần là số gánh (theo xác suất khoảng {n3 // 10}).</p>" + card(tbl(["Số gánh", "Số lần"], [(f"<b>{t}</b>", n) for t, n in gall30.most_common(20)])))
dbt2 = [(d, v[0][-2:]) for d, v in fullmb]
tong = lambda t: (int(t[0]) + int(t[1])) % 10
tc = Counter(tong(t) for _, t in dbt2[-100:]); tl = {}
for i, (_, t) in enumerate(dbt2): tl[tong(t)] = i
cl = lambda t: ("Chẵn" if int(t[0]) % 2 == 0 else "Lẻ") + " – " + ("chẵn" if int(t[1]) % 2 == 0 else "lẻ")
tn = lambda t: ("To" if int(t[0]) >= 5 else "Nhỏ") + " – " + ("to" if int(t[1]) >= 5 else "nhỏ")
clc = Counter(cl(t) for _, t in dbt2[-100:]); tnc = Counter(tn(t) for _, t in dbt2[-100:])
spage("tong-chan-le-dac-biet-xsmb", "Thống kê tổng, chẵn lẻ, to nhỏ giải đặc biệt XSMB", f"Thống kê tổng 2 số cuối, chẵn lẻ và to nhỏ của giải đặc biệt XSMB 100 kỳ gần nhất, số kỳ chưa về của từng tổng, đến {vn(lastd)}. Không quảng cáo.", "Tổng, chẵn lẻ, to nhỏ giải đặc biệt XSMB",
      "Tổng là chữ số hàng đơn vị của tổng hai số cuối giải Đặc biệt (ví dụ 78 có tổng 7 + 8 = 15, tức tổng 5). Chẵn lẻ, to nhỏ xét lần lượt chữ số hàng chục và hàng đơn vị; to là 5–9, nhỏ là 0–4. Mỗi tổng, mỗi nhóm chẵn lẻ hoặc to nhỏ đều có xác suất như nhau.",
      "<h2>Tổng 2 số cuối giải Đặc biệt</h2>" + card(tbl(["Tổng", "Số lần (100 kỳ)", "Số kỳ chưa về", "Lần gần nhất"], [(f"<b>{k}</b>", tc[k], len(dbt2) - 1 - tl[k], vn(dbt2[tl[k]][0])) for k in range(10)])) +
      "<h2>Chẵn lẻ và to nhỏ (100 kỳ)</h2>" + card(tbl(["Nhóm", "Số lần", "Nhóm", "Số lần"], [(a, clc[a], b, tnc[b]) for a, b in zip(["Chẵn – chẵn", "Chẵn – lẻ", "Lẻ – chẵn", "Lẻ – lẻ"], ["To – to", "To – nhỏ", "Nhỏ – to", "Nhỏ – nhỏ"])])) +
      "<h2>30 kỳ gần nhất</h2>" + card(tbl(["Ngày", "Giải Đặc biệt", "Tổng", "Chẵn lẻ", "To nhỏ"], [(vn(d), fmap[d][0], tong(t), cl(t), tn(t)) for d, t in dbt2[-30:][::-1]])) +
      "<p class='note'>Theo xác suất, trong 100 kỳ mỗi tổng trung bình về 10 lần, mỗi nhóm chẵn lẻ hoặc to nhỏ khoảng 25 lần.</p>")

hub = "<p>Các bảng thống kê kết quả XSMB, XSMN, XSMT được tạo lại mỗi ngày từ dữ liệu đã quay.</p>" + "".join(f"<h2>{REG[r][0]}</h2><ul class='ls'>" + "".join(f'<li><a href="../{s}/">{h}</a></li>' for s, h in STATP if s.endswith(r)) + "</ul>" for r in REG)
page("thong-ke/bang-thong-ke/", "Bảng thống kê xổ số XSMB, XSMN, XSMT – lô gan, 3 càng, giải đặc biệt", "Tổng hợp các bảng thống kê XSMB, XSMN, XSMT: lô gan, tần suất lô tô, đầu đuôi, giải đặc biệt, giải nhất, giải tám, 3 càng, 4 càng. Không quảng cáo.", [("Thống kê", "thong-ke/"), ("Bảng thống kê", "thong-ke/bang-thong-ke/")], "Bảng thống kê xổ số", hub)


# ---------- hiện sẵn bảng kết quả mới nhất trong trang ứng dụng (tải nhanh, không nhảy bố cục) ----------
WDV = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN']
def nsp(n): return f'<span class="nm"><i>{n[:-3]}</i><u>{n[-3:-2] if len(n) > 2 else ""}</u><b>{n[-2:]}</b></span>'
def lotoT(lo):
    H = [[] for _ in range(10)]; T = [[] for _ in range(10)]
    for k in sorted(lo): H[k // 10].append(str(k % 10)); T[k % 10].append(str(k // 10))
    return '<table class="lt4"><thead><tr><th>Đầu</th><th>Đuôi</th><th>Đầu</th><th>Đuôi</th></tr></thead><tbody>' + ''.join(f'<tr><td class="k">{i}</td><td>{", ".join(H[i]) or "–"}</td><td>{", ".join(T[i]) or "–"}</td><td class="k">{i}</td></tr>' for i in range(10)) + '</tbody></table>'
def heads(lo):
    h = [[] for _ in range(10)]
    for k in sorted(lo): h[k // 10].append(str(k % 10))
    return h
def pre_mb():
    r = mb[-1]; d = r["date"]
    b = '<div class="ticket">' + ''.join(f'<div class="row {"db" if g == "db" else ""}"><div class="lb">{lb}</div><div class="nums">' + ''.join(nsp(n) for n in r[g]) + '</div></div>' for lb, g in MB_G) + '</div>'
    b += '<div class="loto">' + lotoT(lotos(r, MB_G)) + '</div>'
    return f"XSMB {WDV[wdi(d)]}, {vn(d)}", b
def pre_mn(fn, lab, sel):
    rec = json.load(open(os.path.join(ROOT, fn))); d = max(r["date"] for r in rec)
    rs = sorted([r for r in rec if r["date"] == d], key=lambda r: (r["station"] != "tp-hcm", ST.get(r["station"], "")))
    b = '<div class="mnb"><table><thead><tr><th>Giải</th>' + ''.join(f'<th class="{"sel" if r["station"] == sel else ""}">{ST.get(r["station"], r["station"])}</th>' for r in rs) + '</tr></thead><tbody>'
    b += ''.join(f'<tr class="{g}"><td>{lb}</td>' + ''.join('<td>' + ''.join(nsp(n) for n in r[g]) + '</td>' for r in rs) + '</tr>' for lb, g in MN_G) + '</tbody></table></div>'
    b += '<div class="lt">' + ''.join(f'<div><h3>{ST.get(r["station"], r["station"])}</h3>' + lotoT(lotos(r, MN_G)) + '</div>' for r in rs) + '</div>'
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
    h2 = re.sub(r'<span class="dlab" id="rsDateL" aria-hidden="true">[^<]*</span>', f'<span class="dlab" id="rsDateL" aria-hidden="true">{vn(dlast)}</span>', h2, count=1)
    if h2 != h: open(fp, "w").write(h2)


# ---------- trang trực tiếp: dữ liệu thống kê riêng của kết quả mới nhất (khác nhau mỗi ngày) ----------
def live_mb():
    d = two[-1][0]; today = lo[-1]; H = lo[:-1]; n = len(H)
    pv = {}
    for i, ks in enumerate(H):
        for k in ks: pv[k] = i
    c30p = Counter(k for ks in H[-30:] for k in ks); c100p = Counter(k for ks in H[-100:] for k in ks)
    cnt = Counter(today); ks = sorted(cnt)
    rows = [(f"<b>{SL(k)}</b>", cnt[k], (n - 1 - pv[k]) if k in pv else "–", c30p[k], c100p[k]) for k in sorted(ks, key=lambda k: -((n - 1 - pv.get(k, -1))))]
    back = sorted(ks, key=lambda k: -(n - 1 - pv.get(k, -1)))[:3]
    hot = [k for k in ks if cnt[k] > 1]
    hd = {k // 10 for k in today}; td = {k % 10 for k in today}
    keps = [k for k in ks if k in KEP]
    dao = [f"{10 * a + b:02d} – {10 * b + a:02d}" for a, b in PAIRS if 10 * a + b in cnt and 10 * b + a in cnt]
    r = fmap.get(d); dbv = r[0] if r else ""
    prevdb = [i for i, (dd, t) in enumerate(dbt2[:-1]) if t == dbv[-2:]] if dbv else []
    pva = dict(pv); [pva.__setitem__(k, n) for k in ks]
    ganNow = sorted(range(100), key=lambda k: -(n - pva.get(k, -1)))[:5]
    li = [f"Giải Đặc biệt <b>{dbv}</b>" + (f"; 2 số cuối {dbv[-2:]} lần trước làm giải Đặc biệt ngày {vn(dbt2[prevdb[-1]][0])} ({len(dbt2) - 1 - prevdb[-1]} kỳ trước)." if prevdb else "."),
          f"{len(ks)} lô khác nhau trên 27 giải" + (f"; về nhiều nháy: {', '.join(f'<b>{SL(k)}</b> ({cnt[k]} nháy)' for k in hot)}." if hot else "; không có lô nào về nhiều nháy."),
          "Về lại sau thời gian gan dài nhất: " + ", ".join(f"<b>{SL(k)}</b> ({n - 1 - pv[k]} kỳ)" for k in back if k in pv) + ".",
          "Đầu câm: " + (", ".join(str(x) for x in range(10) if x not in hd) or "không có") + " · Đuôi câm: " + (", ".join(str(x) for x in range(10) if x not in td) or "không có") + ".",
          "Lô kép: " + (", ".join(f"{k:02d}" for k in keps) or "không có") + " · Cặp số đảo cùng về: " + (", ".join(dao) or "không có") + ".",
          "Lô gan nhất sau kỳ này: " + ", ".join(f"<b>{SL(k)}</b> ({n - pva.get(k, -1)} kỳ)" for k in ganNow) + "."]
    return d, li, rows
def live_mn(reg):
    lab = REG[reg][0]
    R = [l.split(",") for l in open(os.path.join(ROOT, reg + ".csv")).read().strip().split("\n")[1:]]
    d = max(x[0] for x in R); byst = {}
    for dd, st, v in R: byst.setdefault(st, []).append((dd, [int(v[j:j + 2]) for j in range(0, len(v), 2)]))
    out = []
    for st in sorted({x[1] for x in R if x[0] == d}, key=lambda s: (s != "tp-hcm", ST.get(s, s))):
        L = byst[st]; today = L[-1][1]; H = L[:-1]; n = len(H); pv = {}
        for i, (_, ks) in enumerate(H):
            for k in ks: pv[k] = i
        c20 = Counter(k for _, ks in H[-20:] for k in ks); cnt = Counter(today)
        rows = [(f"<b>{SL(k)}</b>", cnt[k], (n - 1 - pv[k]) if k in pv else "–", c20[k], vn(H[pv[k]][0]) if k in pv else "–") for k in sorted(cnt, key=lambda k: -(n - 1 - pv.get(k, -1)))]
        back = [k for k in sorted(cnt, key=lambda k: -(n - 1 - pv.get(k, -1))) if k in pv][:2]
        summ = f"{len(cnt)} lô khác nhau; về lại sau gan dài nhất: " + ", ".join(f"<b>{SL(k)}</b> ({n - 1 - pv[k]} kỳ của đài)" for k in back) + (f"; nhiều nháy: {', '.join(f'{k:02d}' for k in cnt if cnt[k] > 1)}" if any(cnt[k] > 1 for k in cnt) else "") + "."
        out.append((ST.get(st, st), n + 1, summ, rows))
    return d, out
LV = {"mb": live_mb(), "mn": live_mn("xsmn"), "mt": live_mn("xsmt")}
def lvblock(reg, full=True):
    if reg == "mb":
        d, li, rows = LV["mb"]
        h = f'<div class="card c12 doc lvday"><h2>Dữ liệu thống kê XSMB {WDL[wdi(d)]} {vn(d)}</h2><p class="sub">So kết quả XSMB ngày {vn(d)} với {fm(N - 1)} kỳ trước đó (từ {vn(two[0][0])}). Bảng tự tạo lại sau mỗi kỳ quay.</p><ul>' + "".join(f"<li>{x}</li>" for x in li) + "</ul>"
        if full: h += "<h3>Từng lô của kỳ " + vn(d) + "</h3>" + tbl(["Lô", "Số nháy", "Số kỳ chưa về trước đó", "Lần về (30 kỳ trước)", "Lần về (100 kỳ trước)"], rows) + "<p class='note'>Trung bình mỗi lô về 8,1 lần trong 30 kỳ và 27 lần trong 100 kỳ. Đây là thống kê kết quả đã quay, không phải dự đoán.</p>"
        return h + "</div>"
    d, sts = LV[reg]; lab = REG["xs" + reg][0]
    h = f'<div class="card c12 doc lvday"><h2>Dữ liệu thống kê {lab} {WDL[wdi(d)]} {vn(d)}</h2><p class="sub">So lô tô từng đài ngày {vn(d)} với các kỳ trước của chính đài đó (mỗi đài quay 1 kỳ mỗi tuần).</p>'
    for name, n, summ, rows in sts:
        h += f"<h3>{name} (kỳ thứ {fm(n)} trong dữ liệu)</h3><p>{summ}</p>"
        if full: h += tbl(["Lô", "Số nháy", "Số kỳ chưa về trước đó", "Lần về (20 kỳ trước)", "Lần về trước"], rows)
    if full: h += "<p class='note'>Mỗi đài có 18 lô mỗi kỳ, nên trong 20 kỳ trung bình mỗi lô về 3,6 lần. Đây là thống kê kết quả đã quay, không phải dự đoán.</p>"
    return h + "</div>"
for f, blk in (("truc-tiep-xsmb/index.html", lvblock("mb")), ("truc-tiep-xsmn/index.html", lvblock("mn")), ("truc-tiep-xsmt/index.html", lvblock("mt")), ("truc-tiep/index.html", lvblock("mn", False) + lvblock("mt", False) + lvblock("mb", False))):
    fp = os.path.join(ROOT, f)
    if not os.path.exists(fp): continue
    h = open(fp).read()
    h2 = re.sub(r'<!--LVDAY-->.*?<!--/LVDAY-->', lambda m: "<!--LVDAY-->" + blk + "<!--/LVDAY-->", h, count=1, flags=re.S)
    if h2 != h: open(fp, "w").write(h2)


# ---------- 100 trang thống kê theo số 00–99 (địa chỉ cố định, nội dung cập nhật mỗi kỳ) ----------
MBL = ["ĐB"] + ["G1"] + ["G2"] * 2 + ["G3"] * 6 + ["G4"] * 4 + ["G5"] * 6 + ["G6"] * 3 + ["G7"] * 4
MNL = ["ĐB", "G1", "G2", "G3", "G3"] + ["G4"] * 7 + ["G5"] + ["G6"] * 3 + ["G7", "G8"]
MNF = {}
for reg in ("xsmn", "xsmt"):
    F = [(l.split(",")[0], l.split(",")[1], l.split(",")[2].split()) for l in open(os.path.join(ROOT, reg + "_full.csv")).read().strip().split("\n")[1:]]
    MNF[reg] = F
SEARCH_FORM = lambda up: f'<form class="nsearch" action="{up}so/" onsubmit="var v=(this.q.value.match(/\\d/g)||[]).join(\'\').slice(-2);if(v.length<2&&v.length)v=\'0\'+v;if(v){{location.href=\'{up}so/\'+v+\'/\';return false}}"><label for="nq">Tra cứu một số</label><div><input id="nq" name="q" inputmode="numeric" maxlength="3" placeholder="Nhập số, ví dụ 06" autocomplete="off"><button>Xem thống kê</button></div></form>'
SCSS = '<style>.nsearch{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin:0 0 16px}.nsearch label{display:block;font-weight:600;font-size:14px;margin-bottom:6px}.nsearch div{display:flex;gap:8px}.nsearch input{flex:1;min-height:44px;border:1px solid var(--line);border-radius:12px;background:var(--band);color:var(--ink);font:inherit;font-size:18px;padding:0 14px}.nsearch button{min-height:44px;border:0;border-radius:12px;background:#d01f3c;color:#fff;font:inherit;font-weight:600;padding:0 16px;cursor:pointer}.ngrid{display:grid;grid-template-columns:repeat(10,minmax(0,1fr));gap:4px}.ngrid a{display:block;text-align:center;padding:8px 0;border:1px solid var(--line);border-radius:8px;text-decoration:none;color:var(--ink);font-weight:700;font-variant-numeric:tabular-nums;background:var(--panel)}.ngrid a small{display:block;font-weight:400;font-size:11px;color:var(--mute)}.ngrid a:hover{border-color:#d01f3c;color:var(--red)}.ngrid a[aria-current]{background:#d01f3c;color:#fff;border-color:#d01f3c}.ngrid a[aria-current] small{color:#fff}@media(max-width:600px){.ngrid{grid-template-columns:repeat(5,minmax(0,1fr))}}</style>'
pvall = {}
for i, ks in enumerate(lo):
    for k in ks: pvall[k] = i
def grid_links(cur=None):
    return '<div class="ngrid">' + ''.join(f'<a href="../{k:02d}/"' + (' aria-current="page"' if k == cur else '') + f'>{k:02d}<small>{N - 1 - pvall.get(k, -1)} kỳ</small></a>' for k in range(100)) + '</div>'
c365 = Counter(k for ks in lo[-365:] for k in ks)
dball = Counter(k for _, k in db)
for k in range(100):
    kk = f"{k:02d}"; dao = int(kk[::-1])
    hits = [i for i, ks in enumerate(lo) if k in ks]
    gap = N - 1 - hits[-1] if hits else N
    mx = max([b - a - 1 for a, b in zip([-1] + hits, hits)] or [0])
    dbh = [i for i, (_, x) in enumerate(db) if x == k]
    rec_rows = []
    for d, v in fullmb[::-1]:
        g = [MBL[j] for j, x in enumerate(v) if x[-2:] == kk and j < len(MBL)]
        if g: rec_rows.append((f'<a href="../../xsmb/{slug_d(d)}/">{vn(d)}</a>', WDL[wdi(d)], len(g), ", ".join(g)))
        if len(rec_rows) >= 15: break
    mb_sum = tbl(["Chỉ số", "Số " + kk, "Trung bình theo xác suất"], [
        ("Số lần về trong 30 kỳ", c30[k], "8,1"), ("Số lần về trong 90 kỳ", c90[k], "24,3"), ("Số lần về trong 365 kỳ", c365[k], "98,6"),
        ("Số kỳ chưa về (tính đến " + vn(lastd) + ")", gap, "–"), ("Kỷ lục số kỳ liên tiếp chưa về", mx, "–"),
        ("Làm 2 số cuối giải Đặc biệt", f"{len(dbh)} lần" + (f", gần nhất {vn(db[dbh[-1]][0])}" if dbh else ""), dec(len(db) / 100, 1) + " lần")])
    mnpart = ""
    for reg in ("xsmn", "xsmt"):
        lab = REG[reg][0]; F = MNF[reg]; ds = sorted({d for d, _, _ in F}); d30 = set(ds[-30:]); d90 = set(ds[-90:])
        n30 = sum(1 for d, st, v in F if d in d30 for x in v if x[-2:] == kk)
        byst = Counter(st for d, st, v in F if d in d90 for x in v if x[-2:] == kk)
        rows = []
        for d, st, v in F[::-1]:
            g = [MNL[j] for j, x in enumerate(v) if x[-2:] == kk and j < len(MNL)]
            if g: rows.append((f'<a href="../../{reg}/{slug_d(d)}/">{vn(d)}</a>', ST.get(st, st), ", ".join(g)))
            if len(rows) >= 10: break
        last = rows[0] if rows else None
        ntot = sum(1 for d, st, v in F if d in d30)
        mnpart += f"<h2>Số {kk} ở {lab}</h2><p>Trong 30 ngày gần nhất số {kk} về <b>{n30}</b> lần trên {fm(ntot * 18)} giải của các đài {lab} (trung bình theo xác suất {dec(ntot * 18 / 100, 1)} lần)." + (f" Lần gần nhất: {last[0]}, đài {last[1]}." if last else "") + (" Đài về nhiều nhất 90 ngày: " + ", ".join(f"{ST.get(a, a)} ({b} lần)" for a, b in byst.most_common(3)) + "." if byst else "") + "</p>"
        mnpart += card(tbl(["Ngày", "Đài", "Giải"], rows))
    nb = [(k - 1) % 100, (k + 1) % 100]
    body = (SCSS + SEARCH_FORM("../../") +
            f"<p>Thống kê số <b>{kk}</b> (2 số cuối các giải) trong kết quả XSMB, XSMN, XSMT, tính đến kỳ {vn(lastd)}. Trang được cập nhật sau mỗi kỳ quay; đây là thống kê kết quả đã quay, không phải dự đoán.</p>" +
            f"<h2>Số {kk} ở XSMB</h2>" + card(mb_sum) + f"<h2>15 lần gần nhất số {kk} về ở XSMB</h2>" + card(tbl(["Ngày", "Thứ", "Số nháy", "Giải"], rec_rows)) + mnpart +
            "<h2>Số liên quan</h2><p>" + (f'Số đảo: <a href="../{dao:02d}/">{dao:02d}</a> · ' if dao != k else f'{kk} là số kép bằng · ') + "Số liền kề: " + ", ".join(f'<a href="../{x:02d}/">{x:02d}</a>' for x in nb) +
            f' · <a href="../../thong-ke/lo-gan-xsmb/">Lô gan XSMB</a> · <a href="../../thong-ke/so-dao-xsmb/">Thống kê số đảo</a></p>' +
            "<h2>Tra cứu số khác</h2><p class='note'>Số nhỏ dưới mỗi ô là số kỳ XSMB chưa về.</p>" + grid_links(k))
    page(f"so/{kk}/", f"Thống kê số {kk} – số {kk} XSMB, XSMN, XSMT về bao nhiêu lần", f"Số {kk}: số lần về trong 30, 90, 365 kỳ XSMB, số kỳ chưa về, kỷ lục gan, lần làm giải đặc biệt và các lần về gần nhất ở XSMB, XSMN, XSMT, cập nhật đến {vn(lastd)}.",
         [("Tra cứu số", "so/"), (f"Số {kk}", f"so/{kk}/")], f"Thống kê số {kk}", body, fam=("so", {"so": kk}))
hubb = SCSS + SEARCH_FORM("../") + f"<p>Chọn một số từ 00 đến 99 để xem thống kê chi tiết ở XSMB, XSMN, XSMT. Số nhỏ dưới mỗi ô là số kỳ XSMB chưa về, tính đến {vn(lastd)}.</p>" + card(grid_links().replace('href="../', 'href="./'))
page("so/", "Tra cứu thống kê số 00–99 XSMB, XSMN, XSMT", f"Tra cứu thống kê từng số từ 00 đến 99: số lần về, số kỳ chưa về, kỷ lục gan ở XSMB, XSMN, XSMT, cập nhật đến {vn(lastd)}.", [("Tra cứu số", "so/")], "Tra cứu thống kê số 00–99", hubb)


# ---------- hiện sẵn kỳ Vietlott mới nhất (tải nhanh, LCP thấp) ----------
WDA = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật']
def vlpre(f, game, nm):
    L = open(os.path.join(ROOT, f)).read().strip().split("\n")
    p = L[-1].split(","); ky, d = int(p[0]), p[1]
    title = f"{nm} · kỳ #{ky:05d} · {WDA[wdi(d)]}, {vn(d)}"
    if game in ("645", "655"):
        nums = [int(x) for x in p[2:8]]
        balls = ''.join(f'<div class="ball r lg">{k:02d}</div>' for k in nums)
        if game == "655" and len(p) > 8 and p[8]: balls += f'<div class="ballwrap"><div class="ball y lg">{int(p[8]):02d}</div><small>số đặc biệt</small></div>'
    else:
        G3 = [("Giải Đặc biệt", p[2]), ("Giải Nhất", p[3]), ("Giải Nhì", p[4]), ("Giải Ba", p[5])]
        balls = '<div class="tbl" style="width:100%"><table><tbody>' + ''.join(f'<tr><td class="left" style="width:120px"><b>{a}</b></td><td class="left" style="font-size:20px;letter-spacing:1px">' + ''.join(f'<b style="color:var(--red);margin-right:14px;display:inline-block">{x}</b>' for x in b.split()) + '</td></tr>' for a, b in G3) + '</tbody></table></div>'
    first = L[1].split(",")[1]; n2 = len(L) - 1
    dr = f"Dữ liệu {fm(n2)} kỳ ({vn(first)} – {vn(d)})."
    if game in ("645", "655"):
        from math import comb
        mx = 45 if game == "645" else 55; T = comb(mx, 6)
        od = [("Jackpot" + (" 1" if game == "655" else ""), 1)] + ([("Jackpot 2 (5 số + số đặc biệt)", 6)] if game == "655" else []) + [("Giải nhất (5 số)", 6 * (mx - 6 - (1 if game == "655" else 0))), ("Giải nhì (4 số)", 15 * comb(mx - 6, 2)), ("Giải ba (3 số)", 20 * comb(mx - 6, 3))]
        days = "thứ 4, thứ 6, chủ nhật" if game == "645" else "thứ 3, thứ 5, thứ 7"
        note = f"{nm} quay {days}, khoảng 18:00. Xác suất mỗi vé: " + " · ".join(f"{a} 1/{fm(round(T / c))}" for a, c in od) + ". " + dr
    elif game == "3dpro":
        note = "Max 3D Pro quay thứ 3, thứ 5, thứ 7, khoảng 18:00; mỗi kỳ quay 20 bộ ba số (Đặc biệt 2, Nhất 4, Nhì 6, Ba 8). Vé gồm 2 bộ ba số: trùng cả 2 bộ số giải Đặc biệt đúng thứ tự là giải Đặc biệt, ngược thứ tự là giải phụ Đặc biệt; các giải còn lại dựa trên số bộ trùng với từng nhóm giải. " + dr
    else:
        note = "Max 3D quay thứ 2, thứ 4, thứ 6, khoảng 18:00; mỗi kỳ quay 20 bộ ba số (Đặc biệt 2, Nhất 4, Nhì 6, Ba 8). Vé Max 3D cơ bản chọn 1 bộ ba số 000–999, trùng đúng thứ tự một bộ số của nhóm giải nào thì trúng giải đó. " + dr
    return title, balls, note
for fdir, f, game, nm in (("mega-645", "vietlott_645.csv", "645", "Mega 6/45"), ("power-655", "vietlott_655.csv", "655", "Power 6/55"), ("max-3d", "vietlott_3d.csv", "3d", "Max 3D"), ("max-3d-pro", "vietlott_3dpro.csv", "3dpro", "Max 3D Pro")):
    fp = os.path.join(ROOT, fdir, "index.html")
    if not os.path.exists(fp) or not os.path.exists(os.path.join(ROOT, f)): continue
    title, balls, note = vlpre(f, game, nm)
    h = open(fp).read()
    h2 = re.sub(r'<h2 id="vlT">[^<]*</h2>', f'<h2 id="vlT">{title}</h2>', h, count=1)
    h2 = re.sub(r'<div class="balls" id="vlBalls">.*?</div><!--/vlb-->', lambda m: f'<div class="balls" id="vlBalls">{balls}</div><!--/vlb-->', h2, count=1, flags=re.S)
    h2 = re.sub(r'<p class="note" id="vlNote"([^>]*)>.*?</p>', lambda m: f'<p class="note" id="vlNote"{m.group(1)}>{note}</p>', h2, count=1, flags=re.S)
    if h2 != h: open(fp, "w").write(h2)


# ---------- KHO LƯU TRỮ VIETLOTT: trang từng kỳ, trang theo năm, mục lục ----------
VLG2 = [("mega-645", "vietlott_645.csv", "645", "Mega 6/45", 45), ("power-655", "vietlott_655.csv", "655", "Power 6/55", 55), ("max-3d", "vietlott_3d.csv", "3d", "Max 3D", 0), ("max-3d-pro", "vietlott_3dpro.csv", "3dpro", "Max 3D Pro", 0)]
G3N = [("Đặc biệt", 2), ("Nhất", 3), ("Nhì", 4), ("Ba", 5)]
SITEMAP_VL = []
for gdir, f, game, nm, mx in VLG2:
    fp = os.path.join(ROOT, f)
    if not os.path.exists(fp): continue
    rows = [l.split(",") for l in open(fp).read().strip().split("\n")[1:]]
    rows = [r for r in rows if len(r) >= 6]
    pvv = {}; byyear = {}
    for i, r in enumerate(rows):
        ky, d = int(r[0]), r[1]; w = wdi(d); y = d[:4]
        byyear.setdefault(y, []).append(i)
        prv = rows[i - 1] if i else None; nxt = rows[i + 1] if i + 1 < len(rows) else None
        if game in ("645", "655"):
            ns = [int(x) for x in r[2:8]]; db = int(r[8]) if game == "655" and len(r) > 8 and r[8] else None
            balls = ''.join(f'<span class="vb">{k:02d}</span>' for k in ns) + (f' <span class="vb y" title="Số đặc biệt">{db:02d}</span>' if db is not None else '')
            back = sorted(((i - 1 - pvv[k], k) for k in ns if k in pvv), reverse=True)[:2]
            same = sorted(set(ns) & set(int(x) for x in prv[2:8])) if prv else []
            ev = sum(1 for k in ns if k % 2 == 0); big = sum(1 for k in ns if k > mx // 2)
            facts_l = [f"Tổng 6 số: {sum(ns)}; {ev} số chẵn, {6 - ev} số lẻ; {big} số lớn (từ {mx // 2 + 1} trở lên), {6 - big} số nhỏ.",
                       f"Trùng với kỳ trước: {', '.join(f'{k:02d}' for k in same) or 'không có số nào'}.",
                       "Về lại sau thời gian dài nhất: " + (", ".join(f"<b>{k:02d}</b> ({n} kỳ)" for n, k in back) or "không có") + "."]
            if db is not None: facts_l.append(f"Số đặc biệt <b>{db:02d}</b> dùng để xác định giải Jackpot 2.")
            for k in ns: pvv[k] = i
            body0 = f'<div class="card" style="text-align:center">{balls}</div>'
            short = " ".join(f"{k:02d}" for k in ns) + (f" | {db:02d}" if db is not None else "")
        else:
            grp = [(gname, r[c].split()) for gname, c in G3N]
            body0 = card(tbl(["Giải", "Các bộ số"], [(gname, " ".join(f"<b>{x}</b>" for x in v)) for gname, v in grp]))
            allv = [x for _, v in grp for x in v]
            back = sorted(((i - 1 - pvv[x], x) for x in set(allv) if x in pvv), reverse=True)[:3]
            dig = Counter(c for x in allv for c in x)
            facts_l = [f"20 bộ ba số; chữ số xuất hiện nhiều nhất: {', '.join(f'{c} ({n} lần)' for c, n in dig.most_common(2))}.",
                       f"Bộ số giải Đặc biệt: {' và '.join(grp[0][1])}.",
                       "Bộ số về lại sau thời gian dài nhất: " + (", ".join(f"<b>{x}</b> ({n} kỳ)" for n, x in back) or "không có") + "."]
            for x in allv: pvv[x] = i
            short = "ĐB " + " ".join(grp[0][1])
        kp = f"{ky:05d}"
        pk = f'<a href="../ky-{int(prv[0]):05d}/">‹ Kỳ #{int(prv[0]):05d}</a>' if prv else '<span></span>'
        nk = f'<a href="../ky-{int(nxt[0]):05d}/">Kỳ #{int(nxt[0]):05d} ›</a>' if nxt else '<span></span>'
        nav = f'<div class="pn">{pk}{nk}</div>'
        body = (f'<p>Kết quả xổ số Vietlott {nm} kỳ quay #{kp}, {WDL[w]} ngày {vn(d)}.</p>' + body0 +
                f'<h2>Thống kê kỳ #{kp}</h2><ul class="facts">' + "".join(f"<li>{x}</li>" for x in facts_l) + '</ul>' + nav +
                f'<p><a class="cta" href="../nam-{y}/">{nm} năm {y}</a><a class="cta" href="../">{nm} kỳ mới nhất</a><a class="cta" href="../lich-su/">Lịch sử {nm}</a></p>'
                f'<p class="note">Thông tin chỉ mang tính chất tham khảo; kết quả chính thức do Vietlott công bố. Thời hạn lĩnh thưởng 60 ngày kể từ ngày quay.</p>')
        p = f"{gdir}/ky-{kp}/"
        page(p, f"{nm} kỳ #{kp} ngày {vn(d)} – Kết quả Vietlott {nm} {WDL[w]} {vn(d)}", f"Kết quả Vietlott {nm} kỳ #{kp} {WDL[w]} ngày {vn(d)}: {short}. Thống kê kỳ quay và liên kết các kỳ trước, kỳ sau.",
             [(nm, gdir + "/"), ("Lịch sử", gdir + "/lich-su/"), (f"Kỳ #{kp}", p)], f"{nm} kỳ #{kp} – {WDL[w]} {vn(d)}", body)
        SITEMAP_VL.append((BASE + p, d))
    years = sorted(byyear)
    for j, y in enumerate(years):
        ii = byyear[y]
        if game in ("645", "655"):
            t = tbl(["Kỳ", "Ngày", "Kết quả"], [(f'<a href="../ky-{int(rows[i][0]):05d}/">#{int(rows[i][0]):05d}</a>', vn(rows[i][1]), " ".join(f"<b>{int(x):02d}</b>" for x in rows[i][2:8]) + (f" · ĐB {int(rows[i][8]):02d}" if game == "655" and len(rows[i]) > 8 and rows[i][8] else "")) for i in ii[::-1]])
            cnt = Counter(int(x) for i in ii for x in rows[i][2:8])
            note = f"Số về nhiều nhất năm {y}: " + ", ".join(f"{k:02d} ({n} lần)" for k, n in cnt.most_common(5)) + "."
        else:
            t = tbl(["Kỳ", "Ngày", "Giải Đặc biệt"], [(f'<a href="../ky-{int(rows[i][0]):05d}/">#{int(rows[i][0]):05d}</a>', vn(rows[i][1]), " ".join(f"<b>{x}</b>" for x in rows[i][2].split())) for i in ii[::-1]])
            note = f"Năm {y} có {len(ii)} kỳ quay."
        py_ = f'<a href="../nam-{years[j-1]}/">‹ Năm {years[j-1]}</a>' if j else '<span></span>'
        ny_ = f'<a href="../nam-{years[j+1]}/">Năm {years[j+1]} ›</a>' if j + 1 < len(years) else '<span></span>'
        yp = f'<div class="pn">{py_}{ny_}</div>'
        p = f"{gdir}/nam-{y}/"
        page(p, f"Kết quả {nm} năm {y} – lịch sử Vietlott {nm} {y}", f"Kết quả Vietlott {nm} năm {y}: {len(ii)} kỳ quay, kết quả từng kỳ và các số về nhiều nhất.", [(nm, gdir + "/"), ("Lịch sử", gdir + "/lich-su/"), (f"Năm {y}", p)], f"Kết quả {nm} năm {y}", f"<p>{len(ii)} kỳ quay {nm} trong năm {y}. {note}</p>" + card(t) + yp)
        SITEMAP_VL.append((BASE + p, rows[ii[-1]][1]))
    p = f"{gdir}/lich-su/"
    page(p, f"Lịch sử kết quả {nm} – tất cả các kỳ từ {years[0]}", f"Lịch sử kết quả Vietlott {nm}: {fm(len(rows))} kỳ quay từ {vn(rows[0][1])}, tra cứu theo năm và từng kỳ.", [(nm, gdir + "/"), ("Lịch sử", p)], f"Lịch sử kết quả {nm}",
         f"<p>XS Lab lưu {fm(len(rows))} kỳ {nm} từ kỳ #{int(rows[0][0]):05d} ({vn(rows[0][1])}) đến kỳ #{int(rows[-1][0]):05d} ({vn(rows[-1][1])}).</p><h2>Theo năm</h2><ul class='ls'>" + "".join(f'<li><a href="../nam-{y}/">{nm} năm {y}</a> ({len(byyear[y])} kỳ)</li>' for y in years[::-1]) + "</ul><h2>20 kỳ gần nhất</h2><ul class='ls'>" + "".join(f'<li><a href="../ky-{int(r[0]):05d}/">Kỳ #{int(r[0]):05d} – {vn(r[1])}</a></li>' for r in rows[::-1][:20]) + "</ul>")
    SITEMAP_VL.append((BASE + p, rows[-1][1]))
    print(nm, "kỳ:", len(rows), "năm:", len(years))


# ---------- Thống kê 30 kỳ gần nhất (mỗi miền một trang cố định, tự cập nhật sau mỗi buổi quay) ----------
from collections import Counter
for reg, (lab, name, tm) in REG.items():
    R = fullrecs(reg); G = MB_G if reg == "xsmb" else MN_G
    byd = {}
    for (d, st), r in R.items(): byd.setdefault(d, []).append(r)
    ds = sorted(byd)
    if len(ds) < 31: continue
    win = ds[-30:]; last = ds[-1]
    lo_d = {d: [k for r in byd[d] for k in lotos(r, G)] for d in ds}
    lastseen = {}
    for i, d in enumerate(ds):
        for k in set(lo_d[d]): lastseen[k] = i
    gan = sorted(range(100), key=lambda k: (-(len(ds) - 1 - lastseen.get(k, -1)), k))[:10]
    cnt = Counter(k for d in win for k in lo_d[d])
    hot = sorted(range(100), key=lambda k: (-cnt[k], k))[:10]
    cold = [k for k in range(100) if cnt[k] == 0]
    kep = sorted({k for d in win for k in lo_d[d] if k % 11 == 0})
    dau = Counter(k // 10 for d in win for k in lo_d[d]); duoi = Counter(k % 10 for d in win for k in lo_d[d])
    tot = sum(cnt.values()); E = tot / 100
    dbs = [(d, r) for d in win for r in sorted(byd[d], key=lambda r: ST.get(r["station"], ""))]
    dbd = Counter(r["db"][0][-2] for _, r in dbs); dbu = Counter(r["db"][0][-1] for _, r in dbs)
    chip = lambda k, sub: f'<a class="c30" href="../../so/{k:02d}/"><b>{k:02d}</b><small>{sub}</small></a>'
    if reg == "xsmb":
        rows = ''.join(f'<tr><td><a href="../../xsmb/{slug_d(d)}/">{vn(d)[:5]}</a><small>{WD[wdi(d)]}</small></td><td class="db">{r["db"][0]}</td><td class="lo">{" ".join(SL(k) for k in sorted(lo_d[d]))}</td></tr>' for d in reversed(win) for r in byd[d])
        head = '<tr><th>Ngày</th><th>Đặc biệt</th><th>2 số cuối 27 giải</th></tr>'
    else:
        rows = ''.join(f'<tr><td><a href="../../{reg}/{slug_d(d)}/">{vn(d)[:5]}</a><small>{WD[wdi(d)]}</small></td><td class="st">{ST.get(r["station"], "")}</td><td class="db">{r["db"][0]}</td><td class="lo">{" ".join(SL(k) for k in lotos(r, G))}</td></tr>' for d in reversed(win) for r in sorted(byd[d], key=lambda r: ST.get(r["station"], "")))
        head = '<tr><th>Ngày</th><th>Đài</th><th>Đặc biệt</th><th>2 số cuối 18 giải</th></tr>'
    unit = "ngày" if reg == "xsmb" else "kỳ"
    w365 = ds[-365:]
    c3 = Counter(t for d in w365 for r in byd[d] for t in {v[-3:] for _, g in G for v in r[g] if len(v) >= 3})
    top3 = sorted(c3, key=lambda t: (-c3[t], t))[:10]
    c3tbl = '<div class="card"><table class="dd30"><tr><th>Hạng</th><th>3 càng</th><th>Số lần về</th></tr>' + ''.join(f'<tr><td>{i+1}</td><td><b>{t}</b></td><td>{c3[t]}</td></tr>' for i, t in enumerate(top3)) + '</table></div>'
    body = f"""<p class="lead"><b>Tính đến kỳ {vn(last)} ({WDL[wdi(last)]}):</b> 30 kỳ {lab} từ {vn(win[0])} đến {vn(last)}, tổng {tot} giải. Lô về nhiều nhất là {', '.join(f'{k:02d}' for k in hot[:3])} ({cnt[hot[0]]} lần); {len(cold)} số chưa về lần nào trong 30 kỳ; lô gan nhất là {gan[0]:02d} ({len(ds) - 1 - lastseen.get(gan[0], -1)} {unit} chưa về).</p>
<p>Trang tự cập nhật sau mỗi buổi quay {lab} ({tm}). Mọi số liệu là thống kê các kỳ đã quay, không phải dự đoán; mỗi kỳ quay độc lập với các kỳ trước.</p>
<h2>Lô về nhiều nhất 30 kỳ</h2><div class="g30">{''.join(chip(k, f"{cnt[k]} lần") for k in hot)}</div>
<p class="note">Theo xác suất, trung bình mỗi số về khoảng {str(round(E, 1)).replace('.', ',')} lần trong 30 kỳ này.</p>
<h2>Lô gan {lab} tính đến {vn(last)}</h2><div class="g30">{''.join(chip(k, f"{len(ds) - 1 - lastseen.get(k, -1)} {unit}") for k in gan)}</div>
<h2>Số chưa về trong 30 kỳ</h2><p>{', '.join(f'<a href="../../so/{k:02d}/">{k:02d}</a>' for k in cold) or 'Không có: số nào cũng đã về ít nhất một lần.'}</p>
<h2>Lô kép đã về trong 30 kỳ</h2><p>{', '.join(f'{k:02d} ({cnt[k]} lần)' for k in kep) or 'Không có'}</p>
<h2>Đầu, đuôi lô tô 30 kỳ</h2><div class="card"><table class="dd30"><tr><th>Số</th>{''.join(f'<th>{i}</th>' for i in range(10))}</tr><tr><td>Đầu</td>{''.join(f'<td>{dau[i]}</td>' for i in range(10))}</tr><tr><td>Đuôi</td>{''.join(f'<td>{duoi[i]}</td>' for i in range(10))}</tr></table></div>
<h2>Giải Đặc biệt 30 kỳ: chữ số hàng chục và hàng đơn vị</h2><div class="card"><table class="dd30"><tr><th>Số</th>{''.join(f'<th>{i}</th>' for i in range(10))}</tr><tr><td>Hàng chục</td>{''.join(f'<td>{dbd[str(i)]}</td>' for i in range(10))}</tr><tr><td>Hàng đơn vị</td>{''.join(f'<td>{dbu[str(i)]}</td>' for i in range(10))}</tr></table></div>
<h2>3 càng về nhiều nhất trong {len(w365)} ngày quay {lab}</h2>{c3tbl}<p class="note">Đếm 3 chữ số cuối của các giải có từ 3 chữ số trở lên{'' if reg == 'xsmb' else ', gộp tất cả các đài ' + lab}, tính đến {vn(last)}.</p>
<p><a class="cta" href="../?mien={reg.replace('xs', '')}#rkCard">Bảng xếp hạng đầy đủ: lô 2 số, 3 càng, 4 càng, đầu đuôi</a></p>
<h2>Bảng kết quả 30 kỳ gần nhất</h2><div class="card t30w"><table class="t30">{head}{rows}</table></div>
<p><a class="cta" href="../../{reg}/">{lab} hôm nay</a><a class="cta" href="../../{reg}-30-ngay/">{lab} 30 ngày</a><a class="cta" href="../lo-gan-{reg}/">Lô gan {lab}</a><a class="cta" href="../../do-ve/">Dò vé số</a></p>"""
    if not os.path.isdir(os.path.join(ROOT, "thong-ke", f"lo-gan-{reg}")):
        body = body.replace(f'<a class="cta" href="../lo-gan-{reg}/">Lô gan {lab}</a>', '')
    p = f"thong-ke/30-ky-{reg}/"
    page(p, f"Thống kê {lab} 30 kỳ gần nhất – tính đến {vn(last)}", f"Thống kê {lab} 30 kỳ gần nhất tính đến {vn(last)}: giải Đặc biệt và 2 số cuối các giải, lô về nhiều, lô gan, số chưa về, đầu đuôi. Chỉ là thống kê, không dự đoán.", [("Thống kê", "thong-ke/"), (f"Thống kê {lab} 30 kỳ", p)], f"Thống kê {lab} 30 kỳ gần nhất", body)


# ---------- Quay thử (mô phỏng ngẫu nhiên, chạy trên trình duyệt) ----------
QT_JS = r"""(function(){var C=window.QT,$=function(i){return document.getElementById(i)};
var MB=[['ĐB','db',1,5],['G1','g1',1,5],['G2','g2',2,5],['G3','g3',6,5],['G4','g4',4,4],['G5','g5',6,4],['G6','g6',3,3],['G7','g7',4,2]],
MN=[['G8','g8',1,2],['G7','g7',1,3],['G6','g6',3,4],['G5','g5',1,4],['G4','g4',7,5],['G3','g3',2,5],['G2','g2',1,5],['G1','g1',1,5],['ĐB','db',1,6]];
var G=C.reg==='mb'?MB:MN,ORD=C.reg==='mb'?['g1','g2','g3','g4','g5','g6','g7','db']:['g8','g7','g6','g5','g4','g3','g2','g1','db'];
var S={},q=[],t=null,roll=null,cur=null,t0=0,sts=[];
function rd(n){var a=new Uint32Array(n),o='';crypto.getRandomValues(a);for(var i=0;i<n;i++)o+=a[i]%10;return o}
function len(g){for(var i=0;i<G.length;i++)if(G[i][1]===g)return G[i][3]}
function cnt(g){for(var i=0;i<G.length;i++)if(G[i][1]===g)return G[i][2]}
function mine(){try{var v=JSON.parse(localStorage.getItem('xs-dvnum'))||'';return (v.match(/\d+/g)||[]).filter(function(x){return x.length<=2}).map(function(x){return ('0'+x).slice(-2)})}catch(e){return []}}
function cell(st,g,i){var v=S[st][g][i];if(v)return '<span>'+v.slice(0,-2)+'<b>'+v.slice(-2)+'</b></span>';if(cur&&cur[0]===st&&cur[1]===g&&cur[2]===i)return '<span class="qroll" data-l="'+len(g)+'">'+rd(len(g))+'</span>';return '<span class="qpend">'+'•'.repeat(len(g))+'</span>'}
function draw(){var h;if(C.reg==='mb'){h='<table>'+G.map(function(r){var a=[];for(var i=0;i<r[2];i++)a.push(cell('mb',r[1],i));return '<tr class="'+r[1]+'"><td class="l">'+r[0]+'</td><td>'+a.join('')+'</td></tr>'}).join('')+'</table>'}
else{h='<table class="mn"><tr><th>Giải</th>'+sts.map(function(s){return '<th>'+s[1]+'</th>'}).join('')+'</tr>'+G.map(function(r){return '<tr class="'+r[1]+'"><td class="l">'+r[0]+'</td>'+sts.map(function(s){var a=[];for(var i=0;i<r[2];i++)a.push(cell(s[0],r[1],i));return '<td>'+a.join('')+'</td>'}).join('')+'</tr>'}).join('')+'</table>'}
$('qtBoard').innerHTML=h;var left=q.length+(cur?1:0);$('qtSt').textContent=t?('Đang quay · còn '+left+' giải'):(left?'Sẵn sàng':'Đã quay xong')}
function lot(){var M=mine(),k=Object.keys(S);$('qtLo').innerHTML='<div class="ltg">'+k.map(function(st){var L=[];G.forEach(function(r){S[st][r[1]].forEach(function(v){if(v)L.push(v.slice(-2))})});L.sort();var H=[[],[],[],[],[],[],[],[],[],[]];L.forEach(function(x){H[+x[0]].push(M.indexOf(x)>=0?'<mark>'+x+'</mark>':x)});
return '<div><h3>Lô tô '+(st==='mb'?'XSMB':(sts.filter(function(s){return s[0]===st})[0]||[0,st])[1])+' (quay thử)</h3><table class="lt"><tr><th>Đầu</th><th>Lô tô</th></tr>'+H.map(function(a,i){return '<tr><td class="k">'+i+'</td><td>'+(a.join(', ')||'–')+'</td></tr>'}).join('')+'</table></div>'}).join('')+'</div>'+(M.length?'<p class="note">Số trong nhóm bạn đã lưu được tô nền.</p>':'')}
function reset(){stop();S={};q=[];cur=null;var w=$('qtDay')?+$('qtDay').value:0;sts=C.reg==='mb'?[['mb','XSMB']]:(C.sched[w]||[]);
sts.forEach(function(s){S[s[0]]={};G.forEach(function(r){S[s[0]][r[1]]=new Array(r[2]).fill('')})});
ORD.forEach(function(g){for(var i=0;i<cnt(g);i++)sts.forEach(function(s){q.push([s[0],g,i])})});$('qtLo').innerHTML='';draw()}
function step(){if(cur){S[cur[0]][cur[1]][cur[2]]=rd(len(cur[1]))}cur=q.shift()||null;if(!cur){stop();draw();lot();return}draw();
var per=spd();t=setTimeout(step,per)}
function spd(){var sp=$('qtSp').value;return sp==='that'?(C.reg==='mb'?44000:66000/Math.max(1,sts.length)):sp==='vua'?2500:500}
function stop(){clearTimeout(t);t=null;clearInterval(roll);roll=null;$('qtGo').textContent='Quay thử'}
$('qtGo').onclick=function(){if(t){stop();draw();return}if(!q.length&&!cur)reset();$('qtGo').textContent='Tạm dừng';t=1;roll=setInterval(function(){var e=document.querySelector('#qtBoard .qroll');if(e)e.textContent=rd(+e.getAttribute('data-l'))},70);step()};
$('qtRe').onclick=function(){reset()};$('qtSp').onchange=function(){if(t){clearTimeout(t);t=setTimeout(step,Math.min(spd(),400))}};if($('qtDay'))$('qtDay').onchange=reset;
if($('qtDay')){var d=new Date(Date.now()+7*3600e3).getUTCDay();$('qtDay').value=String((d+6)%7)}reset()})();"""
QT_CSS_NOTE = '<p class="note"><b>Lưu ý:</b> Quay thử chỉ là mô phỏng: mọi con số được trình duyệt chọn ngẫu nhiên, không lấy từ dữ liệu, không liên quan và không gợi ý gì cho kết quả quay thật. XS Lab không đưa ra dự đoán.</p>'
for reg, (lab, name, tm) in REG.items():
    sched = {}
    if reg != "xsmb":
        rec = json.load(open(os.path.join(ROOT, "recent_mn.json" if reg == "xsmn" else "recent_mt.json")))
        for w in range(7):
            ds = sorted({r["date"] for r in rec if wdi(r["date"]) == w})
            if ds: sched[w] = sorted([[r["station"], ST.get(r["station"], r["station"])] for r in rec if r["date"] == ds[-1]], key=lambda x: ST.get(x[0], ""))
    p = f"mo-phong/quay-thu-{reg}/"
    tabs = '<p class="qttabs">' + ''.join(f'<a href="../quay-thu-{r2}/"' + (' aria-current="page"' if r2 == reg else '') + f'>Quay thử {REG[r2][0]}</a>' for r2 in REG) + '<a href="../#simCard">Mô phỏng cách chơi</a></p>'
    day = '' if reg == "xsmb" else '<label>Lịch đài <select id="qtDay">' + ''.join(f'<option value="{w}">{WD[w]}: {", ".join(x[1] for x in sched.get(w, []))}</option>' for w in range(7) if w in sched) + '</select></label>'
    real = "khoảng 44 giây một giải, đúng thứ tự từ giải Nhất đến giải Đặc biệt" if reg == "xsmb" else "khoảng 1 phút một giải mỗi đài, đúng thứ tự từ giải Tám đến giải Đặc biệt, các đài quay song song"
    body = (tabs + f'<div class="card qtc"><div class="qtbar">{day}<label>Tốc độ <select id="qtSp"><option value="nhanh">Nhanh</option><option value="vua">Vừa</option><option value="that">Như thật</option></select></label><button type="button" id="qtGo" class="qtgo">Quay thử</button><button type="button" id="qtRe" class="qtre">Quay lại</button><span id="qtSt" class="note"></span></div><div id="qtBoard"></div></div><div id="qtLo"></div>'
        + QT_CSS_NOTE
        + f'<h2>Quay thử {lab} là gì</h2><p>Trang mô phỏng một buổi quay {lab} ({name}) trên trình duyệt: các giải lần lượt hiện ra theo đúng thứ tự và số chữ số như buổi quay thật, số đang quay nhảy liên tục rồi dừng lại. Chế độ <b>Như thật</b> giữ nhịp gần với buổi quay thật ({real}); chế độ Nhanh và Vừa để xem trọn bảng trong ít phút.</p>'
        + f'<p>Mỗi lần quay là một lần chọn ngẫu nhiên mới, độc lập với mọi kỳ trước và sau. Kết quả thật của {lab} có tại <a href="../../{reg}/">{lab} hôm nay</a>, hoặc theo dõi từng giải trong giờ quay {tm} tại <a href="../../truc-tiep-{reg}/">Trực tiếp {lab}</a>. Muốn xem một cách chơi lãi hay lỗ qua hàng trăm kỳ đã quay, hãy dùng <a href="../#simCard">Mô phỏng cách chơi</a>.</p>'
        + f'<script>window.QT={json.dumps({"reg": "mb" if reg == "xsmb" else reg[2:], "sched": sched}, ensure_ascii=False)}</script><script>{QT_JS}</script>')
    page(p, f"Quay thử {lab} – mô phỏng quay số {name} như thật", f"Quay thử {lab}: mô phỏng buổi quay xổ số {name} trên trình duyệt, số nhảy và ra từng giải như thật, chọn tốc độ Nhanh, Vừa hoặc Như thật. Số ngẫu nhiên, không phải dự đoán.", [("Mô phỏng", "mo-phong/"), (f"Quay thử {lab}", p)], f"Quay thử {lab}", body)

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
<li>Trình bày dữ liệu thống kê từ kết quả đã quay: lô gan, tần suất, đầu đuôi, giải đặc biệt, 3 càng, 4 càng; công cụ dò vé và tra cứu nhóm số.</li>
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
<li><b>Email:</b> <!--email_off--><a href="mailto:{shell.EMAIL}">{shell.EMAIL}</a><!--/email_off--> – góp ý, báo lỗi kết quả, đề xuất tính năng.</li>
<li><b>Website:</b> <a href="{BASE}">xslab.live</a></li></ul>
<h2>Khi báo lỗi kết quả</h2>
<p>Để sửa nhanh, vui lòng ghi rõ: miền hoặc đài (ví dụ XSMB, Vĩnh Long), ngày quay, giải bị sai, con số đang hiển thị và con số đúng kèm nguồn (trang của công ty xổ số kiến thiết hoặc Vietlott).</p>
<h2>Lưu ý</h2><ul>
<li>XS Lab không bán vé, không nhận đặt cược, không cung cấp số dự đoán và không bao giờ yêu cầu chuyển tiền. Mọi lời mời chào như vậy nhân danh XS Lab đều là giả mạo.</li>
<li>Về lĩnh thưởng, vé trúng hay tranh chấp liên quan đến vé, vui lòng liên hệ trực tiếp công ty xổ số kiến thiết phát hành vé hoặc Vietlott.</li></ul>
<p class="note">{NOTICE}</p></div>"""),
 ("cai-dat-app/", "WebPage", "Cài app XS Lab – xem kết quả xổ số không quảng cáo trên điện thoại", "Hướng dẫn cài XS Lab lên màn hình chính iPhone và Android: mở nhanh như app, toàn màn hình, không quảng cáo, miễn phí, không cần tải từ kho ứng dụng.", "Cài app XS Lab", "Cài XS Lab lên điện thoại", f"""<div class="card doc">
<p>XS Lab có thể cài lên màn hình chính điện thoại như một ứng dụng: chạm biểu tượng là mở ngay kết quả xổ số, toàn màn hình, không thanh địa chỉ, không quảng cáo. Không cần tải từ App Store hay Google Play, không tốn dung lượng và luôn là bản mới nhất.</p>
<p><button type="button" class="cta" id="pwaGo" hidden>Cài XS Lab ngay</button></p><style>#pwaGo[hidden]{{display:none!important}}.bens{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin:14px 0 18px}}.ben{{border:1px solid var(--line,#e4e1db);border-radius:14px;padding:12px 14px;background:var(--band,#f1efea)}}.ben b{{display:block;font-size:15px;margin-bottom:3px}}.ben b:before{{content:"✓ ";color:var(--red)}}.ben span{{font-size:14px;color:var(--mute,#6b6775);line-height:1.5}}</style><h2>Cài một lần, trải nghiệm trọn vẹn</h2><div class="bens"><div class="ben"><b>Cài một lần, dùng mãi</b><span>Mất chưa tới 30 giây. Từ đó chạm biểu tượng XS Lab là vào thẳng kết quả, không cần tìm kiếm hay gõ địa chỉ.</span></div><div class="ben"><b>Luôn là bản mới nhất</b><span>Không cần cập nhật. Tính năng mới và kết quả mới có ngay mỗi lần mở.</span></div><div class="ben"><b>Nhẹ, gần như không tốn dung lượng</b><span>Không có tệp cài đặt lớn, phù hợp cả điện thoại đời cũ và máy đã đầy bộ nhớ.</span></div><div class="ben"><b>Toàn màn hình, gọn như ứng dụng</b><span>Không thanh địa chỉ, không tab trình duyệt. Chỉ có kết quả, trực tiếp, dò vé và thống kê.</span></div><div class="ben"><b>Không quảng cáo, không soi cầu</b><span>Trải nghiệm sạch như trên web: chỉ có kết quả và dữ liệu đã quay.</span></div><div class="ben"><b>Giữ nguyên các cài đặt của bạn</b><span>Vé của tôi, đài mặc định, miền mặc định, giao diện sáng tối: đặt một lần, lần sau mở là có sẵn.</span></div><div class="ben"><b>Không cần tài khoản, không xin quyền</b><span>Không đăng ký, không truy cập danh bạ, ảnh hay vị trí. Dữ liệu bạn lưu chỉ nằm trên máy của bạn.</span></div><div class="ben"><b>Cùng một XS Lab ở mọi nơi</b><span>Trên điện thoại, máy tính bảng hay máy tính đều cùng giao diện, cùng dữ liệu, chuyển qua lại không phải làm quen lại.</span></div></div>
<style>.stps{{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin:12px 0 6px}}.stp{{margin:0;text-align:center}}.stp img{{width:100%;max-width:200px;height:auto;display:block;margin:0 auto 8px;filter:drop-shadow(0 4px 10px rgba(0,0,0,.18))}}.stp figcaption{{font-size:14px;line-height:1.45}}.stp b{{display:block;color:var(--red)}}</style><h2>iPhone, iPad (Safari)</h2><div class="stps"><figure class="stp"><img src="../assets/cai-app/ios-1.svg" width="240" height="440" alt="Bước 1: Mở xslab.live bằng Safari, bấm nút Chia sẻ ở thanh dưới." loading="lazy"><figcaption><b>Bước 1</b> Mở xslab.live bằng Safari, bấm nút <b style="display:inline;color:inherit">Chia sẻ</b> ở thanh dưới.</figcaption></figure><figure class="stp"><img src="../assets/cai-app/ios-2.svg" width="240" height="440" alt="Bước 2: Kéo xuống, chọn Thêm vào MH chính." loading="lazy"><figcaption><b>Bước 2</b> Kéo xuống, chọn <b style="display:inline;color:inherit">Thêm vào MH chính</b>.</figcaption></figure><figure class="stp"><img src="../assets/cai-app/ios-3.svg" width="240" height="440" alt="Bước 3: Bấm Thêm ở góc trên bên phải." loading="lazy"><figcaption><b>Bước 3</b> Bấm <b style="display:inline;color:inherit">Thêm</b> ở góc trên bên phải.</figcaption></figure><figure class="stp"><img src="../assets/cai-app/xong.svg" width="240" height="440" alt="Bước 4: Xong. Chạm biểu tượng XS Lab trên màn hình chính để mở." loading="lazy"><figcaption><b>Bước 4</b> Xong. Chạm biểu tượng XS Lab trên màn hình chính để mở.</figcaption></figure></div><p class="note">Nếu đang mở XS Lab trong Zalo, Facebook hay Messenger, hãy bấm dấu ba chấm và chọn <b>Mở bằng Safari</b> trước, vì trình duyệt trong các ứng dụng này không có chức năng thêm vào màn hình chính. Trên iPhone, Chrome cũng làm được: bấm nút Chia sẻ cạnh thanh địa chỉ rồi chọn Thêm vào MH chính.</p><h2>Android (Chrome)</h2><div class="stps"><figure class="stp"><img src="../assets/cai-app/android-1.svg" width="240" height="440" alt="Bước 1: Mở xslab.live bằng Chrome, bấm dấu ⋮ góc trên bên phải." loading="lazy"><figcaption><b>Bước 1</b> Mở xslab.live bằng Chrome, bấm dấu <b style="display:inline;color:inherit">⋮</b> góc trên bên phải.</figcaption></figure><figure class="stp"><img src="../assets/cai-app/android-2.svg" width="240" height="440" alt="Bước 2: Chọn Cài đặt ứng dụng (hoặc Thêm vào màn hình chính)." loading="lazy"><figcaption><b>Bước 2</b> Chọn <b style="display:inline;color:inherit">Cài đặt ứng dụng</b> (hoặc Thêm vào màn hình chính).</figcaption></figure><figure class="stp"><img src="../assets/cai-app/android-3.svg" width="240" height="440" alt="Bước 3: Bấm Cài đặt để xác nhận." loading="lazy"><figcaption><b>Bước 3</b> Bấm <b style="display:inline;color:inherit">Cài đặt</b> để xác nhận.</figcaption></figure><figure class="stp"><img src="../assets/cai-app/xong.svg" width="240" height="440" alt="Bước 4: Xong. XS Lab có trên màn hình chính như ứng dụng." loading="lazy"><figcaption><b>Bước 4</b> Xong. XS Lab có trên màn hình chính như ứng dụng.</figcaption></figure></div><p class="note">Nếu thấy nút <b>Cài đặt</b> màu đỏ trên XS Lab hoặc ở đầu trang này, bấm vào đó là cài ngay, không cần làm theo các bước trên.</p><h2>Câu hỏi thường gặp</h2><ul>
<li><b>Có mất phí không?</b> Không. XS Lab miễn phí và không quảng cáo.</li>
<li><b>Có cần cập nhật không?</b> Không. Mỗi lần mở là bản mới nhất, kết quả cập nhật ngay sau giờ quay.</li>
<li><b>Có truy cập dữ liệu trên điện thoại không?</b> Không. XS Lab không yêu cầu quyền truy cập danh bạ, ảnh hay vị trí; số bạn lưu trong Vé của tôi chỉ nằm trên chính máy của bạn.</li>
<li><b>Gỡ thế nào?</b> Nhấn giữ biểu tượng XS Lab và chọn Xoá, như mọi ứng dụng khác.</li></ul>
<p class="note">{NOTICE}</p></div>
<script>(function(){{var b=document.getElementById('pwaGo'),e=null;window.addEventListener('beforeinstallprompt',function(x){{x.preventDefault();e=x;b.hidden=false}});b.onclick=function(){{if(e){{e.prompt();e=null;b.hidden=true}}}}}})();</script>"""),
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
core = [BASE] + [BASE + s + "/" for s in spa] + [BASE + x[0] for x in INFO_PAGES] + [BASE + "so/"] + [BASE + f"mo-phong/quay-thu-{r}/" for r in REG]
for reg in list(REG) + ["thong-ke", "so"]:
    for x in sorted(os.listdir(os.path.join(ROOT, reg))):
        if re.match(r"\d{2}-\d{2}-\d{4}$", x) or x.startswith("thang-"): continue
        if os.path.isfile(os.path.join(ROOT, reg, x, "index.html")): core.append(f"{BASE}{reg}/{x}/")
today = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=7))).strftime('%Y-%m-%dT%H:%M:%S+07:00')
def wsm(fn, items):
    data = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f' <url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n' for u, d in items) + '</urlset>\n'
    fp = os.path.join(ROOT, fn)
    if not os.path.exists(fp) or open(fp).read() != data: open(fp, "w").write(data)
    return len(items)
_info = {BASE + x[0] for x in INFO_PAGES}
# Sitemap gọn cho tên miền mới: trang chính đầy đủ; trang ngày 3 miền 12 tháng gần nhất; trang từng đài theo ngày
# và Vietlott từng kỳ 6 tháng gần nhất. Trang cũ hơn vẫn để nguyên, vẫn cho lập chỉ mục (không noindex), chỉ không đưa vào sitemap.
_d0 = datetime.date.today()
CUT_DAY = (_d0 - datetime.timedelta(days=365)).isoformat()
CUT_SUB = (_d0 - datetime.timedelta(days=183)).isoformat()
_isday = re.compile(r"/\d{2}-\d{2}-\d{4}/$")
def _keep_arch(it): return not _isday.search(it[0]) or it[1][:10] >= CUT_DAY
SM = {"sitemap-chinh.xml": [(u, "2026-11-24" if u in _info else today) for u in core],
      "sitemap-vietlott.xml": [it for it in SITEMAP_VL if "/ky-" not in it[0] or it[1][:10] >= CUT_SUB]}
for reg in REG: SM[f"sitemap-{reg}.xml"] = [it for it in SITEMAP_ARCH[reg] if _keep_arch(it)] + [it for it in STATION_SM.get(reg, []) if it[1][:10] >= CUT_SUB]
tot = 0
for fn, items in SM.items(): tot += wsm(fn, items)
idx = '<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f' <sitemap><loc>{BASE}{fn}</loc><lastmod>{max(d for _, d in items)}</lastmod></sitemap>\n' for fn, items in SM.items()) + '</sitemapindex>\n'
open(os.path.join(ROOT, "sitemap.xml"), "w").write(idx)
print("sitemap:", tot, "URL trong", len(SM), "tệp")

# ---- Trang 404 (GitHub Pages trả về khi không có trang) + llms.txt ----
import shutil
_tmp = "khong-tim-thay-tmp/"
page(_tmp, "Không tìm thấy trang", "Trang bạn tìm không có trên XS Lab.", [("Không tìm thấy trang", _tmp)], "Không tìm thấy trang",
     '<div class="card doc"><p>Đường dẫn này không có trên XS Lab, có thể trang đã đổi địa chỉ hoặc gõ nhầm.</p>'
     '<p><a href="/">Kết quả xổ số hôm nay</a> · <a href="/xsmb/">XSMB</a> · <a href="/xsmn/">XSMN</a> · <a href="/xsmt/">XSMT</a> · '
     '<a href="/xsmb/so-ket-qua/">Sổ kết quả theo ngày</a> · <a href="/so/">Thống kê 100 số</a></p></div>')
_h = open(os.path.join(ROOT, _tmp, "index.html")).read()
_h = _h.replace('href="../', 'href="/').replace('src="../', 'src="/')
_h = re.sub(r'<link rel="canonical"[^>]*>', '<meta name="robots" content="noindex">', _h)
_fp = os.path.join(ROOT, "404.html")
if not os.path.exists(_fp) or open(_fp).read() != _h: open(_fp, "w").write(_h)
shutil.rmtree(os.path.join(ROOT, _tmp), ignore_errors=True)

LLMS = f"""# XS Lab

> XS Lab (xslab.live) là trang kết quả xổ số Việt Nam và thống kê dữ liệu quá khứ, không quảng cáo, không dự đoán. Có kết quả XSMB, XSMN, XSMT, Vietlott (Keno, Mega 6/45, Power 6/55, Max 3D, Max 3D Pro), trực tiếp giờ quay, dò vé và các bảng thống kê lô tô.

Mọi số liệu trên trang là thống kê kết quả đã quay. Trang không đưa ra dự đoán hay gợi ý số. Kết quả nên được đối chiếu với kết quả chính thức của công ty xổ số kiến thiết.

## Kết quả

- [Kết quả xổ số hôm nay]({BASE}): XSMB, XSMN, XSMT mới nhất
- [XSMB]({BASE}xsmb/): kết quả xổ số miền Bắc
- [XSMN]({BASE}xsmn/): kết quả xổ số miền Nam
- [XSMT]({BASE}xsmt/): kết quả xổ số miền Trung
- [Trực tiếp xổ số]({BASE}truc-tiep/): cập nhật trong giờ quay
- [Sổ kết quả XSMB]({BASE}xsmb/so-ket-qua/), [XSMN]({BASE}xsmn/so-ket-qua/), [XSMT]({BASE}xsmt/so-ket-qua/): kết quả theo ngày và theo tháng
- [Dò vé số]({BASE}do-ve/)

## Thống kê

- [Thống kê 100 số]({BASE}so/): số lần về, số kỳ chưa về, kỷ lục gan của từng số 00–99
- [Thống kê lô tô]({BASE}thong-ke/)

## Dữ liệu

- [Lịch sử XSMB (CSV)]({BASE}xsmb.csv)
- [Lịch sử XSMN (CSV)]({BASE}xsmn.csv)
- [Lịch sử XSMT (CSV)]({BASE}xsmt.csv)
- [Sitemap]({BASE}sitemap.xml)

## Thông tin

- [Giới thiệu]({BASE}gioi-thieu/)
- [Liên hệ]({BASE}lien-he/)
- [Điều khoản sử dụng]({BASE}dieu-khoan-su-dung/)
"""
_fp = os.path.join(ROOT, "llms.txt")
if not os.path.exists(_fp) or open(_fp).read() != LLMS: open(_fp, "w").write(LLMS)

# Trang đài-ngày quá 365 ngày không còn được dựng lại: thay bằng trang chuyển hướng
# sang trang kết quả cả miền cùng ngày, để không còn bản cũ lệch giao diện, lệch bảo mật.
_RD_MARK = "<!--xslab-redirect-->"
for _reg in ("xsmn", "xsmt"):
    _rb = os.path.join(ROOT, _reg)
    _iso = lambda x: f"{x[6:10]}-{x[3:5]}-{x[0:2]}"
    _ds = [_iso(x) for x in os.listdir(_rb) if re.match(r"^\d{2}-\d{2}-\d{4}$", x)]
    if not _ds: continue
    _cut = (datetime.date.fromisoformat(max(_ds)) - datetime.timedelta(days=367)).isoformat()
    for _st in sorted(os.listdir(_rb)):
        _sd = os.path.join(_rb, _st)
        if not os.path.isdir(_sd) or re.match(r"^\d{2}-\d{2}-\d{4}$", _st): continue
        for _dd in os.listdir(_sd):
            m = re.match(r"^(\d{2})-(\d{2})-(\d{4})$", _dd)
            _f = os.path.join(_sd, _dd, "index.html")
            if not m or not os.path.exists(_f): continue
            if _iso(_dd) >= _cut: continue
            _txt = open(_f, encoding="utf-8").read()
            if _RD_MARK in _txt or _iso(_dd) >= _cut: continue
            _to = f"{BASE}{_reg}/{_dd}/"
            if not os.path.exists(os.path.join(_rb, _dd, "index.html")): _to = f"{BASE}{_reg}/{_st}/"
            open(_f, "w", encoding="utf-8").write(f'<!DOCTYPE html><html lang="vi"><head><meta charset="utf-8">{_RD_MARK}<meta name="robots" content="noindex,follow"><link rel="canonical" href="{_to}"><meta http-equiv="refresh" content="0;url={_to}"><title>Chuyển tới kết quả ngày {_dd}</title></head><body><p>Trang này đã chuyển tới <a href="{_to}">{_to}</a>.</p></body></html>')


# Viết sẵn kết quả mới nhất vào HTML các trang ứng dụng (để Google đọc được không cần chạy JavaScript).
def _ssr_blocks():
    def lj(fn):
        try: return json.load(open(os.path.join(ROOT, fn), encoding="utf-8"))
        except Exception: return []
    MB = sorted(lj("recent.json"), key=lambda r: r["date"])
    MNT = {"mn": lj("recent_mn.json"), "mt": lj("recent_mt.json")}
    NAME = {"mb": ("XSMB", "miền Bắc", "xsmb"), "mn": ("XSMN", "miền Nam", "xsmn"), "mt": ("XSMT", "miền Trung", "xsmt")}
    def block(reg, back=0):
        lab, name, sl = NAME[reg]
        if reg == "mb":
            if len(MB) <= back: return ""
            r = MB[-1 - back]; d = r["date"]
            intro = f'Giải Đặc biệt <b>{esc(r["db"][0])}</b>, giải Nhất <b>{esc(r["g1"][0])}</b>.'
            tb = mb_table(r)
        else:
            rows = MNT[reg]; ds = sorted({x["date"] for x in rows})
            if len(ds) <= back: return ""
            d = ds[-1 - back]; recs = sorted([x for x in rows if x["date"] == d], key=lambda x: ST.get(x["station"], x["station"]))
            intro = "Giải Đặc biệt: " + "; ".join(f'{esc(ST.get(x["station"], x["station"]))} <b>{esc(x["db"][0])}</b>' for x in recs) + "."
            tb = mn_table(recs)
        dd = slug_d(d)
        return (f'<h2>{lab} {WDL[wdi(d)]} {vn(d)} – Kết quả xổ số {name} ngày {vn(d)}</h2><p>{intro} '
                f'<a href="/{sl}/{dd}/">Xem đủ giải, lô tô và thống kê {lab} {vn(d)}</a></p><div class="card">{tb}</div>')
    M = {"": [("mb", 0), ("mn", 0), ("mt", 0)], "xsmb/": [("mb", 0)], "xsmn/": [("mn", 0)], "xsmt/": [("mt", 0)],
         "xsmb-hom-qua/": [("mb", 1)], "xsmn-hom-qua/": [("mn", 1)], "xsmt-hom-qua/": [("mt", 1)],
         "xsmb-30-ngay/": [("mb", 0)], "xsmn-30-ngay/": [("mn", 0)], "xsmt-30-ngay/": [("mt", 0)],
         "xsmb-90-ngay/": [("mb", 0)], "xsmn-90-ngay/": [("mn", 0)], "xsmt-90-ngay/": [("mt", 0)],
         "truc-tiep/": [("mn", 0), ("mt", 0), ("mb", 0)], "truc-tiep-xsmb/": [("mb", 0)], "truc-tiep-xsmn/": [("mn", 0)], "truc-tiep-xsmt/": [("mt", 0)],
         "do-ve/": [("mb", 0), ("mn", 0), ("mt", 0)]}
    return {k: '<div class="ssr">' + "".join(block(r, b) for r, b in v) + "</div>" for k, v in M.items()}
_SSR = _ssr_blocks()
def ssr_apply(pth, h):
    blk = _SSR.get(pth)
    h = re.sub(r"<!--ssr-->.*?<!--/ssr-->", "", h, flags=re.S)
    if not blk: return h
    tgt = '<div id="lvBoard">' if pth.startswith("truc-tiep") else '<div id="rsBoard">'
    if tgt not in h: return h
    return h.replace(tgt, tgt + "<!--ssr-->" + blk + "<!--/ssr-->", 1)

# Áp tiêu đề SEO cho các trang ứng dụng (SPA) và ghi danh sách trang cho trang quản trị.
def _spa_seo():
    lst = os.path.join(ROOT, "tools", "spa_pages.txt")
    paths = [""] + ([l.strip().strip("/") + "/" for l in open(lst, encoding="utf-8") if l.strip()] if os.path.exists(lst) else [])
    rows = []
    for pth in paths:
        fp = os.path.join(ROOT, pth, "index.html")
        if not os.path.exists(fp): continue
        h = open(fp, encoding="utf-8").read()
        m = re.search(r"<!--seo-default:(.*?)-->", h)
        if m:
            dflt = json.loads(html.unescape(m.group(1)))
        else:
            t = re.search(r"<title>(.*?)</title>", h, re.S); dm = re.search(r'<meta name="description" content="([^"]*)"', h)
            if not t: continue
            dflt = {"title": html.unescape(re.sub(r"\s*\|\s*XS Lab\s*$", "", t.group(1).strip())), "desc": html.unescape(dm.group(1)) if dm else ""}
            h = h.replace("<head>", "<head><!--seo-default:" + esc(json.dumps(dflt, ensure_ascii=False)) + "-->", 1)
        o = (CFG.get("seo_trang") or {}).get(pth) or {}
        ti = str(o.get("title", "")).strip() or dflt["title"]; de = str(o.get("desc", "")).strip() or dflt["desc"]
        h2 = re.sub(r"<title>.*?</title>", lambda _: "<title>" + esc(ti) + " | XS Lab</title>", h, count=1, flags=re.S)
        for pat, val in ((r'(<meta name="description" content=")[^"]*(")', de), (r'(<meta property="og:title" content=")[^"]*(")', ti), (r'(<meta property="og:description" content=")[^"]*(")', de), (r'(<meta name="twitter:title" content=")[^"]*(")', ti), (r'(<meta name="twitter:description" content=")[^"]*(")', de)):
            h2 = re.sub(pat, lambda mm: mm.group(1) + esc(val) + mm.group(2), h2, count=1)
        h2 = ssr_apply(pth, h2)
        if h2 != h or not m: open(fp, "w", encoding="utf-8").write(h2)
        rows.append({"path": pth, "loai": "Trang chính", "title": dflt["title"], "desc": dflt["desc"]})
    for pth, (t, d) in sorted(SEO_DEF.items()):
        if (pth.startswith("so/") and pth != "so/") or re.search(r"/(ky-\d+|nam-\d+|thang-\d+-\d+)/$", pth): continue
        rows.append({"path": pth, "loai": "Trang thống kê, thông tin", "title": t, "desc": d})
    os.makedirs(os.path.join(ROOT, "admin"), exist_ok=True)
    data = json.dumps({"trang": rows}, ensure_ascii=False, indent=0)
    fp = os.path.join(ROOT, "admin", "pages.json")
    if not os.path.exists(fp) or open(fp, encoding="utf-8").read() != data: open(fp, "w", encoding="utf-8").write(data)
_spa_seo()
