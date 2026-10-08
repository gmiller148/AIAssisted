#!/usr/bin/env node
// Render a Mermaid (.mmd) or SVG (.svg) source file to PNG with the installed Chrome.
//
//   node .claude/tools/render.mjs <file.mmd|file.svg>                 preview → prints PNG path
//   node .claude/tools/render.mjs <file.mmd|file.svg> --save-as <slug> publish into viz/ → prints filename + path

import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import puppeteer from "puppeteer";

const toolsDir = path.dirname(fileURLToPath(import.meta.url));
const projectRoot = path.resolve(toolsDir, "..", "..");
const chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";

const args = process.argv.slice(2);
const src = args[0];
const saveIdx = args.indexOf("--save-as");
const slug = saveIdx >= 0 ? args[saveIdx + 1] : null;

if (!src || !fs.existsSync(src) || (saveIdx >= 0 && !slug)) {
  console.error("usage: render.mjs <file.mmd|file.svg> [--save-as <slug>]");
  process.exit(2);
}

const ext = path.extname(src).toLowerCase();
let out;
if (slug) {
  const ts = new Date().toISOString().replace(/[-:]/g, "").replace("T", "-").slice(0, 15);
  const clean = slug.toLowerCase().replace(/[^a-z0-9-]+/g, "-").replace(/^-|-$/g, "");
  out = path.join(projectRoot, "viz", `viz-${clean}-${ts}.png`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
} else {
  out = `${src}.preview.png`;
}

try {
  if (ext === ".mmd") {
    const cfg = path.join(toolsDir, "puppeteer-config.json");
    if (!fs.existsSync(cfg)) fs.writeFileSync(cfg, JSON.stringify({ executablePath: chrome, headless: "new" }));
    execFileSync(path.join(toolsDir, "node_modules", ".bin", "mmdc"),
      ["-i", src, "-o", out, "-b", "white", "-s", "2", "-p", cfg], { stdio: ["ignore", "pipe", "pipe"] });
  } else if (ext === ".svg") {
    const svg = fs.readFileSync(src, "utf8");
    const browser = await puppeteer.launch({ executablePath: chrome, headless: true });
    try {
      const page = await browser.newPage();
      await page.setViewport({ width: 2000, height: 2000, deviceScaleFactor: 2 });
      await page.setContent(`<html><body style="margin:0;background:white">${svg}</body></html>`);
      const el = await page.$("svg");
      if (!el) throw new Error("no <svg> element found in source");
      await el.screenshot({ path: out });
    } finally {
      await browser.close();
    }
  } else {
    throw new Error(`unsupported extension ${ext} (use .mmd or .svg)`);
  }
} catch (e) {
  console.error("RENDER ERROR:", (e.stderr?.toString() || e.message).trim());
  process.exit(1);
}

if (slug) {
  console.log(`filename: ${path.basename(out)}\npath: ${out}`);
} else {
  console.log(`preview: ${out}`);
}
