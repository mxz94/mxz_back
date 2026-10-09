// 生成站点社交分享图 + 多尺寸 favicon / apple-touch-icon / webmanifest
// 依赖: sharp(已在 node_modules)。运行: node scripts/gen-site-assets.mjs
import sharp from "sharp";
import fs from "node:fs";
import path from "node:path";

const PUBLIC = path.join(process.cwd(), "public");
const logoPath = path.join(PUBLIC, "logo.png");
const logoBuf = fs.readFileSync(logoPath);
const logoB64 = logoBuf.toString("base64");
const logoDataUri = `data:image/png;base64,${logoB64}`;

const PAPER = "#fbfaf8";
const INK = "#1f2328";
const INK_SOFT = "#4a5158";
const ACCENT = "#3f7d58";
const FONT =
  "'Microsoft YaHei','微软雅黑','PingFang SC','Noto Sans CJK SC',sans-serif";

// ---------- ① 社交分享图 1200x630 (OG / Twitter) ----------
const W = 1200;
const H = 630;
const ogSvg = `<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}">
  <rect width="${W}" height="${H}" fill="${PAPER}"/>
  <circle cx="600" cy="232" r="124" fill="${ACCENT}" opacity="0.08"/>
  <image href="${logoDataUri}" xlink:href="${logoDataUri}" x="512" y="122" width="176" height="176"/>
  <text x="600" y="432" text-anchor="middle" font-family="${FONT}" font-size="92" font-weight="700" fill="${INK}">兰汐</text>
  <text x="600" y="500" text-anchor="middle" font-family="${FONT}" font-size="40" fill="${INK_SOFT}">兰汐爸爸记录的日志</text>
  <rect x="540" y="530" width="120" height="6" rx="3" fill="${ACCENT}"/>
</svg>`;

await sharp(Buffer.from(ogSvg))
  .jpeg({ quality: 90, mozjpeg: true })
  .toFile(path.join(PUBLIC, "og-image.jpg"));
console.log("✓ og-image.jpg (1200x630)");

// ---------- ② 多尺寸 favicon / apple-touch-icon ----------
// 大尺寸图标压在站点底色上(不透明,iOS/Android 要求)
async function onBg(size, outName, pad = 0.82) {
  const logoSize = Math.round(size * pad);
  const bg = await sharp({
    create: { width: size, height: size, channels: 3, background: PAPER },
  })
    .png()
    .toBuffer();
  const lg = await sharp(logoBuf).resize(logoSize, logoSize).png().toBuffer();
  await sharp(bg)
    .composite([{ input: lg, gravity: "center" }])
    .png()
    .toFile(path.join(PUBLIC, outName));
  console.log(`✓ ${outName} (${size}x${size})`);
}

await onBg(180, "apple-touch-icon.png");
await onBg(192, "favicon-192.png");
await onBg(512, "favicon-512.png");
// 小尺寸保留透明通道(浏览器标签页原生支持 alpha)
await sharp(logoBuf)
  .resize(32, 32)
  .png()
  .toFile(path.join(PUBLIC, "favicon-32x32.png"));
await sharp(logoBuf)
  .resize(16, 16)
  .png()
  .toFile(path.join(PUBLIC, "favicon-16x16.png"));
console.log("✓ favicon-32x32.png / favicon-16x16.png");

// ---------- ③ webmanifest ----------
const manifest = {
  name: "兰汐",
  short_name: "兰汐",
  description: "兰汐爸爸记录的日志",
  start_url: "/",
  display: "standalone",
  background_color: PAPER,
  theme_color: PAPER,
  icons: [
    { src: "/favicon-192.png", sizes: "192x192", type: "image/png" },
    { src: "/favicon-512.png", sizes: "512x512", type: "image/png" },
    { src: "/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
  ],
};
fs.writeFileSync(
  path.join(PUBLIC, "site.webmanifest"),
  JSON.stringify(manifest, null, 2) + "\n"
);
console.log("✓ site.webmanifest");
