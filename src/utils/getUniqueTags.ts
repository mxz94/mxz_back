import { slugifyStr } from "./slugify";
import type { CollectionEntry } from "astro:content";

type PostEntry = CollectionEntry<"blog"> | CollectionEntry<"note">;

const getUniqueTags = (posts: PostEntry[]) => {
  const tagCounts: { [key: string]: number } = {};

  for (const post of posts) {
    if (post.data.draft) continue;

    for (const rawTag of post.data.tags || []) {
      const tag = slugifyStr(rawTag);
      tagCounts[tag] = tagCounts[tag] ? tagCounts[tag] + 1 : 1;
    }
  }

  const tags = Object.keys(tagCounts).sort((tagA, tagB) => tagA.localeCompare(tagB));

  return { tags: tags, tagCounts: tagCounts };
};

export default getUniqueTags;
