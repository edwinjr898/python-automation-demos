(function () {
  const hourlyRateEl = document.getElementById("hourlyRate");
  const hoursEl = document.getElementById("hours");
  const rushFeeEl = document.getElementById("rushFee");
  const totalDisplay = document.getElementById("totalDisplay");
  const baseDisplay = document.getElementById("baseDisplay");
  const rushDisplay = document.getElementById("rushDisplay");
  const grandDisplay = document.getElementById("grandDisplay");
  const summaryLine = document.getElementById("summaryLine");
  const themeToggle = document.getElementById("themeToggle");

  function money(n) {
    return n.toLocaleString("en-US", {
      style: "currency",
      currency: "USD",
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    });
  }

  function parseNonNeg(el) {
    const v = parseFloat(el.value);
    if (Number.isNaN(v) || v < 0) return 0;
    return v;
  }

  function update() {
    const rate = parseNonNeg(hourlyRateEl);
    const hours = parseNonNeg(hoursEl);
    let rushPct = parseNonNeg(rushFeeEl);
    if (rushPct > 100) rushPct = 100;

    const base = rate * hours;
    const rushAmount = base * (rushPct / 100);
    const total = base + rushAmount;

    totalDisplay.textContent = money(total);
    baseDisplay.textContent = money(base);
    rushDisplay.textContent =
      rushPct > 0 ? money(rushAmount) + " (" + rushPct + "%)" : money(0);
    grandDisplay.textContent = money(total);

    const hoursLabel = hours === 1 ? "1 hour" : hours + " hours";
    summaryLine.textContent =
      rushPct > 0
        ? money(rate) + "/hr x " + hoursLabel + " + " + rushPct + "% rush"
        : money(rate) + "/hr x " + hoursLabel;
  }

  [hourlyRateEl, hoursEl, rushFeeEl].forEach(function (el) {
    el.addEventListener("input", update);
    el.addEventListener("change", update);
  });

  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    try {
      localStorage.setItem("invoice-estimator-theme", theme);
    } catch (_) {}
  }

  themeToggle.addEventListener("click", function () {
    const current =
      document.documentElement.getAttribute("data-theme") === "light"
        ? "light"
        : "dark";
    applyTheme(current === "light" ? "dark" : "light");
  });

  try {
    const saved = localStorage.getItem("invoice-estimator-theme");
    if (saved === "light" || saved === "dark") applyTheme(saved);
  } catch (_) {}

  update();
})();
