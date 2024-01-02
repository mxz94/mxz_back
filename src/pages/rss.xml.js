import rss from "@astrojs/rss";
import { SITE } from "../config";
import { getCollection } from "astro:content";

export async function get(context) {
    let blog = await getCollection("blog");
    let n = await getCollection("note");
    let items = blog.map((post) => ({
        title: post.data.title,
        pubDatetime: post.data.pubDatetime,
        description: post.data.description,
        link: `/blog/${post.slug}/`,
    }));
    let items2 = n.map((post) => ({
        title: post.data.title,
        pubDatetime: post.data.pubDatetime,
        description: post.data.description,
        link: `/note/${post.slug}/`,
    }));
    let items3 = items.contact(items2)
    return rss({
        title: SITE.title,
        description: SITE.desc,
        site: SITE.website,
        items: items3,
    });
}
