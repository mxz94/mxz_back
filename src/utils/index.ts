import {getCollection} from "astro:content";
import { sortPostsByDate } from "./postList";

export async function getBlogs() {
    const posts = await getCollection('blog')
    return sortPostsByDate(posts)
}
export async function getNotes() {
    const posts = await getCollection('note')
    return sortPostsByDate(posts)
}

export async function getAllPosts() {
    let notes = await getBlogs()
    let posts = await getNotes()
    posts = posts.concat(notes)
    return sortPostsByDate(posts)
}
