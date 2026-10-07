import rss from "@astrojs/rss";
import { SITE } from "../config";
import type { APIContext } from "astro";
import sanitizeHtml from "sanitize-html";
import MarkdownIt from "markdown-it";
import { getPublicAllPosts } from "../utils";

const parser = new MarkdownIt();

export async function GET(_context: APIContext) {
    const posts = await getPublicAllPosts();
    const allowedTags = sanitizeHtml.defaults.allowedTags.concat(["img"]);

    return rss({
      title: SITE.title,
      description: SITE.desc,
      site: SITE.website,
      items: posts.map((post) => ({
        title: post.data.title,
        pubDate: post.data.pubDatetime,
        description: post.data.description,
        link: `/${post.collection}/${post.slug}/`,
        content: sanitizeHtml(parser.render(post.body), { allowedTags }),
        categories: post.data.tags,
      })),
      stylesheet: "/pretty-feed-v3.xsl",
    });
}
