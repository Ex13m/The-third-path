/* GAUSSE HOLLER CUSTOM LAB · shared runtime */
(function () {
  document.body.classList.add('js');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(hover:hover) and (pointer:fine)').matches;

  /* ── custom cursor ── */
  if (fine) {
    document.body.classList.add('cursor-on');
    var cur = document.createElement('div'); cur.id = 'cur';
    var dot = document.createElement('div'); dot.id = 'curDot';
    var lbl = document.createElement('div'); lbl.id = 'curLbl';
    document.body.append(cur, dot, lbl);
    var mx = innerWidth / 2, my = innerHeight / 2, cx = mx, cy = my;
    addEventListener('mousemove', function (e) {
      mx = e.clientX; my = e.clientY;
      dot.style.transform = 'translate(' + mx + 'px,' + my + 'px)';
      lbl.style.transform = 'translate(' + (mx + 14) + 'px,' + (my + 14) + 'px)';
    });
    (function loop() {
      cx += (mx - cx) * 0.16; cy += (my - cy) * 0.16;
      cur.style.transform = 'translate(' + cx + 'px,' + cy + 'px)';
      requestAnimationFrame(loop);
    })();
    document.querySelectorAll('a,button,[data-hover]').forEach(function (el) {
      el.addEventListener('mouseenter', function () {
        cur.classList.add('hov');
        var t = el.getAttribute('data-cur');
        if (t) { lbl.textContent = t; lbl.classList.add('show'); }
      });
      el.addEventListener('mouseleave', function () {
        cur.classList.remove('hov'); lbl.classList.remove('show');
      });
    });
  }

  /* ── boot overlay ── */
  var boot = document.getElementById('boot');
  if (boot) {
    if (reduced) { boot.classList.add('done'); }
    else {
      var pre = boot.querySelector('pre');
      var lines = JSON.parse(boot.getAttribute('data-lines'));
      var i = 0;
      (function next() {
        if (i < lines.length) {
          pre.innerHTML += lines[i] + '\n'; i++;
          setTimeout(next, 130);
        } else {
          setTimeout(function () { boot.classList.add('done'); }, 350);
        }
      })();
    }
  }

  /* ── reveal on scroll ── */
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12 });
  document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });

  /* ── page wipe transition ── */
  var wipe = document.getElementById('wipe');
  document.querySelectorAll('a[data-wipe]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (reduced || !wipe) return;
      e.preventDefault();
      wipe.classList.add('go');
      setTimeout(function () { location.href = a.href; }, 460);
    });
  });

  /* ── live counter ── */
  var num = document.getElementById('omni');
  if (num) {
    var v = 1204880;
    var render = function () {
      num.textContent = '$ ' + v.toLocaleString('ru-RU').replace(/,/g, ' ');
    };
    render();
    if (!reduced) setInterval(function () { v += Math.random() < 0.7 ? 1 : 3; render(); }, 2600);
  }

  /* ── hero parallax ── */
  var hero = document.querySelector('.hero');
  var hudLayer = document.querySelector('.hud-layer');
  if (hero && hudLayer && fine && !reduced) {
    hero.addEventListener('mousemove', function (e) {
      var r = hero.getBoundingClientRect();
      var dx = (e.clientX - r.width / 2) / r.width;
      var dy = (e.clientY - r.height / 2) / r.height;
      hudLayer.style.transform = 'translate(' + (-dx * 30) + 'px,' + (-dy * 22) + 'px)';
    });
    hero.addEventListener('mouseleave', function () { hudLayer.style.transform = ''; });
  }

  /* ── video fallback ── */
  var vid = document.querySelector('.hero video');
  if (vid) {
    vid.addEventListener('error', function () { vid.remove(); }, true);
    var src = vid.querySelector('source');
    if (src) src.addEventListener('error', function () { vid.remove(); });
  }

  /* ── transmissions: play in view, pause out of view ── */
  var tvs = document.querySelectorAll('.tv video');
  if (tvs.length) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting) { v.play().catch(function () {}); }
        else { v.pause(); }
      });
    }, { threshold: 0.25 });
    tvs.forEach(function (v) {
      v.addEventListener('error', function () {
        var f = v.closest('.tv'); if (f) f.style.display = 'none';
      });
      vio.observe(v);
    });
  }

  /* ── GRADUS II: triangle allocation + tier logic ── */
  var triSvg = document.getElementById('triSvg');
  var tiers = document.querySelectorAll('.tier');
  if (triSvg) {
    var state = { v: 30, a: 30, n: 30, tier: null };
    var fDir = document.getElementById('fDir');
    var fSum = document.getElementById('fSum');
    var fInv = document.getElementById('fInv');
    var goBtn = document.getElementById('goBtn');
    /* triangle vertices: V (top), A (bottom-left), N (bottom-right) */
    var V = { x: 240, y: 36 }, A = { x: 36, y: 390 }, N = { x: 444, y: 390 };
    var node = document.getElementById('triNode');
    var core = document.getElementById('triNodeCore');
    var rays = { V: document.getElementById('rayV'), A: document.getElementById('rayA'), N: document.getElementById('rayN') };
    var rows = { V: document.getElementById('rowV'), A: document.getElementById('rowA'), N: document.getElementById('rowN') };

    function roundTo90(w) { /* w: normalized weights summing to 1 → ints summing to 90 */
      var raw = [w[0] * 90, w[1] * 90, w[2] * 90];
      var fl = raw.map(Math.floor);
      var rest = 90 - (fl[0] + fl[1] + fl[2]);
      var order = [0, 1, 2].sort(function (i, j) { return (raw[j] - fl[j]) - (raw[i] - fl[i]); });
      for (var k = 0; k < rest; k++) fl[order[k % 3]]++;
      return fl;
    }
    function setNode(x, y) {
      node.setAttribute('cx', x); node.setAttribute('cy', y);
      core.setAttribute('cx', x); core.setAttribute('cy', y);
      ['V', 'A', 'N'].forEach(function (k) { rays[k].setAttribute('x2', x); rays[k].setAttribute('y2', y); });
    }
    function applyWeights(wv, wa, wn) { /* normalized, sum 1 */
      var r = roundTo90([wv, wa, wn]);
      state.v = r[0]; state.a = r[1]; state.n = r[2];
      document.getElementById('pV').textContent = state.v + '%';
      document.getElementById('pA').textContent = state.a + '%';
      document.getElementById('pN').textContent = state.n + '%';
      document.getElementById('bV').style.width = (state.v / 90 * 100) + '%';
      document.getElementById('bA').style.width = (state.a / 90 * 100) + '%';
      document.getElementById('bN').style.width = (state.n / 90 * 100) + '%';
      rows.V.classList.toggle('hot', state.v >= 45);
      rows.A.classList.toggle('hot', state.a >= 45);
      rows.N.classList.toggle('hot', state.n >= 45);
      paint();
    }
    function fromPoint(px, py) {
      var den = (A.y - N.y) * (V.x - N.x) + (N.x - A.x) * (V.y - N.y);
      var wv = ((A.y - N.y) * (px - N.x) + (N.x - A.x) * (py - N.y)) / den;
      var wa = ((N.y - V.y) * (px - N.x) + (V.x - N.x) * (py - N.y)) / den;
      var wn = 1 - wv - wa;
      wv = Math.max(0, wv); wa = Math.max(0, wa); wn = Math.max(0, wn);
      var s = wv + wa + wn; wv /= s; wa /= s; wn /= s;
      setNode(V.x * wv + A.x * wa + N.x * wn, V.y * wv + A.y * wa + N.y * wn);
      applyWeights(wv, wa, wn);
    }
    function fromWeights(v90, a90, n90) {
      var wv = v90 / 90, wa = a90 / 90, wn = n90 / 90;
      setNode(V.x * wv + A.x * wa + N.x * wn, V.y * wv + A.y * wa + N.y * wn);
      applyWeights(wv, wa, wn);
    }
    function svgPoint(e) {
      var r = triSvg.getBoundingClientRect();
      return { x: (e.clientX - r.left) * 480 / r.width, y: (e.clientY - r.top) * 430 / r.height };
    }
    var dragging = false;
    triSvg.addEventListener('pointerdown', function (e) {
      dragging = true; triSvg.setPointerCapture(e.pointerId);
      triSvg.parentElement.classList.add('grabbing');
      var p = svgPoint(e); fromPoint(p.x, p.y);
    });
    triSvg.addEventListener('pointermove', function (e) {
      if (!dragging) return;
      var p = svgPoint(e); fromPoint(p.x, p.y);
    });
    ['pointerup', 'pointercancel'].forEach(function (ev) {
      triSvg.addEventListener(ev, function () {
        dragging = false; triSvg.parentElement.classList.remove('grabbing');
      });
    });
    document.querySelectorAll('.pre-chip').forEach(function (b) {
      b.addEventListener('click', function () {
        var s = b.getAttribute('data-set').split(',').map(Number);
        fromWeights(s[0], s[1], s[2]);
      });
    });

    function paint() {
      fDir.textContent = 'V' + state.v + ' · A' + state.a + ' · T' + state.n + ' · +10';
      fSum.textContent = state.tier || '—';
      if (state.tier) { fInv.textContent = 'NON REQUIRITUR'; fInv.classList.add('g'); }
      else { fInv.textContent = 'ЖДИ ИНВАЙТ'; fInv.classList.remove('g'); }
      if (state.tier) goBtn.removeAttribute('disabled');
    }
    tiers.forEach(function (t) {
      t.addEventListener('click', function () {
        tiers.forEach(function (x) { x.classList.remove('sel'); });
        t.classList.add('sel'); state.tier = t.getAttribute('data-name'); paint();
      });
    });
    var modal = document.getElementById('modal');
    var mpre = modal.querySelector('pre');
    goBtn.addEventListener('click', function () {
      modal.classList.add('open');
      var txt = '> ЗАЯВКА ПРИНЯТА\n' +
        '> РАСПРЕДЕЛЕНИЕ: VITA ' + state.v + '% · AUGMENTATIO ' + state.a + '% · VIA TERTIA ' + state.n + '%\n' +
        '> DIRECTORIUM: 10% — СТРАЖА, АДМИНИСТРАЦИЯ, МЕЛКИЙ ШРИФТ. КАК ВСЕГДА. КАК ВЕЗДЕ.\n' +
        '> ВКЛАД: ' + state.tier + '\n' +
        '> ПРОТОКОЛ GRADUS II: ЗАПУЩЕН\n' +
        '> УЗЕЛ ОПЛАТЫ: АКТИВИРУЕТСЯ ВРУЧНУЮ — INCEPTOR PRIMARIS\n' +
        '> СТАТУС: ЖДИ ИНВАЙТ. ИЛИ НЕ ЖДИ — ТЫ УЖЕ ВНУТРИ.';
      if (reduced) { mpre.textContent = txt; return; }
      mpre.textContent = '';
      var i = 0;
      (function type() {
        if (i <= txt.length) { mpre.textContent = txt.slice(0, i); i += 2; setTimeout(type, 14); }
      })();
    });
    modal.querySelector('.x').addEventListener('click', function () { modal.classList.remove('open'); });
    modal.addEventListener('click', function (e) { if (e.target === modal) modal.classList.remove('open'); });
  }
})();
