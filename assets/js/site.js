/* ------------------------------------------------------------
   Schwarzweiß-Portfolio · Verhalten
   Kopfbereich, Menü, Einblenden, Lightbox. Ohne Bibliotheken.
   Ohne JavaScript funktioniert die Seite weiter: Bilder sind
   sichtbar, ein Klick öffnet die große Datei.
   ------------------------------------------------------------ */
(() => {
  "use strict";
  const root = document.documentElement;
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Bilder sanft einblenden, sobald sie geladen sind */
  document.querySelectorAll(".frame img").forEach(img => {
    const show = () => img.classList.add("loaded");
    if (img.complete && img.naturalWidth > 0) show();
    else {
      img.addEventListener("load", show, { once: true });
      img.addEventListener("error", show, { once: true });
    }
  });

  /* Beim Scrollen einblenden: nur was beim Laden unterhalb des Bildschirms liegt */
  if (!reduceMotion && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(entries => {
      for (const e of entries) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      }
    }, { rootMargin: "0px 0px -6% 0px", threshold: 0.08 });
    const vh = window.innerHeight;
    document.querySelectorAll("main .ph, .pubs li, .posts li, .pager").forEach(n => {
      if (n.getBoundingClientRect().top < vh * 0.9) return;
      n.classList.add("rv");
      io.observe(n);
    });
  }

  /* Kopfbereich und Menü */
  const bar = document.getElementById("bar");
  const head = bar ? bar.querySelector(".head") : null;
  const menuBtn = bar ? bar.querySelector(".menu-btn") : null;
  const lb = document.getElementById("lb");
  const lbIsOpen = () => !!lb && !lb.hidden;

  function setMenu(open) {
    if (!head || !menuBtn) return;
    head.classList.toggle("open", open);
    menuBtn.setAttribute("aria-expanded", String(open));
    menuBtn.textContent = open ? "Schließen" : "Menü";
    root.classList.toggle("locked", open || lbIsOpen());
    if (open) bar.classList.remove("hide");
  }
  if (menuBtn) {
    menuBtn.addEventListener("click", () => setMenu(!head.classList.contains("open")));
    document.addEventListener("keydown", e => {
      if (e.key === "Escape" && head.classList.contains("open")) { setMenu(false); menuBtn.focus(); }
    });
  }
  if (bar) {
    let lastY = window.scrollY, ticking = false;
    window.addEventListener("scroll", () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const y = Math.max(0, window.scrollY);
        if (!head || !head.classList.contains("open")) {
          if (y > lastY + 4 && y > 240) bar.classList.add("hide");
          else if (y < lastY - 4 || y < 240) bar.classList.remove("hide");
        }
        lastY = y;
        ticking = false;
      });
    }, { passive: true });
  }

  /* Lightbox auf den Serienseiten */
  const frames = Array.from(document.querySelectorAll(".wall--series a.frame"));
  if (!lb || !frames.length) return;

  const img = lb.querySelector(".lb-img");
  const count = lb.querySelector(".lb-count");
  const title = lb.querySelector(".lb-title");
  const meta = lb.querySelector(".lb-meta");
  const btnClose = lb.querySelector(".lb-close");
  const btnPrev = lb.querySelector(".lb-prev");
  const btnNext = lb.querySelector(".lb-next");

  const items = frames.map(a => {
    const thumb = a.querySelector("img");
    return {
      src: a.href,
      title: a.dataset.title || "",
      meta: a.dataset.meta || "",
      alt: thumb ? thumb.alt : ""
    };
  });
  const pageUrl = location.pathname + location.search;
  let idx = 0, lastFocus = null, viaClick = false;

  function paint() {
    const it = items[idx], n = items.length;
    count.textContent = (idx + 1) + " / " + n;
    title.textContent = it.title;
    meta.textContent = it.meta;
    img.alt = it.alt;
    if (img.src !== it.src) { img.classList.add("swap"); img.src = it.src; }
    [idx + 1, idx - 1].forEach(j => { const p = new Image(); p.src = items[(j + n) % n].src; }); // Nachbarn vorladen
  }
  img.addEventListener("load", () => img.classList.remove("swap"));
  img.addEventListener("error", () => img.classList.remove("swap"));

  function open(i) {
    idx = i;
    if (!lastFocus) lastFocus = document.activeElement;
    lb.hidden = false;
    root.classList.add("locked");
    paint();
    btnClose.focus();
  }
  function close() {
    lb.hidden = true;
    root.classList.toggle("locked", !!head && head.classList.contains("open"));
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
    lastFocus = null;
  }
  function step(d) {
    idx = (idx + d + items.length) % items.length;
    history.replaceState(null, "", "#bild-" + (idx + 1));
    paint();
  }
  // Schließen: war die Lightbox per Klick geöffnet, geht es einen Schritt zurück im Verlauf.
  // So schließt auch die Zurück-Taste des Handys die Lightbox, statt die Seite zu verlassen.
  function requestClose() {
    if (viaClick) {
      viaClick = false;
      history.back();
      setTimeout(() => { if (!lb.hidden) { close(); history.replaceState(null, "", pageUrl); } }, 350);
    } else {
      close();
      history.replaceState(null, "", pageUrl);
    }
  }
  function fromHash() {
    const m = location.hash.match(/^#bild-(\d+)$/);
    const i = m ? parseInt(m[1], 10) - 1 : -1;
    if (i >= 0 && i < items.length) {
      if (lb.hidden) open(i);
      else if (i !== idx) { idx = i; paint(); }
    } else if (!lb.hidden) {
      close();
    }
  }

  frames.forEach((a, i) => a.addEventListener("click", e => {
    if (e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return; // neuer Tab bleibt möglich
    e.preventDefault();
    lastFocus = a;
    viaClick = true;
    location.hash = "bild-" + (i + 1);
  }));
  window.addEventListener("hashchange", fromHash);

  btnClose.addEventListener("click", requestClose);
  btnPrev.addEventListener("click", () => step(-1));
  btnNext.addEventListener("click", () => step(1));
  img.addEventListener("click", () => step(1));

  document.addEventListener("keydown", e => {
    if (lb.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); requestClose(); }
    else if (e.key === "ArrowRight") step(1);
    else if (e.key === "ArrowLeft") step(-1);
    else if (e.key === "Tab") {
      const f = [btnClose, btnPrev, btnNext].filter(b => b.offsetParent !== null);
      const k = f.indexOf(document.activeElement);
      e.preventDefault();
      f[e.shiftKey ? (k <= 0 ? f.length - 1 : k - 1) : (k + 1) % f.length].focus();
    }
  });

  let sx = null, sy = null;
  lb.addEventListener("touchstart", e => {
    if (e.touches.length !== 1) { sx = null; return; }
    sx = e.touches[0].clientX; sy = e.touches[0].clientY;
  }, { passive: true });
  lb.addEventListener("touchend", e => {
    if (sx === null) return;
    const dx = e.changedTouches[0].clientX - sx;
    const dy = e.changedTouches[0].clientY - sy;
    sx = null;
    if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) step(dx < 0 ? 1 : -1);
    else if (dy > 90 && dy > Math.abs(dx)) requestClose();
  }, { passive: true });

  fromHash(); // direkter Link auf ein Bild, z. B. /serien/japan/#bild-3
})();
