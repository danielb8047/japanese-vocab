import { getStore } from "@netlify/blobs";
import { createHash } from "node:crypto";

const MAX_BYTES = 2 * 1024 * 1024;

const json = (body, status = 200) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json", "cache-control": "no-store" },
  });

export default async (req) => {
  const phrase = req.headers.get("x-sync-key") || "";
  // The phrase is the only credential. Short ones are guessable, so refuse them.
  if (phrase.length < 10)
    return json({ error: "A sync phrase of at least 10 characters is required." }, 401);

  // Never store the phrase itself — only an opaque hash of it.
  const id = createHash("sha256").update(phrase).digest("hex").slice(0, 40);

  // Construct the store per request: a client cached in module scope holds
  // request-scoped credentials past their lifetime and starts failing when warm.
  const store = getStore({ name: "jpvocab", consistency: "strong" });

  try {
    if (req.method === "GET") {
      const rec = await store.get(id, { type: "json" });
      return json(rec || { data: null, updatedAt: 0 });
    }

    if (req.method === "PUT") {
      const body = await req.json();
      if (typeof body?.data !== "string") return json({ error: "Expected a data string." }, 400);
      if (body.data.length > MAX_BYTES) return json({ error: "Payload too large." }, 413);
      const rec = { data: body.data, updatedAt: Number(body.updatedAt) || Date.now() };
      await store.setJSON(id, rec);
      return json({ ok: true, updatedAt: rec.updatedAt });
    }

    if (req.method === "DELETE") {
      await store.delete(id);
      return json({ ok: true });
    }
  } catch (e) {
    return json({ error: String(e?.message || e).slice(0, 200) }, 500);
  }

  return json({ error: "Method not allowed." }, 405);
};

export const config = { path: "/api/progress" };
