"""
EVERYDAY_SHINGI_LITURGY.PY
The 'Sacred Library' for the Keizan Society.

PURPOSE:
    This module contains 100% of the liturgical text. 
    All mantras, dharanis, and dedications reside here. 
    Structured for dyslexia-aware rendering and ritual use.

REVISION HISTORY:
    2026-06-06: Initial creation of the Keizan Society Sacred Library.
    2026-06-06: Graphic redesign for dyslexia-aware ritual use.
                - Converted flat strings to dictionaries with 'chant_lines'.
                - Added specific 'label' fields for UI dropdowns.
                - Implemented line-tracking breaks for Sino-Japanese text.
                - Fixed mislabeled Daikokuten dedication.
                - Organized dedications into liturgical phrases.

MAINTAINER:
    Senior Full-Stack Developer / Keizan Society Technical Editor
"""

import os

# PRIVACY SETTING: 
# If running on a website, this pulls from your "GitHub Secrets."
# If running locally, it defaults to the text in the quotes below.
SANGHA_NAMES = os.getenv("SANGHA_NAMES", "our family, friends, and all those in need of healing")

# Short verses for specific daily actions
VERSES = {
    "waking": "Waking from sleep, the Bodhisattva inspires all beings to awaken to All-Knowledge, gazing upon the ten directions.",
    "toothbrush": "Taking a toothbrush in hand, the Bodhisattva inspires all beings to attain the wonderful teaching and be ultimately pure.",
    "brushing": "Brushing the teeth, the Bodhisattva inspires all beings to be harmonious and pure in mind, biting through all afflictions.",
    "flossing": "Flossing the teeth, The Bodhisattva inspires all beings to draw out the hair’s breadth Between heaven and earth.",
    "rinsing": "Rinsing the mouth, the Bodhisattva inspires all beings to approach the Gate of the Pure Dharma and accomplish liberation.",
    "face": "Using water to wash the face, the Bodhisattva inspires all beings to obtain the Gate of the Pure Dharma, forever without stain.",
    "toilet": "Going to the toilet, the Bodhisattva inspires all beings to reject greed, hatred, and ignorance, and cleanse all transgressions.",
    "hands": "Using water to wash the hands, the Bodhisattva inspires all beings to obtain pure hands to receive and uphold the Buddha-Dharma.",
    "bathing": "Bathing the body, the Bodhisattva inspires all beings to have hearts and bodies without defilement, pure and bright inside and out.",
    "road_start": "Setting out on a road, the Bodhisattva inspires all beings to proceed toward the Buddha’s conduct and enter the place of no-reliance.",
    "right_livelihood": "Seeing a person of Right Livelihood, the Bodhisattva inspires all beings to obtain pure livelihood and not put on a false appearance.",
    "sleep": "Going to sleep, the Bodhisattva inspires all beings to have bodies that attain peace and hearts without disturbance.",
    "kesa": {
        "title": "Verse of the Kesa",
        "label": "Show Verse of the Kesa",
        "chant_lines": [
            "How great, the robe of liberation,",
            "a formless field of merit.",
            "Wrapping ourselves in Buddha's teaching,",
            "we free all living beings.",
            "(Romaji: Dai sai gedap-puku musō fuku den e / hi bu nyorai kyo / ko do shoshu jo)"
        ]
    },
    "tonsure": "In shaving off beard and hair, we pray that all living beings should forever be free from mental afflictions and in the end attain nirvana. (Romaji: teijo shuhatsu / to gan shujō / yōri bon-no / kugyō jaku metsu)"
}

MEALS = {
    "five_contemplations": {
        "title": "The Five Contemplations",
        "label": "Show Five Contemplations",
        "chant_lines": [
            "1. We reflect on the effort that brought us this food and consider how it comes to us.",
            "2. We reflect on our virtue and practice, and whether we are worthy of this offering.",
            "3. We regard greed as the obstacle to freedom of mind.",
            "4. We regard this meal as medicine to sustain our life.",
            "5. For the sake of enlightenment we now receive this food."
        ]
    },
    "purity_lotus": "Abiding in this ephemeral world like a lotus in muddy water. the mind is pure and goes beyond. Thus we bow to buddha."
}

CHANTS = {
    "kaikyo_ge": {
        "title": "Sutra-Opening Verse",
        "label": "Show Sutra-Opening Verse",
        "chant_lines": [
            "The unsurpassed, profound, and wondrous dharma",
            "is rarely met with, even in a hundred, thousand, million kalpas.",
            "Now we can see and hear it, accept and maintain it.",
            "May we unfold the meaning of the Tathagata's truth."
        ]
    },
    "repentance": {
        "title": "Repentance Verse",
        "label": "Show Repentance Verse",
        "chant_lines": [
            "All my past and harmful karma,",
            "born from beginningless greed, hate, and delusion,",
            "through body, speech, and mind,",
            "I now fully avow."
        ]
    },
    "three_refuges_prayer": {
        "title": "Three Refuges Prayer",
        "label": "Show Three Refuges Prayer",
        "chant_lines": [
            "I take refuge in buddha. May all beings embody the great way, resolving to awaken.",
            "I take refuge in dharma. May all living beings deeply enter the sutras, wisdom like an ocean.",
            "I take refuge in sangha. May all beings support harmony in the community, free from hindrance."
        ]
    },
    "three_refuges_verse": {
        "title": "Three Refuges Verse",
        "label": "Show Three Refuges Verse",
        "chant_lines": [
            "I take refuge in buddha; I take refuge in dharma; I take refuge in sangha.",
            "I take refuge in buddha, honored as the highest;",
            "I take refuge in dharma, honored as the stainless;",
            "I take refuge in sangha, honored as harmonious.",
            "I have completely taken refuge in buddha;",
            "I have completely taken refuge in dharma;",
            "I have completely taken refuge in sangha."
        ]
    },
    "heart_sutra_sino": {
        "title": "Maka Han-nya Hara Mit-ta Shin Gyo",
        "label": "Open Heart Sutra — Sino-Japanese",
        "chant_lines": [
            "Kan ji zai bo sa",
            "gyo jin han-nya ha ra mi ta ji",
            "sho ken ◎ go on kai ku",
            "do is-sai ku yaku",
            "sha ri shi",
            "shiki fu i ku / ku fu i shiki",
            "shiki soku ze ku / ku soku ze shiki",
            "ju so gyo shiki / yaku bu nyo ze",
            "sha ri shi",
            "ze sho ho ku so",
            "fu sho fu metsu / fu ku fu jo / fu zo fu gen",
            "ze ko ku chu / mu shiki",
            "mu ju so gyo shiki",
            "mu gen ni bi zes-shin ni",
            "mu shiki sho ko mi soku ho",
            "mu gen kai nai shi mu i shiki kai",
            "mu mu myo yaku mu mu myo jin",
            "nai shi mu ro shi / yaku mu ro shi jin",
            "mu ku shu metsu do",
            "mu chi yaku mu toku / i mu sho tok-ko",
            "bo dai sat-ta / e han-nya ha ra mi ta ◎ ko",
            "shin mu kei ge / mu kei ge ko",
            "mu u ku fu",
            "on ri is-sai ten do mu so / ku gyo ne han",
            "san ze sho butsu / e han-nya ha ra mi ta ◎ ko",
            "toku a noku ta ra san myaku san bo dai",
            "ko chi han-nya ha ra mi ta",
            "ze dai jin shu / ze dai myo shu",
            "ze mu jo shu / ze mu to do shu",
            "no jo is-sai ku / shin jitsu fu ko",
            "ko setsu han-nya ha ra mi ta shu",
            "soku setsu shu watsu",
            "gya tei gya tei",
            "● ha ra gya tei",
            "hara so gya tei",
            "● bo ji sowa ka",
            "han-nya shin gyo"
        ]
    },
    "heart_sutra_english": {
        "title": "The Heart of Great Perfect Wisdom Sutra",
        "label": "Open Heart Sutra — English",
        "chant_lines": [
            "Avalokiteshvara Bodhisattva, when deeply practicing prajna paramita,",
            "clearly saw that all five aggregates are empty and thus relieved all suffering.",
            "Shariputra, form does not differ from emptiness, emptiness does not differ from form.",
            "Form itself is emptiness, emptiness itself form.",
            "Sensations, perceptions, formations, and consciousness are also like this.",
            "Shariputra, all dharmas are marked by emptiness;",
            "they neither arise nor cease, are neither defiled nor pure, neither increase nor decrease.",
            "Therefore, given emptiness, there is no form, no sensation, no perception, no formation, no consciousness;",
            "no eyes, no ears, no nose, no tongue, no body, no mind;",
            "no sight, no sound, no smell, no taste, no touch, no object of mind;",
            "no realm of sight, and so forth until no realm of mind consciousness.",
            "There is neither ignorance nor extinction of ignorance,",
            "and so forth until neither old age and death, nor extinction of old age and death;",
            "no suffering, no cause, no cessation, no path; no knowledge and no attainment.",
            "With nothing to attain, a bodhisattva relies on prajna paramita,",
            "and thus the mind is without hindrance. Without hindrance, there is no fear.",
            "Far beyond all inverted views, one realizes nirvana.",
            "All buddhas of past, present, and future rely on prajna paramita",
            "and thereby attain unsurpassed, complete, perfect enlightenment.",
            "Therefore, know the prajna paramita as the great miraculous mantra,",
            "the great bright mantra, the supreme mantra, the incomparable mantra,",
            "which removes all suffering and is true, not false.",
            "Therefore we proclaim the prajna paramita mantra, the mantra that says:",
            "Gate Gate ● Paragate Parasamgate ● Bodhi Svaha."
        ]
    },
    "daihishin_darani": {
        "title": "Daihishin Darani",
        "label": "Open Great Compassion Dharani",
        "chant_lines": [
            "Namu kara tan no / tora ya ya",
            "namu ori ya",
            "boryo ki chi shifu ra ya",
            "fuji sato bo ya / moko sato bo ya",
            "mo ko kya runi kya ya",
            "◎ en / sa hara ha e shu tan no ton sha",
            "namu shiki ri toi mo / ori ya",
            "boryo ki chi / shifu ra / rin to bo",
            "na mu no ra / kin ji ki ri / mo ko ho do",
            "sha mi sa bo / o to jo shu ben / o shu in",
            "sa bo sa to / no mo bo gya / mo ha te cho",
            "to ji to / en / o bo ryo ki / ru gya chi / kya ra chi",
            "i kiri mo ko / fuji sa to",
            "sa bo sa bo / mo ra mo ra / mo ki mo ki",
            "ri to in ku ryo ku ryo",
            "ke mo to ryo to ryo / ho ja ya chi",
            "mo ko ho ja ya chi / to ra to ra / chiri ni",
            "shifu ra ya / sha ro sha ro",
            "mo mo ha mo ra / ho chi ri / i ki i ki",
            "shi no shi no / ora san fura sha ri",
            "ha za ha zan / fura sha ya",
            "評 ryo ku ryo / mo ra ku ryo ku ryo",
            "ki ri sha ro sha ro / shi ri shi ri / su ryo su ryo",
            "fuji ya / fuji ya / fudo ya fudo ya / mi chiri ya",
            "◎ nora kin ji / chiri shuni no / hoya mono / somo ko",
            "shido ya / somo ko / moko shido ya / somo ko",
            "shido yu ki / shifu ra ya / somo ko",
            "◎ nora kin ji / somo ko",
            "mo ra no ra somo ko / shira su omo gya ya / so mo ko",
            "sobo moko shido ya / somo ko",
            "shaki ra oshi do ya / somo ko",
            "hodo mogya shido ya / somo ko",
            "nora kin ji ha gyara ya / somo ko",
            "mo hori shin gyara ya somo ko",
            "namu kara tan no tora ya ya",
            "● namu ori ya / boryo ki chi / shifu ra ya / somo ko",
            "● shite do modo ra / hodo ya / so mo ko"
        ]
    },
    "jukku_kannon_gyo": {
        "title": "Enmei Jukku Kannon Gyō",
        "label": "Show Ten-Line Kannon Sutra",
        "chant_lines": [
            "Kanzeon / namu butsu",
            "yo butsu u en / yo butsu u on",
            "bup po so en / jo raku ga jo",
            "cho nen kanzeon / bo nen kanzeon",
            "nen nen ju shin ki / nen nen bu ri shin"
        ]
    },
    "ten_names": {
        "title": "The Ten Buddha Names",
        "label": "Show Ten Buddha Names",
        "chant_lines": [
            "Vairochana Buddha, pure Dharmakaya;",
            "Lochana Buddha, complete Sambhogakaya;",
            "Shakyamuni Buddha, myriad Nirmanakaya;",
            "Maitreya Buddha, of future birth;",
            "all buddhas throughout space and time;",
            "Lotus of the Wondrous Dharma, Mahayana sutra.",
            "Manjushri Bodhisattva, great wisdom;",
            "Samantabhadra Bodhisattva, great activity;",
            "Avalokiteshvara Bodhisattva, great compassion；",
            "all honored ones, bodhisattvas, mahasattvas；",
            "wisdom beyond wisdom, maha prajna paramita."
        ]
    },
    "vows": {
        "title": "The Four Great Vows",
        "label": "Show Four Great Vows",
        "chant_lines": [
            "1. Beings are numberless; I vow to free them.",
            "2. Delusions are inexhaustible; I vow to end them.",
            "3. Dharma gates are boundless; I vow to enter them.",
            "4. The buddha way is unsurpassable; I vow to realize it."
        ]
    },
    "impermanence": "Since the Great Master Tathagata entered Parinirvana, our lives likewise diminish. Like fish in a shrinking pond, what joy is there in this? We should strive with diligence as if saving our heads from fire. Be mindful of impermanence, and do not be negligent.",
    "pure_precepts": [
        "(1) The precept of embracing all moral codes: This is the abode of the laws and codes of all buddhas.",
        "(2) The precept of embracing all good acts: This is the dharma of the ultimate awakening.",
        "(3) The precept of embracing and benefiting all living beings: One should transcend distinction between ordinary beings and sages."
    ],
    "major_precepts": [
        "1. Not killing: By not killing life, buddha seeds are nurtured.",
        "2. Not stealing: When mind and objects are such, the gate of liberation stands open.",
        "3. Not indulging in sexual greed: When the three wheels are pure, there is nothing to be desired.",
        "4. Not speaking falsehood: Since the dharma-wheel turns, reality and truth are revealed.",
        "5. Not selling intoxicating liquor: This is truly the great light of wisdom.",
        "6. Not talking of the faults of others: Do not discuss the faults of others. Do not corrupt the way.",
        "7. Not praising oneself nor slandering others: Buddhas and ancestors attain realization with the whole sky.",
        "8. Not begrudging the dharma or materials: One should give them freely when requested.",
        "9. Not being angry: Withdrawing without attachment, right there you can see an ocean of bright clouds.",
        "10. Not slandering the Three Treasures: We should respectfully accept the Three Treasures and devote ourselves to them."
    ]
}

DEDICATIONS = {
    "morning": {
        "label": "Show Morning Dedication",
        "chant_lines": [
            "Chanting the Heart Sutra Mantra,",
            "we dedicate this merit to the pure body of the dharma realm,",
            "and to our household's protective spirits.",
            "We pray for our family's peace, for their health and longevity,",
            "and for the awakening of all beings."
        ]
    },
    "midday": {
        "label": "Show Midday Dedication",
        "chant_lines": [
            "Chanting the Victor’s Mantra,",
            "we dedicate this merit to the Three Jewels,",
            "and to the good fortune of our family.",
            "We pray for a peaceful household, for a stable lay practice,",
            "and for auspicious conditions for all."
        ]
    },
    "evening": {
        "label": "Show Evening Dedication",
        "chant_lines": [
            "Chanting the Surangama Mantra,",
            "we dedicate this merit to the pure body of the dharma realm,",
            "to the myriad spirits, and to our kitchen deity.",
            "We pray for a safe and peaceful household,",
            "and for the flourishing of the Dharma through our actions."
        ]
    },
    "weekly_repaying": {
        "label": "Show Dedication for Repaying Blessings",
        "chant_lines": [
            "Having chanted the Heart Sutra, we reverently offer the merit generated thereby",
            "to our Great Benefactor and Founder of the Teachings, the Original Teacher Shakyamuni,",
            "to Yuima Kōji, to the Eminent Ancestor Dogen, and to the Great Ancestor Keizan,",
            "that it may adorn their awakening, the unsurpassed fruit of Buddhahood.",
            "We humbly pray that the blessings of the four benefactors may be fully requited,",
            "that the three classes of existences may all be saved,",
            "and that sentient beings throughout the triple world equally perfect omniscience.",
            "We pray that this family shall flourish, and we pray for the health,",
            f"healing, and safeguarding of {SANGHA_NAMES}.",
            "We pray that misfortunes and hindrances shall be prevented and removed,",
            "and that all conditions shall be favorable."
        ]
    },
    "weekly_spirits": {
        "label": "Show Dedication for All Spirits",
        "chant_lines": [
            "The clear, cool moon of the bodhisattva floats in the sky of utter emptiness；",
            "in the pure water of the mind of beings, the reflection of bodhi will appear.",
            "We humbly beg the three treasures for their illumination.",
            "Having chanted the Great Compassion Dharani, we offer the merit generated thereby",
            "to the spirits of ancestors and deceased family members of this household,",
            "to the six close kin and seven generations of parents,",
            "and to all sentient beings of the dharma realm,",
            "including the myriad spirits of the triple world both with and without connections to the living.",
            "What we pray for is that their delusion of long kalpas will now be extinguished,",
            "that the marvelous wisdom of true emptiness will hereby appear,",
            "and that they will immediately comprehend the uncreated",
            "and quickly confirm the fruit of Buddhahood."
        ]
    },
    "stove_god": {
        "label": "Show Dedication for Stove God — Daikokuten",
        "chant_lines": [
            "Having recited the Heart of Great Perfect Wisdom Sutra,",
            "we dedicate the merit to Daikokuten, the kitchen spirit of this household,",
            "that he may guard the dharma and protect our family."
        ]
    },
    "universal_closing": "◎ ji ho san shi i shi fu / shi son bu sa mo ko sa / ◎ mo ko ho ja ho rō mi",
    "final_closing": "◎ All buddhas throughout space and time, all honored ones, bodhisattvas, mahasattvas, ◎ wisdom beyond wisdom, maha-prajnaparamita."
}

ANNUAL_LITURGY = {
    "gotan_e": "Having chanted the Heart of Great Perfect Wisdom, we respectfully celebrate the birth of the Eminent Ancestor, Great Master Jōyō (Dōgen). We have reverently prepared this humble offering of tea. We offer the excellent merit accumulated thereby to requite his compassionate blessings, praying that the ancestral wind shall ever blow through this household.",
    "nehan_e": "The pure body of the dharma realm fundamentally has no emerging or disappearing. On the fifteenth day of this month, we respectfully celebrate the occasion of the entry into final nirvana of our Great Benefactor, the Original Master Shakyamuni Buddha. We offer up the excellent merit accumulated thereby to requite his compassionate blessings.",
    "robiraki": "May the warmth of this hearth sustain the health of this family, and may the fire of wisdom burn away our afflictions.",
    "ancestral_higan": "We dedicate the merit from the preceding sutra chanting to our family ancestors and all departed spirits in the inexhaustible dharma realms. May they be fully satiated with the taste of dharma, and and may living beings everywhere be saved.",
    "hana_matsuri": "On the eighth day of this month, we respectfully celebrate the occasion of the birth of our Great Benefactor, the Original Master Shakyamuni Buddha. Having respectfully provided this flower and fresh water, we offer up the excellent merit accumulated thereby to requite his compassionate blessings.",
    "zengetsu": "In this month of good cultivation, we dedicate this merit to the guardians of the Dharma and the earth spirits of this land. We pray that our wholesome conduct may increase, that peace may prevail in the world, and that all conditions for our lay practice remain auspicious.",
    "women_ancestors": "We dedicate this gathered merit to the great compassion of Kannon Bodhisattva, to the Abbess Ekyu, and to all the women ancestors of the Sōtō lineage. May their spiritual light continue to guide our practice, and may all beings realize the Way.",
    "sejiki": "We offer this pure food and water to the ancestors of this family, to all unconnected spirits of the three realms, and to those suffering in the hungry ghost realm. May they be fully satiated with the taste of the Dharma, escape their suffering, and perfectly realize awakening.",
    "ryosoki": "On this day of remembrance, we have prepared this humble offering of tea and sweets. We dedicate the excellent merit accumulated thereby to the Eminent Ancestor Eihei Dōgen, and the Great Ancestor Keizan Jōkin. May the ancestral wind of their teachings ever blow through this household, guiding our daily practice.",
    "rofuji": "As the seasons turn cold, we close the summer hearth. May we remain vigilant against the disasters of fire, and may the warmth of compassion sustain this household.",
    "darumaki": "We offer this merit to the First Ancestor in China, Great Master Bodhidharma. We pray that his transmission of mind-to-mind awakening remains luminous, and that our own practice of Zazen remains as immovable as a wall.",
    "jodo_e": "On this Commemoration Day of Enlightenment, the original teacher Shakyamuni Tathagata realized his awakening. Respectfully preparing this humble offering of tea and light, we dedicate the vast merit accrued therefrom to discharge our indebtedness to the Dharma and the spiritual nourishment he granted to us.",
    "eka_eko": "We offer this merit to the Second Ancestor in China, Great Master Shōshū Fukaku, the Most Reverend Eka. We raise it to requite his compassionate blessings and honor his unshakable determination.",
    "year_end": "Welcoming the New Year's Eve of the year's end, we offer this food and merit to all sentient beings in the inexhaustible dharma realms, and to the unconnected spirits. May the 108 afflictions be purified, and may all beings escape the round of rebirth and equally perfect awakening."
}

WEEKEND_RITUALS = {
    "hosan_greeting": "Chin-cha (Take care).",
    "kaisei_salutation": "Throughout this weekend, we have relied on each other. If my three modes of karma have been unwholesome, I humbly beg your compassion."
}
