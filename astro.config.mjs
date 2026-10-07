import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import tailwind from "@astrojs/tailwind";
import { SITE } from "./src/config";
import remarkToc from "remark-toc";
import markdoc from "@astrojs/markdoc";
import { bilibiliPlugin } from "./src/utils/bilibiliPlugin.ts";
import { rehypeResponsiveImages } from "./src/utils/rehypeResponsiveImages.ts";

// https://astro.build/config
export default defineConfig({
  site: SITE.website,
  // 站内链接预取：鼠标悬停/进入视口即后台拉取，点文章近瞬时打开
  prefetch: { prefetchAll: true, defaultStrategy: "viewport" },
  integrations: [mdx(), sitemap(), tailwind(), markdoc()],
  markdown: {
    remarkPlugins: [[remarkToc, { heading: "目录" }], bilibiliPlugin],
    rehypePlugins: [rehypeResponsiveImages],
  },
  image: {
    domains: ["pub-4232cd0528364004a537285f400807bf.r2.dev"],
  },
});
