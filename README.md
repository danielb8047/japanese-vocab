# 語彙 — Japanese Vocabulary (Netlify build)

Static app plus one serverless function, using **Netlify Blobs** for storage.
Progress syncs across devices; no Supabase, no separate database.

## How storage works

- **localStorage on the device is the source of truth for reads.** The app opens
  instantly and works with no connection.
- **Writes also push to Netlify Blobs**, debounced by two seconds, and again when
  you close the app.
- **On startup the app pulls from the cloud** and keeps whichever copy is newer.

This means iOS evicting localStorage no longer loses your history — the cloud
copy restores it on next open.

## Deploying

1. Put every file in a Git repository (GitHub, GitLab).
2. netlify.com → Add new site → Import an existing project → pick the repo.
3. Accept the detected settings. `netlify.toml` already specifies them.
4. Deploy. Blobs provisions itself on first write — nothing to configure.

Drag-and-drop deploys via Netlify Drop will **not** work here, because the
function needs a build step to install `@netlify/blobs`. Use the Git route.

### Cost

Netlify's free plan is credit-based — 300 credits/month with a hard limit, so it
cannot run up a bill. A personal vocabulary app makes a handful of function
calls per session, which is a rounding error against that. Blob storage space
itself was free until 1 July 2026; check current terms if that matters to you.

## Turning sync on

1. Open the site, tap **SYNC** in the bar at the bottom.
2. Enter a phrase of at least 10 characters. Four or five random words is ideal.
3. Enter the *same* phrase on your other devices.

### About that phrase

The phrase is the only thing protecting your data. There are no accounts and no
passwords. Anyone who guesses it can read and overwrite your progress, so don't
use a short or memorable one.

The server never stores the phrase — only a SHA-256 hash of it, used as the
storage key. That also means **it cannot be recovered if you forget it**. Your
data would still exist in the blob store, but nothing could find it. Write it
down somewhere.

This is appropriate security for a personal vocabulary tracker and would not be
appropriate for anything sensitive.

## Adding to your home screen

Open the site in **Safari** on iOS (not Chrome), then Share → Add to Home Screen.

## Files

| File | Purpose |
|---|---|
| `index.html` | The app, plus the storage and sync layer |
| `netlify/functions/progress.mjs` | Reads and writes Netlify Blobs |
| `netlify.toml` | Build and function configuration |
| `package.json` | Declares the `@netlify/blobs` dependency |
| `sw.js` | Service worker — offline shell, never caches `/api/` |
| `manifest.json`, `icon-*.png` | Home screen presentation |

## Endpoints

`/api/progress` — `GET` returns `{data, updatedAt}`, `PUT` accepts the same,
`DELETE` removes the record. All require an `x-sync-key` header.

## Conflict handling

Last write wins, by timestamp. Reviewing on two devices simultaneously while
offline will lose one side's session. For single-user daily use this is fine;
per-card merging would be the fix if it ever bites.

## Updating the app after it's installed

Push to your Git branch. Netlify rebuilds and redeploys automatically, usually
in under a minute. Devices with the app on their home screen pick it up like
this:

1. On launch (and whenever you switch back to the app), it checks for a new
   deploy.
2. If one exists, a gold **UPDATE** bar appears at the bottom.
3. Tapping it activates the new version and reloads.

The prompt is deliberate rather than automatic — an update that reloaded the
page mid-review would lose the cards in your current session.

**Your progress is never touched by a deploy.** It lives in localStorage and in
Netlify Blobs, both of which are independent of the deployed files.

### Why the configuration matters

Three things have to line up or updates silently never arrive:

- `sw.js` serves the app shell **network-first**, so a new deploy wins over the
  cached copy. Cache-first would pin devices to whatever version they installed.
- `netlify.toml` sets `must-revalidate` on `sw.js` and `index.html`, so neither
  the browser nor the CDN serves a stale copy.
- The build command stamps the commit hash into `sw.js`, which changes the file
  on every deploy. Browsers only treat a service worker as new if its bytes
  differ.

If you edit these, keep those three properties.

### If an update seems stuck

Close the app from the iOS app switcher and reopen it, which forces a fresh
check. Failing that, open the site in Safari, then Settings → Safari → Advanced
→ Website Data and remove the entry. Your cloud progress restores on next
launch, provided sync is on.

## Known limits

- Pitch accents and JLPT levels are approximate — verify against OJAD.
- Safari blocks audio until you tap something, so the first card may be silent.
- JSX compiles in the browser at startup, costing about a second on first load.
  Run it through Vite if that ever matters.
