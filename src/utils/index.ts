import { getCollection, type CollectionEntry } from "astro:content";
import { sortPostsByDate } from "./postList";

type BlogEntry = CollectionEntry<"blog">;
type NoteEntry = CollectionEntry<"note">;
type PostEntry = BlogEntry | NoteEntry;

let blogsPromise: Promise<BlogEntry[]> | undefined;
let publicBlogsPromise: Promise<BlogEntry[]> | undefined;

export async function getBlogs() {
  blogsPromise ??= getCollection("blog").then((posts) => sortPostsByDate(posts));
  return blogsPromise;
}

export async function getPublicBlogs() {
  publicBlogsPromise ??= getBlogs().then((posts) => posts.filter((item) => !item.data.auth));
  return publicBlogsPromise;
}

// 站点只展示日记：AllPosts 直接等价于 Blogs，
// 首页 / 标签 / RSS 都走这两个函数。
export async function getAllPosts() {
  return getBlogs();
}

export async function getPublicAllPosts() {
  return getPublicBlogs();
}
