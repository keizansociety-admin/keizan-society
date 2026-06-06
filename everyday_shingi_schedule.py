"""
EVERYDAY_SHINGI_SCHEDULE.PY
The logic engine for the Keizan Society.

PURPOSE:
    Determines the chronological flow of the day, organizing liturgical 
    content into a three-level hierarchy for web rendering.

REVISION HISTORY:
    2025-01-24: Refactored for three-level hierarchy and web accessibility.
                - Added 'At a Glance' summary logic.
                - Added Ritual Symbol Legend.
                - Implemented gentle status notices for cancelled services.
                - Organized output into Time Blocks, Sections, and Actions.

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
    """Assembles the bi-monthly precepts ceremony."""
    return [
        "Repentance Verse (3x in Gassho): " + CHANTS['repentance'],
        "Four Great Vows (3x):"
    ] + CHANTS['vows'] + [
        "Sutra-Opening Verse: " + CHANTS['kaikyo_ge'],
        "Three Refuges: " + CHANTS['three_refuges_verse'],
        "Threefold Pure Precepts:"
    ] + CHANTS['pure_precepts'] + [
        "Ten Major Precepts:"
    ] + CHANTS['major_precepts'] + [
        "Verse of Purity: " + MEALS['purity_lotus'],
        "Three Refuges Prayer (Prostrate after each): " + CHANTS['three_refuges_prayer'],
        "Closing: " + DEDICATIONS['closing'] + " (3 Prostrations)"
    ]

def get_weekly_home_service():
    """Assembles the weekend morning service."""
    return [
        "PREPARATION: Light candle and 3 sticks of incense. Regulate breath.",
        "◎ ◎ Perform gasshō and three full prostrations.",
        "1. Sutra-Opening Verse (Kaikyō ge): " + CHANTS['kaikyo_ge'],
        "2. Repentance Verse (Sange mon): " + CHANTS['repentance'],
        "3. Three Refuges Prayer (Sanki raimon): " + CHANTS['three_refuges_prayer'],
        "4. Three Refuges Verse (Sankie mon): " + CHANTS['three_refuges_verse'],
        "5. Maka han-nya hara mit-ta shin gyo (Sino-Japanese):",
        CHANTS['heart_sutra_sino'],
        "6. Dedication (Repaying Blessings): " + DEDICATIONS['weekly_repaying'],
        DEDICATIONS['universal_closing'],
        "7. Daihishin darani (Great Compassion Dharani):",
        CHANTS['daihishin_darani'],
        "8. Dedication (For All Spirits): " + DEDICATIONS['weekly_spirits'],
        DEDICATIONS['universal_closing'],
        "● ● ● [Make three prostrations]",
        "9. SERVICE FOR SPIRIT OF THE KITCHEN (Move to Kitchen):",
        "Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'],
        "Dedication for Stove God (Daikokuten): " + DEDICATIONS['stove_god'],
        DEDICATIONS['final_closing'],
        "FINAL ACTION: ◎ [Make three deep standing bows]"
    ]

def get_annual_event(target_date):
    """Returns annual event data if the date matches an observance."""
    m, d = target_date.month, target_date.day
    
    # Winter
    if m == 1 and d == 26:
        return {"name": "KOSO GOTAN-E (Dogen Zenji's Birthday)", "step": "morning_service", "action": "Before sitting Zazen, brew a fresh cup of tea and place it on the home altar.", "liturgy": ["Heart Sutra Mantra (7x): " + CHANTS['heart_sutra_mantra'], "Gotan-e Eko: " + ANNUAL_LITURGY['gotan_e']]}
    if m == 2 and d == 15:
        return {"name": "NEHAN-E (Nirvana Day)", "step": "evening_service", "action": "Dim the lights in the house. Light a single candle on the altar to represent the passing of the light.", "liturgy": ["Surangama Heart Mantra (7x): " + CHANTS['surangama_heart_mantra'], "Nehan-e Eko: " + ANNUAL_LITURGY['nehan_e']]}
    
    # Spring
    if m == 3 and d == 1:
        return {"name": "ROBIRAKI (Hearth Opening)", "step": "breakfast", "action": "When turning on the stove or thermostat, take a moment of continuous mindfulness.", "liturgy": ["Silent Intention: " + ANNUAL_LITURGY['robiraki']]}
    if m == 3 and d == 20:
        return {"name": "HIGAN-E (Spring Equinox)", "step": "evening_service", "action": "Place a photograph of deceased family members on the altar. Offer water or rice.", "liturgy": ["Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'], "Ancestral Eko: " + ANNUAL_LITURGY['ancestral_higan']]}
    if m == 4 and d == 8:
        return {"name": "HANA-MATSURI (Buddha's Birthday)", "step": "morning_service", "action": "Place a single fresh flower (or a bowl of water with a flower) on the altar.", "liturgy": ["Morning Chant (Heart Sutra Mantra 7x)", "Birth Eko: " + ANNUAL_LITURGY['hana_matsuri']]}
    
    # Summer
    if (m == 1 or m == 5 or m == 9) and d == 16:
        return {"name": "ZENGETSU KITO-E (Month of Good Cultivation)", "step": "evening_service", "action": "Ensure the altar is clean. Sit Zazen with a specific intention toward ethical renewal.", "liturgy": ["Ten Buddha Names: " + CHANTS['ten_names'], "Zengetsu Eko: " + ANNUAL_LITURGY['zengetsu']]}
    if m == 6 and d == 18:
        return {"name": "WOMEN'S ANCESTORS COMMEMORATION", "step": "evening_service", "action": "Light a special candle on the home altar to honor the maternal lineage and female ancestors.", "liturgy": ["Ten-Line Kannon Sutra: " + CHANTS['jukku_kannon_gyo'], "Women's Lineage Eko: " + ANNUAL_LITURGY['women_ancestors']]}
    if (m == 7 or m == 8) and d == 15:
        return {"name": "O-BON & SEJIKI-E (Festival of Remembrance)", "step": "evening_service", "action": "Place a small bowl of water and a pinch of dinner (saba) on the altar or outside.", "liturgy": ["Great Compassion Dharani: " + CHANTS['daihishin_darani'], "Sejiki Eko: " + ANNUAL_LITURGY['sejiki']]}
    
    # Autumn
    if m == 9 and d == 21:
        return {"name": "HIGAN-E (Autumn Equinox)", "step": "evening_service", "action": "Place a photograph of deceased family members on the altar. Offer water or rice.", "liturgy": ["Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'], "Ancestral Eko: " + ANNUAL_LITURGY['ancestral_higan']]}
    if m == 9 and d == 29:
        return {"name": "RYOSOKI (Two Ancestors Memorial)", "step": "morning_service", "action": "Brew a fresh cup of tea and place a small sweet or piece of fruit on the altar.", "liturgy": ["Surangama Heart Mantra (7x): " + CHANTS['surangama_heart_mantra'], "Ryosoki Eko: " + ANNUAL_LITURGY['ryosoki']]}
    if m == 10 and d == 1:
        return {"name": "ROFUJI (Hearth Closure)", "step": "evening_purification", "action": "When turning on the heating or securing the house, take a moment of mindfulness regarding fire safety.", "liturgy": ["Silent Intention: " + ANNUAL_LITURGY['rofuji']]}
    if m == 10 and d == 5:
        return {"name": "DARUMAKI (Bodhidharma Memorial)", "step": "morning_service", "action": "Offer a fresh cup of tea to the altar.", "liturgy": ["Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'], "Daruma Eko: " + ANNUAL_LITURGY['darumaki']]}

    # Early Winter
    if m == 12 and d == 8:
        return {"name": "ROHATSU & JODO-E (Buddha's Awakening)", "step": "night_zazen", "action": "Cancel evening leisure. Extend Zazen until midnight. Place a candle and tea on the altar.", "liturgy": ["Surangama Heart Mantra (7x): " + CHANTS['surangama_heart_mantra'], "Jodo-e Eko: " + ANNUAL_LITURGY['jodo_e']]}
    if m == 12 and (d == 9 or d == 10):
        return {"name": "DANPI HO-ON SESSHIN (Memorial for Huike)", "step": "morning_service", "action": "Offer a fresh cup of tea. Reflect on the sacrifices made by the ancestors.", "liturgy": ["Great Compassion Dharani: " + CHANTS['daihishin_darani'], "Eka Eko: " + ANNUAL_LITURGY['eka_eko']]}
    if m == 12 and d == 31:
        return {"name": "O-MISOKA (Year-End Purification)", "step": "night_zazen", "action": "Clean altar. Place food pinch on altar. Strike bell 108 times at end of Zazen.", "liturgy": ["Great Compassion Dharani: " + CHANTS['daihishin_darani'], "Year-End Eko: " + ANNUAL_LITURGY['year_end']]}

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
    
    # Waking
    morning_sections.append(("Waking & Morning Purification", [VERSES['waking'], VERSES['toothbrush'], VERSES['brushing'], VERSES['rinsing'], VERSES['face']]))
    summary["morning"] = "purification · "

    # Morning Service
    m_actions = []
    if annual and annual['step'] == "morning_service":
        m_actions.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        m_actions.append(f"ACTION: {annual['action']}")
        m_actions.extend(annual['liturgy'])
        morning_sections.append(("Dawn Zazen & Annual Morning Service", m_actions))
        summary["morning"] += "zazen · annual service"
    elif is_weekend:
        m_actions = ["Extended 45-minute Dawn Zazen", "WEEKLY HOME SUTRA CHANTING SERVICE:"]
        if is_maintenance_day: m_actions.append("Shaving Verse: " + VERSES['tonsure'])
        m_actions.extend(get_weekly_home_service())
        morning_sections.append(("Dawn Zazen & Weekly Home Service", m_actions))
        summary["morning"] += "45m zazen · home service"
    elif is_maintenance_day:
        morning_sections.append(("Morning Service: Cancelled — Maintenance Day", ["Focus on physical maintenance, grooming, and household care.", "Shaving Verse: " + VERSES['tonsure']]))
        summary["morning"] += "maintenance & self-care"
    else:
        morning_dedication = DEDICATIONS['morning']
        if day_val in [1, 15]: morning_dedication = DEDICATIONS['earth']
        if day_val in [2, 16]: morning_dedication = DEDICATIONS['local']
        morning_sections.append(("Dawn Zazen & Morning Service", ["Dawn Zazen", "Verse of the Kesa (3x): " + VERSES['kesa'], "Heart Sutra Mantra (Chant 7x): " + CHANTS['heart_sutra_mantra'], "Dedication: " + morning_dedication, DEDICATIONS['closing']]))
        summary["morning"] += "zazen · morning service"

    # Breakfast
    b_actions = []
    if annual and annual['step'] == "breakfast":
        b_actions.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        b_actions.append(f"ACTION: {annual['action']}")
        b_actions.extend(annual['liturgy'])
    b_actions.extend(["Five Contemplations:"] + MEALS['five_contemplations'])
    if not is_weekend: b_actions.append(MEALS['purity_lotus'])
    morning_sections.append(("Breakfast", b_actions))

    # Showering
    morning_sections.append(("Showering & Preparation", [VERSES['bathing']]))
    blocks.append(("Morning", morning_sections))

    # --- MIDDAY BLOCK ---
    midday_sections = []
    if is_weekend:
        midday_sections.append(("Household Work & Family Time", ["Engage in chores, errands, or rest as temple work."]))
        midday_sections.append(("Lunch", ["Five Contemplations Only:"] + MEALS['five_contemplations']))
        summary["midday"] = "household work · family time"
    else:
        midday_sections.append(("Commute & Morning Work", [VERSES['road_start'], VERSES['right_livelihood']]))
        midday_sections.append(("Midday Pause", ["Midday Zazen", "Victor's Heart Mantra (Chant 7x): " + CHANTS['victor_heart_mantra'], "Dedication: " + DEDICATIONS['midday'], "Five Contemplations:"] + MEALS['five_contemplations'] + [MEALS['purity_lotus']]))
        summary["midday"] = "work practice · midday zazen"
    blocks.append(("Midday", midday_sections))

    # --- AFTERNOON & EVENING BLOCK ---
    evening_sections = []
    if not is_weekend:
        evening_sections.append(("Afternoon Work Practice & Return Home", []))
    
    # Evening Service
    e_actions = []
    if annual and annual['step'] == "evening_service":
        e_actions.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        e_actions.append(f"ACTION: {annual['action']}")
        e_actions.extend(annual['liturgy'])
        evening_sections.append(("Late Afternoon Zazen & Annual Evening Service", e_actions))
        summary["evening"] = "zazen · annual service · "
    elif day_of_week == "Friday":
        evening_sections.append(("Evening Transition: Service Cancelled", ["Transition from secular work to spiritual refuge."]))
        summary["evening"] = "secular transition · "
    elif is_weekend:
        evening_sections.append(("Afternoon & Evening: Service Cancelled", ["Undivided family time and rest."]))
        summary["evening"] = "family time · "
    else:
        readings = {1: "Zazen Yojinki", 5: "Shushogi Ch 1", 10: "Shushogi Ch 2", 15: "Shushogi Ch 3", 20: "Shushogi Ch 4", 25: "Shushogi Ch 5"}
        if day_val in readings: e_actions.append("READING (Lay Exhortation): " + readings[day_val])
        e_actions.extend(["Late Afternoon Zazen", "Surangama Heart Mantra (Chant 7x): " + CHANTS['surangama_heart_mantra']])
        evening_dedication = DEDICATIONS['evening']
        if day_val in [3, 13, 23]: evening_dedication = DEDICATIONS['peace']
        if day_val == 28: evening_dedication = DEDICATIONS['memorial']
        e_actions.append("Dedication: " + evening_dedication)
        if day_val in [8, 18, 28]: e_actions.append("Admonition of Impermanence: " + CHANTS['impermanence'])
        if day_val == 18:
            e_actions.append("Ten-Line Kannon Sutra (Enmei Jukku Kannon Gyō): " + CHANTS['jukku_kannon_gyo'])
            e_actions.append("Kannon Dedication (Keizan): " + DEDICATIONS['kannon_dedication'])
        has_ten_names = day_val in [3, 13, 23, 8, 18, 28]
        if has_ten_names: e_actions.append("Ten Buddha Names: " + CHANTS['ten_names'])
        if not has_ten_names: e_actions.append(DEDICATIONS['closing'])
        if day_val == 15 or is_last_day: e_actions.extend(get_uposatha_ceremony())
        evening_sections.append(("Late Afternoon Zazen & Evening Service", e_actions))
        summary["evening"] = "zazen · evening service · "

    # Dinner
    if day_of_week == "Friday":
        evening_sections.append(("Communal Dinner", ["Relaxed, celebratory family dinner or social time."]))
        summary["evening"] += "communal dinner"
    else:
        evening_sections.append(("Dinner & Free Time", []))
        summary["evening"] += "dinner & rest"
    blocks.append(("Afternoon & Evening", evening_sections))

    # --- NIGHT BLOCK ---
    night_sections = []
    
    # Purification
    p_actions = [VERSES['toothbrush'], VERSES['brushing'], VERSES['flossing'], VERSES['rinsing'], VERSES['face']]
    if annual and annual['step'] == "evening_purification":
        p_actions.insert(0, f"ANNUAL OBSERVANCE: {annual['name']}")
        p_actions.insert(1, f"ACTION: {annual['action']}")
        p_actions.insert(2, f"LITURGY: {annual['liturgy'][0]}")
    night_sections.append(("Evening Purification", p_actions))
    summary["night"] = "purification · "

    # Night Zazen
    n_actions = []
    if annual and annual['step'] == "night_zazen":
        n_actions.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        n_actions.append(f"ACTION: {annual['action']}")
        n_actions.extend(annual['liturgy'])
        n_actions.append("Going to Sleep: " + VERSES['sleep'])
        night_sections.append(("Night Zazen & Annual Observance", n_actions))
        summary["night"] += "zazen · annual observance · sleep"
    elif day_of_week == "Friday":
        n_actions = ["Extended 45-minute Zazen", "Four Great Vows:"] + CHANTS['vows']
        n_actions.append("HOSAN (Calling-Off the Week): Ring bell 3 times. Perform a single bow and say: " + WEEKEND_RITUALS['hosan_greeting'])
        n_actions.append("Going to Sleep: " + VERSES['sleep'])
        night_sections.append(("Night Zazen (Hosan)", n_actions))
        summary["night"] += "45m zazen · hosan · sleep"
    elif day_of_week == "Sunday":
        n_actions = ["Extended 45-minute Night Zazen to ground for Monday morning", "Four Great Vows:"] + CHANTS['vows']
        n_actions.append("KAISEI (Retreat-Ending Reset): Strike the final 'Settling Bell'. Recite: " + WEEKEND_RITUALS['kaisei_salutation'])
        n_actions.append("Going to Sleep: " + VERSES['sleep'])
        night_sections.append(("Night Zazen (Kaisei)", n_actions))
        summary["night"] += "45m zazen · kaisei · sleep"
    else:
        zazen_time = "45-minute Zazen" if day_of_week == "Saturday" else "Night Zazen"
        night_sections.append(("Night Zazen & Sleep", [zazen_time, "Four Great Vows:"] + CHANTS['vows'] + ["Going to Sleep: " + VERSES['sleep']]))
        summary["night"] += f"{zazen_time.lower()} · vows · sleep"
    blocks.append(("Night", night_sections))

    return {
        "summary": summary,
        "legend": get_ritual_legend(),
        "blocks": blocks
    }
