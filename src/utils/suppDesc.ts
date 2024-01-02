import type { CollectionEntry } from "astro:content";

const suppDesc = (desc: string, content) => {
  if (!desc && content) {
      desc = content.substring(0, 100);
  }
  return desc;
};

export default suppDesc;
