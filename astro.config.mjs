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
  // 站内链接预取：只在鼠标悬停/触摸时拉取，避免进页面就并发十几个请求反而拖慢
  prefetch: { prefetchAll: true, defaultStrategy: "hover" },
  integrations: [mdx(), sitemap(), tailwind(), markdoc()],
  markdown: {
    remarkPlugins: [[remarkToc, { heading: "目录" }], bilibiliPlugin],
    rehypePlugins: [rehypeResponsiveImages],
  },
  image: {
    domains: ["pub-4232cd0528364004a537285f400807bf.r2.dev"],
  },
});
