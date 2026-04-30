import type { CollectionEntry } from "astro:content";

type PostLike =
  | CollectionEntry<"blog">
  | CollectionEntry<"note">
  | {
      body?: string;
      data?: {
        heroImage?: string;
      };
      heroImage?: string;
    }
  | string
  | null
  | undefined;

const VIDEO_EXTENSIONS = /\.(mp4|mov|m4v|webm|ogv)(?:[?#].*)?$/i;
const IMAGE_EXTENSIONS = /\.(avif|gif|jpe?g|png|svg|webp)(?:[?#].*)?$/i;

function cleanAssetPath(src?: string | null) {
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

  if (normalized.startsWith("//")) {
    return `https:${normalized}`;
  }

  if (/^https?:\/\//i.test(normalized) || normalized.startsWith("/")) {
    return normalized;
  }

  if (normalized.startsWith("img/") && IMAGE_EXTENSIONS.test(normalized)) {
    return `/${normalized}`;
  }

  return null;
}

function addMatches(
  candidates: Array<{ src: string; index: number }>,
  body: string,
  pattern: RegExp,
) {
  let match;
  while ((match = pattern.exec(body)) !== null) {
    const src = cleanAssetPath(match[1]);
    if (src) {
      candidates.push({ src, index: match.index });
    }
  }
}

export default function getHeroImageLinkFromMd(post: PostLike) {
  if (!post) return null;

  if (typeof post !== "string") {
    const heroImage = cleanAssetPath(post.data?.heroImage || post.heroImage);
    if (heroImage) return heroImage;
  }

  const body = typeof post === "string" ? post : post.body || "";
  const candidates: Array<{ src: string; index: number }> = [];

  addMatches(candidates, body, /!\[[^\]]*]\(([^)\s]+)(?:\s+["'][^)]*["'])?\)/g);
  addMatches(candidates, body, /<img\b[^>]*\bsrc=["']([^"']+)["'][^>]*>/gi);
  addMatches(candidates, body, /<video\b[^>]*\bposter=["']([^"']+)["'][^>]*>/gi);
  addMatches(candidates, body, /\bdata-photo-src=["']([^"']+)["']/gi);

  candidates.sort((a, b) => a.index - b.index);
  return candidates[0]?.src || null;
}
