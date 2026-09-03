/* ============================================================
   Beyond the Leash with Sandra — shared script
   Handles: Tailwind color config, mobile menu toggle,
   and fade-in-on-scroll animations. Loaded on every page.
   ============================================================ */

/* Newsletter setup — connected to the Buttondown newsletter below. */
const BUTTONDOWN_USERNAME = 'beyond_the_leash';

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
  if (BUTTONDOWN_USERNAME) {
    document.querySelectorAll('.newsletter-form').forEach(function (form) {
      form.action = 'https://buttondown.com/api/emails/embed-subscribe/' + encodeURIComponent(BUTTONDOWN_USERNAME);
    });
  }


  /* ---------- Homepage: mirror the newest real blog post ---------- */
  const latestBlogCard = document.getElementById('latest-blog-card');
  if (latestBlogCard) {
    fetch('blog.html', { cache: 'no-store' })
      .then(function (response) {
        if (!response.ok) throw new Error('Could not load blog page');
        return response.text();
      })
      .then(function (html) {
        const blogDocument = new DOMParser().parseFromString(html, 'text/html');
        const newestPost = blogDocument.querySelector('article.blog-entry:not(.template-post)');
        if (newestPost) {
          latestBlogCard.innerHTML = newestPost.innerHTML;
        }
      })
      .catch(function () {
        /* Local file previews may block fetch(). The live GitHub Pages site will load it normally. */
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

    menuBtn.setAttribute('aria-controls', 'mobileMenu');

    function setMenu(open) {
      menuOpen = open;
      mobileMenu.classList.toggle('hidden', !open);
      menuBtn.setAttribute('aria-expanded', String(open));
      /* Stop the page behind the menu from scrolling while it is open. */
      document.body.style.overflow = open ? 'hidden' : '';
      if (bar1) bar1.style.transform = open ? 'translateY(6px) rotate(45deg)' : '';
      if (bar3) bar3.style.transform = open ? 'translateY(-6px) rotate(-45deg)' : '';
      if (bar2) bar2.style.opacity = open ? '0' : '1';
    }

    menuBtn.addEventListener('click', function () {
      setMenu(!menuOpen);
    });

    mobileMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () { setMenu(false); });
    });

    /* Escape closes the menu and returns focus to the button that opened it. */
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menuOpen) {
        setMenu(false);
        menuBtn.focus();
      }
    });

    /* Rotating to landscape or resizing past the md breakpoint reveals the
       desktop nav, so the mobile menu must not stay open (and must not leave
       the page scroll locked). Driven off resize rather than a matchMedia
       'change' listener, which some environments do not dispatch. */
    window.addEventListener('resize', function () {
      if (menuOpen && window.matchMedia('(min-width: 768px)').matches) setMenu(false);
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
