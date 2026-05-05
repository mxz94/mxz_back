import { getCollection, type CollectionEntry } from "astro:content";
import { sortPostsByDate } from "./postList";

type BlogEntry = CollectionEntry<"blog">;
type NoteEntry = CollectionEntry<"note">;
type PostEntry = BlogEntry | NoteEntry;

let blogsPromise: Promise<BlogEntry[]> | undefined;
let notesPromise: Promise<NoteEntry[]> | undefined;
let publicBlogsPromise: Promise<BlogEntry[]> | undefined;
let publicNotesPromise: Promise<NoteEntry[]> | undefined;
let allPostsPromise: Promise<PostEntry[]> | undefined;
let publicAllPostsPromise: Promise<PostEntry[]> | undefined;

export async function getBlogs() {
  blogsPromise ??= getCollection("blog").then((posts) => sortPostsByDate(posts));
  return blogsPromise;
}

export async function getNotes() {
  notesPromise ??= getCollection("note").then((posts) => sortPostsByDate(posts));
  return notesPromise;
}

export async function getPublicBlogs() {
  publicBlogsPromise ??= getBlogs().then((posts) => posts.filter((item) => !item.data.auth));
  return publicBlogsPromise;
}

export async function getPublicNotes() {
  publicNotesPromise ??= getNotes().then((posts) => posts.filter((item) => !item.data.auth));
  return publicNotesPromise;
}

export async function getAllPosts() {
  allPostsPromise ??= Promise.all([getBlogs(), getNotes()]).then(([blogs, notes]) =>
    sortPostsByDate([...blogs, ...notes]),
  );
  return allPostsPromise;
}

export async function getPublicAllPosts() {
  publicAllPostsPromise ??= Promise.all([getPublicBlogs(), getPublicNotes()]).then(([blogs, notes]) =>
    sortPostsByDate([...blogs, ...notes]),
  );
  return publicAllPostsPromise;
}
