// ── AOS Init ──────────────────────────────────────────────────────
AOS.init({
  duration: 700,
  once: true,
  easing: 'ease-out-cubic',
  offset: 60,
});



// ── Navbar scroll ─────────────────────────────────────────────────
const navbar = document.getElementById('navbar');
const backTop = document.getElementById('backTop');

// Pre-cache DOM queries for scroll performance
const scrollSections = document.querySelectorAll('section[id]');
const navLinkMap = new Map();
scrollSections.forEach(sec => {
  const link = document.querySelector(`.nav-links a[href="#${sec.id}"]`);
  if (link) {
    navLinkMap.set(sec, link);
  }
});

let scrollTicking = false;
window.addEventListener('scroll', () => {
  if (!scrollTicking) {
    window.requestAnimationFrame(() => {
      const y = window.scrollY;
      if (navbar) navbar.classList.toggle('scrolled', y > 50);
      if (backTop) backTop.classList.toggle('visible', y > 400);

      navLinkMap.forEach((link, sec) => {
        const top = sec.offsetTop - 100;
        const bot = top + sec.offsetHeight;
        link.classList.toggle('active', y >= top && y < bot);
      });
      scrollTicking = false;
    });
    scrollTicking = true;
  }
});

// ── Mobile nav ────────────────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const navLinks  = document.getElementById('navLinks');
hamburger.addEventListener('click', () => navLinks.classList.toggle('open'));
navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => navLinks.classList.remove('open')));

// ── Typed text ────────────────────────────────────────────────────
const phrases = [
  'AI Software Developer',
  'Python Developer',
  'Django Developer',
  'AI/ML Enthusiast',
];
let pi = 0, ci = 0, deleting = false;
const typedEl = document.getElementById('typedText');

function type() {
  if (!typedEl) return;
  const phrase = phrases[pi % phrases.length];
  typedEl.textContent = deleting ? phrase.slice(0, ci--) : phrase.slice(0, ci++);

  if (!deleting && ci > phrase.length) {
    deleting = true;
    setTimeout(type, 1800);
    return;
  }
  if (deleting && ci < 0) {
    deleting = false;
    pi++;
    ci = 0;
    setTimeout(type, 300);
    return;
  }
  setTimeout(type, deleting ? 40 : 80);
}
type();

// ── Counter animation ─────────────────────────────────────────────
function animateCounter(el) {
  const rawTarget = el.dataset.count;
  if (rawTarget === 'AI/ML') {
    el.textContent = 'AI/ML';
    return;
  }
  const target = parseInt(rawTarget);
  const dur = 1500;
  const step = target / (dur / 16);
  let current = 0;
  const timer = setInterval(() => {
    current = Math.min(current + step, target);
    if (rawTarget === '100') {
      el.textContent = Math.floor(current) + '%';
    } else if (rawTarget === '6') {
      el.textContent = Math.floor(current) + '+';
    } else {
      el.textContent = Math.floor(current) + (target >= 10 ? '+' : '');
    }
    if (current >= target) clearInterval(timer);
  }, 16);
}

const counters = document.querySelectorAll('[data-count]');
const counterObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { animateCounter(e.target); counterObs.unobserve(e.target); }});
}, { threshold: .5 });
counters.forEach(c => counterObs.observe(c));

// ── Skill bar animation on scroll ────────────────────────────────
const skillCards = document.querySelectorAll('.skill-card');
const skillObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('animated'); skillObs.unobserve(e.target); }});
}, { threshold: .3 });
skillCards.forEach(c => skillObs.observe(c));

// ── Skill category filter ─────────────────────────────────────────
document.querySelectorAll('.cat-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.cat-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const cat = btn.dataset.cat;
    skillCards.forEach(card => {
      const show = cat === 'all' || card.dataset.category === cat;
      card.style.display = show ? '' : 'none';
    });
  });
});

// ── Floating code particles ───────────────────────────────────────
const snippets = [
  'def __init__(self):',
  'import asyncio',
  'async with session:',
  '@dataclass',
  'yield from queue',
  'except Exception as e:',
  'return Response(data)',
  'celery.task()',
  'docker-compose up',
  'git push origin main',
  'SELECT * FROM users',
  'redis.set(key, val)',
  'pytest -v --cov',
  'uvicorn app:main',
  'pip install -r req',
];
const container = document.getElementById('codeParticles');
if (container) {
  snippets.forEach((s, i) => {
    const el = document.createElement('div');
    el.className = 'code-float';
    el.textContent = s;
    el.style.left = (5 + Math.random() * 90) + '%';
    el.style.animationDuration = (20 + Math.random() * 30) + 's';
    el.style.animationDelay    = (Math.random() * 20) + 's';
    container.appendChild(el);
  });
}

// ── Contact form AJAX ─────────────────────────────────────────────
const contactForm = document.getElementById('contactForm');
const feedback    = document.getElementById('formFeedback');

if (contactForm) {
  contactForm.addEventListener('submit', async e => {
    e.preventDefault();
    const btn = contactForm.querySelector('button[type=submit]');
    const originalText = btn.innerHTML;
    btn.textContent = 'Sending...';
    btn.disabled = true;

    try {
      const res = await fetch(contactForm.action, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': contactForm.querySelector('[name=csrfmiddlewaretoken]').value,
        },
        body: new FormData(contactForm),
      });
      const data = await res.json();
      feedback.className = 'form-feedback ' + (res.ok ? 'success' : 'error');
      feedback.textContent = data.message;
      if (res.ok) contactForm.reset();
    } catch {
      feedback.className = 'form-feedback error';
      feedback.textContent = 'Something went wrong. Please try again.';
    } finally {
      btn.innerHTML = originalText;
      btn.disabled = false;
    }
  });
}
