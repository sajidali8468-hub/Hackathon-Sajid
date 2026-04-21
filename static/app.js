const form = document.querySelector("#brandForm");
const description = document.querySelector("#description");
const generateButton = document.querySelector("#generateButton");

const nodes = {
  brandName: document.querySelector("#brandName"),
  mockBrandName: document.querySelector("#mockBrandName"),
  mockHeadline: document.querySelector("#mockHeadline"),
  mockTone: document.querySelector("#mockTone"),
  mockButton: document.querySelector("#mockButton"),
  mockHomepage: document.querySelector("#mockHomepage"),
  toneGuide: document.querySelector("#toneGuide"),
  strategyList: document.querySelector("#strategyList"),
  latencyMetric: document.querySelector("#latencyMetric"),
  tokenMetric: document.querySelector("#tokenMetric"),
  groundingMetric: document.querySelector("#groundingMetric"),
  sanityLog: document.querySelector("#sanityLog"),
  primarySwatch: document.querySelector("#primarySwatch"),
  secondarySwatch: document.querySelector("#secondarySwatch"),
  accentSwatch: document.querySelector("#accentSwatch"),
};

function loadFonts(typography) {
  const families = [typography.heading, typography.body]
    .filter(Boolean)
    .map((family) => `family=${encodeURIComponent(family).replaceAll("%20", "+")}:wght@400;600;700`);

  if (!families.length) return;
  const existing = document.querySelector("#dynamicFonts");
  if (existing) existing.remove();

  const link = document.createElement("link");
  link.id = "dynamicFonts";
  link.rel = "stylesheet";
  link.href = `https://fonts.googleapis.com/css2?${families.join("&")}&display=swap`;
  document.head.appendChild(link);
}

function applyBrand(brand) {
  const palette = brand.palette;
  const typography = brand.typography;
  loadFonts(typography);

  document.documentElement.style.setProperty("--brand-primary", palette.primary);
  document.documentElement.style.setProperty("--brand-secondary", palette.secondary);
  document.documentElement.style.setProperty("--brand-accent", palette.accent);
  document.documentElement.style.setProperty("--heading-font", `"${typography.heading}", Georgia, serif`);
  document.documentElement.style.setProperty("--body-font", `"${typography.body}", system-ui, sans-serif`);

  if (nodes.brandName) nodes.brandName.textContent = brand.brand_name;
  if (nodes.mockBrandName) nodes.mockBrandName.textContent = brand.brand_name;
  if (nodes.mockHeadline) nodes.mockHeadline.textContent = brand.tagline;
  if (nodes.mockTone) nodes.mockTone.textContent = brand.tone;
  if (nodes.toneGuide) nodes.toneGuide.textContent = brand.tone;
  if (nodes.latencyMetric) nodes.latencyMetric.textContent = `${brand.latency_ms || 0} ms`;
  if (nodes.tokenMetric) nodes.tokenMetric.textContent = brand.token_count || 0;
  if (nodes.groundingMetric) nodes.groundingMetric.textContent = brand.grounding?.profile || "General Founder Brand";
  if (nodes.sanityLog) {
    nodes.sanityLog.textContent = brand.sanity_log?.length ? brand.sanity_log.join(" ") : "Contrast checks passed.";
  }

  if (nodes.primarySwatch) nodes.primarySwatch.style.background = palette.primary;
  if (nodes.secondarySwatch) nodes.secondarySwatch.style.background = palette.secondary;
  if (nodes.accentSwatch) nodes.accentSwatch.style.background = palette.accent;

  if (nodes.strategyList) {
    nodes.strategyList.innerHTML = "";
    brand.social_strategy.forEach((pillar) => {
      const item = document.createElement("li");
      item.textContent = pillar;
      nodes.strategyList.appendChild(item);
    });
  }
}

async function fetchCurrentBrand() {
  try {
    const response = await fetch("/api/current-brand");
    if (response.ok) applyBrand(await response.json());
  } catch {
    // Initial preview remains usable when no server state exists.
  }
}

if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    generateButton.disabled = true;
    generateButton.querySelector("span").textContent = "Generating...";

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description: description.value }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.detail || "Unable to generate a brand identity.");
      applyBrand(payload);
    } catch (error) {
      if (nodes.sanityLog) nodes.sanityLog.textContent = error.message;
    } finally {
      generateButton.disabled = false;
      generateButton.querySelector("span").textContent = "Generate Identity";
    }
  });
}

fetchCurrentBrand();
