"""
EVERYDAY_SHINGI_SCHEDULE.PY
The logic engine for the Keizan Society.

PURPOSE:
    Determines the chronological flow of the day, organizing liturgical 
    content into a three-level hierarchy for web rendering.

REVISION HISTORY:
    2026-06-06: Initial creation of the logic engine.
    2026-06-06: Refactored for structured data and ritual-use logic.
                - Implemented rich object passing for chants and dedications.
                - Fixed duplicated blessings in service flows.
                - Standardized service step numbering in titles only.
                - Separated ritual instructions from liturgical content.

MAINTAINER:
    Senior Full-Stack Developer / Keizan Society Technical Editor
"""

import calendar
from everyday_shingi_liturgy import VERSES, MEALS, CHANTS, DEDICATIONS, ANNUAL_LITURGY, WEEKEND_RITUALS

def get_ritual_legend():
    """Returns the standard ritual symbol legend for the Keizan Society."""
    return [
        ("◎", "Strike large bowl-bell"),
        ("●", "Strike small bowl-bell"),
        ("▲", "Muffle hand-bell with striker")
    ]

def get_uposatha_ceremony():
    """Assembles the bi-monthly precepts ceremony as structured objects."""
    return [
        {"type": "instruction", "content": "Perform Repentance (3x in Gassho)"},
        CHANTS['repentance'],
        {"type": "instruction", "content": "Four Great Vows (3x)"},
        CHANTS['vows'],
        CHANTS['kaikyo_ge'],
        CHANTS['three_refuges_verse'],
        {"type": "header", "content": "The Threefold Pure Precepts"},
        {"type": "list", "content": CHANTS['pure_precepts']},
        {"type": "header", "content": "The Ten Major Precepts"},
        {"type": "list", "content": CHANTS['major_precepts']},
        {"type": "instruction", "content": "Verse of Purity"},
        {"type": "text", "content": MEALS['purity_lotus']},
        {"type": "instruction", "content": "Three Refuges Prayer (Prostrate after each)"},
        CHANTS['three_refuges_prayer'],
        {"type": "ritual", "content": "Closing: 3 Prostrations"},
        {"type": "liturgy", "content": DEDICATIONS['final_closing']}
    ]

def get_weekly_home_service():
    """Assembles the weekend morning service with explicit step numbering."""
    return [
        {"type": "instruction", "content": "PREPARATION: Light candle and incense. Regulate breath."},
        {"type": "ritual", "content": "◎ ◎ Perform gasshō and three full prostrations."},
        
        # Steps are numbered in titles only
        {"step": 1, "data": CHANTS['kaikyo_ge']},
        {"step": 2, "data": CHANTS['repentance']},
        {"step": 3, "data": CHANTS['three_refuges_prayer']},
        {"step": 4, "data": CHANTS['three_refuges_verse']},
        {"step": 5, "data": CHANTS['heart_sutra_sino']},
        {"step": 6, "data": DEDICATIONS['weekly_repaying']},
        
        {"type": "ritual", "content": DEDICATIONS['universal_closing']},
        
        {"step": 7, "data": CHANTS['daihishin_darani']},
        {"step": 8, "data": DEDICATIONS['weekly_spirits']},
        
        {"type": "ritual", "content": "● ● ● [Make three prostrations]"},
        
        {"step": 9, "title": "Service for the Spirit of the Kitchen", "type": "transition", "content": "Move to the Kitchen"},
        {"type": "chant", "data": CHANTS['heart_sutra_english']},
        {"type": "dedication", "data": DEDICATIONS['stove_god']},
        
        {"type": "ritual", "content": DEDICATIONS['final_closing']},
        {"type": "ritual", "content": "FINAL ACTION: ◎ [Make three deep standing bows]"}
    ]

def get_annual_event(target_date):
    """Returns annual event data if the date matches an observance."""
    m, d = target_date.month, target_date.day
    
    # Winter
    if m == 1 and d == 26:
        return {"name": "KOSO GOTAN-E (Dogen Zenji's Birthday)", "step": "morning_service", "action": "Before sitting Zazen, brew a fresh cup of tea and place it on the home altar.", "liturgy": [CHANTS['heart_sutra_mantra'], ANNUAL_LITURGY['gotan_e']]}
    if m == 2 and d == 15:
        return {"name": "NEHAN-E (Nirvana Day)", "step": "evening_service", "action": "Dim the lights in the house. Light a single candle on the altar.", "liturgy": [CHANTS['surangama_heart_mantra'], ANNUAL_LITURGY['nehan_e']]}
    
    # Spring
    if m == 3 and d == 1:
        return {"name": "ROBIRAKI (Hearth Opening)", "step": "breakfast", "action": "When turning on the stove, take a moment of continuous mindfulness.", "liturgy": [ANNUAL_LITURGY['robiraki']]}
    if m == 3 and d == 20:
        return {"name": "HIGAN-E (Spring Equinox)", "step": "evening_service", "action": "Place a photograph of deceased family members on the altar.", "liturgy": [CHANTS['heart_sutra_english'], ANNUAL_LITURGY['ancestral_higan']]}
    if m == 4 and d == 8:
        return {"name": "HANA-MATSURI (Buddha's Birthday)", "step": "morning_service", "action": "Place a single fresh flower on the altar.", "liturgy": [CHANTS['heart_sutra_mantra'], ANNUAL_LITURGY['hana_matsuri']]}
    
    # Summer
    if (m == 1 or m == 5 or m == 9) and d == 16:
        return {"name": "ZENGETSU KITO-E (Month of Good Cultivation)", "step": "evening_service", "action": "Sit Zazen with a specific intention toward ethical renewal.", "liturgy": [CHANTS['ten_names'], ANNUAL_LITURGY['zengetsu']]}
    if m == 6 and d == 18:
        return {"name": "WOMEN'S ANCESTORS COMMEMORATION", "step": "evening_service", "action": "Light a special candle to honor the maternal lineage.", "liturgy": [CHANTS['jukku_kannon_gyo'], ANNUAL_LITURGY['women_ancestors']]}
    if (m == 7 or m == 8) and d == 15:
        return {"name": "O-BON & SEJIKI-E (Festival of Remembrance)", "step": "evening_service", "action": "Place a small bowl of water and a pinch of food on the altar.", "liturgy": [CHANTS['daihishin_darani'], ANNUAL_LITURGY['sejiki']]}
    
    # Autumn
    if m == 9 and d == 21:
        return {"name": "HIGAN-E (Autumn Equinox)", "step": "evening_service", "action": "Place a photograph of deceased family members on the altar.", "liturgy": [CHANTS['heart_sutra_english'], ANNUAL_LITURGY['ancestral_higan']]}
    if m == 9 and d == 29:
        return {"name": "RYOSOKI (Two Ancestors Memorial)", "step": "morning_service", "action": "Brew a fresh cup of tea and place a small sweet on the altar.", "liturgy": [CHANTS['surangama_heart_mantra'], ANNUAL_LITURGY['ryosoki']]}
    if m == 10 and d == 1:
        return {"name": "ROFUJI (Hearth Closure)", "step": "evening_purification", "action": "Take a moment of mindfulness regarding fire safety.", "liturgy": [ANNUAL_LITURGY['rofuji']]}
    if m == 10 and d == 5:
        return {"name": "DARUMAKI (Bodhidharma Memorial)", "step": "morning_service", "action": "Offer a fresh cup of tea to the altar.", "liturgy": [CHANTS['heart_sutra_english'], ANNUAL_LITURGY['darumaki']]}

    # Early Winter
    if m == 12 and d == 8:
        return {"name": "ROHATSU & JODO-E (Buddha's Awakening)", "step": "night_zazen", "action": "Extend Zazen until midnight. Place a candle and tea on the altar.", "liturgy": [CHANTS['surangama_heart_mantra'], ANNUAL_LITURGY['jodo_e']]}
    if m == 12 and (d == 9 or d == 10):
        return {"name": "DANPI HO-ON SESSHIN (Memorial for Huike)", "step": "morning_service", "action": "Offer a fresh cup of tea. Reflect on ancestral sacrifice.", "liturgy": [CHANTS['daihishin_darani'], ANNUAL_LITURGY['eka_eko']]}
    if m == 12 and d == 31:
        return {"name": "O-MISOKA (Year-End Purification)", "step": "night_zazen", "action": "Clean altar. Strike bell 108 times at end of Zazen.", "liturgy": [CHANTS['daihishin_darani'], ANNUAL_LITURGY['year_end']]}

    return None

def generate_daily_schedule(target_date):
    """
    Generates a structured daily schedule.
    Returns: {
        "summary": {"morning": str, "midday": str, "evening": str, "night": str},
        "blocks": [ (block_name, [ (section_name, [actions]) ]) ]
    }
    """
    day_of_week = target_date.strftime('%A')
    day_val = target_date.day
    is_last_day = day_val == calendar.monthrange(target_date.year, target_date.month)[1]
    is_maintenance_day = day_val % 10 in [4, 9]
    is_weekend = day_of_week in ["Saturday", "Sunday"]
    annual = get_annual_event(target_date)
    
    blocks = []
    summary = {"morning": "", "midday": "", "evening": "", "night": ""}

    # --- MORNING BLOCK ---
    morning_sections = []
    morning_sections.append(("Waking & Morning Purification", [VERSES['waking'], VERSES['toothbrush'], VERSES['brushing'], VERSES['rinsing'], VERSES['face']]))
    summary["morning"] = "purification · "

    m_actions = []
    if annual and annual['step'] == "morning_service":
        m_actions.append({"type": "annual", "content": f"ANNUAL OBSERVANCE: {annual['name']}"})
        m_actions.append({"type": "instruction", "content": annual['action']})
        for item in annual['liturgy']: m_actions.append(item)
        morning_sections.append(("Dawn Zazen & Annual Morning Service", m_actions))
        summary["morning"] += "zazen · annual service"
    elif is_weekend:
        m_actions = [{"type": "instruction", "content": "Extended 45-minute Dawn Zazen"}]
        if is_maintenance_day: m_actions.append({"type": "text", "content": "Shaving Verse: " + VERSES['tonsure']})
        m_actions.extend(get_weekly_home_service())
        morning_sections.append(("Dawn Zazen & Weekly Home Service", m_actions))
        summary["morning"] += "45m zazen · home service"
    elif is_maintenance_day:
        morning_sections.append(("Morning Service: Cancelled — Maintenance Day", [{"type": "instruction", "content": "Focus on physical maintenance and household care."}, {"type": "text", "content": "Shaving Verse: " + VERSES['tonsure']}]))
        summary["morning"] += "maintenance"
    else:
        morning_dedication = DEDICATIONS['morning']
        if day_val in [1, 15]: morning_dedication = DEDICATIONS['weekly_repaying'] # Use structured repaying for 1st/15th
        morning_sections.append(("Dawn Zazen & Morning Service", [
            {"type": "instruction", "content": "Dawn Zazen"},
            VERSES['kesa'],
            {"type": "instruction", "content": "Chant Heart Sutra Mantra 7x"},
            CHANTS['heart_sutra_sino'], # Or just the mantra if preferred
            morning_dedication,
            {"type": "ritual", "content": DEDICATIONS['final_closing']}
        ]))
        summary["morning"] += "zazen · morning service"

    morning_sections.append(("Breakfast", [MEALS['five_contemplations']]))
    morning_sections.append(("Showering & Preparation", [VERSES['bathing']]))
    blocks.append(("Morning", morning_sections))

    # --- MIDDAY BLOCK ---
    midday_sections = []
    if is_weekend:
        midday_sections.append(("Household Work & Family Time", [{"type": "instruction", "content": "Engage in chores or rest as temple work."}]))
        summary["midday"] = "household work"
    else:
        midday_sections.append(("Commute & Morning Work", [VERSES['road_start'], VERSES['right_livelihood']]))
        midday_sections.append(("Midday Pause", [
            {"type": "instruction", "content": "Midday Zazen"},
            {"type": "instruction", "content": "Victor's Heart Mantra (7x)"},
            DEDICATIONS['midday'],
            MEALS['five_contemplations']
        ]))
        summary["midday"] = "work practice · midday zazen"
    blocks.append(("Midday", midday_sections))

    # --- AFTERNOON & EVENING BLOCK ---
    evening_sections = []
    e_actions = []
    if annual and annual['step'] == "evening_service":
        e_actions.append({"type": "annual", "content": f"ANNUAL OBSERVANCE: {annual['name']}"})
        e_actions.append({"type": "instruction", "content": annual['action']})
        for item in annual['liturgy']: e_actions.append(item)
        evening_sections.append(("Late Afternoon Zazen & Annual Evening Service", e_actions))
        summary["evening"] = "zazen · annual service"
    elif is_weekend or day_of_week == "Friday":
        evening_sections.append(("Evening Transition", [{"type": "instruction", "content": "Transition to rest and family time."}]))
        summary["evening"] = "rest"
    else:
        e_actions.append({"type": "instruction", "content": "Late Afternoon Zazen"})
        e_actions.append(DEDICATIONS['evening'])
        if day_val in [8, 18, 28]: e_actions.append({"type": "text", "content": CHANTS['impermanence']})
        if day_val == 18: e_actions.append(CHANTS['jukku_kannon_gyo'])
        if day_val == 15 or is_last_day: e_actions.extend(get_uposatha_ceremony())
        e_actions.append({"type": "ritual", "content": DEDICATIONS['final_closing']})
        evening_sections.append(("Late Afternoon Zazen & Evening Service", e_actions))
        summary["evening"] = "zazen · evening service"
    blocks.append(("Afternoon & Evening", evening_sections))

    # --- NIGHT BLOCK ---
    night_sections = []
    n_actions = [{"type": "instruction", "content": "Evening Purification"}]
    if day_of_week == "Friday":
        n_actions.append({"type": "ritual", "content": "HOSAN: " + WEEKEND_RITUALS['hosan_greeting']})
    elif day_of_week == "Sunday":
        n_actions.append({"type": "ritual", "content": "KAISEI: " + WEEKEND_RITUALS['kaisei_salutation']})
    n_actions.append(CHANTS['vows'])
    n_actions.append({"type": "text", "content": VERSES['sleep']})
    night_sections.append(("Night Zazen & Sleep", n_actions))
    summary["night"] = "zazen · vows · sleep"
    blocks.append(("Night", night_sections))

    return {
        "summary": summary,
        "legend": get_ritual_legend(),
        "blocks": blocks
    }
