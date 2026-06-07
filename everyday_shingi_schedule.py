"""
EVERYDAY_SHINGI_SCHEDULE.PY
The logic engine for the Keizan Society.

PURPOSE:
    Determines the chronological flow of the day, organizing liturgical 
    content into a three-level hierarchy for web rendering.

REVISION HISTORY:
    2026-06-06: Initial creation of the logic engine.
    2026-06-06: Refactored for structured data and ritual-use logic.
    2026-06-06: BUGFIX: Restored missing Flower Garland Sutra verses 
                in Morning and Evening Purification sections.

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
    
    if m == 1 and d == 26:
        return {"name": "KOSO GOTAN-E (Dogen Zenji's Birthday)", "step": "morning_service", "action": "Before sitting Zazen, brew a fresh cup of tea.", "liturgy": [CHANTS['heart_sutra_sino'], ANNUAL_LITURGY['gotan_e']]}
    if m == 2 and d == 15:
        return {"name": "NEHAN-E (Nirvana Day)", "step": "evening_service", "action": "Dim the lights in the house.", "liturgy": [CHANTS['heart_sutra_english'], ANNUAL_LITURGY['nehan_e']]}
    if m == 3 and d == 1:
        return {"name": "ROBIRAKI (Hearth Opening)", "step": "breakfast", "action": "Mindful stove opening.", "liturgy": [ANNUAL_LITURGY['robiraki']]}
    if m == 3 and d == 20:
        return {"name": "HIGAN-E (Spring Equinox)", "step": "evening_service", "action": "Place ancestor photos on altar.", "liturgy": [CHANTS['heart_sutra_english'], ANNUAL_LITURGY['ancestral_higan']]}
    if m == 4 and d == 8:
        return {"name": "HANA-MATSURI (Buddha's Birthday)", "step": "morning_service", "action": "Place a flower on the altar.", "liturgy": [CHANTS['heart_sutra_sino'], ANNUAL_LITURGY['hana_matsuri']]}
    if (m == 1 or m == 5 or m == 9) and d == 16:
        return {"name": "ZENGETSU KITO-E", "step": "evening_service", "action": "Ethical renewal intention.", "liturgy": [CHANTS['ten_names'], ANNUAL_LITURGY['zengetsu']]}
    if m == 6 and d == 18:
        return {"name": "WOMEN'S ANCESTORS", "step": "evening_service", "action": "Light candle for maternal lineage.", "liturgy": [CHANTS['jukku_kannon_gyo'], ANNUAL_LITURGY['women_ancestors']]}
    if (m == 7 or m == 8) and d == 15:
        return {"name": "O-BON & SEJIKI-E", "step": "evening_service", "action": "Offer water and food pinch.", "liturgy": [CHANTS['daihishin_darani'], ANNUAL_LITURGY['sejiki']]}
    if m == 9 and d == 21:
        return {"name": "HIGAN-E (Autumn Equinox)", "step": "evening_service", "action": "Place ancestor photos on altar.", "liturgy": [CHANTS['heart_sutra_english'], ANNUAL_LITURGY['ancestral_higan']]}
    if m == 9 and d == 29:
        return {"name": "RYOSOKI", "step": "morning_service", "action": "Offer tea and sweet.", "liturgy": [CHANTS['heart_sutra_sino'], ANNUAL_LITURGY['ryosoki']]}
    if m == 10 and d == 1:
        return {"name": "ROFUJI (Hearth Closure)", "step": "evening_purification", "action": "Mindfulness of fire safety.", "liturgy": [ANNUAL_LITURGY['rofuji']]}
    if m == 10 and d == 5:
        return {"name": "DARUMAKI", "step": "morning_service", "action": "Offer tea to Bodhidharma.", "liturgy": [CHANTS['heart_sutra_english'], ANNUAL_LITURGY['darumaki']]}
    if m == 12 and d == 8:
        return {"name": "ROHATSU & JODO-E", "step": "night_zazen", "action": "Extend Zazen until midnight.", "liturgy": [CHANTS['heart_sutra_sino'], ANNUAL_LITURGY['jodo_e']]}
    if m == 12 and (d == 9 or d == 10):
        return {"name": "DANPI HO-ON SESSHIN", "step": "morning_service", "action": "Reflect on Huike's sacrifice.", "liturgy": [CHANTS['daihishin_darani'], ANNUAL_LITURGY['eka_eko']]}
    if m == 12 and d == 31:
        return {"name": "O-MISOKA", "step": "night_zazen", "action": "Clean altar. Strike bell 108 times.", "liturgy": [CHANTS['daihishin_darani'], ANNUAL_LITURGY['year_end']]}

    return None

def generate_daily_schedule(target_date):
    """Generates a structured daily schedule."""
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
    
    # Waking Verses (Restored)
    morning_sections.append(("Waking & Morning Purification", [
        {"type": "text", "content": VERSES['waking']},
        {"type": "text", "content": VERSES['toothbrush']},
        {"type": "text", "content": VERSES['brushing']},
        {"type": "text", "content": VERSES['rinsing']},
        {"type": "text", "content": VERSES['face']}
    ]))
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
        morning_sections.append(("Morning Service: Cancelled — Maintenance Day", [
            {"type": "instruction", "content": "Focus on physical maintenance and household care."},
            {"type": "text", "content": "Shaving Verse: " + VERSES['tonsure']}
        ]))
        summary["morning"] += "maintenance"
    else:
        morning_sections.append(("Dawn Zazen & Morning Service", [
            {"type": "instruction", "content": "Dawn Zazen"},
            VERSES['kesa'],
            {"type": "instruction", "content": "Chant Heart Sutra Mantra 7x"},
            CHANTS['heart_sutra_sino'],
            DEDICATIONS['morning'],
            {"type": "ritual", "content": DEDICATIONS['final_closing']}
        ]))
        summary["morning"] += "zazen · morning service"

    morning_sections.append(("Breakfast", [MEALS['five_contemplations']]))
    morning_sections.append(("Showering & Preparation", [{"type": "text", "content": VERSES['bathing']}]))
    blocks.append(("Morning", morning_sections))

    # --- MIDDAY BLOCK ---
    midday_sections = []
    if is_weekend:
        midday_sections.append(("Household Work & Family Time", [{"type": "instruction", "content": "Engage in chores or rest as temple work."}]))
        summary["midday"] = "household work"
    else:
        midday_sections.append(("Commute & Morning Work", [
            {"type": "text", "content": VERSES['road_start']},
            {"type": "text", "content": VERSES['right_livelihood']}
        ]))
        midday_sections.append(("Midday Pause", [
            {"type": "instruction", "content": "Midday Zazen"},
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
    
    # Evening Purification (Restored Verses)
    p_actions = []
    if annual and annual['step'] == "evening_purification":
        p_actions.append({"type": "annual", "content": f"ANNUAL OBSERVANCE: {annual['name']}"})
        p_actions.append({"type": "instruction", "content": annual['action']})
    
    p_actions.extend([
        {"type": "text", "content": VERSES['toothbrush']},
        {"type": "text", "content": VERSES['brushing']},
        {"type": "text", "content": VERSES['flossing']},
        {"type": "text", "content": VERSES['rinsing']},
        {"type": "text", "content": VERSES['face']}
    ])
    night_sections.append(("Evening Purification", p_actions))

    # Night Zazen
    n_actions = [{"type": "instruction", "content": "Night Zazen"}]
    if day_of_week == "Friday":
        n_actions.append({"type": "ritual", "content": "HOSAN: " + WEEKEND_RITUALS['hosan_greeting']})
    elif day_of_week == "Sunday":
        n_actions.append({"type": "ritual", "content": "KAISEI: " + WEEKEND_RITUALS['kaisei_salutation']})
    n_actions.append(CHANTS['vows'])
    n_actions.append({"type": "text", "content": VERSES['sleep']})
    night_sections.append(("Night Zazen & Sleep", n_actions))
    
    summary["night"] = "purification · zazen · vows · sleep"
    blocks.append(("Night", night_sections))

    return {
        "summary": summary,
        "legend": get_ritual_legend(),
        "blocks": blocks
    }
