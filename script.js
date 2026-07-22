/* ============================================================
   Jordan Hale — shared script
   Handles: Tailwind color config, mobile menu toggle,
   and fade-in-on-scroll animations. Loaded on every page.
   ============================================================ */

/* Newsletter setup — replace the placeholder below once with your
   Buttondown username. This activates the Subscribe form on every page. */
const BUTTONDOWN_USERNAME = 'YOUR-BUTTONDOWN-USERNAME';

/* Tailwind Play CDN configuration — keeps the same custom color
   names (navy, deep, ocean, sky, baby, mist, ink, slate) available
   as Tailwind utility classes (e.g. bg-navy, text-ocean) on every page. */
tailwind.config = {
  theme: {
    extend: {
      colors: {
        navy: '#0F2647',
        deep: '#1B3A6B',
        ocean: '#2E5C9A',
        sky: '#7FAEDD',
        baby: '#BFDBFE',
        mist: '#F4F7FB',
        ink: '#334155',
        slate: '#64748B',
      },
      fontFamily: {
        display: ['Manrope', 'sans-serif'],
        body: ['Inter', 'sans-serif'],
      },
    },
  },
};

document.addEventListener('DOMContentLoaded', function () {
  /* ---------- Activate the shared newsletter forms ---------- */
  if (BUTTONDOWN_USERNAME && BUTTONDOWN_USERNAME !== 'YOUR-BUTTONDOWN-USERNAME') {
    document.querySelectorAll('.newsletter-form').forEach(function (form) {
      form.action = 'https://buttondown.com/api/emails/embed-subscribe/' + encodeURIComponent(BUTTONDOWN_USERNAME);
    });
  }

  /* ---------- Mobile hamburger menu ---------- */
  const menuBtn = document.getElementById('menuBtn');
  const mobileMenu = document.getElementById('mobileMenu');

  if (menuBtn && mobileMenu) {
    const bar1 = document.getElementById('bar1');
    const bar2 = document.getElementById('bar2');
    const bar3 = document.getElementById('bar3');
    let menuOpen = false;

    menuBtn.addEventListener('click', function () {
      menuOpen = !menuOpen;
      mobileMenu.classList.toggle('hidden', !menuOpen);
      menuBtn.setAttribute('aria-expanded', String(menuOpen));
      if (bar1) bar1.style.transform = menuOpen ? 'translateY(6px) rotate(45deg)' : '';
      if (bar3) bar3.style.transform = menuOpen ? 'translateY(-6px) rotate(-45deg)' : '';
      if (bar2) bar2.style.opacity = menuOpen ? '0' : '1';
    });

    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        menuOpen = false;
        mobileMenu.classList.add('hidden');
        menuBtn.setAttribute('aria-expanded', 'false');
        if (bar1) bar1.style.transform = '';
        if (bar3) bar3.style.transform = '';
        if (bar2) bar2.style.opacity = '1';
      });
    });
  }

  /* ---------- Reveal elements as the user scrolls ---------- */
  const revealEls = document.querySelectorAll('.reveal');
  if (revealEls.length && 'IntersectionObserver' in window) {
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add('is-visible'); });
  }
});
