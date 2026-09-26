#!/usr/bin/env python3
"""
Build the vocabulary deck by cross-referencing several JLPT word lists.

The JLPT has not published official vocabulary lists since 2010, so every
list in circulation is a reconstruction. Rather than trust one, this merges
three and records how many agree on each word's level.

Sources (fetched by fetch_sources.sh):
  n{1..5}.csv                open-anki-jlpt-decks (MIT) — word, reading, meaning
  src2/vocab/n{1..5}.json    OpenJLPT (CC BY-SA 4.0) — meanings, examples
  src3/JLPT_vocab_ALL.csv    Bluskyo/JLPT_Vocabulary — word, reading, level
  accents.txt                Kanjium (CC BY-SA 4.0) — pitch accent
  JmdictFurigana.txt         JmdictFurigana (CC BY-SA 4.0) — furigana alignment

Output: cats.js and words-n{1..5}.js
"""

import csv, json, os, re, sys
from collections import defaultdict
from usage_notes import USAGE_NOTES

KANJI = re.compile(r"[\u4E00-\u9FAF\u3005]")
KANA_ONLY = re.compile(r"^[\u3040-\u30FF\u30FCー]+$")
KATAKANA = re.compile(r"^[\u30A0-\u30FF\u30FCー]+$")
SMALL = "ゃゅょぁぃぅぇぉゎャュョァィゥェォヮ"
LEVELS = ["N5", "N4", "N3", "N2", "N1"]

# ---------------------------------------------------------------- categories
CATS = [
    ("grt", "挨拶",      "Greetings & set phrases"),
    ("num", "数字",      "Numbers & counting"),
    ("tim", "時間",      "Time & days"),
    ("ppl", "人・家族",   "People & family"),
    ("foo", "食べ物",    "Food & drink"),
    ("pla", "場所",      "Places"),
    ("obj", "身の回り",   "Everyday things"),
    ("dir", "方向・位置",  "Directions & position"),
    ("col", "色・形",     "Colours & shapes"),
    ("bod", "体",        "The body & health"),
    ("nat", "自然",      "Nature & weather"),
    ("ani", "動物・植物",  "Animals & plants"),
    ("tra", "乗り物",    "Getting around"),
    ("hom", "家",        "Home & housework"),
    ("stu", "学校・仕事",  "School & work"),
    ("com", "会話・気持ち", "Talking & feelings"),
    ("lei", "趣味・娯楽",   "Leisure & media"),
    ("gra", "文法語",      "Pronouns & connectors"),
    ("vrb", "動詞",      "Verbs"),
    ("adj", "形容詞",    "Descriptions"),
    ("abs", "その他",    "Ideas & everything else"),
]

GLOSS_RULES = [
    ("grt", ["hello", "good morning", "good evening", "good afternoon", "goodbye",
             "thank you", "excuse me", "sorry", "welcome", "congratulation",
             "see you", "good night", "how do you do", "nice to meet", "pardon",
             "greeting", "farewell", "cheers", "bless you", "good luck",
             "you're welcome", "no thank you", "please"]),
    ("num", ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
             "ten", "hundred", "thousand", "million", "counter", "number", "how many",
             "half", "several", "amount", "quantity", "dozen", "double", "triple",
             "digit", "figure", "total", "sum", "percent", "fraction", "zero",
             "first", "second", "third", "fourth", "fifth", "unit", "measure"]),
    ("tim", ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday",
             "sunday", "january", "february", "march", "april", "june", "july",
             "august", "september", "october", "november", "december", "morning",
             "afternoon", "evening", "night", "today", "tomorrow", "yesterday",
             "week", "month", "year", "hour", "minute", "o'clock", "time", "date",
             "season", "spring", "summer", "autumn", "fall", "winter", "daytime",
             "midnight", "noon", "past", "future", "recently", "already", "soon",
             "always", "sometimes", "often", "never", "now", "later", "early",
             "late", "age", "birthday", "holiday", "weekend", "day", "moment",
             "period", "era", "century", "decade", "deadline", "schedule",
             "beginning", "end", "duration", "while", "when", "anniversary"]),
    ("ppl", ["person", "people", "father", "mother", "brother", "sister", "child",
             "baby", "family", "friend", "husband", "wife", "parent", "grandmother",
             "grandfather", "uncle", "aunt", "son", "daughter", "man", "woman",
             "boy", "girl", "adult", "teacher", "student", "doctor", "nurse",
             "police", "policeman", "guest", "customer", "name", "everyone",
             "somebody", "someone", "mr.", "mrs.", "couple", "neighbor",
             "neighbour", "relative", "colleague", "boss", "staff", "member",
             "citizen", "foreigner", "stranger", "self", "human", "population"]),
    ("foo", ["food", "rice", "bread", "meat", "beef", "pork", "chicken",
             "vegetable", "fruit", "egg", "milk", "tea", "coffee", "water",
             "alcohol", "sake", "beer", "wine", "sugar", "salt", "soy sauce",
             "soup", "noodle", "curry", "cake", "sweet", "candy", "snack", "meal",
             "breakfast", "lunch", "dinner", "supper", "restaurant", "menu",
             "taste", "delicious", "apple", "orange", "banana", "potato", "carrot",
             "onion", "cheese", "butter", "sandwich", "chopstick", "plate", "cup",
             "glass", "bowl", "fork", "spoon", "hungry", "thirsty", "recipe",
             "flavour", "flavor", "juice", "grape", "melon", "lemon", "cuisine",
             "cooking", "confection", "drink", "beverage", "dish", "ingredient",
             "seasoning", "tofu", "sushi", "ramen", "fish"]),
    ("pla", ["place", "shop", "store", "station", "hospital", "bank", "library",
             "park", "post office", "hotel", "airport", "cafe", "café", "temple",
             "shrine", "museum", "theater", "theatre", "cinema", "market", "city",
             "town", "village", "country", "prefecture", "building",
             "factory", "farm", "embassy", "toilet", "bathroom", "zoo", "beach",
             "abroad", "overseas", "america", "japan", "china", "korea", "england",
             "france", "germany", "world", "map", "address", "area", "region",
             "location", "site", "venue", "capital", "border", "district",
             "neighborhood", "neighbourhood", "countryside", "square"]),
    ("obj", ["book", "paper", "pen", "pencil", "notebook", "letter", "newspaper",
             "magazine", "dictionary", "bag", "umbrella", "shoe", "clothes",
             "clothing", "shirt", "trousers", "pants", "hat", "cap", "coat",
             "jacket", "skirt", "dress", "sock", "glasses", "watch", "clock",
             "telephone", "phone", "camera", "computer", "television", "radio",
             "money", "wallet", "ticket", "key", "box", "bottle", "photo",
             "picture", "stamp", "envelope", "card", "machine", "tool", "toy",
             "gift", "present", "cigarette", "tobacco", "match", "battery",
             "goods", "luggage", "baggage", "souvenir", "ring", "necklace",
             "towel", "soap", "brush", "mirror", "bell", "rope", "string",
             "needle", "knife", "scissors", "container", "device", "equipment"]),
    ("dir", ["above", "below", "under", "inside", "outside", "front", "behind",
             "right", "left", "north", "south", "east", "west", "near", "far",
             "next to", "between", "middle", "center", "centre", "beside",
             "around", "opposite", "direction", "side", "top", "bottom", "corner",
             "here", "there", "where", "forward", "backward", "across",
             "distance", "position", "surface", "edge", "interior", "exterior",
             "vicinity", "beyond", "toward", "upward", "downward", "diagonal"]),
    ("col", ["colour", "color", "red", "blue", "white", "black", "yellow", "green",
             "brown", "purple", "pink", "grey", "gray", "shape", "circle",
             "square", "triangle", "line", "dot", "pattern", "stripe", "round",
             "flat", "curve", "angle", "size", "width", "length", "height",
             "thickness", "depth"]),
    ("bod", ["body", "head", "face", "eye", "ear", "nose", "mouth", "tooth",
             "teeth", "hand", "finger", "arm", "leg", "foot", "knee", "shoulder",
             "neck", "hair", "skin", "heart", "stomach", "chest", "blood", "bone",
             "voice", "health", "illness", "sick", "medicine", "injury", "pain",
             "fever", "cold", "flu", "tired", "sleep", "rest", "bath", "muscle",
             "breath", "nerve", "brain", "throat", "lip", "cheek", "wound",
             "symptom", "treatment", "surgery", "diet", "exercise"]),
    ("nat", ["weather", "rain", "snow", "wind", "cloud", "sky", "sun", "moon",
             "star", "mountain", "river", "sea", "ocean", "lake", "island",
             "forest", "field", "stone", "rock", "sand", "soil", "fire", "ice",
             "nature", "earth", "air", "light", "shadow", "heat", "typhoon",
             "earthquake", "temperature", "climate", "storm", "fog", "rainbow",
             "pond", "valley", "hill", "coast", "wave", "thunder", "lightning",
             "energy", "environment", "planet", "universe", "season"]),
    ("ani", ["animal", "dog", "cat", "bird", "horse", "cow", "pig", "sheep",
             "bear", "monkey", "rabbit", "mouse", "rat", "insect", "butterfly",
             "elephant", "tiger", "lion", "snake", "frog", "plant", "tree",
             "flower", "grass", "leaf", "seed", "root", "branch", "bamboo", "pet",
             "creature", "species", "wing", "tail", "feather", "nest", "pine",
             "cherry blossom", "bug", "spider", "whale", "chicken"]),
    ("tra", ["car", "train", "bus", "bicycle", "bike", "taxi", "airplane",
             "aeroplane", "plane", "ship", "boat", "subway", "underground",
             "road", "street", "bridge", "travel", "trip", "journey",
             "ticket", "platform", "traffic", "highway", "railway", "vehicle",
             "automobile", "transport", "transportation", "passenger", "driver",
             "flight", "route", "departure", "arrival", "parking", "harbor",
             "harbour", "port", "crossing", "intersection", "sightseeing"]),
    ("hom", ["house", "home", "room", "kitchen", "bedroom", "living room", "door",
             "window", "wall", "floor", "ceiling", "roof", "stair", "garden",
             "furniture", "table", "desk", "chair", "bed", "sofa", "shelf",
             "closet", "curtain", "carpet", "refrigerator", "laundry", "garbage",
             "rubbish", "apartment", "rent", "entrance", "gate", "lamp", "yard",
             "housework", "cleaning", "washing", "drawer", "cupboard", "pillow",
             "blanket", "vase", "elevator", "lift", "corridor", "balcony"]),
    ("stu", ["school", "class", "classroom", "lesson", "study", "homework",
             "test", "exam", "question", "answer", "word", "sentence", "grammar",
             "kanji", "katakana", "hiragana", "language", "english", "japanese",
             "university", "college", "graduate", "work", "job", "company",
             "employee", "meeting", "business", "salary", "office", "career",
             "practice", "research", "report", "project", "subject",
             "mathematics", "science", "history", "art", "music", "sport",
             "education", "training", "skill", "knowledge", "essay",
             "composition", "textbook", "notebook", "degree", "industry",
             "economy", "society", "government", "law", "politics"]),
    ("lei", ["movie", "film", "cinema", "music", "song", "guitar", "piano",
             "concert", "game", "hobby", "sport", "swimming", "baseball",
             "soccer", "football", "tennis", "golf", "ski", "camera", "photo",
             "television", "radio", "magazine", "comic", "novel", "theatre",
             "theater", "dance", "party", "festival", "holiday", "vacation",
             "leisure", "entertainment", "shopping", "shower", "gram",
             "calendar", "instrument"]),
    ("gra", ["you", "this", "that", "which", "who", "what", "myself", "oneself",
             "yourself", "himself", "herself", "themselves", "however", "but",
             "therefore", "because", "so", "and", "or", "if", "although",
             "moreover", "furthermore", "nevertheless", "very", "quite",
             "really", "rather", "almost", "together", "various", "same",
             "identical", "each", "every", "any", "some", "all", "both",
             "other", "another", "such", "only", "just", "even", "still",
             "yes", "no", "not", "maybe", "perhaps", "probably", "certainly",
             "these", "those", "here", "somewhat", "surplus", "in what way"]),
    ("com", ["say", "speak", "talk", "tell", "ask", "answer", "explain",
             "conversation", "discussion", "opinion", "meaning", "story", "news",
             "message", "promise", "reason", "advice", "complaint", "apology",
             "happy", "sad", "angry", "afraid", "surprised", "worried", "lonely",
             "glad", "pleasant", "unpleasant", "feeling", "emotion", "mood",
             "love", "hate", "like", "dislike", "hope", "wish", "dream", "fear",
             "joy", "sorrow", "kindness", "trust", "doubt", "confidence",
             "interest", "boring", "fun", "funny", "song", "singing"]),
]

VERB_HINT = re.compile(r"^to [a-z]")
_RULE_RE = None


def compile_rules():
    """Whole-word matching, but tolerant of plural and -ing forms.

    Two bugs motivated this. A bare substring let 'wind' match 'window' and
    'yes' match 'yesterday'. Requiring \\b at both ends then broke plurals, so
    'shoe' stopped matching 'shoes'. The optional suffix group fixes both.
    """
    global _RULE_RE
    _RULE_RE = []
    for cid, keys in GLOSS_RULES:
        pats = []
        for k in keys:
            if not k.replace(" ", "").replace("'", "").replace(".", "").isalpha():
                pats.append(re.escape(k))
            else:
                pats.append(r"\b" + re.escape(k) + r"(?:s|es|ing)?\b")
        _RULE_RE.append((cid, re.compile("|".join(pats))))


def categorise(expr, reading, gloss):
    if _RULE_RE is None:
        compile_rules()
    g = gloss.lower()
    for cid, rx in _RULE_RE:
        if rx.search(g):
            # A concrete-noun keyword inside a verb gloss usually means the
            # verb sense dominates: "to open a shop" is not a shop.
            if VERB_HINT.match(g) and cid in ("dir", "col", "num", "abs", "tim"):
                return "vrb"
            return cid
    if VERB_HINT.match(g):
        return "vrb"
    if reading.endswith("い") and KANJI.search(expr) and len(g.split()) <= 4:
        return "adj"
    if g.startswith(("being ", "having ")):
        return "adj"
    return "abs"


def moras(kana):
    out = []
    for ch in kana:
        if ch in SMALL and out:
            out[-1] += ch
        else:
            out.append(ch)
    return out


# ------------------------------------------------------------------- loading
def load_accents(path):
    by_pair, by_reading = {}, {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) < 3:
                continue
            first = p[2].split(",")[0].strip()
            if not first.isdigit():
                continue
            by_pair[(p[0], p[1])] = int(first)
            by_reading.setdefault(p[1], int(first))
    return by_pair, by_reading


def load_furigana(path):
    out = {}
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            p = line.rstrip("\n").split("|")
            if len(p) == 3:
                out[(p[0], p[1])] = p[2]
    return out


def apply_furigana(expr, reading, seg):
    if not KANJI.search(expr):
        return expr
    if not seg:
        return f"{expr}[{reading}]"
    spans = []
    for chunk in seg.split(";"):
        if ":" not in chunk:
            continue
        idx, r = chunk.split(":", 1)
        if "-" in idx:
            a, b = idx.split("-", 1)
            spans.append((int(a), int(b), r))
        else:
            spans.append((int(idx), int(idx), r))
    spans.sort()
    out, pos = [], 0
    for a, b, r in spans:
        if a > pos:
            out.append(expr[pos:a])
        out.append(f"{expr[a:b + 1]}[{r}]")
        pos = b + 1
    if pos < len(expr):
        out.append(expr[pos:])
    return "".join(out)


def split_senses(text):
    """'to open, to become open; opening' -> ['to open', 'to become open', 'opening']"""
    text = re.sub(r"\([^)]*\)", "", text)
    parts = re.split(r"[;,/]", text)
    return [re.sub(r"\s+", " ", p).strip() for p in parts if p.strip()]


# ------------------------------------------------------------------ gathering
def gather():
    """key -> record, where key is (written form, reading)."""
    entries = defaultdict(lambda: {
        "levels": defaultdict(set),   # level -> set of source names
        "senses": [],
        "examples": [],
        "forms": set(),               # which sources used this written form
    })
    # Sources write the same word differently (ある / 在る, おばさん / 伯母さん),
    # so votes are pooled by reading. Entries stay keyed by written form.
    by_reading = defaultdict(lambda: defaultdict(set))

    # Source 1: open-anki-jlpt-decks
    for lv in LEVELS:
        path = f"{lv.lower()}.csv"
        if not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                expr = re.split(r"[;；]", (row.get("expression") or "").strip())[0].strip()
                reading = (row.get("reading") or "").strip() or expr
                if not expr or not KANA_ONLY.match(reading):
                    continue
                e = entries[(expr, reading)]
                e["forms"] = e.get("forms", set()) | {"anki"}
                e["levels"][lv].add("anki")
                by_reading[reading][lv].add("anki")
                for s in split_senses(row.get("meaning") or ""):
                    if s not in e["senses"]:
                        e["senses"].append(s)

    # Source 2: OpenJLPT
    for lv in LEVELS:
        path = f"src2/vocab/{lv.lower()}.json"
        if not os.path.exists(path):
            continue
        for item in json.load(open(path, encoding="utf-8")):
            expr = (item.get("word") or "").strip()
            reading = (item.get("reading") or "").strip() or expr
            if not expr or not KANA_ONLY.match(reading):
                continue
            e = entries[(expr, reading)]
            e["forms"] = e.get("forms", set()) | {"openjlpt"}
            e["levels"][lv].add("openjlpt")
            by_reading[reading][lv].add("openjlpt")
            for s in item.get("meanings") or []:
                for t in split_senses(s):
                    if t not in e["senses"]:
                        e["senses"].append(t)
            for ex in (item.get("examples") or [])[:1]:
                ja, en = (ex.get("ja") or "").strip(), (ex.get("en") or "").strip()
                if ja and en and len(ja) <= 30 and len(en) <= 60 and not e["examples"]:
                    e["examples"].append({"ja": ja, "en": en})

    # Source 3: Bluskyo — level votes only
    path = "src3/JLPT_vocab_ALL.csv"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                expr = (row.get("Kanji") or "").strip()
                reading = (row.get("Reading") or "").strip() or expr
                lvnum = (row.get("Level") or "").strip()
                if not expr or not lvnum.isdigit() or not KANA_ONLY.match(reading):
                    continue
                # This source numbers 1=N1 ... 5=N5 — verified against known
                # words (水/犬 are 5, 概念/沈黙 are 1).
                n = int(lvnum)
                lv = {5: "N5", 4: "N4", 3: "N3", 2: "N2", 1: "N1"}.get(n)
                if not lv:
                    continue
                entries[(expr, reading)]["levels"][lv].add("bluskyo")
                by_reading[reading][lv].add("bluskyo")
    return entries, by_reading


SOURCE_RANK = ["anki", "openjlpt", "bluskyo"]


def resolve_level(levels):
    """Majority vote across the lists. On a tie, defer to the most carefully
    curated list rather than to the easiest level — resolving ties downward
    piled genuinely harder vocabulary into N5."""
    if not levels:
        return None, 0, 0
    total = len(set().union(*levels.values()))
    ranked = sorted(
        levels.items(),
        key=lambda kv: (-len(kv[1]),
                        min((SOURCE_RANK.index(s) for s in kv[1]), default=9)),
    )
    best, srcs = ranked[0]
    return best, len(srcs), total


# ---------------------------------------------------------------- pitch accent
def generate_pitch(expr, reading, gloss):
    """A rule-based guess, used only where Kanjium has no entry. Flagged in
    the app so it is never mistaken for real data."""
    n = len(moras(reading))
    if n == 0:
        return 0
    g = gloss.lower()
    if KATAKANA.match(reading):
        # Loanwords overwhelmingly take the accent on the third mora from the
        # end; shorter ones on the first.
        return max(1, n - 2) if n >= 3 else 1
    if reading.endswith("い") and not g.startswith("to "):
        # i-adjectives are mostly accented on the mora before the final い.
        return max(1, n - 1)
    if g.startswith("to "):
        # Verbs split between heiban and penultimate; penultimate is the safer
        # single guess for dictionary form.
        return max(1, n - 1)
    if reading.endswith(("しつ", "かん", "こう", "せい", "がく", "きょく")):
        return 0
    return 0                               # heiban is the largest noun class


def main():
    ap, ar = load_accents("kanjium-master/data/source_files/raw/accents.txt")
    furi = load_furigana("JmdictFurigana.txt")
    entries, by_reading = gather()

    stats = defaultdict(int)
    out = []
    for (expr, reading), e in entries.items():
        lv, votes, total = resolve_level(by_reading.get(reading) or e["levels"])
        if not lv:
            continue
        senses = [s for s in e["senses"] if s][:6]
        if not senses:
            stats["dropped_no_meaning"] += 1
            continue

        groups = [(senses[:3], None)]

        seg = furi.get((expr, reading))
        jp = apply_furigana(expr, reading, seg)
        if seg is None and KANJI.search(expr):
            stats["no_furigana"] += 1

        for gl, ctx in groups:
            en = ", ".join(gl)[:52].rstrip(" ,")
            cat = categorise(expr, reading, en)

            pitch = ap.get((expr, reading))
            psrc = "exact"
            if pitch is None:
                pitch = ar.get(reading)
                psrc = "reading"
            if pitch is None or pitch > len(moras(reading)):
                pitch = generate_pitch(expr, reading, en)
                psrc = "generated"
            stats[f"pitch_{psrc}"] += 1

            rec = {
                "id": f"{cat}:{reading}:{en}",
                "cat": cat,
                "jp": jp,
                "kana": reading,
                "en": en,
                "pitch": pitch,
                "ps": psrc,
                "level": lv,
                "src": votes,          # how many lists agreed on this level
            }
            rec["_forms"] = sorted(e.get("forms", ()))
            if ctx:
                rec["ctx"] = ctx
            if e["examples"]:
                rec["ex"] = e["examples"][0]
            out.append(rec)
            stats[lv] += 1
            stats[f"agree_{votes}"] += 1

    # 大変 and たいへん are one word listed twice, once in kanji and once in
    # kana. Merge them on reading plus leading sense. Which spelling to keep is
    # not obvious — 大変 is normally written in kanji but とても normally is not
    # — so prefer whichever form the most carefully curated list used, and fall
    # back to the kanji form.
    kana_pairs = defaultdict(list)
    for r in out:
        kana_pairs[(r["kana"], r["en"].split(",")[0].strip().lower())].append(r)
    drop = set()
    for (kana, sense), group in kana_pairs.items():
        if len(group) < 2:
            continue
        plain = [r for r in group if re.sub(r"\[[^\]]*\]", "", r["jp"]) == kana]
        withk = [r for r in group if r not in plain]
        if not plain or not withk:
            continue
        anki_plain = any("anki" in r.get("_forms", ()) for r in plain)
        anki_kanji = any("anki" in r.get("_forms", ()) for r in withk)
        losers = withk if (anki_plain and not anki_kanji) else plain
        for r in losers:
            drop.add(id(r))
            stats["merged_kana_kanji"] += 1
    out = [r for r in out if id(r) not in drop]

    # Homophones need context: 橋 and 箸 are both はし, and a card showing only
    # kana is ambiguous. Tag each with its own leading sense so they can be
    # told apart. This is the only place a context note is added, replacing an
    # earlier verb/noun split that invented distinctions that were not real.
    by_read = defaultdict(list)
    for r in out:
        by_read[r["kana"]].append(r)
    for kana, group in by_read.items():
        forms = {re.sub(r"\[[^\]]*\]", "", r["jp"]) for r in group}
        if len(forms) < 2:
            continue
        firsts = [r["en"].split(",")[0].strip() for r in group]
        if len(set(firsts)) < 2:
            continue                       # a tag that repeats explains nothing
        for r, first in zip(group, firsts):
            if first:
                r["ctx"] = first[:26]
                stats["homophone_tagged"] += 1

    # 明るい and 明かるい are the same word written two ways. Collapse pairs that
    # share a reading, a leading sense and the same kanji, keeping the shorter
    # (standard) okurigana. Words with different kanji are left alone, so
    # 会う and 遭う stay distinct.
    def kanji_set(j):
        return frozenset(KANJI.findall(re.sub(r"\[[^\]]*\]", "", j)))

    variant = {}
    for r in out:
        k = (r["kana"], r["en"].split(",")[0].strip(), kanji_set(r["jp"]))
        prev = variant.get(k)
        surface = re.sub(r"\[[^\]]*\]", "", r["jp"])
        if prev is None:
            variant[k] = r
        elif len(surface) < len(re.sub(r"\[[^\]]*\]", "", prev["jp"])):
            variant[k] = r
            stats["okurigana_variant"] += 1
        else:
            stats["okurigana_variant"] += 1
    out = list(variant.values())

    # Words that share an English gloss are not necessarily interchangeable.
    # これ/それ/あれ all read "that" or "this" but differ by distance from the
    # speaker, and nothing in the gloss says so. Attach a hand-written note
    # where we have one, and otherwise point at the siblings so at least the
    # existence of a distinction is visible.
    surface_of = lambda j: re.sub(r"\[[^\]]*\]", "", j)
    for r in out:
        # Reading-keyed notes are for words written in kana (これ, ここ). Applying
        # them to any word with that reading gave 個々 the note for ここ.
        sf = surface_of(r["jp"])
        note = USAGE_NOTES.get(sf) or (USAGE_NOTES.get(r["kana"]) if sf == r["kana"] else None)
        if note:
            r["note"] = note
            stats["usage_note"] += 1

    same_sense = defaultdict(list)
    for r in out:
        same_sense[r["en"].split(",")[0].strip().lower()].append(r)
    for sense, group in same_sense.items():
        if len(group) < 2 or len(group) > 6:
            continue                       # a huge group is a vague gloss, not a set
        for r in group:
            others = [x for x in group if x is not r]
            # Only worth comparing within reach of each other.
            near = [x for x in others
                    if abs(LEVELS.index(x["level"]) - LEVELS.index(r["level"])) <= 1]
            if not near:
                continue
            r["cf"] = [{"jp": x["jp"], "kana": x["kana"]} for x in near[:3]]
            stats["compare_linked"] += 1

    # Final dedupe: identical id can only arise from identical content.
    seen, deduped = set(), []
    for r in out:
        if r["id"] in seen:
            stats["dupe_id"] += 1
            continue
        seen.add(r["id"])
        deduped.append(r)

    for r in deduped:
        r.pop("_forms", None)

    hdr = ("/* Generated by build_deck.py — do not edit by hand.\n"
           "   JLPT levels cross-referenced across three lists:\n"
           "     open-anki-jlpt-decks (MIT), OpenJLPT (CC BY-SA 4.0),\n"
           "     Bluskyo/JLPT_Vocabulary.\n"
           "   Pitch accent: Kanjium (CC BY-SA 4.0). Furigana: JmdictFurigana\n"
           "     (CC BY-SA 4.0), from JMdict (EDRDG).\n"
           "   ps: exact = Kanjium matched word+reading; reading = matched the\n"
           "   reading only; generated = rule-based guess, flagged in the app.\n"
           "   src: how many of the three lists agreed on the level. */\n")

    with open("cats.js", "w", encoding="utf-8") as f:
        f.write(hdr + "window.JPVOCAB_CATS = ")
        json.dump([{"id": c, "jp": j, "en": e} for c, j, e in CATS], f,
                  ensure_ascii=False, separators=(",", ":"))
        f.write(";\n")

    for lv in LEVELS:
        ws = [w for w in deduped if w["level"] == lv]
        fn = f"words-{lv.lower()}.js"
        with open(fn, "w", encoding="utf-8") as f:
            f.write(hdr)
            f.write("window.JPVOCAB_LEVELS = window.JPVOCAB_LEVELS || {};\n")
            f.write(f'window.JPVOCAB_LEVELS["{lv}"] = ')
            json.dump(ws, f, ensure_ascii=False, separators=(",", ":"))
            f.write(";\n")
        print(f"{fn}: {len(ws):5} words, {os.path.getsize(fn)/1024:6.0f} KB")

    print(f"\ntotal: {len(deduped)}")
    for k in sorted(stats):
        print(f"  {k}: {stats[k]}")


if __name__ == "__main__":
    main()
