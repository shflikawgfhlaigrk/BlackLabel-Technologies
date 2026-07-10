#!/usr/bin/env node
// Zero-dependency static build: renders dist/ from data/site.json.
// Usage: node build.js   (from site/; writes site/dist/)
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const DIST = path.join(ROOT, "dist");
const data = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "site.json"), "utf8"));

const esc = (s) =>
  String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");

const STATUS_ORDER = { Verified: 0, Partial: 1, Building: 2 };
const statusBadge = (s) => `<span class="status status-${s.toLowerCase()}">${esc(s)}</span>`;

const entry = (item) => `
      <article class="entry">
        <div class="entry-head">
          <h3>${item.link ? `<a href="${esc(item.link)}">${esc(item.name)}</a>` : esc(item.name)}</h3>
          ${item.status ? statusBadge(item.status) : ""}
        </div>
        <p>${esc(item.summary)}</p>
      </article>`;

const sortedProducts = [...data.products].sort(
  (a, b) => STATUS_ORDER[a.status] - STATUS_ORDER[b.status] || a.name.localeCompare(b.name)
);

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
${data.meta.noindex ? '<meta name="robots" content="noindex, nofollow">' : ""}
<title>${esc(data.meta.title)}</title>
<meta name="description" content="${esc(data.meta.description)}">
<style>
  :root { --bg:#0a0a0b; --panel:#121214; --line:#232326; --ink:#ece9e2; --dim:#9b968c; --brass:#c8a96a; }
  * { margin:0; padding:0; box-sizing:border-box; }
  html { scroll-behavior:smooth; }
  body { background:var(--bg); color:var(--ink); font:16px/1.65 -apple-system, "Helvetica Neue", Segoe UI, sans-serif; -webkit-font-smoothing:antialiased; }
  a { color:var(--brass); text-decoration:none; }
  a:hover { text-decoration:underline; }
  .notice { background:var(--panel); border-bottom:1px solid var(--line); color:var(--dim); font-size:13px; padding:10px 24px; text-align:center; letter-spacing:.02em; }
  .band { max-width:1060px; margin:0 auto; padding:88px 24px; border-bottom:1px solid var(--line); }
  header.band { padding:140px 24px 120px; }
  h1 { font-size:clamp(34px,6vw,64px); line-height:1.06; letter-spacing:-.02em; font-weight:750; max-width:17ch; }
  .support { color:var(--dim); font-size:clamp(17px,2.4vw,21px); margin-top:26px; max-width:52ch; }
  .actions { margin-top:44px; display:flex; gap:16px; flex-wrap:wrap; }
  .btn { display:inline-block; padding:13px 26px; border:1px solid var(--brass); color:var(--brass); font-weight:600; letter-spacing:.03em; }
  .btn.primary { background:var(--brass); color:#0a0a0b; }
  .btn:hover { text-decoration:none; filter:brightness(1.1); }
  h2 { font-size:13px; text-transform:uppercase; letter-spacing:.22em; color:var(--brass); font-weight:650; margin-bottom:40px; }
  .entry { padding:26px 0; border-top:1px solid var(--line); }
  .entry:first-of-type { border-top:0; }
  .entry-head { display:flex; align-items:baseline; gap:14px; flex-wrap:wrap; }
  .entry h3 { font-size:21px; font-weight:650; letter-spacing:-.01em; }
  .entry h3 a { color:var(--ink); }
  .entry p { color:var(--dim); margin-top:8px; max-width:64ch; }
  .status { font-size:11px; text-transform:uppercase; letter-spacing:.14em; padding:3px 10px; border:1px solid var(--line); color:var(--dim); }
  .status-verified { border-color:var(--brass); color:var(--brass); }
  .status-partial { border-color:#8b8577; color:#b3ac9d; }
  .archive-note, .contact p { color:var(--dim); max-width:60ch; }
  .contact a.mail { font-size:clamp(19px,3vw,26px); font-weight:650; display:inline-block; margin-top:18px; }
  footer { padding:48px 24px 64px; color:var(--dim); font-size:13px; text-align:center; }
</style>
</head>
<body>
<div class="notice">${esc(data.meta.workingNameNotice)}</div>

<header class="band">
  <h1>${esc(data.hero.headline)}</h1>
  <p class="support">${esc(data.hero.support)}</p>
  <div class="actions">
    <a class="btn primary" href="${esc(data.hero.primaryAction.href)}">${esc(data.hero.primaryAction.label)}</a>
    <a class="btn" href="${esc(data.hero.secondaryAction.href)}">${esc(data.hero.secondaryAction.label)}</a>
  </div>
</header>

<section class="band" id="work">
  <h2>Work</h2>${data.work.map(entry).join("\n")}
</section>

<section class="band" id="products">
  <h2>Products</h2>${sortedProducts.map(entry).join("\n")}
</section>

<section class="band" id="systems">
  <h2>Systems</h2>${data.systems.map(entry).join("\n")}
</section>

<section class="band" id="archive">
  <h2>Archive</h2>
  <p class="archive-note">${esc(data.archive.note)}</p>
</section>

<section class="band contact" id="contact">
  <h2>${esc(data.contact.heading)}</h2>
  <p>${esc(data.contact.body)}</p>
  <a class="mail" href="mailto:${esc(data.contact.email)}">${esc(data.contact.email)}</a>
</section>

<footer>${esc(data.meta.workingNameNotice)} &middot; &copy; 2026 Black Label</footer>
</body>
</html>
`;

fs.rmSync(DIST, { recursive: true, force: true });
fs.mkdirSync(DIST, { recursive: true });
fs.writeFileSync(path.join(DIST, "index.html"), html);
fs.writeFileSync(
  path.join(DIST, "robots.txt"),
  data.meta.noindex ? "User-agent: *\nDisallow: /\n" : "User-agent: *\nAllow: /\n"
);
console.log(`built dist/index.html (${html.length} bytes), noindex=${data.meta.noindex}`);
