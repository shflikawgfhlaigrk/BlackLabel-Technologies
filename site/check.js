#!/usr/bin/env node
// Automated truth/ship-clean checks per the 2026-07-10 site design spec.
// Usage: node check.js   (run after build.js; exits non-zero on any failure)
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const data = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "site.json"), "utf8"));
const distPath = path.join(ROOT, "dist", "index.html");
const failures = [];
const ok = (cond, msg) => { if (!cond) failures.push(msg); };

// 1. Status vocabulary is limited to Verified / Partial / Building.
const ALLOWED = new Set(["Verified", "Partial", "Building"]);
for (const item of [...data.work, ...data.products]) {
  if (item.status) ok(ALLOWED.has(item.status), `status "${item.status}" on "${item.name}" not in {Verified, Partial, Building}`);
}

// 2. No fabrication vocabulary anywhere in content or output.
const BANNED = [/verified buyer/i, /testimonial/i, /★/, /five stars/i, /trusted by/i, /customers say/i];
const rendered = fs.existsSync(distPath) ? fs.readFileSync(distPath, "utf8") : "";
ok(rendered.length > 0, "dist/index.html missing — run build.js first");
const corpus = JSON.stringify(data) + rendered;
for (const re of BANNED) ok(!re.test(corpus), `banned fabrication pattern ${re} found`);

// 3. noindex gate: while meta.noindex is true, the rendered page must carry the robots meta
//    and robots.txt must disallow.
if (data.meta.noindex) {
  ok(/<meta name="robots" content="noindex, nofollow">/.test(rendered), "noindex meta missing while gate is on");
  const robots = fs.readFileSync(path.join(ROOT, "dist", "robots.txt"), "utf8");
  ok(/Disallow: \//.test(robots), "robots.txt does not disallow while noindex gate is on");
}

// 4. Working-name notice must be visible.
ok(rendered.includes("working name"), "working-name notice missing from rendered page");
ok(rendered.includes("blacklabelbots.com"), "pointer to current verified public surface missing");

// 5. Ship-clean: no machine-local paths or undeclared local services in data or output.
for (const re of [/\/Users\//, /localhost/, /127\.0\.0\.1/, /:5433/, /~\/(?!\w)/]) {
  ok(!re.test(corpus), `machine-local reference ${re} found`);
}

// 6. Links: every href in data must be https:// , mailto:, or an in-page anchor.
const links = [];
const walk = (v) => {
  if (typeof v === "string") { if (/^(href|link)$/.test("")) {} }
  else if (Array.isArray(v)) v.forEach(walk);
  else if (v && typeof v === "object") for (const [k, val] of Object.entries(v)) {
    if ((k === "link" || k === "href") && typeof val === "string") links.push(val);
    else walk(val);
  }
};
walk(data);
for (const l of links) ok(/^(https:\/\/|mailto:|#)/.test(l), `link "${l}" is not https/mailto/anchor`);

// 7. Metadata present.
ok(!!data.meta.title && !!data.meta.description, "meta title/description missing");

if (failures.length) {
  console.error("CHECK FAILED:");
  for (const f of failures) console.error(" - " + f);
  process.exit(1);
}
console.log(`all checks passed (${links.length} links validated, noindex=${data.meta.noindex})`);
