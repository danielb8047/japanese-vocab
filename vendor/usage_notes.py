"""
Usage notes for words that share an English gloss but are not interchangeable.

Keyed by the written form as it appears in the deck, or by reading for words
normally written in kana. Notes are deliberately short — one line that fits on
a card and says the thing that actually distinguishes the word.

Written by hand rather than generated, because the distinctions are exactly
the kind a keyword rule cannot see.
"""

USAGE_NOTES = {
    # --- こそあど: the distance system ---------------------------------
    "これ": "Near the speaker — the thing in my hand or right by me.",
    "それ": "Near the listener — the thing by you, or something just mentioned.",
    "あれ": "Away from both of us — over there, or something we both already know.",
    "どれ": "The question word: which one, out of three or more.",
    "この": "Used before a noun: this ~ here by me.",
    "その": "Used before a noun: that ~ by you, or that ~ we just spoke about.",
    "あの": "Used before a noun: that ~ over there, away from us both.",
    "どの": "Used before a noun: which ~.",
    "ここ": "This place — where I am.",
    "そこ": "That place — where you are.",
    "あそこ": "Over there — away from us both.",
    "どこ": "Where — the question word.",
    "こちら": "Polite 'this way' or 'this one'. Also introduces a person politely.",
    "そちら": "Polite 'that way' or 'that one', near the listener.",
    "あちら": "Polite 'over there', away from both.",
    "どちら": "Polite 'which' or 'where'. Softer than どこ or どれ.",
    "こっち": "Casual こちら — this way, over here.",
    "そっち": "Casual そちら — that way, by you.",
    "あっち": "Casual あちら — over there.",
    "どっち": "Casual どちら — which of two.",
    "こんな": "This kind of ~, like this.",
    "そんな": "That kind of ~, like that (yours or just mentioned).",
    "あんな": "That kind of ~ over there, or that sort we both know.",
    "こう": "Like this — describing a manner near the speaker.",
    "そう": "Like that — echoing what the listener said.",
    "ああ": "Like that — a manner away from both speakers.",

    # --- giving and receiving ------------------------------------------
    "あげる": "I give to someone else. Never used for gifts coming to me.",
    "くれる": "Someone gives to me or my side. The gift moves toward me.",
    "もらう": "I receive from someone. Focus is on the receiver.",
    "くださる": "Polite くれる — a superior gives to me.",
    "いただく": "Humble もらう — I receive from a superior.",
    "さしあげる": "Humble あげる — I give to a superior.",
    "やる": "Blunt あげる — giving to animals, plants or close juniors.",

    # --- transitive / intransitive pairs --------------------------------
    "開く": "Intransitive: the door opens by itself. No one is doing it.",
    "開ける": "Transitive: someone opens something. Takes を.",
    "閉まる": "Intransitive: it closes. Nobody is named as doing it.",
    "閉める": "Transitive: someone closes it. Takes を.",
    "始まる": "Intransitive: it begins. The event starts.",
    "始める": "Transitive: someone begins it. Takes を.",
    "終わる": "Intransitive: it ends.",
    "止まる": "Intransitive: it stops moving.",
    "止める": "Transitive: someone stops it. Takes を.",
    "入る": "Intransitive: to go in, to enter.",
    "入れる": "Transitive: to put something in. Takes を.",
    "出る": "Intransitive: to go out, to leave.",
    "出す": "Transitive: to take something out, to send. Takes を.",
    "つく": "Intransitive: it switches on, it sticks.",
    "つける": "Transitive: someone switches it on. Takes を.",
    "消える": "Intransitive: it goes out, it disappears.",
    "消す": "Transitive: someone turns it off or erases it. Takes を.",
    "落ちる": "Intransitive: it falls.",
    "落とす": "Transitive: someone drops it. Takes を.",
    "並ぶ": "Intransitive: they line up.",
    "並べる": "Transitive: someone arranges them. Takes を.",

    # --- wearing ---------------------------------------------------------
    "着る": "Worn on the torso: shirts, coats, dresses.",
    "履く": "Worn on the legs or feet: trousers, skirts, shoes, socks.",
    "はく": "Worn on the legs or feet: trousers, skirts, shoes, socks.",
    "かぶる": "Worn on the head: hats, caps, helmets.",
    "かける": "Used for glasses — メガネをかける.",
    "する": "Used for small accessories: ties, scarves, gloves, rings.",

    # --- kanji spellings of kana-keyed words above -------------------------
    # Listed explicitly: matching by reading alone attached ここ's note to 個々
    # and つく's note to 着く, which are different words.
    "在る": "Existence of things that do not move by themselves. Usually written ある.",
    "有る": "To have or exist, for things. Usually written ある.",
    "居る": "Existence of living things that move. Usually written いる.",
    "余り": "With a negative: not very. Positively it means 'excess'.",
    "点く": "Intransitive: a light or device switches on.",
    "点ける": "Transitive: someone switches it on. Takes を.",
    "上げる": "To raise or lift. In the giving sense usually written あげる.",
    "被る": "Worn on the head: hats, caps, helmets. Usually written かぶる.",

    # --- existence -------------------------------------------------------
    "ある": "Existence of things that do not move by themselves.",
    "いる": "Existence of living things that move — people and animals.",

    # --- 'very' and degree ------------------------------------------------
    "とても": "Very — neutral and usable almost anywhere.",
    "大変": "Very, or terribly. Also means 'a serious matter' on its own.",
    "なかなか": "Quite, considerably. With a negative it means 'not easily'.",
    "ずいぶん": "Quite a lot — often surprise at more than expected.",
    "あまり": "With a negative: not very. Positively it means 'excess'.",
    "ちょっと": "A little. Also softens a refusal — ちょっと… means no.",
    "少し": "A little, a small amount. Plainer than ちょっと.",

    # --- people ----------------------------------------------------------
    "妻": "My own wife, used when speaking to others.",
    "奥さん": "Someone else's wife. Never used for your own.",
    "夫": "My own husband.",
    "ご主人": "Someone else's husband.",
    "父": "My own father, spoken about to outsiders.",
    "お父さん": "Someone else's father, or how you address your own.",
    "母": "My own mother, spoken about to outsiders.",
    "お母さん": "Someone else's mother, or how you address your own.",
    "兄": "My own older brother.",
    "お兄さん": "Someone else's older brother, or how you address yours.",
    "姉": "My own older sister.",
    "お姉さん": "Someone else's older sister, or how you address yours.",

    # --- verbs of taking, listening, seeing -------------------------------
    "見る": "To look at or watch something deliberately.",
    "見える": "To be visible — it comes into view without effort.",
    "聞く": "To listen, or to ask a question.",
    "聞こえる": "To be audible — the sound reaches you without trying.",
    "取る": "To take or pick up in the hand.",
    "撮る": "To take a photograph.",
    "知る": "To come to know a fact. Usually 知っている for 'I know'.",
    "分かる": "To understand. Takes が, not を.",

    # --- time ------------------------------------------------------------
    "時間": "Time as a duration, or the counter for hours.",
    "時": "A point in time — the moment when something happens.",
    "今度": "Next time, or this coming time. Rarely 'this time' exactly.",
    "この間": "The other day — a short while ago.",

    # --- other frequent confusions ----------------------------------------
    "暑い": "Hot weather or air temperature.",
    "熱い": "Hot to the touch — objects, drinks, baths.",
    "早い": "Early in time.",
    "速い": "Fast in speed.",
    "会う": "To meet a person.",
    "合う": "To fit, match or suit.",
    "上手": "Skilful. Not used about yourself — it sounds boastful.",
    "得意": "Good at, and comfortable saying about yourself.",
    "住む": "To live somewhere. Usually 住んでいる.",
    "生きる": "To be alive.",
    "働く": "To work, in the sense of labour.",
    "勤める": "To be employed at a place. Takes に.",
    "習う": "To be taught by someone.",
    "勉強": "To study, by your own effort.",
    "学ぶ": "To learn, in a broader or more formal sense.",
    "旅行": "A trip as an event — going travelling.",
    "旅": "A journey, with a more literary feel.",
    "値段": "The price asked for something.",
    "料金": "A fee or charge for a service.",
}
