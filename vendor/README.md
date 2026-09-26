# Rebuilding the vocabulary deck

You do not need to run any of this to use the app — `cats.js` and
`words-n*.js` in the site root are already built. This is here for when you
want to refresh the data or change how words are categorised.

## Running it

Needs Python 3 and about 200 MB of temporary disk space.

    cd vendor
    ./fetch_sources.sh
    python3 build_deck.py
    cp cats.js words-n*.js ../

Then commit the changed files. Netlify redeploys, and your phone offers the
update next time you open the app. Your progress is unaffected — cards are
keyed on category, reading and meaning, which the build keeps stable.

## Sources

| Data | Source | Licence |
|---|---|---|
| JLPT list A (words, readings, meanings) | [open-anki-jlpt-decks](https://github.com/jamsinclair/open-anki-jlpt-decks) | MIT |
| JLPT list B (meanings, example sentences) | [OpenJLPT](https://github.com/evanclan/OpenJLPT) | CC BY-SA 4.0 |
| JLPT list C (level cross-check) | [Bluskyo/JLPT_Vocabulary](https://github.com/Bluskyo/JLPT_Vocabulary) | see repo |
| Pitch accent | [Kanjium](https://github.com/mifunetoshiro/kanjium) | CC BY-SA 4.0 |
| Furigana alignment | [JmdictFurigana](https://github.com/Doublevil/JmdictFurigana) | CC BY-SA 4.0 |
| Underlying dictionary | JMdict / EDRDG | CC BY-SA 4.0 |

CC BY-SA asks for attribution, carried in the header of every generated file.
Keep it there if you republish.

## Hand-maintained files

- `essential_expressions.py` — greetings and set phrases, placed by hand. JLPT
  word lists omit most of these or file them at odd levels.
- `usage_notes.py` — "when to use it" notes for words easily confused.

Both are plain Python lists; edit and rebuild.

## What the build does

1. Reads all three JLPT lists.
2. Pools level votes **by reading**, not by written form — the lists spell the
   same word differently (ある / 在る, おばさん / 伯母さん) and keying on the
   written form made every word look like a lone opinion.
3. Assigns the level a majority of lists agree on. Ties defer to the most
   carefully curated list rather than to the easiest level; resolving ties
   downward piled genuinely hard vocabulary into N5. Each word records `src`,
   the number of lists that agreed.
4. Merges meanings from all sources, keeping up to three senses, and attaches
   one short example sentence where OpenJLPT has one.
5. Looks up pitch accent in Kanjium by word+reading, then by reading alone.
   Where neither matches, a rule-based estimate is used and marked `ps:
   "generated"` — the app labels those ESTIMATED so they are never mistaken
   for real data.
6. Applies per-kanji furigana segmentation.
7. Collapses okurigana variants of the same word (明るい / 明かるい), keeping
   the standard spelling. Words with different kanji stay separate, so 会う and
   遭う are not merged.
8. Tags homophones with their leading sense, so あく as 開く, 悪 and 灰 can be
   told apart — but only when the tags actually differ.
9. Assigns a category by matching the English gloss with whole-word matching
   that tolerates plurals and -ing forms.

## Known imperfections

Categorisation is keyword-driven and gets a slice of words wrong — a word
whose gloss is unusual lands in the "everything else" bucket. Editing
`GLOSS_RULES` in `build_deck.py` and rebuilding is the way to improve it.

JLPT has not published official word lists since 2010, so every list including
this one is a reconstruction. Treat level assignments as a good guide rather
than authoritative.
