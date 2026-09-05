/* Cache strategy, chosen so deploys actually reach installed devices:
   - The app shell (HTML) is network-first. A new deploy is picked up as soon
     as the device is online; the cache is only a fallback for offline use.
   - Pinned CDN libraries are cache-first. Their URLs contain the version, so
     a cached copy is never stale.
   - /api/ is never cached — stale progress is worse than none. */

const VERSION = "__BUILD_ID__"; // replaced at deploy time by netlify.toml
const SHELL = `shell-${VERSION}`;
const LIB = "lib-v1";

const LIBS = [
  "https://cdn.tailwindcss.com",
  "https://unpkg.com/react@18/umd/react.production.min.js",
  "https://unpkg.com/react-dom@18/umd/react-dom.production.min.js",
  "https://unpkg.com/@babel/standalone/babel.min.js",
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    (async () => {
      const shell = await caches.open(SHELL);
      await shell.add("./index.html").catch(() => {});
      const lib = await caches.open(LIB);
      await Promise.all(
        LIBS.map(async (u) => {
          if (!(await lib.match(u))) await lib.add(u).catch(() => {});
        })
      );
      // Deliberately NOT skipWaiting — the page asks the user first, so an
      // update never interrupts a review session mid-card.
    })()
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    (async () => {
      const keys = await caches.keys();
      await Promise.all(
        keys.filter((k) => k !== SHELL && k !== LIB).map((k) => caches.delete(k))
      );
      await self.clients.claim();
    })()
  );
});

self.addEventListener("message", (e) => {
  if (e.data === "skip-waiting") self.skipWaiting();
});

self.addEventListener("fetch", (e) => {
  const req = e.request;
  if (req.method !== "GET") return;
  const url = new URL(req.url);

  if (url.pathname.startsWith("/api/")) return;

  const isShell = req.mode === "navigate" || url.pathname.endsWith("/index.html");

  if (isShell) {
    e.respondWith(
      fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(SHELL).then((c) => c.put("./index.html", copy));
          }
          return res;
        })
        .catch(async () => (await caches.match("./index.html")) || Response.error())
    );
    return;
  }

  e.respondWith(
    caches.match(req).then(
      (hit) =>
        hit ||
        fetch(req).then((res) => {
          if (res && res.status === 200 && LIBS.some((u) => req.url.startsWith(u))) {
            const copy = res.clone();
            caches.open(LIB).then((c) => c.put(req, copy));
          }
          return res;
        })
    )
  );
});
