/* AB Coaching Fitness — progressive enhancement only.
   The site is complete and readable with this file removed. */
(function () {
  "use strict";

  var reduced = window.matchMedia &&
                window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* Scroll reveals. Elements marked .r are visible by default; the
     .js class on <html> (set inline in <head>) is what hides them,
     so no-JS visitors never see a blank page. */
  var targets = document.querySelectorAll(".r");

  if (reduced || !("IntersectionObserver" in window)) {
    for (var i = 0; i < targets.length; i++) targets[i].classList.add("in");
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    for (var j = 0; j < entries.length; j++) {
      if (entries[j].isIntersecting) {
        entries[j].target.classList.add("in");
        io.unobserve(entries[j].target);
      }
    }
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.05 });

  for (var k = 0; k < targets.length; k++) io.observe(targets[k]);
})();
