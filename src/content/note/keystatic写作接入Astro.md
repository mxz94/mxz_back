---
title: keystatic写作接入Astro
slug: keystatic写作接入Astro
pubDatetime: 2024-04-05
tags:
  - 工具
---
# keystatic写作接入Astro

keystatic 是cms平台， astro 接入后，可以方便写作

接入流程

1. 添加依赖

```bash
npx astro add react markdoc
npm install @keystatic/core @keystatic/astro
```

\
2. 添加集成到astro.config.mjs

```diff
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import markdoc from '@astrojs/markdoc';
import keystatic from '@keystatic/astro';

import vercel from "@astrojs/vercel/serverless";

// https://astro.build/config
export default defineConfig({
+  integrations: [react(), markdoc(), keystatic()],
+  output: "server",
+  adapter: vercel() // server 必须添加vercel ssr集成
});


```

3. 添加keystatic 配置文件

```typescript
import { config, fields, collection } from '@keystatic/core';

export default config({
  ui: {
    brand: { name: 'mlx的作业板' }
  },
  storage: {  // 设定保存位置
    kind: 'local',
    // kind: 'github',
    // repo: 'mxz94/mxz_back',
    // branchPrefix: 'master'
  },
  collections: {
    posts: collection({
      columns: ['title', 'pubDatetime'],
      label: '朝花夕拾',
      slugField: 'title',
      path: 'src/content/blog/朝花夕拾/*',
      entryLayout: 'content',
      format: { contentField: 'content' },
      schema: {
        title: fields.slug({ name: { label: '标题' } }),
        slug: fields.text({ label: 'slug',  description:"加入文档中的slug", validation: {isRequired:true} }),
        pubDatetime: fields.date({ label: '发布时间', defaultValue: {
            kind: "today"
            } }),
        tags: fields.multiselect({
          label: 'Tag',
          options: [
              { label: '朝花夕拾', value: '朝花夕拾' }
          ],
          defaultValue: ['朝花夕拾'],
        }),
        content: fields.document({
          label: 'Content',
          formatting: true,
          dividers: true,
          links: true,
          images: {
            directory: 'public/img/zhxs',
            publicPath: '../../../../public/img/zhxs',
          },
        }),
      },
    })
  },
});

```

4. 运行起来 访问 /keystatic
