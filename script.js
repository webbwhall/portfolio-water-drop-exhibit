/**
 * Portfolio interactions: mobile nav, reveal on scroll, scroll-spy nav,
 * lightbox modal, back-to-top, graceful fallbacks for broken images.
 */

(function () {
  const header = document.querySelector(".site-header");
  const nav = document.getElementById("site-nav");
  const navLinks = nav ? Array.from(nav.querySelectorAll("a[href^='#']")) : [];
  const navToggle = document.querySelector(".nav-toggle");
  const sections = Array.from(document.querySelectorAll("main section[id]"));
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-image");
  const lightboxCaption = document.getElementById("lightbox-caption");
  const toTopBtn = document.querySelector(".to-top");
  let lastLightboxTrigger = null;

  /* ------------------------------------------------------------------ */
  /* Header polish on scroll */
  /* ------------------------------------------------------------------ */
  if (header) {
    const onScroll = () => {
      header.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ------------------------------------------------------------------ */
  /* Mobile menu toggle */
  /* ------------------------------------------------------------------ */
  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = !document.body.classList.contains("nav-open");
      document.body.classList.toggle("nav-open", open);
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ------------------------------------------------------------------ */
  /* Reveal on scroll */
  /* ------------------------------------------------------------------ */
  const revealEls = document.querySelectorAll(".reveal");
  if (revealEls.length && "IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
          }
        });
      },
      { rootMargin: "-6% 0px -6% 0px", threshold: 0.08 }
    );
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* ------------------------------------------------------------------ */
  /* Active nav highlight: reliable scroll-based */
  /* ------------------------------------------------------------------ */
  function setActiveNav(id) {
    navLinks.forEach((link) => {
      const href = link.getAttribute("href");
      link.classList.toggle("is-active", href === `#${id}`);
    });
  }

  function getHeaderOffset() {
    return header ? Math.round(header.getBoundingClientRect().height) + 10 : 82;
  }

  function getNavSectionIds() {
    const ids = new Set();
    navLinks.forEach((link) => {
      const href = link.getAttribute("href") || "";
      if (href.startsWith("#") && href.length > 1) ids.add(href.slice(1));
    });
    return ids;
  }

  function scrollToAnchorTarget(target) {
    if (!target) return;
    const prefersReducedMotion = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches;
    const y = target.getBoundingClientRect().top + window.scrollY - getHeaderOffset();
    window.scrollTo({ top: Math.max(0, Math.round(y)), behavior: prefersReducedMotion ? "auto" : "smooth" });
  }

  /* Same scroll math for header nav and in-page anchor links */
  document.body.addEventListener("click", (e) => {
    const anchor = e.target.closest("a[href^='#']");
    if (!anchor || anchor.closest("#lightbox")) return;
    const href = anchor.getAttribute("href");
    if (!href || href === "#") return;
    const rawId = href.slice(1);
    const id = rawId.includes("%") ? decodeURIComponent(rawId) : rawId;
    const target = document.getElementById(id);
    if (!target) return;
    e.preventDefault();
    if (nav?.contains(anchor)) {
      document.body.classList.remove("nav-open");
      navToggle?.setAttribute("aria-expanded", "false");
    }
    scrollToAnchorTarget(target);
    if (history.replaceState) history.replaceState(null, "", `#${encodeURIComponent(id)}`);
  });

  let ticking = false;
  function updateScrollSpy() {
    ticking = false;
    if (!sections.length || !navLinks.length) return;

    const offset = getHeaderOffset();
    const scrollY = window.scrollY || window.pageYOffset || 0;
    const navIds = getNavSectionIds();

    function clearHighlight() {
      navLinks.forEach((link) => link.classList.remove("is-active"));
    }

    // If near bottom, highlight the last nav-linked section reached in the layout
    const nearBottom = window.innerHeight + scrollY >= document.body.scrollHeight - 4;
    if (nearBottom) {
      for (let i = sections.length - 1; i >= 0; i -= 1) {
        const id = sections[i].id;
        if (id && navIds.has(id)) {
          setActiveNav(id);
          return;
        }
      }
      clearHighlight();
      return;
    }

    // Prefer the furthest-down nav section whose top passes the sticky header threshold
    let currentNavId = null;
    for (const sec of sections) {
      const topAbs = sec.getBoundingClientRect().top + scrollY;
      if (topAbs - offset <= scrollY + 2) {
        if (navIds.has(sec.id)) currentNavId = sec.id;
      } else {
        break;
      }
    }

    if (currentNavId) setActiveNav(currentNavId);
    else clearHighlight();
  }

  function onScrollSpy() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(updateScrollSpy);
  }

  window.addEventListener("scroll", onScrollSpy, { passive: true });
  window.addEventListener("resize", onScrollSpy, { passive: true });
  updateScrollSpy();

  /* Landing with #section in the URL lands under the sticky header */
  function scrollToHashIfPresent() {
    const hash = window.location.hash;
    if (!hash || hash === "#") return;
    const id = decodeURIComponent(hash.slice(1));
    const target = document.getElementById(id);
    if (!target) return;
    requestAnimationFrame(() => scrollToAnchorTarget(target));
  }
  scrollToHashIfPresent();

  /* ------------------------------------------------------------------ */
  /* Lightbox */
  /* ------------------------------------------------------------------ */
  function openLightbox(src, alt, captionText) {
    if (!lightbox || !lightboxImg || !lightboxCaption) return;
    lastLightboxTrigger = document.activeElement;
    lightboxImg.src = src;
    lightboxImg.alt = alt || "";
    lightboxCaption.textContent = captionText || "";
    lightbox.hidden = false;
    document.body.classList.add("lightbox-open");
    lightbox.querySelector(".lightbox-close")?.focus?.();
  }

  function closeLightbox() {
    if (!lightbox || !lightboxImg) return;
    lightbox.hidden = true;
    lightboxImg.removeAttribute("src");
    document.body.classList.remove("lightbox-open");
    if (lastLightboxTrigger && typeof lastLightboxTrigger.focus === "function") {
      lastLightboxTrigger.focus();
    }
    lastLightboxTrigger = null;
  }

  document.querySelectorAll(".lightbox-trigger").forEach((btn) => {
    btn.addEventListener("click", () => {
      const img = btn.querySelector("img");
      const src = img?.currentSrc || img?.src || "";
      const alt = img?.getAttribute("alt") || "";
      const cap = btn.getAttribute("data-caption") || "";
      openLightbox(src, alt, cap);
    });
  });

  lightbox?.addEventListener("click", (e) => {
    if (e.target.matches("[data-close-lightbox], .lightbox-backdrop")) {
      closeLightbox();
    }
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !lightbox?.hidden) {
      closeLightbox();
    }
  });

  /* ------------------------------------------------------------------ */
  /* Back to top */
  /* ------------------------------------------------------------------ */
  toTopBtn?.addEventListener("click", () => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  });

  // Intentionally no \"missing image\" placeholders:
  // this site is meant to ship with real exported assets in assets/images.
})();
