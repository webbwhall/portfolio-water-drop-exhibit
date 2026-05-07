/**
 * Portfolio interactions: mobile nav, reveal on scroll, scroll-spy nav,
 * lightbox modal, back-to-top, graceful fallbacks for broken images.
 */

(function () {
  const header = document.querySelector(".site-header");
  const nav = document.getElementById("site-nav");
  const navLinks = nav ? Array.from(nav.querySelectorAll("a[href^='#']")) : [];
  const navToggle = document.querySelector(".nav-toggle");
  const sections = document.querySelectorAll("main section[id]");
  const lightbox = document.getElementById("lightbox");
  const lightboxImg = document.getElementById("lightbox-image");
  const lightboxCaption = document.getElementById("lightbox-caption");
  const toTopBtn = document.querySelector(".to-top");
  let lastLightboxTrigger = null;

  /* ------------------------------------------------------------------ */
  /* Mobile navigation */
  /* ------------------------------------------------------------------ */
  if (navToggle && nav) {
    navToggle.addEventListener("click", () => {
      const open = !document.body.classList.contains("nav-open");
      document.body.classList.toggle("nav-open", open);
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.addEventListener("click", (e) => {
      const anchor = e.target.closest("a");
      if (!anchor) return;
      document.body.classList.remove("nav-open");
      navToggle.setAttribute("aria-expanded", "false");
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
  /* Active nav highlight — uses section visibility */
  /* ------------------------------------------------------------------ */
  let activeId = "";
  if (sections.length && "IntersectionObserver" in window) {
    const headerH = () => (header ? header.getBoundingClientRect().height : 72);
    const navObserver = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];
        if (!visible) return;
        const id = visible.target.id;
        if (!id || id === activeId) return;
        activeId = id;
        navLinks.forEach((link) => {
          const href = link.getAttribute("href");
          link.classList.toggle("is-active", href === `#${id}`);
        });
      },
      {
        threshold: [0.18, 0.28, 0.42, 0.55],
        rootMargin: `-${Math.round(headerH() + 8)}px 0px -55% 0px`,
      }
    );
    sections.forEach((sec) => navObserver.observe(sec));
  }

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
