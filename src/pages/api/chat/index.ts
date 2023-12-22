import type { APIRoute } from "astro";

export const GET: APIRoute = async ({ request, redirect }) => {
  try {
    return new Response("{'name':22}", {
      headers: { "Content-Type": "application/json; charset=UTF-8" },
    });
  } catch (error) {
    return new Response("Something went wrong", {
      status: 500,
    });
  }
  return redirect("/dashboard");
};
