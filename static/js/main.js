/* Portfolio — shared behaviour (theme, menu, reveal, typing, counters, skill bars, quotes) */
(function () {
  const root = document.documentElement;
  const themeBtn = document.getElementById('themeBtn');
  const setIcon = () => { themeBtn.textContent = root.dataset.theme === 'dark' ? '🌙' : '☀️'; };
  setIcon();
  themeBtn.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
    setIcon();
  });

  // mobile menu
  const burger = document.getElementById('burger'), links = document.getElementById('navLinks');
  burger.addEventListener('click', () => links.classList.toggle('open'));
  links.addEventListener('click', e => { if (e.target.matches('a')) links.classList.remove('open'); });

  // cursor glow
  const glow = document.getElementById('glow');
  window.addEventListener('pointermove', e => { glow.style.left = e.clientX + 'px'; glow.style.top = e.clientY + 'px'; });

  // reveal on scroll (+ skill bars)
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (!en.isIntersecting) return;
    en.target.classList.add('in');
    en.target.querySelectorAll('.bar i').forEach(b => b.style.width = b.dataset.w + '%');
    io.unobserve(en.target);
  }), { threshold: .12 });
  document.querySelectorAll('.reveal').forEach(el => io.observe(el));

  // typing effect
  const typed = document.getElementById('typed');
  if (typed) {
    const words = JSON.parse(typed.dataset.words || '[]');
    let w = 0, c = 0, del = false;
    (function tick() {
      const word = words[w] || '';
      typed.textContent = word.slice(0, c);
      if (!del && c === word.length) { del = true; return setTimeout(tick, 1400); }
      if (del && c === 0) { del = false; w = (w + 1) % words.length; }
      c += del ? -1 : 1;
      setTimeout(tick, del ? 40 : 90);
    })();
  }

  // animated counters
  document.querySelectorAll('[data-count]').forEach(el => {
    const target = +el.dataset.count, suffix = el.dataset.suffix || '';
    let n = 0; const step = Math.max(1, Math.ceil(target / 40));
    const t = setInterval(() => { n = Math.min(target, n + step); el.textContent = n + suffix; if (n >= target) clearInterval(t); }, 35);
  });

  // rotating quotes
  const quotes = document.querySelectorAll('#quotes .quote');
  if (quotes.length > 1) {
    let q = 0;
    setInterval(() => { quotes[q].classList.remove('show'); q = (q + 1) % quotes.length; quotes[q].classList.add('show'); }, 4500);
  }
})();
