/* Blade of Ages: Çağların Kılıcı site · small page behaviours (the playable hero lives in arena.js). */
(() => {
  "use strict";
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Language menu: close on outside click or Escape.
  const langs = document.querySelector(".langs");
  if (langs) {
    document.addEventListener("click", (ev) => { if (langs.open && !langs.contains(ev.target)) langs.open = false; });
    document.addEventListener("keydown", (ev) => { if (ev.key === "Escape") langs.open = false; });
  }

  // Journey through the Ages: the figures drift at different depths while their age is on screen.
  if (reduced) return;
  const stages = [...document.querySelectorAll(".era-stage")];
  const DEPTH = { "fig-set": 0.04, "fig-boss": 0.12, "fig-boss2": 0.08, "fig-minion": 0.18, "fig-minion2": 0.15 };
  const active = new Set();
  let ticking = false;
  const update = () => {
    ticking = false;
    const vh = innerHeight;
    for (const stage of active) {
      const r = stage.getBoundingClientRect();
      const offset = r.top + r.height / 2 - vh / 2; // 0 when the age is centred
      for (const fig of stage.children) {
        const depth = DEPTH[[...fig.classList].find((c) => c in DEPTH)] || 0.1;
        fig.style.transform = `translate3d(0, ${(-offset * depth).toFixed(1)}px, 0)`;
      }
    }
  };
  const io = new IntersectionObserver((entries) => {
    for (const en of entries) en.isIntersecting ? active.add(en.target) : active.delete(en.target);
    update();
  }, { rootMargin: "100px 0px" });
  stages.forEach((s) => io.observe(s));
  addEventListener("scroll", () => { if (!ticking && active.size) { ticking = true; requestAnimationFrame(update); } }, { passive: true });
})();
