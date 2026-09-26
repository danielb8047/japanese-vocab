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

## What the app does

- **Review** — spaced repetition over the level you are studying, with kanji,
  furigana, audio, pitch accent contour and usage notes.
- **Browse** — tap a category on the home screen to see every word in it with
  its mastery bar and due date.
- **Daily progress** — how much you did each day and how you graded it.
- **Words** — switch study level, browse or search the entire dictionary
  across all levels, or import extra vocabulary.
- **Setup** — audio, pitch display, daily new-word limit, backup, version.

## Versions

The app shows its version under **Setup → VERSION**. `CHANGELOG.md` lists what
changed in each one.

Downloads are named `japanese-vocab-vX.Y.Z.zip` so you can tell them apart.
The files *inside* keep fixed names — `index.html`, `cats.js`, `words-n5.js`
and so on — because the app and service worker load those exact paths.
Renaming them breaks the app, so version the download, never the contents.

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

## The vocabulary deck

8,528 words, built by cross-referencing three independent JLPT reconstructions
rather than trusting any one of them.

| Level | Words | Pitch from real data | All three lists agree |
|---|---|---|---|
| N5 | 921 | 91% | |
| N4 | 838 | 87% | 94% of the deck overall |
| N3 | 1,981 | 91% | |
| N2 | 1,976 | 88% | |
| N1 | 3,079 | 89% | |

Only the level you are studying downloads.

**Pitch accent** comes from Kanjium wherever it has an entry. Where it does
not, a rule-based estimate is used and the card shows an **ESTIMATED** badge,
so a guess is never mistaken for real data. Roughly one word in ten is
estimated.

**Homophones carry context.** あく appears as 開く, 空く, 悪 and 灰; each card
notes the sense so they can be told apart. Context is only added where it
actually distinguishes.

**Confusable words carry usage notes.** Words that share an English gloss are
often not interchangeable — これ / それ / あれ differ by distance from the
speaker, 着る / 履く / かぶる by which part of the body. Cards for these show a
**WHEN TO USE IT** note, hand-written rather than generated, since the
distinction is exactly what a keyword rule cannot see. Where no note exists,
the card names the words it might be confused with.

**Example sentences** appear on reveal for most words, from OpenJLPT.

**No duplicates.** Cards are unique on written form, reading and meaning.
Okurigana variants of the same word are collapsed to the standard spelling,
while genuinely different words that share a reading stay separate.

To rebuild or re-categorise, see `vendor/README.md`.

## Known limits

- Levels are a cross-referenced best guess. The JLPT has published no official
  list since 2010, and about 6% of words have only one or two lists behind
  them; each card records how many agreed.
- Estimated pitch accents follow broad rules (loanwords on the third mora from
  the end, i-adjectives on the penultimate) and will be wrong for irregular
  words. The badge tells you when to check OJAD.
- Category assignment is keyword-based. Around 12% of words land in "Ideas &
  everything else" — usually because their gloss is unusual, not because they
  have no home.
- Safari blocks audio until you tap something, so the first card may be silent.
- JSX compiles in the browser at startup, costing about a second on first load.
  Run it through Vite if that ever matters.
