/* Blades of Ages · playable hero.
   A small canvas version of the game's core feel (game: docs/03, reference: HUD.dc.html):
   outward-facing blades orbit the hero; moving = wide orbit, standing = tight and faster; per-blade hit cooldown;
   enemies come from the four edges and in ring waves; a defeated enemy turns into gold that flies to the counter.
   Starts after the first paint, pauses off-screen, and never starts on its own with prefers-reduced-motion. */
(() => {
  "use strict";
  const root = document.querySelector("[data-arena]");
  if (!root) return;
  const hero = root.closest(".hero");
  const canvas = root.querySelector("canvas");
  const ctx = canvas.getContext("2d");
  const goldEl = root.querySelector("[data-gold]");
  const pill = root.querySelector(".gold-pill");
  const tryBtn = document.querySelector("[data-try]");
  const exitBtn = root.querySelector("[data-exit]");
  const hint = document.querySelector("[data-hint]");
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const coarse = matchMedia("(pointer: coarse)").matches;

  // Tuning (game values scaled for a web canvas). Radii and speeds in CSS px at scale 1.
  const R_WIDE = 70, R_TIGHT = 46, OMEGA_MOVE = 3.6, OMEGA_STAND = 5.2, RADIUS_LERP = 6;
  const BODY = 40; // hero body centre above the feet, px at scale 1
  const SWORDS = 6, HIT_COOLDOWN = 0.22, DAMAGE = 1, HERO_SPEED = 260, AUTO_SPEED = 90;
  const SPAWN_EVERY = 0.55, RING_EVERY = 10, RING_COUNT = 12, COIN_VALUE = 5;
  const MAX_ENEMIES = matchMedia("(pointer: coarse)").matches ? 32 : 46; // phones: fewer sprites per frame
  const MAX_DPR = 1.5; // sharp enough for the clay sprites; a 3x phone would otherwise fill 4x the pixels
  const TYPES = {
    boar: { src: "tas-domuz", hp: 3, speed: 52, box: 92, knock: 85 },
    scorpion: { src: "akrep-ruhu", hp: 2, speed: 62, box: 80, knock: 110 },
    fox: { src: "tilki-golgesi", hp: 1, speed: 96, box: 80, knock: 150 },
  };

  const img = {};
  const load = (name) => new Promise((ok) => {
    const im = new Image();
    im.onload = () => ok(im);
    im.onerror = () => ok(null);
    im.src = `/assets/art/${name}.webp`;
    img[name] = im;
  });

  let W = 0, H = 0, S = 1, dpr = 1;
  let running = false, visible = true, raf = 0, last = 0;
  let mode = "auto"; // auto | pointer | play
  const st = {
    t: 0, ang: 0, r: R_WIDE, x: 0, y: 0, tx: 0, ty: 0, moving: true, stillFor: 0,
    enemies: [], coins: [], sparks: [], spawn: 0, ring: 3, gold: 0, pointerAt: -9,
  };

  function resize() {
    const r = root.getBoundingClientRect();
    dpr = Math.min(MAX_DPR, window.devicePixelRatio || 1);
    cache.clear(); // scaled sprites and the blade depend on size and dpr
    W = r.width; H = r.height;
    S = Math.max(0.78, Math.min(1.25, Math.min(W, H) / 640));
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (!st.x) { st.x = home().x; st.y = home().y; }
  }
  const home = () => (W > 860 ? { x: W * 0.66, y: H * 0.5 } : { x: W * 0.5, y: H * 0.5 });

  // ------------------------------------------------------------- simulation
  function spawn(px, py) {
    const r = Math.random();
    const type = r < 0.4 ? "boar" : r < 0.75 ? "scorpion" : "fox";
    const T = TYPES[type];
    let x = px, y = py;
    if (x === undefined) {
      const side = Math.floor(Math.random() * 4), m = 60;
      if (side === 0) { x = Math.random() * W; y = -m; }
      else if (side === 1) { x = Math.random() * W; y = H + m; }
      else if (side === 2) { x = -m; y = Math.random() * H; }
      else { x = W + m; y = Math.random() * H; }
    }
    st.enemies.push({ type, x, y, hp: T.hp, max: T.hp, spd: T.speed * S * (0.88 + Math.random() * 0.24),
      rad: T.box * S * 0.24, lift: T.box * S * 0.3, kx: 0, ky: 0, hits: new Array(SWORDS).fill(-9), flash: -9, face: 1,
      ph: Math.random() * 6.3 });
  }

  function autopilot(dt) {
    // The demo hero walks a slow figure-eight for 5 s, then stands for 3 s (like the design canvas).
    const h = home(), t = st.t;
    const walking = (t % 8) < 5;
    if (walking) {
      const k = t * 0.45;
      st.tx = h.x + Math.cos(k) * Math.min(160, W * 0.18) * S;
      st.ty = h.y + Math.sin(k * 2) * Math.min(90, H * 0.12) * S;
    } else { st.tx = st.x; st.ty = st.y; }
    move(dt, AUTO_SPEED * S);
  }

  function move(dt, speed) {
    const dx = st.tx - st.x, dy = st.ty - st.y, d = Math.hypot(dx, dy);
    const step = speed * dt;
    if (d > 2) {
      const k = Math.min(1, step / d);
      st.x += dx * k; st.y += dy * k;
      st.moving = true; st.stillFor = 0;
    } else {
      st.stillFor += dt;
      st.moving = st.stillFor < 0.15;
    }
    const m = 40 * S;
    st.x = Math.max(m, Math.min(W - m, st.x));
    st.y = Math.max(m * 1.6, Math.min(H - m, st.y));
  }

  function step(dt) {
    st.t += dt;
    if (mode === "auto") autopilot(dt);
    else move(dt, HERO_SPEED * S);
    if (mode === "pointer" && st.t - st.pointerAt > 2.5) mode = "auto";

    const target = (st.moving ? R_WIDE : R_TIGHT) * S;
    st.r += (target - st.r) * Math.min(1, dt * RADIUS_LERP);
    st.ang += (st.moving ? OMEGA_MOVE : OMEGA_STAND) * dt;

    st.spawn -= dt;
    if (st.spawn <= 0 && st.enemies.length < MAX_ENEMIES) { spawn(); st.spawn = SPAWN_EVERY; }
    st.ring -= dt;
    if (st.ring <= 0) {
      st.ring = RING_EVERY;
      const rr = Math.max(W, H) * 0.42;
      for (let k = 0; k < RING_COUNT && st.enemies.length < MAX_ENEMIES + RING_COUNT; k++) {
        const a = (k / RING_COUNT) * Math.PI * 2;
        spawn(st.x + Math.cos(a) * rr, st.y + Math.sin(a) * rr);
      }
    }

    const es = st.enemies;
    for (const e of es) {
      const dx = st.x - e.x, dy = st.y - e.y, d = Math.hypot(dx, dy) || 1;
      e.face = dx >= 0 ? 1 : -1;
      if (d > 26 * S + e.rad) { e.x += (dx / d) * e.spd * dt; e.y += (dy / d) * e.spd * dt; }
      e.x += e.kx * dt; e.y += e.ky * dt;
      const damp = Math.pow(0.02, dt); e.kx *= damp; e.ky *= damp;
    }
    for (let i = 0; i < es.length; i++) for (let j = i + 1; j < es.length; j++) {
      const a = es[i], b = es[j], dx = b.x - a.x, dy = b.y - a.y, d = Math.hypot(dx, dy), m = a.rad + b.rad;
      if (d > 0 && d < m) { const p = (m - d) / 2, ux = dx / d, uy = dy / d; a.x -= ux * p; a.y -= uy * p; b.x += ux * p; b.y += uy * p; }
    }

    // Hit sweep: a blade hits an enemy inside its angular window; the cooldown is per blade (game rule).
    const TAU = Math.PI * 2;
    const hy = st.y - BODY * S; // positions are feet; the orbit circles the body centre
    for (const e of es) {
      const dx = e.x - st.x, dy = e.y - e.lift - hy, d = Math.hypot(dx, dy);
      if (d < st.r - 26 * S || d > st.r + 58 * S + e.rad) continue;
      const phi = Math.atan2(dy, dx), allow = Math.atan2(e.rad, d) + 0.06;
      for (let i = 0; i < SWORDS; i++) {
        const th = st.ang + (i * TAU) / SWORDS;
        const df = (((phi - th + Math.PI) % TAU) + TAU) % TAU - Math.PI;
        if (Math.abs(df) < allow && st.t - e.hits[i] > HIT_COOLDOWN) {
          e.hp -= DAMAGE; e.hits[i] = st.t; e.flash = st.t;
          const kb = TYPES[e.type].knock * S;
          e.kx += Math.cos(phi) * kb; e.ky += Math.sin(phi) * kb;
          st.sparks.push({ x: st.x + Math.cos(th) * d, y: hy + Math.sin(th) * d, born: st.t });
        }
      }
    }
    const alive = [];
    for (const e of es) {
      if (e.hp > 0) { alive.push(e); continue; }
      const n = e.type === "boar" ? 3 : e.type === "scorpion" ? 2 : 1;
      for (let k = 0; k < n; k++) st.coins.push({ x: e.x, y: e.y - 8 * S, vx: (Math.random() * 160 - 80) * S, vy: (-40 - Math.random() * 120) * S, born: st.t });
      st.sparks.push({ x: e.x, y: e.y, puff: true, born: st.t });
    }
    st.enemies = alive;

    const keep = [];
    for (const c of st.coins) {
      const age = st.t - c.born;
      if (age < 0.45) { c.x += c.vx * dt; c.y += c.vy * dt; c.vy += 320 * S * dt; keep.push(c); continue; }
      const dx = st.x - c.x, dy = st.y - BODY * S - c.y, d = Math.hypot(dx, dy) || 1, sp = (220 + (age - 0.45) * 900) * S;
      c.x += (dx / d) * sp * dt; c.y += (dy / d) * sp * dt;
      if (d < 18 * S) collect(); else keep.push(c);
    }
    st.coins = keep;
    st.sparks = st.sparks.filter((p) => st.t - p.born < (p.puff ? 0.5 : 0.2));
  }

  let bumpTimer = 0;
  function collect() {
    st.gold += COIN_VALUE;
    goldEl.textContent = st.gold.toLocaleString(document.documentElement.lang);
    pill.classList.add("bump");
    clearTimeout(bumpTimer);
    bumpTimer = setTimeout(() => pill.classList.remove("bump"), 120);
  }

  // ------------------------------------------------------------- drawing
  function shadow(x, y, w) {
    ctx.fillStyle = "rgba(58, 74, 96, 0.18)";
    ctx.beginPath(); ctx.ellipse(x, y, w, w * 0.32, 0, 0, Math.PI * 2); ctx.fill();
  }

  // Per-frame cost matters on phones: sprites are scaled once into offscreen canvases (per size, dpr and facing) and the
  // blade, with its gradients, is drawn once; each frame only copies pixels.
  const cache = new Map();
  function scaled(im, box, flip) {
    const px = Math.max(1, Math.round(box * dpr));
    const key = im.src + "|" + px + "|" + (flip ? 1 : 0);
    let c = cache.get(key);
    if (!c) {
      c = document.createElement("canvas");
      c.width = c.height = px;
      const g = c.getContext("2d");
      if (flip) { g.translate(px, 0); g.scale(-1, 1); }
      g.drawImage(im, 0, 0, px, px);
      cache.set(key, c);
    }
    return c;
  }

  function drawSprite(im, x, y, box, flip, bob) {
    if (!im) return;
    ctx.drawImage(scaled(im, box, flip), x - box / 2, y + bob - box * 0.86, box, box);
  }

  // The blade sprite covers x in [-0.5, 0.7]·len and y in [-1, 0.35]·len around the blade's pivot.
  const BLADE_BOX = { x0: -0.5, x1: 0.7, y0: -1, y1: 0.35 };
  function bladeSprite() {
    let c = cache.get("blade");
    if (c) return c;
    const len = 44 * S, b = BLADE_BOX;
    c = document.createElement("canvas");
    c.width = Math.ceil((b.x1 - b.x0) * len * dpr); c.height = Math.ceil((b.y1 - b.y0) * len * dpr);
    const g = c.getContext("2d");
    g.scale(dpr, dpr); g.translate(-b.x0 * len, -b.y0 * len);
    paintBlade(g);
    cache.set("blade", c);
    return c;
  }

  function drawBlade(th) {
    const r = st.r, len = 44 * S, b = BLADE_BOX, sprite = bladeSprite();
    ctx.save();
    ctx.translate(st.x + Math.cos(th) * r, st.y - BODY * S + Math.sin(th) * r);
    ctx.rotate(th);
    ctx.drawImage(sprite, b.x0 * len, b.y0 * len, (b.x1 - b.x0) * len, (b.y1 - b.y0) * len);
    ctx.restore();
  }

  function paintBlade(ctx) {
    const len = 44 * S, w = 6.5 * S;
    // light trail behind the blade (opposite to the spin direction)
    ctx.save();
    ctx.rotate(Math.PI / 2);
    const g = ctx.createLinearGradient(0, 0, -len * 0.9, 0);
    g.addColorStop(0, "rgba(127, 211, 255, 0.55)"); g.addColorStop(1, "rgba(127, 211, 255, 0)");
    ctx.fillStyle = g;
    ctx.beginPath(); ctx.moveTo(0, -len * 0.55); ctx.lineTo(-len * 0.9, -len * 0.2); ctx.lineTo(-len * 0.9, len * 0.15); ctx.lineTo(0, len * 0.25); ctx.closePath(); ctx.fill();
    ctx.restore();
    // blade: tip outward (+x after rotation)
    const bg = ctx.createLinearGradient(0, -w, 0, w);
    bg.addColorStop(0, "#FFFFFF"); bg.addColorStop(0.55, "#EEF3FF"); bg.addColorStop(1, "#B8D3EA");
    ctx.fillStyle = bg; ctx.strokeStyle = "#6E93B4"; ctx.lineWidth = 1.4 * S; ctx.lineJoin = "round";
    ctx.beginPath();
    ctx.moveTo(len * 0.62, 0); ctx.lineTo(len * 0.44, -w); ctx.lineTo(-len * 0.18, -w); ctx.lineTo(-len * 0.18, w); ctx.lineTo(len * 0.44, w); ctx.closePath();
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = "#E5A526"; ctx.strokeStyle = "#8A5A12";
    ctx.beginPath(); ctx.rect(-len * 0.24, -w * 2, 5 * S, w * 4); ctx.fill(); ctx.stroke(); // guard
    ctx.fillStyle = "#8A5A3A";
    ctx.fillRect(-len * 0.4, -w * 0.55, len * 0.16, w * 1.1);
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    const TAU = Math.PI * 2;
    const drawables = st.enemies.map((e) => ({ y: e.y, e })).concat([{ y: st.y, hero: true }]);
    drawables.sort((a, b) => a.y - b.y);
    for (const d of drawables) {
      if (d.hero) {
        shadow(st.x, st.y, 30 * S);
        const bob = st.moving ? Math.sin(st.t * 12) * 2 * S : 0;
        drawSprite(img["hero-kaya"], st.x, st.y + 6 * S, 128 * S, st.tx < st.x - 4, bob);
      } else {
        const e = d.e, T = TYPES[e.type];
        shadow(e.x, e.y, e.rad * 1.2);
        drawSprite(img[T.src], e.x, e.y + 4 * S, T.box * S, e.face < 0, Math.sin(st.t * 10 + e.ph) * 1.5 * S);
        if (st.t - e.flash < 0.09) {
          ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
          ctx.beginPath(); ctx.arc(e.x, e.y - T.box * S * 0.3, e.rad * 1.3, 0, TAU); ctx.fill();
        }
      }
    }
    for (let i = 0; i < SWORDS; i++) drawBlade(st.ang + (i * TAU) / SWORDS);
    for (const p of st.sparks) {
      const k = (st.t - p.born) / (p.puff ? 0.5 : 0.2);
      if (p.puff) {
        ctx.fillStyle = `rgba(232, 211, 166, ${0.6 * (1 - k)})`;
        for (let j = 0; j < 5; j++) {
          const a = j * 1.26, rr = (10 + 26 * k) * S;
          ctx.beginPath(); ctx.arc(p.x + Math.cos(a) * rr, p.y - 20 * S + Math.sin(a) * rr * 0.6, (7 - 4 * k) * S, 0, TAU); ctx.fill();
        }
      } else {
        ctx.strokeStyle = `rgba(255, 255, 255, ${1 - k})`; ctx.lineWidth = 3 * S;
        ctx.beginPath(); ctx.arc(p.x, p.y, (6 + 14 * k) * S, 0, TAU); ctx.stroke();
      }
    }
    const coin = img["gold-coin"];
    if (coin) { const cs = scaled(coin, 22 * S, false); for (const c of st.coins) ctx.drawImage(cs, c.x - 11 * S, c.y - 11 * S, 22 * S, 22 * S); }
  }

  function frame(now) {
    raf = 0;
    if (!running || !visible) return;
    const dt = Math.min(0.05, (now - last) / 1000 || 0);
    last = now;
    step(dt);
    draw();
    raf = requestAnimationFrame(frame);
  }
  function kick() { if (!raf && running && visible) { last = performance.now(); raf = requestAnimationFrame(frame); } }

  // ------------------------------------------------------------- input
  function local(ev) { const r = canvas.getBoundingClientRect(); return { x: ev.clientX - r.left, y: ev.clientY - r.top }; }
  canvas.addEventListener("pointermove", (ev) => {
    if (ev.pointerType === "mouse" && mode !== "play") {
      const p = local(ev); mode = "pointer"; st.tx = p.x; st.ty = p.y + 30 * S; st.pointerAt = st.t;
    } else if (mode === "play" && ev.buttons) {
      const p = local(ev); st.tx = p.x; st.ty = p.y - 40 * S; // keep the hero above the thumb
    }
  });
  canvas.addEventListener("pointerdown", (ev) => {
    if (mode !== "play") return;
    canvas.setPointerCapture(ev.pointerId);
    const p = local(ev); st.tx = p.x; st.ty = p.y - 40 * S;
  });
  const standStill = () => { if (mode === "play") { st.tx = st.x; st.ty = st.y; } };
  canvas.addEventListener("pointerup", standStill);
  canvas.addEventListener("pointercancel", standStill);

  function enterPlay() {
    start();
    mode = "play"; st.tx = st.x; st.ty = st.y;
    hero.classList.add("playing");
    exitBtn.hidden = false;
    root.scrollIntoView({ behavior: reduced ? "auto" : "smooth", block: "start" });
    setTimeout(resize, 350);
    exitBtn.focus({ preventScroll: true });
  }
  function exitPlay() {
    mode = "auto";
    hero.classList.remove("playing");
    exitBtn.hidden = true;
    setTimeout(resize, 350);
    tryBtn.focus({ preventScroll: true });
  }

  // ------------------------------------------------------------- lifecycle
  async function start() {
    if (running) return;
    running = true;
    await Promise.all(["hero-kaya", "tas-domuz", "akrep-ruhu", "tilki-golgesi", "gold-coin"].map(load));
    resize();
    root.classList.add("live");
    kick();
  }

  if (hint) hint.textContent = coarse ? hint.dataset.touch : hint.dataset.pointer;
  if (coarse) { tryBtn.hidden = false; tryBtn.addEventListener("click", enterPlay); }
  else if (reduced) { tryBtn.hidden = false; tryBtn.addEventListener("click", () => { start(); tryBtn.hidden = true; }); }
  exitBtn.addEventListener("click", exitPlay);
  document.addEventListener("keydown", (ev) => { if (ev.key === "Escape" && mode === "play") exitPlay(); });
  addEventListener("resize", () => { if (running) resize(); });
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; kick(); }, { threshold: 0.05 }).observe(root);
  document.addEventListener("visibilitychange", () => { visible = !document.hidden; kick(); });

  // The demo wakes up after the first paint so it never competes with the page's first render.
  if (!reduced) {
    const go = () => start();
    if ("requestIdleCallback" in window) requestIdleCallback(go, { timeout: 1200 });
    else setTimeout(go, 600);
  }
})();
