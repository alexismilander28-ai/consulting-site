(function () {
  var d = document;
  // Sample report: one page at a time. Without this script all three pages show.
  var pager = d.querySelector("[data-pager]");
  if (pager) {
    var btns = [].slice.call(pager.querySelectorAll("button"));
    var show = function (id) {
      btns.forEach(function (b) {
        var on = b.getAttribute("aria-controls") === id;
        b.setAttribute("aria-current", on ? "true" : "false");
        d.getElementById(b.getAttribute("aria-controls")).hidden = !on;
      });
    };
    btns.forEach(function (b) {
      b.addEventListener("click", function () { show(b.getAttribute("aria-controls")); });
    });
    show(btns[0].getAttribute("aria-controls"));
  }
  // Sample approval message: the two buttons only change this card. Nothing is sent.
  [].forEach.call(d.querySelectorAll("[data-approve]"), function (card) {
    var out = card.querySelector("[role=status]");
    var idle = out.textContent;
    [].forEach.call(card.querySelectorAll("button[data-say]"), function (b) {
      b.addEventListener("click", function () { out.textContent = b.getAttribute("data-say") || idle; });
    });
  });
  // See it work: one step at a time. Without this script every step shows, in order.
  [].forEach.call(d.querySelectorAll("[data-steps]"), function (box) {
    var tabs = [].slice.call(box.querySelectorAll(".stepper button"));
    var go = function (id, focus) {
      tabs.forEach(function (b) {
        var on = b.getAttribute("aria-controls") === id;
        b.setAttribute("aria-current", on ? "step" : "false");
        d.getElementById(b.getAttribute("aria-controls")).hidden = !on;
      });
      if (focus) { var h = d.getElementById(id).querySelector("h3"); if (h) { h.tabIndex = -1; h.focus(); } }
    };
    tabs.forEach(function (b) { b.addEventListener("click", function () { go(b.getAttribute("aria-controls")); }); });
    [].forEach.call(box.querySelectorAll("[data-next]"), function (b) {
      b.addEventListener("click", function () { go(b.getAttribute("data-next"), true); });
    });
    box.classList.add("steps-js");
    if (tabs.length) go(tabs[0].getAttribute("aria-controls"));
  });
  // Leave-behind: the print button.
  [].forEach.call(d.querySelectorAll("[data-print]"), function (b) {
    b.addEventListener("click", function () { window.print(); });
  });
})();
