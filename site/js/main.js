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

  /* ── video fallback ── */
  var vid = document.querySelector('.hero video');
  if (vid) {
    vid.addEventListener('error', function () { vid.remove(); }, true);
    var src = vid.querySelector('source');
    if (src) src.addEventListener('error', function () { vid.remove(); });
  }

  /* ── GRADUS II selector logic ── */
  var dirs = document.querySelectorAll('.dir');
  var tiers = document.querySelectorAll('.tier');
  if (dirs.length) {
    var state = { dir: null, tier: null };
    var fDir = document.getElementById('fDir');
    var fSum = document.getElementById('fSum');
    var fInv = document.getElementById('fInv');
    var goBtn = document.getElementById('goBtn');
    function paint() {
      fDir.textContent = state.dir || '—';
      fSum.textContent = state.tier || '—';
      if (state.tier) { fInv.textContent = 'NON REQUIRITUR'; fInv.classList.add('g'); }
      else { fInv.textContent = 'ЖДИ ИНВАЙТ'; fInv.classList.remove('g'); }
      if (state.dir && state.tier) goBtn.removeAttribute('disabled');
    }
    dirs.forEach(function (d) {
      d.addEventListener('click', function () {
        dirs.forEach(function (x) { x.classList.remove('sel'); });
        d.classList.add('sel'); state.dir = d.getAttribute('data-name'); paint();
      });
    });
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
        '> НАПРАВЛЕНИЕ: ' + state.dir + '\n' +
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
