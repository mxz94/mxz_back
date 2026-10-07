// 列表页缩略图生成器
//
// 文章原图放在 public/img 下（95MB / 786 张），Astro 不会优化 public 里的图片，
// 直接用原图当列表缩略图会让首页/列表页加载好几 MB。这里预先生成一份 400px 宽的
// webp 缩略图到 public/thumb（保持同样的目录结构），列表页优先用它。
//
// 关键：只给「列表页真正会用到的封面图」生成（默认模式，约 316 张）。
// 逻辑与运行时 src/utils/getHeroImageLinkFromMd.ts 保持一致：
// frontmatter 的 heroImage 优先，否则取正文里第一张图。
// 其余图不生成、已有的旧缩略图会被清掉，避免 dist 白白多十几个 MB。
//
// 用法：
//   node scripts/gen-thumbs.mjs           增量：只处理缺失或源图已更新的（默认只处理被用到的图）
//   node scripts/gen-thumbs.mjs --force   强制重生成
//   node scripts/gen-thumbs.mjs --all     给 public/img 下所有图生成（不清理）
//
// 已挂到 package.json 的 build 前置步骤，所以 `npm run build` 会自动跑一遍。
// 并发可用 THUMB_JOBS 覆盖；CI 上建议同时设 UV_THREADPOOL_SIZE=8（sharp 走 libuv 线程池）。

import { createRequire } from "module";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const require = createRequire(import.meta.url);
const sharp = require("sharp");

const SRC = path.resolve("public/img");
const OUT = path.resolve("public/thumb");
const CONTENT = path.resolve("src/content");
const WIDTH = 400;
const EXTS = new Set([".jpg", ".jpeg", ".png", ".webp"]);
const MD_EXTS = new Set([".md", ".mdx"]);

const FORCE = process.argv.includes("--force");
const ALL = process.argv.includes("--all");
const CONCURRENCY = Number(process.env.THUMB_JOBS) || 8;

function walk(dir, exts) {
  const out = [];
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...walk(full, exts));
    else if (exts.has(path.extname(entry.name).toLowerCase())) out.push(full);
  }
  return out;
}

/* ---------- 与运行时一致的封面图提取 ---------- */

const VIDEO_EXTENSIONS = /\.(mp4|mov|m4v|webm|ogv)(?:[?#].*)?$/i;
const IMAGE_EXTENSIONS = /\.(avif|gif|jpe?g|png|svg|webp)(?:[?#].*)?$/i;

function cleanAssetPath(src) {
  if (!src) return null;
  const cleanSrc = src.trim().replace(/^['"]|['"]$/g, "");
  if (!cleanSrc || cleanSrc.startsWith("#") || cleanSrc.startsWith("data:")) {
    return null;
  }
  const imageCandidate = cleanSrc.split("?v=")[0];
  if (
    !imageCandidate ||
    VIDEO_EXTENSIONS.test(imageCandidate) ||
    /[{}<>]/.test(imageCandidate)
  ) {
    return null;
  }
  const normalized = imageCandidate.replace(/\\/g, "/");
  const publicIndex = normalized.lastIndexOf("public/");
  if (publicIndex >= 0) {
    return `/${normalized.slice(publicIndex + "public/".length)}`;
  }
  if (normalized.startsWith("//")) return `https:${normalized}`;
  if (/^https?:\/\//i.test(normalized) || normalized.startsWith("/")) {
    return normalized;
  }
  if (normalized.startsWith("img/") && IMAGE_EXTENSIONS.test(normalized)) {
    return `/${normalized}`;
  }
  return null;
}

function heroFromMd(text) {
  const fm = /^---\r?\n([\s\S]*?)\r?\n---/.exec(text);
  if (fm) {
    const m = /^heroImage:\s*(.+)$/m.exec(fm[1]);
    if (m) {
      const hero = cleanAssetPath(m[1].trim().replace(/^['"]|['"]$/g, ""));
      if (hero) return hero;
    }
  }
  const body = fm ? text.slice(fm.index + fm[0].length) : text;
  const candidates = [];
  const patterns = [
    /!\[[^\]]*]\(([^)\s]+)(?:\s+["'][^)]*["'])?\)/g,
    /<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi,
    /<video\b[^>]*\bposter=["']([^"']+)["'][^>]*>/gi,
    /\bdata-photo-src=["']([^"']+)["']/gi,
  ];
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(body)) !== null) {
      const src = cleanAssetPath(match[1]);
      if (src) candidates.push({ src, index: match.index });
    }
  }
  candidates.sort((a, b) => a.index - b.index);
  return candidates[0]?.src || null;
}

// 返回「相对 public/img、不含扩展名」的集合
function collectUsedBases() {
  const bases = new Set();
  for (const md of walk(CONTENT, MD_EXTS)) {
    const hero = heroFromMd(fs.readFileSync(md, "utf8"));
    if (!hero || !hero.startsWith("/img/")) continue;
    let rel = hero.slice("/img/".length);
    try {
      rel = decodeURIComponent(rel);
    } catch {
      /* 保持原样 */
    }
    rel = rel.replace(/\\/g, "/");
    bases.add(rel.replace(/\.[^./]+$/, ""));
  }
  return bases;
}

const stripExt = (rel) => rel.replace(/\.[^./]+$/, "");

// 固定并发的任务池
async function runPool(items, size, worker) {
  let cursor = 0;
  const workers = Array.from(
    { length: Math.min(size, Math.max(items.length, 1)) },
    async () => {
      while (cursor < items.length) {
        await worker(items[cursor++]);
      }
    }
  );
  await Promise.all(workers);
}

/* ---------- 主流程 ---------- */

const t0 = Date.now();
const files = walk(SRC, EXTS);
const usedBases = ALL ? null : collectUsedBases();

let made = 0;
let skipped = 0;
let failed = 0;
let pruned = 0;

// 清掉不再被用到的旧缩略图（并行删，串行删在 Windows 上慢到几十秒）
if (usedBases) {
  const stale = walk(OUT, new Set([".webp"]))
    .filter((file) => !usedBases.has(stripExt(path.relative(OUT, file).replace(/\\/g, "/"))))
    .map((file) => path.relative(OUT, file));
  await runPool(stale, 8, async (rel) => {
    await fs.promises.rm(path.join(OUT, rel), { force: true });
    pruned += 1;
  });
}

const jobs = [];
for (const file of files) {
  const rel = path.relative(SRC, file).replace(/\\/g, "/");
  if (usedBases && !usedBases.has(stripExt(rel))) continue;

  const dest = path.join(OUT, rel.replace(/\.(jpe?g|png|webp)$/i, ".webp"));

  if (!FORCE && fs.existsSync(dest)) {
    // 源图没被替换过就跳过
    if (fs.statSync(dest).mtimeMs >= fs.statSync(file).mtimeMs) {
      skipped += 1;
      continue;
    }
  }

  jobs.push({ file, rel, dest });
}

// 目录先串行建好：并发 mkdir 在 Windows 上会偶发 "unable to open for write"
for (const dir of new Set(jobs.map((job) => path.dirname(job.dest)))) {
  fs.mkdirSync(dir, { recursive: true });
}

await runPool(jobs, CONCURRENCY, async (job) => {
  try {
    await sharp(job.file)
      .rotate()
      .resize({ width: WIDTH, withoutEnlargement: true })
      .webp({ quality: 72 })
      .toFile(job.dest);
    made += 1;
  } catch (err) {
    failed += 1;
    console.error("失败:", job.rel, err.message);
  }
});

console.log(
  `缩略图：新建 ${made}，跳过 ${skipped}，清理 ${pruned}，失败 ${failed}` +
    `（候选 ${usedBases ? usedBases.size : files.length} / 全库 ${files.length}），` +
    `耗时 ${((Date.now() - t0) / 1000).toFixed(1)}s`
);
