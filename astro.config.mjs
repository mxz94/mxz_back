import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import tailwind from "@astrojs/tailwind";
import { SITE } from "./src/config";
import react from "@astrojs/react";
import remarkToc from "remark-toc";
import markdoc from "@astrojs/markdoc";
import { livePhotoPlugin } from "./src/utils/livePhotoPlugin.ts";
import { bilibiliPlugin } from "./src/utils/bilibiliPlugin.ts";

// https://astro.build/config
export default defineConfig({
  site: SITE.website,
  integrations: [mdx(), sitemap(), tailwind(), react(), markdoc()],
  markdown: {
    //     // 应用于 .md 和 .mdx 文件
    remarkPlugins: [[remarkToc, { heading: "目录" }], livePhotoPlugin, bilibiliPlugin]
    //     remarkPlugins: [[remarkToc, {heading: "目录"}], bilibiliPlugin]
  },
  image: {
    domains: ["pub-4232cd0528364004a537285f400807bf.r2.dev"],
  },
});
