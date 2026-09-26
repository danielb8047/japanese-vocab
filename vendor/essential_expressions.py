"""
Greetings and set phrases every beginner course teaches in its first weeks.

The JLPT reconstructions this deck is built from are lists of words, not
phrases, so these fall through the cracks: 13 of 29 were missing entirely,
こんにちは sat at N3 and すみません at N1. Entries here override the lists — any
list entry with the same reading is replaced — and are always filed under
Greetings & set phrases.

Fields: written form with furigana, reading, meaning, level, optional note.
Pitch accent is still looked up in Kanjium and shown as ESTIMATED where it has
no entry; it is never hand-assigned here.
"""

ESSENTIALS = [
    # --- greetings through the day -------------------------------------
    ("おはようございます", "おはようございます", "good morning (polite)", "N5",
     "Polite. To friends and family, just おはよう."),
    ("おはよう", "おはよう", "good morning (casual)", "N5",
     "Casual — friends and family. Say おはようございます to anyone else."),
    ("こんにちは", "こんにちは", "hello, good afternoon", "N5",
     "The daytime greeting. Rarely used with family or people you see daily."),
    ("こんばんは", "こんばんは", "good evening", "N5", None),
    ("さようなら", "さようなら", "goodbye", "N5",
     "Fairly final — sounds like a longer parting. Friends say じゃあね or またね."),
    ("お休[やす]みなさい", "おやすみなさい", "good night", "N5",
     "Said when going to bed or parting late at night. Casually, おやすみ."),
    ("また明日[あした]", "またあした", "see you tomorrow", "N5", None),

    # --- thanks and apology ---------------------------------------------
    ("ありがとうございます", "ありがとうございます", "thank you (polite)", "N5",
     "Polite. Use this with anyone you'd say ございます to."),
    ("ありがとう", "ありがとう", "thanks (casual)", "N5",
     "Casual — friends and family."),
    ("どういたしまして", "どういたしまして", "you're welcome", "N5",
     "Correct but can sound formal; in practice people often say いいえ instead."),
    ("すみません", "すみません", "excuse me, sorry", "N5",
     "Excuse me or sorry — and also a thank-you when someone goes to trouble for you."),
    ("ごめんなさい", "ごめんなさい", "I'm sorry", "N5",
     "A personal apology, mostly to friends and family. すみません is the all-purpose one."),
    ("失礼[しつれい]します", "しつれいします", "excuse me (entering or leaving)", "N5",
     "Said when entering or leaving a room, especially an office or a teacher's room."),

    # --- requests -------------------------------------------------------
    ("お願[ねが]いします", "おねがいします", "please (requesting)", "N5",
     "When asking for something or handing something over — ordering, a favour."),
    ("よろしくお願[ねが]いします", "よろしくおねがいします", "nice to meet you; please treat me well", "N5",
     "On meeting someone, or when asking a favour. No neat English equivalent."),
    ("ください", "ください", "please (give me / do for me)", "N5",
     "After a thing: コーヒーをください, 'coffee, please'. After a て-form verb: 'please do'. "
     "Usually written in kana; 下さい is the same word."),
    ("もう一度[いちど]お願[ねが]いします", "もういちどおねがいします", "once more, please", "N5", None),
    ("ちょっと待[ま]ってください", "ちょっとまってください", "please wait a moment", "N5", None),

    # --- meeting people -------------------------------------------------
    ("初[はじ]めまして", "はじめまして", "how do you do", "N5",
     "Only on first meeting. Usually followed by your name and よろしくお願いします."),
    ("どうぞよろしく", "どうぞよろしく", "pleased to meet you", "N5",
     "Slightly shorter and less formal than よろしくお願いします."),
    ("お元気[げんき]ですか", "おげんきですか", "how are you?", "N5",
     "Asked after not seeing someone for a while — not a daily 'how are you'."),
    ("元気[げんき]です", "げんきです", "I'm fine", "N5", None),

    # --- home and meals -------------------------------------------------
    ("行[い]ってきます", "いってきます", "I'm off (leaving home)", "N5",
     "Said by the person leaving. The reply is いってらっしゃい."),
    ("行[い]ってらっしゃい", "いってらっしゃい", "see you (to someone leaving)", "N5",
     "Said to the person leaving, in reply to いってきます."),
    ("ただいま", "ただいま", "I'm home", "N5",
     "Said on arriving home. The reply is おかえりなさい."),
    ("お帰[かえ]りなさい", "おかえりなさい", "welcome home", "N5",
     "Said to someone arriving home, in reply to ただいま."),
    ("いただきます", "いただきます", "said before eating", "N5",
     "Said before a meal — thanks for the food. Often with hands together."),
    ("ごちそうさまでした", "ごちそうさまでした", "thank you for the meal", "N5",
     "Said after eating. Also to whoever cooked or paid."),
    ("いらっしゃいませ", "いらっしゃいませ", "welcome (in shops)", "N5",
     "You'll hear this from staff, not say it. No reply is expected."),

    # --- responses ------------------------------------------------------
    ("そうです", "そうです", "that's right", "N5", None),
    ("そうですか", "そうですか", "I see; is that so?", "N5",
     "Falling intonation: 'I see'. Rising: 'really?'."),
    ("分[わ]かりました", "わかりました", "understood, I see", "N5",
     "Understood, or 'OK, I'll do that' when agreeing to a request."),
    ("分[わ]かりません", "わかりません", "I don't understand, I don't know", "N5", None),

    # --- N4: a step further -----------------------------------------------
    ("お疲[つか]れ様[さま]です", "おつかれさまです", "thanks for your hard work", "N4",
     "Used constantly at work — as a greeting, and when someone finishes for the day."),
    ("ご苦労様[くろうさま]", "ごくろうさま", "thanks for your trouble", "N4",
     "Said by a senior to a junior. To anyone senior to you, use お疲れ様です instead."),
    ("お先[さき]に失礼[しつれい]します", "おさきにしつれいします", "excuse me for leaving first", "N4",
     "Said when leaving work while others are still there."),
    ("おめでとうございます", "おめでとうございます", "congratulations", "N4", None),
    ("お大事[だいじ]に", "おだいじに", "get well soon, take care", "N4",
     "Said to someone who is ill or injured."),
    ("気[き]をつけて", "きをつけて", "take care, be careful", "N4", None),
    ("結構[けっこう]です", "けっこうです", "no thank you; that's fine", "N4",
     "Usually a polite refusal. Tone and context decide whether it means yes or no."),
    ("申[もう]し訳[わけ]ありません", "もうしわけありません", "I'm very sorry (formal)", "N4",
     "A formal apology — businesses to customers, or for a real mistake at work."),
]
