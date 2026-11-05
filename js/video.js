/* Trình phát video cho website Trang trại Thanh Xuân.
   - Trang chỉ tải ảnh bìa nhỏ. Khi khách bấm vào mới tải trình phát YouTube,
     nên trang vẫn nhẹ và nhanh trên điện thoại.
   - Video mở trong khung nổi (trên điện thoại trượt lên từ đáy màn hình).
   - Trang Video có thư viện: tìm kiếm, lọc theo chủ đề, "Xem thêm". */
(function () {
  "use strict";

  var THUMB = function (id, size) { return "https://i.ytimg.com/vi/" + id + "/" + (size || "mqdefault") + ".jpg"; };
  var WATCH = function (id) { return "https://www.youtube.com/watch?v=" + id; };
  var EMBED = function (id) {
    return "https://www.youtube-nocookie.com/embed/" + id + "?autoplay=1&playsinline=1&rel=0&modestbranding=1";
  };

  /* ---------- Khung phát video ---------- */
  var dlg = document.getElementById("vplayer");
  var frameBox = dlg && dlg.querySelector(".vp-frame");
  var titleEl = dlg && dlg.querySelector(".vp-title");
  var ytLink = dlg && dlg.querySelector(".vp-yt");
  var canDialog = !!(dlg && typeof dlg.showModal === "function");

  function openVideo(id, title) {
    if (!canDialog) { window.open(WATCH(id), "_blank", "noopener"); return; }
    frameBox.innerHTML = '<iframe src="' + EMBED(id) + '" title="' + escapeHtml(title || "Video") +
      '" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>';
    titleEl.textContent = title || "";
    ytLink.href = WATCH(id);
    dlg.showModal();
    document.documentElement.classList.add("vp-open");
  }

  function closeVideo() {
    if (!dlg) return;
    if (dlg.open) dlg.close();
  }

  if (dlg) {
    dlg.addEventListener("close", function () {
      frameBox.innerHTML = "";            // dừng video khi đóng
      document.documentElement.classList.remove("vp-open");
    });
    dlg.addEventListener("click", function (e) {
      if (e.target === dlg) closeVideo(); // bấm ra ngoài khung để đóng
    });
    var closeBtn = dlg.querySelector(".vp-close");
    if (closeBtn) closeBtn.addEventListener("click", closeVideo);
  }

  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("[data-yt]") : null;
    if (!a || !canDialog) return;          // không hỗ trợ khung nổi: mở YouTube như link thường
    e.preventDefault();
    openVideo(a.getAttribute("data-yt"), a.getAttribute("data-title"));
  });

  function escapeHtml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  /* ---------- Thư viện video (trang Video & tin tức) ---------- */
  var lib = document.getElementById("vlib");
  var data = window.VIDEOS;
  if (!lib || !data) return;

  var list = lib.querySelector(".vlist");
  var more = lib.querySelector(".vlib-more");
  var count = lib.querySelector(".vlib-count");
  var search = lib.querySelector("#vlib-search");
  var chips = lib.querySelectorAll("[data-filter]");
  var PAGE = 12;
  var state = { tag: "all", q: "", shown: PAGE };

  function fold(s) {                         // bỏ dấu để tìm "nuoi de" vẫn ra "nuôi dế"
    return s.normalize("NFD").replace(/[̀-ͯ]/g, "").replace(/đ/g, "d").replace(/Đ/g, "D").toLowerCase();
  }
  data.forEach(function (v) { v.f = fold(v.t); });

  function matches() {
    var q = fold(state.q.trim());
    return data.filter(function (v) {
      return (state.tag === "all" || v.g.indexOf(state.tag) !== -1) && (!q || v.f.indexOf(q) !== -1);
    });
  }

  function render() {
    var all = matches();
    var items = all.slice(0, state.shown);
    list.innerHTML = items.map(function (v) {
      var t = escapeHtml(v.t);
      return '<li><a class="vrow" href="' + WATCH(v.id) + '" target="_blank" rel="noopener" data-yt="' + v.id + '" data-title="' + t + '">' +
        '<span class="vthumb"><img src="' + THUMB(v.id) + '" alt="" loading="lazy" width="320" height="180">' +
        '<span class="vplay" aria-hidden="true"><svg><use href="#i-play"/></svg></span></span>' +
        '<span class="vtext"><span class="vtitle">' + t + '</span>' +
        (v.y ? '<span class="vmeta">Năm ' + v.y + "</span>" : "") + "</span></a></li>";
    }).join("");
    count.textContent = all.length ? ("Đang xem " + items.length + " / " + all.length + " video") : "Không tìm thấy video phù hợp";
    more.hidden = items.length >= all.length;
    more.textContent = "Xem thêm " + Math.min(PAGE, all.length - items.length) + " video";
  }

  chips.forEach(function (c) {
    c.addEventListener("click", function () {
      chips.forEach(function (x) { x.setAttribute("aria-pressed", x === c ? "true" : "false"); });
      state.tag = c.getAttribute("data-filter");
      state.shown = PAGE;
      render();
    });
  });
  var timer;
  search.addEventListener("input", function () {
    clearTimeout(timer);
    timer = setTimeout(function () { state.q = search.value; state.shown = PAGE; render(); }, 150);
  });
  lib.querySelector(".vlib-form").addEventListener("submit", function (e) { e.preventDefault(); search.blur(); });
  more.addEventListener("click", function () { state.shown += PAGE; render(); });

  render();
})();
