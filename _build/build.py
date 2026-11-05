#!/usr/bin/env python3
"""Ghép header, menu, footer, thanh điều hướng vào từng trang.

Nội dung từng trang nằm trong _build/pages/<ten-trang>.html.
Dòng đầu mỗi file là thông tin trang dạng:
    <!--meta {"title": "...", "desc": "...", "tab": "..."} -->

Chạy:  python3 _build/build.py           -> ghi các file .html ra thư mục gốc repo
       python3 _build/build.py --preview OUT  -> bản xem thử (trang chủ không có thẻ <html>)
GitHub Pages bỏ qua thư mục bắt đầu bằng dấu gạch dưới, nên _build/ không bị đăng lên web.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_build", "pages")

SITE = "Trang trại Thanh Xuân"
HOTLINE = "097 487 0000"
HOTLINE_TEL = "0974870000"

# (file, tên menu, mô tả ngắn)
PAGES = [
    ("index", "Trang chủ", "Giới thiệu trang trại"),
    ("de-men", "Dế mèn", "Khay trứng, kỹ thuật nuôi"),
    ("tac-ke", "Tắc kè", "Giống, chuồng nuôi"),
    ("bo-cap", "Bọ cạp", "Giống, hồ nuôi"),
    ("bang-gia", "Bảng giá", "Giá giống, gói bao tiêu"),
    ("dau-ra", "Đầu ra", "Thu mua, phân phối"),
    ("mua-hang", "Mua hàng", "Đặt hàng, thanh toán"),
    ("tin-tuc", "Video & tin tức", "VTV2, YouTube, báo chí"),
    ("lien-he", "Liên hệ", "Địa chỉ, điện thoại"),
]
INLINE = ["de-men", "tac-ke", "bo-cap", "bang-gia", "dau-ra", "mua-hang", "lien-he"]
TABS = [("index", "Trang chủ", "i-home"), ("bang-gia", "Bảng giá", "i-tag"),
        ("mua-hang", "Mua hàng", "i-box"), ("lien-he", "Liên hệ", "i-pin")]

ICONS = """<svg width="0" height="0" style="position:absolute" aria-hidden="true">
<symbol id="i-phone" viewBox="0 0 24 24"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></symbol>
<symbol id="i-home" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M3 10.5 12 3l9 7.5V20a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/></symbol>
<symbol id="i-tag" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M3 12V4a1 1 0 0 1 1-1h8l9 9-9 9z"/><circle cx="7.5" cy="7.5" r="1.6" fill="currentColor"/></symbol>
<symbol id="i-box" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" d="M3 7.5 12 3l9 4.5v9L12 21l-9-4.5zM3 7.5l9 4.5 9-4.5M12 12v9"/></symbol>
<symbol id="i-pin" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2" d="M12 21s-7-6.2-7-11.5A7 7 0 0 1 19 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5" fill="currentColor"/></symbol>
<symbol id="i-menu" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" d="M4 7h16M4 12h16M4 17h16"/></symbol>
<symbol id="i-close" viewBox="0 0 24 24"><path fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" d="M6 6l12 12M18 6 6 18"/></symbol>
<symbol id="i-play" viewBox="0 0 24 24"><path fill="currentColor" d="M8 5v14l11-7z"/></symbol>
<symbol id="i-yt" viewBox="0 0 24 24"><path fill="currentColor" d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3z"/></symbol>
</svg>"""


def href(name):
    return "index.html" if name == "index" else f"{name}.html"


def cur(name, active):
    return ' aria-current="page"' if name == active else ""


def header(active):
    inline = "".join(
        f'<li><a href="{href(n)}"{cur(n, active)}>{label}</a></li>'
        for n, label, _ in PAGES if n in INLINE)
    menu = "".join(
        f'<a href="{href(n)}"{cur(n, active)}><b>{label}</b><span>{d}</span></a>'
        for n, label, d in PAGES)
    return f"""<div class="topbar"><div class="wrap">
  <span>Cơ sở 1: 119 Tam Trinh, Mai Động, Hoàng Mai, Hà Nội · Cơ sở 2: Thôn Hóp, Mỹ Phúc, Mỹ Lộc, Nam Định</span>
  <span>Hotline: <b class="num">{HOTLINE}</b> · <b class="num">038 995 8888</b></span>
</div></div>
<header class="site-head"><div class="wrap">
  <a class="brand" href="index.html">
    <img src="images/logo.jpg" alt="" width="208" height="120">
    <div><strong>Trang trại Thanh Xuân</strong><span>Dế mèn · Tắc kè · Bọ cạp · từ 2004</span></div>
  </a>
  <ul class="nav-inline">{inline}</ul>
  <a class="btn btn-call head-call" href="tel:{HOTLINE_TEL}"><svg><use href="#i-phone"/></svg>{HOTLINE}</a>
  <details class="menu">
    <summary aria-label="Mở menu"><svg class="ic-open"><use href="#i-menu"/></svg><svg class="ic-close"><use href="#i-close"/></svg>Menu</summary>
    <nav class="menu-panel" aria-label="Tất cả các trang"><div class="wrap">{menu}
      <a class="menu-call" href="tel:{HOTLINE_TEL}"><b>Gọi đặt hàng</b><span class="num">{HOTLINE}</span></a>
    </div></nav>
  </details>
</div></header>"""


def footer():
    links = "".join(f'<a href="{href(n)}">{label}</a>' for n, label, _ in PAGES)
    return f"""<footer class="site-foot"><div class="wrap">
  <div>
    <strong>Trang trại Thanh Xuân</strong>
    <p>Nhà cung cấp dế mèn, tắc kè, bọ cạp, côn trùng trong nước và ngoài nước. Khởi nghiệp chăn nuôi côn trùng từ 2004.</p>
    <p>Cơ sở 1: 119 Tam Trinh, Mai Động, Hoàng Mai, Hà Nội.<br>Cơ sở 2: Thôn Hóp, Mỹ Phúc, Mỹ Lộc, Nam Định.</p>
    <p>Hotline: <a class="num" href="tel:{HOTLINE_TEL}">{HOTLINE}</a> · <a class="num" href="tel:0389958888">038 995 8888</a> · <a class="num" href="tel:0945370300">0945 370 300</a></p>
  </div>
  <nav aria-label="Các trang">{links}</nav>
  <p class="copy">© Bản quyền thuộc về trang trại Thanh Xuân · trangtraithanhxuan.com</p>
</div></footer>"""


def tabbar(active):
    items = "".join(
        f'<a href="{href(n)}"{cur(n, active)}><svg><use href="#{ic}"/></svg>{label}</a>'
        for n, label, ic in TABS)
    return f"""<nav class="tabbar" aria-label="Điều hướng nhanh">{items}<a class="tab-call" href="tel:{HOTLINE_TEL}"><svg><use href="#i-phone"/></svg>Gọi ngay</a></nav>"""


HEAD = """<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
"""

FONTS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Be+Vietnam+Pro:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">"""


# ------------------------------------------------------------------ video
VSETS = json.load(open(os.path.join(ROOT, "_build", "video_sets.json"), encoding="utf-8"))
VLIB = json.load(open(os.path.join(ROOT, "_build", "video_library.json"), encoding="utf-8"))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;"))


def vlink_attrs(vid, title):
    return (f'href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener" '
            f'data-yt="{vid}" data-title="{esc(title)}"')


def video_card(vid, title, meta):
    return (f'<a class="vcard" {vlink_attrs(vid, title)} aria-label="Phát video: {esc(title)}">'
            f'<span class="vthumb"><img src="https://i.ytimg.com/vi/{vid}/mqdefault.jpg" alt="" loading="lazy" width="320" height="180">'
            f'<span class="vplay" aria-hidden="true"><svg><use href="#i-play"/></svg></span></span>'
            f'<span class="vtitle">{esc(title)}</span><span class="vmeta">{esc(meta)}</span></a>')


def video_rail(key):
    r = VSETS["rails"][key]
    cards = "".join(video_card(*it) for it in r["items"])
    note = f'<p class="vnote">{esc(r["note"])}</p>' if r.get("note") else ""
    return (f'<div class="vblock"><div class="vhead"><h3><svg aria-hidden="true"><use href="#i-yt"/></svg>{esc(r["title"])}</h3>'
            f'<span class="vhint">{len(r["items"])} video<span class="vswipe"> · vuốt ngang</span></span></div>'
            f'{note}<div class="vrail">{cards}</div></div>')


def video_feature(key):
    vid, title, meta = VSETS["features"][key]
    return (f'<a class="vfeature" {vlink_attrs(vid, title)} aria-label="Phát video: {esc(title)}">'
            f'<span class="vthumb"><img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" alt="" loading="lazy" width="480" height="360">'
            f'<span class="vplay" aria-hidden="true"><svg><use href="#i-play"/></svg></span></span>'
            f'<span class="vcap"><b>{esc(title)}</b><span>{esc(meta)}</span></span></a>')


def video_library():
    chips = [("all", "Tất cả"), ("de", "Dế mèn"), ("tacke", "Tắc kè"), ("bocap", "Bọ cạp"), ("kythuat", "Kỹ thuật nuôi"),
             ("daura", "Thu mua & đầu ra"), ("tv", "Truyền hình"), ("monan", "Món ăn")]
    btns = "".join(
        f'<button type="button" class="chipbtn" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{label}</button>'
        for k, label in chips)
    return f"""<div class="vlib" id="vlib">
  <form class="vlib-form" role="search">
    <label class="sr" for="vlib-search">Tìm video</label>
    <input id="vlib-search" type="search" placeholder="Tìm video, ví dụ: ấp trứng" autocomplete="off" enterkeyhint="search">
  </form>
  <div class="vlib-chips" role="group" aria-label="Lọc theo chủ đề">{btns}</div>
  <p class="vlib-count" aria-live="polite">Đang tải danh sách video…</p>
  <ul class="vlist"></ul>
  <button type="button" class="btn btn-green btn-block vlib-more" hidden>Xem thêm</button>
  <noscript><p class="note">Bật JavaScript để xem thư viện video, hoặc xem trực tiếp trên các kênh YouTube bên dưới.</p></noscript>
</div>"""


PLAYER = """<dialog class="vplayer" id="vplayer" aria-label="Xem video">
  <div class="vp-frame"></div>
  <div class="vp-bar">
    <p class="vp-title"></p>
    <div class="vp-actions">
      <a class="vp-yt" href="#" target="_blank" rel="noopener"><svg aria-hidden="true"><use href="#i-yt"/></svg>Mở trên YouTube</a>
      <button type="button" class="vp-close"><svg aria-hidden="true"><use href="#i-close"/></svg>Đóng</button>
    </div>
  </div>
</dialog>"""


def expand_videos(body):
    body = re.sub(r"<!--rail:([\w-]+)-->", lambda m: video_rail(m.group(1)), body)
    body = re.sub(r"<!--feature:([\w-]+)-->", lambda m: video_feature(m.group(1)), body)
    body = body.replace("<!--library-->", video_library())
    return body


def write_video_data(out):
    os.makedirs(os.path.join(out, "js"), exist_ok=True)
    with open(os.path.join(out, "js", "videos-data.js"), "w", encoding="utf-8") as f:
        f.write("/* Danh sách video lấy từ website cũ trangtraithanhxuan.com (đã kiểm tra còn xem được). Tạo bởi _build/build.py */\n")
        f.write("window.VIDEOS=" + json.dumps(VLIB, ensure_ascii=False, separators=(",", ":")) + ";\n")


def render(name, preview_index=False):
    raw = open(os.path.join(SRC, name + ".html"), encoding="utf-8").read()
    m = re.match(r"\s*<!--meta (.*?) -->\s*", raw, re.S)
    meta = json.loads(m.group(1))
    body = expand_videos(raw[m.end():])
    active = meta.get("tab", name)
    title = SITE if name == "index" else f"{meta['title']} · {SITE}"
    if preview_index:
        title = "Trang Trại Thanh Xuân"
    head_meta = (f"<title>{title}</title>\n"
                 f'<meta name="description" content="{meta["desc"]}">\n'
                 '<meta name="theme-color" content="#0e3b25">\n')
    if preview_index:
        head_meta += '<meta name="claude:viewport-fit-sides" content="cover">\n'
    page = (head_meta + FONTS + "\n" + ("" if preview_index else "</head>\n<body>\n") +
            ICONS + "\n" + header(active) + "\n<main>\n" + body.strip() + "\n</main>\n" +
            footer() + "\n" + tabbar(active) + "\n" + PLAYER + "\n" +
            ('<script src="js/videos-data.js"></script>\n' if "<!--library-->" in raw else "") +
            '<script src="js/video.js" defer></script>\n')
    if preview_index:
        return page
    return HEAD + page + "</body>\n</html>\n"


def main():
    out = ROOT
    preview = False
    if len(sys.argv) > 2 and sys.argv[1] == "--preview":
        out, preview = sys.argv[2], True
        os.makedirs(out, exist_ok=True)
    write_video_data(ROOT)
    for name, _, _ in PAGES:
        with open(os.path.join(out, href(name)), "w", encoding="utf-8") as f:
            f.write(render(name))
        print("wrote", href(name))
    if preview:
        with open(os.path.join(out, "trang-trai-thanh-xuan.html"), "w", encoding="utf-8") as f:
            f.write(render("index", preview_index=True))
        print("wrote preview main page")


if __name__ == "__main__":
    main()
