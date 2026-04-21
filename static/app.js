const form = document.querySelector("#brandForm");
const description = document.querySelector("#description");
const generateButton = document.querySelector("#generateButton");

let currentBrand = null;

const nodes = {
  brandName: document.querySelector("#brandName"),
  mockBrandName: document.querySelector("#mockBrandName"),
  mockHeadline: document.querySelector("#mockHeadline"),
  mockTone: document.querySelector("#mockTone"),
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
  buildBioButton: document.querySelector("#buildBioButton"),
  buildCaptionButton: document.querySelector("#buildCaptionButton"),
  buildTaglinesButton: document.querySelector("#buildTaglinesButton"),
  brandBioOutput: document.querySelector("#brandBioOutput"),
  launchCaptionOutput: document.querySelector("#launchCaptionOutput"),
  taglineListOutput: document.querySelector("#taglineListOutput"),
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

function getGroundingLabel(brand) {
  return brand?.grounding?.profile || "General Founder Brand";
}

function getFirstSentence(text) {
  if (!text) return "";
  const [first] = text.split(".").filter(Boolean);
  return first ? `${first.trim()}.` : text;
}

function toLowerStart(text) {
  if (!text) return "";
  return text.charAt(0).toLowerCase() + text.slice(1);
}

function buildBrandBio(brand) {
  const focus = brand.social_strategy?.[0] || "clear positioning";
  return `${brand.brand_name} is a ${getGroundingLabel(brand).toLowerCase()} concept designed to make a stronger first impression. ${getFirstSentence(brand.tone)} The identity is built around ${toLowerStart(focus)}, giving the business a brand system that feels distinctive, useful, and ready to launch.`;
}

function buildLaunchCaption(brand) {
  const proof = brand.social_strategy?.[1] || "clear customer insight";
  return `Introducing ${brand.brand_name} — ${brand.tagline} Built with a ${toLowerStart(getFirstSentence(brand.tone).replace(/\.$/, ""))} voice, a grounded palette, and a sharper point of view. Start with ${toLowerStart(proof)} and turn attention into trust.`;
}

function buildTaglines(brand) {
  const brandWord = brand.brand_name.split(" ")[0];
  return [
    brand.tagline,
    `${brandWord} for sharper brand moments.`,
    `Clear positioning for ${getGroundingLabel(brand).toLowerCase()}.`,
    "A cleaner story, a stronger first impression.",
  ];
}

function renderBrandBio(brand) {
  if (nodes.brandBioOutput) {
    nodes.brandBioOutput.textContent = buildBrandBio(brand);
  }
}

function renderLaunchCaption(brand) {
  if (nodes.launchCaptionOutput) {
    nodes.launchCaptionOutput.textContent = buildLaunchCaption(brand);
  }
}

function renderTaglines(brand) {
  if (!nodes.taglineListOutput) return;

  nodes.taglineListOutput.innerHTML = "";
  buildTaglines(brand).forEach((tagline) => {
    const item = document.createElement("li");
    item.textContent = tagline;
    nodes.taglineListOutput.appendChild(item);
  });
}

function renderExtraOutputs(brand) {
  renderBrandBio(brand);
  renderLaunchCaption(brand);
  renderTaglines(brand);
}

function withBrand(callback, emptyMessage) {
  if (!currentBrand) {
    if (nodes.sanityLog) nodes.sanityLog.textContent = emptyMessage;
    return;
  }
  callback(currentBrand);
}

function applyBrand(brand) {
  currentBrand = brand;

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
  if (nodes.groundingMetric) nodes.groundingMetric.textContent = getGroundingLabel(brand);
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

  renderExtraOutputs(brand);
}

async function fetchCurrentBrand() {
  try {
    const response = await fetch("/api/current-brand");
    if (response.ok) applyBrand(await response.json());
  } catch {
    // Initial preview remains usable when no server state exists.
  }
}

if (nodes.buildBioButton) {
  nodes.buildBioButton.addEventListener("click", () => {
    withBrand(renderBrandBio, "Generate a brand identity first to create a brand bio.");
  });
}

if (nodes.buildCaptionButton) {
  nodes.buildCaptionButton.addEventListener("click", () => {
    withBrand(renderLaunchCaption, "Generate a brand identity first to create a launch caption.");
  });
}

if (nodes.buildTaglinesButton) {
  nodes.buildTaglinesButton.addEventListener("click", () => {
    withBrand(renderTaglines, "Generate a brand identity first to spin tagline variations.");
  });
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
      if (nodes.sanityLog) {
        nodes.sanityLog.textContent = error.message || "Something went wrong.";
      }
    } finally {
      generateButton.disabled = false;
      generateButton.querySelector("span").textContent = "Generate Identity";
    }
  });
}

fetchCurrentBrand();
