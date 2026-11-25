# Khung giao diện dùng chung cho ứng dụng (build.py) và các trang tĩnh (make_pages.py):
# menu trên cùng, thanh bên, thanh tab điện thoại, chân trang, CSS và biểu tượng.
import json
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><symbol id="i-home" viewBox="0 0 24 24"><path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6h-6v6H4a1 1 0 0 1-1-1z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol><symbol id="i-target" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="12" cy="12" r="1.3" fill="currentColor"/></symbol><symbol id="i-book" viewBox="0 0 24 24"><path d="M5 4h11a3 3 0 0 1 3 3v13H8a3 3 0 0 1-3-3z M5 17a3 3 0 0 1 3-3h11" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol><symbol id="i-wallet" viewBox="0 0 24 24"><rect x="3" y="6" width="18" height="13" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M16 12.5h5M6 6l9-3 1 3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></symbol><symbol id="i-chart" viewBox="0 0 24 24"><path d="M4 20V4M4 20h16M8 16l4-5 3 3 5-7" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol><symbol id="i-grid" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="4" width="6.5" height="6.5" rx="1.5"/><rect x="4" y="13.5" width="6.5" height="6.5" rx="1.5"/><rect x="13.5" y="13.5" width="6.5" height="6.5" rx="1.5"/></g></symbol><symbol id="i-stats" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M5 20V11M10 20V5M15 20v-7M20 20V8"/></g></symbol><symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 11v6M12 7.5v.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></symbol><symbol id="i-more" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 6.5h16M4 12h16M4 17.5h10"/></g></symbol><symbol id="i-live" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="2.2" fill="currentColor"/><path d="M8 8a5.6 5.6 0 0 0 0 8M16 8a5.6 5.6 0 0 1 0 8M5 5a9.9 9.9 0 0 0 0 14M19 5a9.9 9.9 0 0 1 0 14"/></g></symbol><symbol id="i-ticket" viewBox="0 0 24 24"><path d="M4 7.5A1.5 1.5 0 0 1 5.5 6h13A1.5 1.5 0 0 1 20 7.5V10a2 2 0 0 0 0 4v2.5a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 16.5V14a2 2 0 0 0 0-4z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M14 6.5v11" stroke="currentColor" stroke-width="1.6" stroke-dasharray="2 2"/></symbol><symbol id="i-vl" viewBox="0 0 24 24"><g fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="8" cy="8" r="4"/><circle cx="16" cy="8" r="4"/><circle cx="12" cy="16" r="4"/></g></symbol><symbol id="i-moon" viewBox="0 0 24 24"><path d="M19 14.5A7.5 7.5 0 0 1 9.5 5a7.5 7.5 0 1 0 9.5 9.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></symbol></svg>'
EMAIL = "lienhe@xslab.live"
NOTICE = "Thông tin và kết quả xổ số trên XS Lab được chúng tôi cập nhật từ nguồn công khai và chỉ mang tính chất tham khảo. Vui lòng kiểm tra lại kết quả chính thức được công bố bởi các công ty xổ số kiến thiết."


def _reg(c, n):
    return [("", f"{n} hôm nay", f"{c}/"), ("", f"Trực tiếp {n}", f"truc-tiep-{c}/"), ("", f"{n} hôm qua", f"{c}-hom-qua/"), ("", f"{n} 30 ngày", f"{c}-30-ngay/"), ("", f"{n} 90 ngày", f"{c}-90-ngay/"),
            ("", f"Sổ kết quả {n}", f"{c}/so-ket-qua/"), ("", f"Quay thử {n}", f"mo-phong/quay-thu-{c}/"), ("h", "Thống kê", ""), ("", f"Thống kê {n} 30 kỳ", f"thong-ke/30-ky-{c}/"),
            ("", f"Giải đặc biệt {n}", f"thong-ke/giai-dac-biet-{c}/"), ("", f"3 càng {n}", f"thong-ke/3-cang-{c}/")]


MENU = [
    ("XSMB", _reg("xsmb", "XSMB")[:9] + [("", "Lô gan XSMB", "thong-ke/lo-gan-xsmb/"), ("", "Giải đặc biệt XSMB", "thong-ke/giai-dac-biet-xsmb/"), ("", "3 càng XSMB", "thong-ke/3-cang-xsmb/"), ("", "Thống kê nhóm số XSMB", "thong-ke-dan-xsmb/")]),
    ("XSMN", _reg("xsmn", "XSMN") + [("", "Giải 8 XSMN", "thong-ke/giai-8-xsmn/"), ("", "Thống kê nhóm số XSMN", "thong-ke-dan-xsmn/")]),
    ("XSMT", _reg("xsmt", "XSMT") + [("", "Giải 8 XSMT", "thong-ke/giai-8-xsmt/"), ("", "Thống kê nhóm số XSMT", "thong-ke-dan-xsmt/")]),
    ("Vietlott", [("", "Keno", "keno/"), ("", "Mega 6/45", "mega-645/"), ("", "Power 6/55", "power-655/"), ("", "Max 3D, Max 3D+", "max-3d/"), ("", "Max 3D Pro", "max-3d-pro/"), ("", "Tất cả Vietlott", "vietlott/")]),
    ("Thống kê", [("", "Tra cứu số 00–99", "so/"), ("", "Bảng thống kê", "thong-ke/bang-thong-ke/"), ("", "Thống kê lô tô", "thong-ke/"), ("", "Lô gan XSMB", "thong-ke/lo-gan-xsmb/"), ("", "Tần suất lô tô", "thong-ke/tan-suat-lo-to-xsmb/"), ("", "Đầu đuôi", "thong-ke/dau-duoi-xsmb/"), ("", "Giải nhất", "thong-ke/giai-nhat-xsmb/"), ("", "Lô kép", "thong-ke/lo-kep-xsmb/"), ("", "Số đảo", "thong-ke/so-dao-xsmb/"), ("", "Số gánh", "thong-ke/so-ganh-xsmb/"), ("", "Tổng, chẵn lẻ ĐB", "thong-ke/tong-chan-le-dac-biet-xsmb/"), ("h", "Công cụ", ""), ("", "Thống kê nhóm số, 3 càng", "thong-ke-dan/"), ("", "Bản đồ số", "ban-do-so/")]),
    ("Mô phỏng", [("", "Quay thử XSMB", "mo-phong/quay-thu-xsmb/"), ("", "Quay thử XSMN", "mo-phong/quay-thu-xsmn/"), ("", "Quay thử XSMT", "mo-phong/quay-thu-xsmt/"), ("", "Mô phỏng cách chơi", "mo-phong/"), ("", "Kiểm định ngẫu nhiên", "kiem-dinh/")]),
]


def menu_html(up, cur=""):
    o = ['<nav class="mbar" aria-label="Menu chính"><div class="mrow">']
    for lab, items in MENU:
        here = any(u and u == cur for _, _, u in items)
        hub = {"XSMB": "xsmb/", "XSMN": "xsmn/", "XSMT": "xsmt/", "Vietlott": "vietlott/", "Thống kê": "thong-ke/", "Mô phỏng": "mo-phong/"}.get(lab, "")
        o.append('<details' + (' class="is-cur"' if here else '') + (f' data-href="{up}{hub}"' if hub else '') + f'><summary>{lab}</summary><div class="mdd">')
        for k, t, u in items:
            if k == "h":
                o.append(f'<span class="h">{t}</span>')
            else:
                o.append(f'<a href="{up}{u}"' + (' aria-current="page"' if u == cur else '') + f'>{t}</a>')
        o.append('</div></details>')
    o.append('</div>')
    o.append(f'<a class="dv" href="{up}do-ve/"' + (' aria-current="page"' if cur == "do-ve/" else '') + '>Dò vé</a></nav>')
    return ''.join(o)


LOGO = '<svg width="38" height="38" viewBox="0 0 42 42" aria-hidden="true"><defs><radialGradient id="lg1" cx=".32" cy=".28"><stop offset="0" stop-color="#ff8a9b"/><stop offset=".55" stop-color="#d01f3c"/><stop offset="1" stop-color="#8f1027"/></radialGradient><radialGradient id="lg2" cx=".32" cy=".28"><stop offset="0" stop-color="#fff"/><stop offset=".6" stop-color="#e9e7e3"/><stop offset="1" stop-color="#b9b5ae"/></radialGradient></defs><circle cx="15" cy="17" r="12" fill="url(#lg1)"/><circle cx="29" cy="27" r="10" fill="url(#lg2)"/><text x="15" y="21.5" font-size="11" font-weight="700" fill="#fff" text-anchor="middle" font-family="sans-serif">XS</text></svg>'


def home(up):
    return up if up and up != "/*R*/" else (up + "./")


def brand(up):
    return f'<a class="brand" href="{home(up)}" aria-label="XS Lab – về trang chủ">{LOGO}<div><b>XS Lab</b><span>Kết quả &amp; thống kê xổ số</span></div></a>'


def mhead(up, ic="#"):
    return f'<header class="mhead"><a class="mlogo" href="{home(up)}" aria-label="XS Lab – về trang chủ">{LOGO.replace("lg1", "mg1").replace("lg2", "mg2")}<b>XS Lab</b></a><button class="mtheme" type="button" aria-label="Đổi giao diện sáng tối"><svg aria-hidden="true"><use href="{ic}i-moon"/></svg></button></header>'


SIDE = [("Xổ số kiến thiết", [("Kết quả xổ số", "", "i-home"), ("Trực tiếp xổ số", "truc-tiep/", "i-live"), ("Dò vé số", "do-ve/", "i-ticket")]),
        ("Vietlott", [("Keno", "keno/", "i-vl"), ("Mega 6/45", "mega-645/", "i-vl"), ("Power 6/55", "power-655/", "i-vl"), ("Max 3D", "max-3d/", "i-vl"), ("Max 3D Pro", "max-3d-pro/", "i-vl")]),
        ("Thống kê", [("Thống kê lô tô", "thong-ke/", "i-stats"), ("Bảng thống kê", "thong-ke/bang-thong-ke/", "i-book"), ("Thống kê nhóm số", "thong-ke-dan/", "i-target"), ("Bản đồ số", "ban-do-so/", "i-grid"), ("Kiểm định", "kiem-dinh/", "i-chart"), ("Mô phỏng", "mo-phong/", "i-wallet")]),
        ("Thông tin", [("Giới thiệu", "gioi-thieu/", "i-info"), ("Liên hệ", "lien-he/", "i-info")])]


def _side_cur(cur, u):
    if not cur or not u:
        return False
    if cur == u:
        return True
    if u == "thong-ke/":
        return cur.startswith("thong-ke/") and not cur.startswith("thong-ke/bang-thong-ke/")
    return cur.startswith(u)


def side_html(up, cur="", ic="#"):
    nav = ''.join(f'<h3>{g}</h3>' + ''.join((f'<a href="{up}{u}"' if u else f'<a href="{home(up)}"') + (' aria-current="page"' if _side_cur(cur, u) else '') + f'><svg aria-hidden="true"><use href="{ic}{i}"/></svg><span>{t}</span></a>' for t, u, i in it) for g, it in SIDE)
    return f'<aside class="side">{brand(up)}<nav class="nav" aria-label="Điều hướng chính">{nav}</nav><div class="side-foot"><button class="themebtn" type="button">Giao diện: Tự động</button></div></aside>'


def tab_html(up, cur="", ic="#"):
    T = [("Kết quả", "", "i-home"), ("Trực tiếp", "truc-tiep/", "i-live"), ("Vietlott", "vietlott/", "i-vl"), ("Dò vé", "do-ve/", "i-ticket"), ("Thống kê", "thong-ke/", "i-stats")]
    return '<nav class="tab" aria-label="Điều hướng">' + ''.join((f'<a href="{up}{u}"' if u else f'<a href="{home(up)}"') + (' aria-current="page"' if cur and u and cur.startswith(u) else '') + f'><svg aria-hidden="true"><use href="{ic}{i}"/></svg><span>{t}</span></a>' for t, u, i in T) + '</nav>'


SUBNAV_WD = [("thu-2", "Thứ 2"), ("thu-3", "Thứ 3"), ("thu-4", "Thứ 4"), ("thu-5", "Thứ 5"), ("thu-6", "Thứ 6"), ("thu-7", "Thứ 7"), ("chu-nhat", "Chủ nhật")]
def subnav_items(sl):
    S = sl.upper()
    return [(f"{sl}/", f"{S} hôm nay"), (f"truc-tiep-{sl}/", "Trực tiếp"), (f"{sl}-hom-qua/", "Hôm qua")] + \
        [(f"{sl}/{a}/", b) for a, b in SUBNAV_WD] + [(f"{sl}-30-ngay/", "30 ngày"), (f"{sl}-90-ngay/", "90 ngày"), (f"{sl}/so-ket-qua/", "Sổ kết quả"), (f"thong-ke/30-ky-{sl}/", "Thống kê 30 kỳ")]
def subnav_html(sl, up, cur=""):
    return f'<nav class="subnav" id="subNav" aria-label="Mục {sl.upper()}">' + "".join(
        f'<a href="{up}{u}"' + (' aria-current="page"' if u == cur else "") + f'>{t}</a>' for u, t in subnav_items(sl)) + "</nav>"

def footer_html(up, year="2026"):
    def L(items):
        return '<ul>' + ''.join(f'<li><a href="{up}{u}">{t}</a></li>' for t, u in items) + '</ul>'
    return f"""<footer class="foot" id="siteFoot"><div class="fgrid">
<div class="fsrc"><h2>Thông tin nguồn</h2><p>{NOTICE}</p><p>XS Lab chỉ trình bày kết quả và thống kê dữ liệu đã quay, không đưa ra dự đoán kết quả.</p><p>Liên hệ: <!--email_off--><a href="mailto:{EMAIL}">{EMAIL}</a><!--/email_off--> · <a href="{up}lien-he/">Trang liên hệ</a></p></div>
<nav aria-label="Kết quả và thống kê"><h2>Kết quả &amp; thống kê</h2>{L([("Kết quả XSMB","xsmb/"),("Kết quả XSMN","xsmn/"),("Kết quả XSMT","xsmt/"),("Trực tiếp XSMB","truc-tiep-xsmb/"),("Trực tiếp XSMN","truc-tiep-xsmn/"),("Trực tiếp XSMT","truc-tiep-xsmt/"),("XSMB 30 ngày","xsmb-30-ngay/"),("Sổ kết quả XSMB","xsmb/so-ket-qua/"),("Sổ kết quả XSMN","xsmn/so-ket-qua/"),("Sổ kết quả XSMT","xsmt/so-ket-qua/"),("Dò vé số","do-ve/"),("Thống kê lô tô","thong-ke/"),("Tra cứu số 00–99","so/"),("Thống kê nhóm số","thong-ke-dan/"),("Bảng thống kê","thong-ke/bang-thong-ke/")])}</nav>
<nav aria-label="Vietlott"><h2>Vietlott</h2>{L([("Keno","keno/"),("Mega 6/45","mega-645/"),("Power 6/55","power-655/"),("Max 3D","max-3d/"),("Max 3D Pro","max-3d-pro/"),("Tất cả Vietlott","vietlott/")])}</nav>
<nav aria-label="Về XS Lab"><h2>Về XS Lab</h2>{L([("Giới thiệu","gioi-thieu/"),("Liên hệ","lien-he/"),("Điều khoản sử dụng","dieu-khoan-su-dung/"),("Hỏi đáp (FAQ)","hoi-dap/"),("Miễn trừ trách nhiệm","mien-tru-trach-nhiem/"),("Chính sách bảo mật","chinh-sach-bao-mat/"),("Chính sách cookie","cookies/"),("Về dữ liệu","ve-du-lieu/"),("RSS","rss/")])}</nav>
</div><p class="fcopy">© {year} XS Lab · <a href="{up}rss.xml">rss.xml</a> · <a href="{up}sitemap.xml">sitemap.xml</a></p></footer>"""


def org_ld(base):
    return json.dumps({"@context": "https://schema.org", "@type": "Organization", "@id": base + "#org", "name": "XS Lab", "url": base,
                       "logo": base + "icon-512.png", "description": "Trang kết quả xổ số và thống kê dữ liệu XSMB, XSMN, XSMT, Vietlott, không quảng cáo.",
                       "email": EMAIL, "contactPoint": {"@type": "ContactPoint", "contactType": "customer support", "email": EMAIL, "url": base + "lien-he/", "availableLanguage": "vi"}}, ensure_ascii=False)


THEME_HEAD = "<script>try{var t=JSON.parse(localStorage.getItem('xs-theme'));if(t&&t!=='auto')document.documentElement.dataset.theme=t}catch(e){}</script>"

MENU_CSS = """@media(hover:hover) and (pointer:fine){.mbar summary::after{display:none}}
.mbar details .mdd:before{content:"";position:absolute;left:0;right:0;top:-12px;height:12px}
html:root{--side:light-dark(#ffffff,#16151b);--sideink:light-dark(#17161c,#e9e7ee);--sidemute:light-dark(#6c6975,#8e8a99);--sidehov:light-dark(#0000000a,#ffffff12);--sideln:light-dark(#e7e4df,#ffffff22)}html .side{border-right:1px solid var(--line)}html .side .nav a:hover{background:var(--sidehov)}html .side .nav a[aria-current=page]:hover{background:#d01f3c}html .side .themebtn{background:var(--sidehov);border-color:var(--sideln);color:var(--sideink)}html .brand:hover b{color:#d01f3c}html .tab{border-top:1px solid var(--line)}
@media(min-width:1500px){.app{max-width:1488px;margin:0 auto}html[data-theme=dark] body{background:linear-gradient(90deg,var(--side) calc((100vw - 1488px)/2 + 24px),var(--bg) 0) no-repeat,var(--bg)}}@media(min-width:1500px) and (prefers-color-scheme:dark){html:not([data-theme=light]) body{background:linear-gradient(90deg,var(--side) calc((100vw - 1488px)/2 + 24px),var(--bg) 0) no-repeat,var(--bg)}}
.subnav{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin:-8px 0 16px;padding:2px 0 4px;-webkit-overflow-scrolling:touch}.subnav::-webkit-scrollbar{display:none}@media(min-width:821px){.subnav{flex-wrap:wrap;overflow:visible}}@media(max-width:820px){.subnav{-webkit-mask-image:linear-gradient(90deg,#000 85%,transparent);mask-image:linear-gradient(90deg,#000 85%,transparent)}.subnav.end{-webkit-mask-image:none;mask-image:none}}.subnav a{flex:0 0 auto;padding:7px 12px;border-radius:999px;border:1px solid var(--line);background:var(--panel);color:var(--ink);text-decoration:none;font-size:14px;font-weight:600;white-space:nowrap}.subnav a:hover{border-color:#d01f3c;color:#d01f3c}.subnav a[aria-current=page]{background:#d01f3c;border-color:#d01f3c;color:#fff}
.mbar{position:relative;display:flex;align-items:center;gap:2px;margin:0 0 18px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:4px;z-index:30}
.mrow{display:flex;align-items:center;gap:2px;flex:1 1 auto;min-width:0}.mbar details{position:relative}.mbar summary,.mbar>a{list-style:none;display:flex;align-items:center;gap:7px;min-height:40px;padding:0 14px;border-radius:10px;font-weight:600;font-size:14px;cursor:pointer;color:var(--ink);text-decoration:none;white-space:nowrap;-webkit-user-select:none;user-select:none}
.mbar summary::-webkit-details-marker{display:none}.mbar summary::marker{content:""}
.mbar summary::after{content:"";width:6px;height:6px;border-right:2px solid currentColor;border-bottom:2px solid currentColor;transform:translateY(-2px) rotate(45deg);opacity:.5;transition:transform .15s}
.mbar details[open]>summary::after{transform:translateY(1px) rotate(-135deg)}
.mbar summary:hover,.mbar>a:hover{background:var(--band)}.mbar summary:focus-visible,.mbar a:focus-visible{outline:3px solid #ff5872;outline-offset:1px}
.mbar details[open]>summary{background:var(--redsoft);color:var(--red)}.mbar .is-cur>summary{color:var(--red)}
.mbar>a.dv{margin-left:auto;background:#d01f3c;color:#fff}.mbar>a.dv:hover{background:#b3172f}
.mbar .mdd{position:absolute;top:calc(100% + 8px);left:0;min-width:240px;background:var(--panel);border:1px solid var(--line);border-radius:14px;box-shadow:0 14px 36px #0003;padding:6px;display:grid;gap:1px}
.mbar .mdd a{display:block;padding:9px 12px;border-radius:9px;color:var(--ink);text-decoration:none;font-size:14px;line-height:1.3}
.mbar .mdd a:hover{background:var(--band)}.mbar .mdd a[aria-current=page]{color:var(--red);font-weight:600;background:var(--redsoft)}
.mbar .mdd .h{font-size:11px;text-transform:uppercase;letter-spacing:.06em;color:var(--mute);padding:10px 12px 3px;font-weight:600;grid-column:1/-1}
@media(max-width:820px){.mbar{gap:1px;padding:3px;margin:0 0 14px}.mrow{overflow-x:auto;scrollbar-width:none}.mbar:after{content:"";position:absolute;top:3px;bottom:3px;right:3px;width:40px;border-radius:0 11px 11px 0;background:linear-gradient(90deg,transparent,var(--panel) 85%);pointer-events:none;z-index:1;transition:opacity .2s}.mbar.end:after{opacity:0}.mbar .mdd{z-index:3}.mrow::-webkit-scrollbar{display:none}.mbar details{position:static;flex:0 0 auto}.mbar summary{justify-content:center;padding:0 10px;font-size:13.5px;min-height:40px;gap:4px;letter-spacing:-.1px}.mbar summary::after{width:4px;height:4px;border-width:0 1.5px 1.5px 0}.mbar>a.dv{display:none}
.mbar .mdd{left:0;right:0;min-width:0;grid-template-columns:1fr 1fr;top:calc(100% + 6px)}.mbar .mdd a{padding:11px 10px}}
@media(max-width:374px){.mbar summary{font-size:13px;padding:0 8px}}
.brand{display:flex;gap:12px;align-items:center;padding:4px 8px;color:var(--sideink);text-decoration:none;border-radius:12px}.brand:hover b{color:#fff}.brand:focus-visible{outline:3px solid #ff5872}
.brand b{display:block;font-size:19px;letter-spacing:.2px}.brand span{font-size:13px;color:var(--sidemute)}
.nav{scrollbar-width:none}.nav::-webkit-scrollbar{display:none}
.app>.side{gap:16px;padding:20px 14px 16px}.side .nav a{min-height:35px}.side .nav h3{margin:10px 12px 3px}.side .nav h3:first-child{margin-top:0}#sideFoot{font-size:12px;line-height:1.45}@media(max-height:960px){#sideFoot{display:none}}.side .themebtn{margin-top:0!important}
.mhead{display:none}
@media(max-width:820px){.mhead{display:flex;align-items:center;justify-content:space-between;margin:-6px 0 10px}.mlogo{display:flex;align-items:center;gap:8px;color:var(--ink);text-decoration:none;font-size:18px}.mlogo svg{width:32px;height:32px}
.mtheme{width:40px;height:40px;border-radius:50%;border:1px solid var(--line);background:var(--panel);display:grid;place-items:center;cursor:pointer;color:var(--ink)}.mtheme svg{width:20px;height:20px}}"""

MENU_JS = """(function(){var D=document.querySelectorAll('.mbar details');function closeAll(x){D.forEach(function(d){if(d!==x)d.open=false})}
D.forEach(function(d){d.addEventListener('toggle',function(){if(d.open)closeAll(d)})});
document.querySelectorAll('.subnav').forEach(function(n){var f=function(){n.classList.toggle('end',n.scrollLeft+n.clientWidth>=n.scrollWidth-4)};n.addEventListener('scroll',f,{passive:true});f();var c=n.querySelector('[aria-current]');if(c&&c.offsetLeft+c.offsetWidth>n.clientWidth)n.scrollLeft=c.offsetLeft-12});var MR=document.querySelector('.mrow');if(MR){var me=function(){MR.parentNode.classList.toggle('end',MR.scrollLeft+MR.clientWidth>=MR.scrollWidth-4)};MR.addEventListener('scroll',me,{passive:true});addEventListener('resize',me);me();
var cu=MR.querySelector('.is-cur');if(cu&&cu.offsetLeft+cu.offsetWidth>MR.clientWidth)MR.scrollLeft=cu.offsetLeft-12;}
document.addEventListener('click',function(e){if(!e.target.closest('.mbar'))closeAll()});
document.addEventListener('keydown',function(e){if(e.key==='Escape')closeAll()});
if(window.matchMedia&&matchMedia('(hover:hover) and (pointer:fine)').matches)D.forEach(function(d){var t;
d.addEventListener('mouseenter',function(){clearTimeout(t);closeAll(d);d.open=true});
d.addEventListener('mouseleave',function(){t=setTimeout(function(){d.open=false},200)});
d.querySelector('summary').addEventListener('click',function(e){var h=d.getAttribute('data-href');if(h){e.preventDefault();location.href=h}});
d.addEventListener('focusin',function(){closeAll(d);d.open=true});d.addEventListener('focusout',function(e){if(!d.contains(e.relatedTarget))d.open=false})});
if(!document.body.classList.contains('static'))return;
var TH=[['auto','Tự động'],['light','Sáng'],['dark','Tối']];function get(){try{return JSON.parse(localStorage.getItem('xs-theme'))||'auto'}catch(e){return 'auto'}}
function lab(){var t=get(),n=TH.find(function(x){return x[0]===t})||TH[0];document.querySelectorAll('.themebtn').forEach(function(b){b.textContent='Giao diện: '+n[1]})}
function cyc(){var t=get(),i=TH.findIndex(function(x){return x[0]===t});t=TH[(i+1)%3][0];try{localStorage.setItem('xs-theme',JSON.stringify(t))}catch(e){}if(t==='auto')delete document.documentElement.dataset.theme;else document.documentElement.dataset.theme=t;lab()}
document.querySelectorAll('.mtheme,.themebtn').forEach(function(b){b.addEventListener('click',cyc)});lab()})();"""

STATIC_CSS = """:root{color-scheme:light dark;--bg:light-dark(#f4f3f0,#111015);--panel:light-dark(#ffffff,#1b1a21);--ink:light-dark(#17161c,#efedf3);--mute:light-dark(#6c6975,#a3a0ad);
--line:light-dark(#e7e4df,#2c2a34);--red:light-dark(#d01f3c,#ff5872);--redsoft:light-dark(#fdebee,#3b1821);--side:#16151b;--sideink:#e9e7ee;--sidemute:#8e8a99;--band:light-dark(#efede9,#25232c)}
:root[data-theme=light]{color-scheme:light}:root[data-theme=dark]{color-scheme:dark}
*{box-sizing:border-box;min-width:0}html,body{margin:0}body{background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;overflow-x:clip}
button{font:inherit;color:inherit}a{color:var(--red)}
.app{display:grid;grid-template-columns:248px minmax(0,1fr);min-height:100vh;background:linear-gradient(90deg,var(--side) 248px,transparent 248px)}
.side{background:var(--side);color:var(--sideink);padding:20px 14px 16px;position:sticky;top:0;height:100vh;display:flex;flex-direction:column;gap:16px}
.nav{display:flex;flex-direction:column;gap:2px;overflow-y:auto}.nav h3{font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--sidemute);margin:10px 12px 3px;font-weight:600}.nav h3:first-child{margin-top:0}
.nav a{display:flex;align-items:center;gap:12px;min-height:35px;padding:0 12px;border-radius:10px;color:var(--sideink);text-decoration:none;font-weight:500;font-size:14px}.nav a svg{width:20px;height:20px;flex:none;opacity:.8}.nav a:hover{background:#ffffff12}.nav a[aria-current=page]{background:#d01f3c;color:#fff}
.side-foot{margin-top:auto;padding:0 8px}.themebtn{background:#ffffff12;border:1px solid #ffffff22;color:var(--sideink);width:100%;border-radius:999px;min-height:38px;cursor:pointer;font-size:14px}
.main{padding:24px clamp(16px,3vw,40px) 48px;width:100%;max-width:1240px;margin:0 auto}
.bc{font-size:13px;color:var(--mute);margin:0 0 6px}.bc a{color:var(--mute);text-decoration:none}.bc a:hover{color:var(--red)}
h1{font-size:clamp(24px,3vw,34px);line-height:1.15;margin:0 0 14px;font-weight:700;text-wrap:balance}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:clamp(14px,2vw,22px);margin:0 0 16px;overflow-x:auto}
.card h2,.main h2{font-size:19px;line-height:1.25;margin:0 0 10px;font-weight:600}.main>h2{margin:22px 0 10px}
p{margin:0 0 10px}.note{color:var(--mute);font-size:14px}
table{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}th,td{border:1px solid var(--line);padding:7px 6px;text-align:center}th{background:var(--band);font-size:14px;font-weight:600}
td.l{width:48px;color:var(--mute);font-weight:600;background:var(--band);font-size:13px}td span{display:inline-block;margin:2px 8px;font-size:18px;font-weight:600}td b{color:var(--red)}
tr.db td span,tr.g8 td span{font-size:22px;font-weight:700;color:var(--red)}
.lt td{text-align:left}.lt td:first-child,.lt td.k{width:44px;text-align:center;color:var(--red);font-weight:700;background:var(--band)}.lt td.r{text-align:right}
.pn{display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap;margin:10px 0}.pn a{text-decoration:none;font-weight:600}
.cta{display:inline-flex;align-items:center;min-height:40px;background:#d01f3c;color:#fff!important;text-decoration:none;padding:0 16px;border-radius:999px;font-weight:600;font-size:14px;margin:4px 6px 4px 0}.cta:hover{background:#b3172f}
ul.ls{columns:2;padding-left:18px}@media(min-width:700px){ul.ls{columns:4}}
table.wk td i{font-style:normal}table.wk b{color:var(--red)}
.g100 td{padding:5px 2px;font-size:15px;line-height:1.2}.g100 small{color:var(--mute);font-size:12px}
.foot{margin-top:28px;border-top:1px solid var(--line);padding:22px 0 24px;color:var(--mute);font-size:14px}
.fgrid{display:grid;grid-template-columns:minmax(0,1.3fr) minmax(0,1.6fr) minmax(0,.9fr) minmax(0,1.1fr);gap:20px 32px}
.foot nav:nth-of-type(1) ul{display:block;columns:2;column-gap:24px}.foot nav:nth-of-type(1) li{margin-bottom:6px;break-inside:avoid}
.foot h2{font-size:14px;color:var(--ink);margin:0 0 8px}.foot p{margin:0 0 8px;line-height:1.6}.foot ul{list-style:none;margin:0;padding:0;display:grid;gap:6px}.foot a{color:var(--mute);text-decoration:none}.foot a:hover{color:var(--red);text-decoration:underline}
.fcopy{margin-top:14px}
.tab{display:none}
.doc h3{font-size:16px;margin:18px 0 8px}.doc ul{padding-left:20px}.doc li{margin-bottom:6px}
@media(max-width:900px){.fgrid{grid-template-columns:1fr 1fr}.fsrc{grid-column:1/-1}}
@media(max-width:820px){.app{grid-template-columns:1fr;background:none}.side{display:none}.main{padding:18px 14px 96px}
.tab{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));position:fixed;left:0;right:0;bottom:0;background:var(--side);padding:6px 4px calc(6px + env(safe-area-inset-bottom));z-index:10}
.tab a{display:flex;flex-direction:column;align-items:center;gap:2px;color:var(--sidemute);text-decoration:none;font-size:11px;min-height:48px;justify-content:center;border-radius:10px}.tab a svg{width:22px;height:22px}.tab a[aria-current=page]{color:#fff;background:#d01f3c}}
@media(max-width:600px){table.wk i{display:none}table.wk td,table.wk th{font-size:13px;padding:5px 2px}table.sm td,table.sm th{font-size:12px;padding:5px 1px}
table.mn{table-layout:fixed}table.mn td span{display:block;margin:1px 0;font-size:15px;letter-spacing:-.2px}table.mn tr.db td span,table.mn tr.g8 td span{font-size:16px}table.mn th{font-size:12px;padding:6px 2px}table.mn td{padding:5px 1px}table.mn td.l{width:30px;font-size:11px}td span{margin:2px 5px;font-size:16px}}
"""
