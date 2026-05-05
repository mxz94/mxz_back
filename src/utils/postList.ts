import type { CollectionEntry } from "astro:content";
import createSlug from "./createSlug";
import getHeroImageLinkFromMd from "./getHeroImageLinkFromMd";
import suppDesc from "./suppDesc";

type PostEntry = CollectionEntry<"blog"> | CollectionEntry<"note">;

export type PostListItem = {
  post: PostEntry;
  img: string | null;
  desc: string;
  url: string;
  priority: boolean;
};

const summaryCache = new WeakMap<PostEntry, string>();
const heroImageCache = new WeakMap<PostEntry, string | null>();
const slugCache = new WeakMap<PostEntry, string>();

function getCachedSummary(post: PostEntry) {
  const cached = summaryCache.get(post);
  if (cached !== undefined) return cached;

  const summary = suppDesc(post.data.description, post.body);
  summaryCache.set(post, summary);
  return summary;
}

function getCachedHeroImage(post: PostEntry) {
  if (heroImageCache.has(post)) return heroImageCache.get(post) ?? null;

  const img = getHeroImageLinkFromMd(post);
  heroImageCache.set(post, img);
  return img;
}

function getCachedSlug(post: PostEntry) {
  const cached = slugCache.get(post);
  if (cached !== undefined) return cached;

  const slug = createSlug(post);
  slugCache.set(post, slug);
  return slug;
}

export function sortPostsByDate(posts: PostEntry[]) {
  return posts.sort((a, b) => {
    const aDate = a.data.pubDatetime || new Date(0);
    const bDate = b.data.pubDatetime || new Date(0);
    return bDate.getTime() - aDate.getTime();
  });
}

export function buildPostListItems(posts: PostEntry[], priorityImageLimit = 2): PostListItem[] {
  let priorityImageCount = 0;

  return posts.map((post) => {
    const img = getCachedHeroImage(post);
    const priority = Boolean(img) && priorityImageCount < priorityImageLimit;
    if (img) priorityImageCount += 1;

    return {
      post,
      img,
      desc: getCachedSummary(post),
      url: getCachedSlug(post),
      priority,
    };
  });
}
