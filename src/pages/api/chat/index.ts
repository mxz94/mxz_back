import type { APIRoute } from "astro";
import { escapeHtml } from "@pages/chat/escape.js";

const defaultData = { chatList: [] };
const setCache = (key, data) => import.meta.env.MXZ_BACK.put(key, data);
const getCache = key => import.meta.env.MXZ_BACK.get(key);

export const GET: APIRoute = async ({ request, redirect }) => {
  try {
    const cacheKey = `data`;
    let data;
    const cache = await getCache(cacheKey);
    if (!cache) {
      await setCache(cacheKey, JSON.stringify(defaultData));
      data = defaultData;
    } else {
      data = JSON.parse(cache);
    }

    const list = JSON.stringify(
      data.chatList?.map(todo => ({
        id: escapeHtml(todo.id),
        name: escapeHtml(todo.name),
        message: escapeHtml(todo.message),
        date: escapeHtml(todo.date),
      })) ?? []
    );
    return new Response(list, {
      status: 200,
      headers: { "Content-Type": "application/json; charset=UTF-8" },
    });
  } catch (error) {
    console.log(error);
    return new Response(error.message, {
      status: 500,
    });
  }
};
export const PUT: APIRoute = async ({ request, redirect }) => {
  try {
    const body = await request.text();
    const cacheKey = `data`;
    JSON.parse(body);
    var data = await setCache(cacheKey, body);
    return new Response(body, { status: 200 });
  } catch (error) {
    console.log(error);
    return new Response(error.message, {
      status: 500,
    });
  }
};
