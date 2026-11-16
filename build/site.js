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
  // Leave-behind: the print button.
  [].forEach.call(d.querySelectorAll("[data-print]"), function (b) {
    b.addEventListener("click", function () { window.print(); });
  });
})();
