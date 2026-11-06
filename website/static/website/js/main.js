(function () {
  'use strict';

  // Mobile navigation
  var toggle = document.getElementById('nav-toggle');
  var nav = document.getElementById('primary-nav');
  if (toggle && nav) {
    var setOpen = function (open) {
      nav.classList.toggle('open', open);
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    toggle.addEventListener('click', function () {
      setOpen(!nav.classList.contains('open'));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { setOpen(false); }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { setOpen(false); }
    });
    window.addEventListener('resize', function () {
      if (window.innerWidth > 860) { setOpen(false); }
    });
  }

  // Header border on scroll
  var header = document.getElementById('site-header');
  var onScroll = function () {
    if (header) { header.classList.toggle('scrolled', window.scrollY > 10); }
  };
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Reveal-on-scroll
  var items = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });
    items.forEach(function (el) { observer.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add('visible'); });
  }

  // Fade out success messages after a while (errors stay)
  document.querySelectorAll('.message-success').forEach(function (el) {
    setTimeout(function () {
      el.style.transition = 'opacity 0.6s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 700);
    }, 9000);
  });
})();
