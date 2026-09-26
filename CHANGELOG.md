# Changelog

The version shown in the app under **Setup → VERSION** tells you what your
phone is actually running. If it does not match the newest entry here, the
update has not reached the device yet — close the app from the iOS app
switcher and reopen it.

Numbering is `major.minor.patch`:
- **major** — something that changes how the app works or how data is stored
- **minor** — new vocabulary, new features
- **patch** — bug fixes only

---

## 1.5.0 — the whole dictionary, and two fixes

- **Browse every word from the Words screen** — all five levels, every
  category, locked ones included. Pick a level, tap a category, and see its
  words with their mastery. Browsing is separate from studying: looking at N3
  doesn't change your study level, and locked categories are marked as not yet
  in your reviews.
- **Search** within a level by kanji, kana or English.
- Large categories load in pages of 150 with a Show more button, since N1
  categories run to several hundred words.
- **Fixed: review buttons could disappear off the bottom of the screen.** A
  card carrying a usage note, comparison chips and an example sentence could
  be taller than the phone, pushing Again / Hard / Good / Easy out of reach.
  They are now pinned to the bottom during review, and the sync bar steps
  aside until the session ends.
- **Fixed: 49 cards showed a usage note belonging to a different word.** Notes
  were matched by reading as a fallback, so 個々 inherited ここ's "this place"
  note and 着く (to arrive) was described as "switches on". Reading-keyed notes
  now apply only to words written in kana. Genuine kanji spellings of the same
  word — 在る, 居る, 余り — have their own explicit notes.
- The review header showed "N5" whatever level you were on; it now shows the
  card's actual level.

## 1.4.1 — fix

- Japanese text was rendering in dark ink on the dark browse rows, making it
  unreadable. The Furigana component had the flashcard's colours baked in;
  it now takes them as props, so it works on both backgrounds.

## 1.4.0 — browse your words, and see your days

- **Tap any unlocked category to browse its words.** Each word shows a mastery
  bar derived from its review interval — the same figure the home screen totals
  up — plus how many days until it is due, and a play button to hear it. Sort
  by mastery to see what is lagging, or A–Z to find something specific.
- **New "Daily progress" screen.** A stacked bar per day for the last two
  weeks, coloured to match the review buttons: Again, Hard, Good, Easy. A
  second chart splits new words from reviews. Headline figures for cards
  studied, days active and recall rate.
- Reviews are logged from this version onward, so the charts start empty and
  fill in as you use the app. The log keeps 120 days and rides along with sync.

## 1.3.1 — fixes

- **The version number now actually appears.** 1.2.0 defined it but never
  rendered it, so Setup showed nothing. It sits at the foot of "About the
  data".
- **"About the data" now reports the real deck.** It had been counting the
  173-word fallback list built into the app rather than the loaded level, and
  claimed progress was saved to a Claude account rather than to the device and
  your Netlify site.

## 1.3.0 — usage notes for confusable words

- **Words that share an English meaning now explain themselves.** これ, それ
  and あれ all glossed as "this/that one" with nothing to distinguish them.
  116 N5 words now carry a hand-written **WHEN TO USE IT** note covering the
  distance system (こそあど), giving and receiving (あげる / くれる / もらう),
  transitive and intransitive pairs (開く / 開ける), what you wear on which
  part of the body, ある versus いる, and family terms that differ for your own
  family and someone else's.
- Where no hand-written note exists, cards list **not to be confused with**
  and name the siblings, so the existence of a distinction is at least visible.
- Fixed: 大変 and たいへん were listed as two separate words, as were おいしい /
  美味しい and たくさん / 沢山. 358 of these kana-and-kanji pairs were one word
  counted twice; they are now merged, keeping whichever spelling the
  best-curated list used.

## 1.2.0 — cross-referenced vocabulary

- Deck rebuilt from **three** independent JLPT lists rather than one. 8,528
  words; 94% have all three lists agreeing on the level.
- Fixed: the third source numbers levels backwards (1 = N1, not N5), which
  would have filed 概念 and 沈黙 as beginner vocabulary.
- Fixed: level votes are pooled by reading rather than written form. Sources
  spell the same word differently (ある / 在る), so keying on the written form
  made almost every word look unsupported.
- Fixed: ties between lists now defer to the best-curated source instead of
  the easiest level, which had inflated N5 to 1,647 words.
- Pitch accents that are estimated rather than looked up now carry an
  **ESTIMATED** badge. About one word in ten.
- Homophones carry a context note — あく as 開く, 空く, 悪 and 灰 — but only
  where the note actually distinguishes them.
- Example sentences shown on reveal for most words.
- Okurigana variants collapsed (明るい / 明かるい); genuinely different words
  sharing a reading kept separate (会う / 遭う).
- Two new categories: Pronouns & connectors, Leisure & media.

## 1.1.0 — real vocabulary data

- Replaced the 173 hand-written words with 7,689 built from JMdict-derived
  sources, split per level so only the level being studied downloads.
- Real pitch accent from Kanjium; per-kanji furigana from JmdictFurigana.
- Progress migration: cards orphaned by a deck rebuild are re-homed by reading.
- Fixed category matching that had filed 明るい under directions ("b**right**")
  and 窓 under nature ("**wind**ow").

## 1.0.0 — first deploy

- Spaced repetition with SM-2 scheduling, mastery-gated category unlocking.
- Kanji with furigana, no romaji. English on reveal only.
- Text to speech with replay and an off switch; pitch accent contour.
- Progress in localStorage, synced to Netlify Blobs behind a sync phrase.
- Installable to the iOS home screen; offline via service worker.
