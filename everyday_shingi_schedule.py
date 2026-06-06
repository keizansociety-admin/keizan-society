"""
EVERYDAY_SHINGI_SCHEDULE.PY
The logic engine for the Keizan Society.
"""

import calendar
from everyday_shingi_liturgy import VERSES, MEALS, CHANTS, DEDICATIONS, ANNUAL_LITURGY, WEEKEND_RITUALS

def get_uposatha_ceremony():
    """Assembles the bi-monthly precepts ceremony from the library."""
    return [
        "\n--- UPOSATHA PRECEPTS CEREMONY ---",
        "1. Repentance Verse (3x in Gassho): " + CHANTS['repentance'],
        "Four Great Vows (3x):"
    ] + CHANTS['vows'] + [
        "3. Sutra-Opening Verse: " + CHANTS['kaikyo_ge'],
        "4. Three Refuges: " + CHANTS['three_refuges_verse'],
        "5. Threefold Pure Precepts:"
    ] + CHANTS['pure_precepts'] + [
        "6. Ten Major Precepts:"
    ] + CHANTS['major_precepts'] + [
        "7. Verse of Purity: " + MEALS['purity_lotus'],
        "8. Three Refuges Prayer (Prostrate after each): " + CHANTS['three_refuges_prayer'],
        "9. Closing: " + DEDICATIONS['closing'] + " (3 Prostrations)"
    ]

def get_weekly_home_service():
    """Assembles the weekend morning service from the library."""
    return [
        "PREPARATION: Light candle and 3 sticks of incense. Regulate breath.",
        "◎ ◎ Perform gasshō and three full prostrations.",
        "1. Sutra-Opening Verse (Kaikyō ge): " + CHANTS['kaikyo_ge'],
        "2. Repentance Verse (Sange mon): " + CHANTS['repentance'],
        "3. Three Refuges Prayer (Sanki raimon): " + CHANTS['three_refuges_prayer'],
        "4. Three Refuges Verse (Sankie mon): " + CHANTS['three_refuges_verse'],
        "5. Maka han-nya hara mit-ta shin gyo (Sino-Japanese):",
        "   " + CHANTS['heart_sutra_sino'],
        "6. Dedication (Repaying Blessings): " + DEDICATIONS['weekly_repaying'],
        DEDICATIONS['universal_closing'],
        "7. Daihishin darani (Great Compassion Dharani):",
        "   " + CHANTS['daihishin_darani'],
        "8. Dedication (For All Spirits): " + DEDICATIONS['weekly_spirits'],
        DEDICATIONS['universal_closing'],
        "● ● ● [Make three prostrations]",
        "9. SERVICE FOR SPIRIT OF THE KITCHEN (Move to Kitchen):",
        "   - Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'],
        "   - Dedication for Stove God (Daikokuten): " + DEDICATIONS['stove_god'],
        DEDICATIONS['final_closing'],
        "FINAL ACTION: ◎ [Make three deep standing bows]"
    ]

def get_annual_event(target_date):
    """Returns annual event data if the date matches an observance."""
    m, d = target_date.month, target_date.day
    last_day = calendar.monthrange(target_date.year, target_date.month)[1]

    # Winter
    if m == 1 and d == 26:
        return {"name": "KOSO GOTAN-E (Dogen Zenji's Birthday)", "step": 2, "action": "Before sitting Zazen, brew a fresh cup of tea and place it on the home altar.", "liturgy": ["Heart Sutra Mantra (7x): " + CHANTS['heart_sutra_mantra'], "Gotan-e Eko: " + ANNUAL_LITURGY['gotan_e']]}
    if m == 2 and d == 15:
        return {"name": "NEHAN-E (Nirvana Day)", "step": 9, "action": "Dim the lights in the house. Light a single candle on the altar to represent the passing of the light.", "liturgy": ["Surangama Heart Mantra (7x): " + CHANTS['surangama_heart_mantra'], "Nehan-e Eko: " + ANNUAL_LITURGY['nehan_e']]}
    
    # Spring
    if m == 3 and d == 1:
        return {"name": "ROBIRAKI (Hearth Opening)", "step": 4, "action": "When turning on the stove or thermostat, take a moment of continuous mindfulness.", "liturgy": ["Silent Intention: " + ANNUAL_LITURGY['robiraki']]}
    if m == 3 and d == 20:
        return {"name": "HIGAN-E (Spring Equinox)", "step": 9, "action": "Place a photograph of deceased family members on the altar. Offer water or rice.", "liturgy": ["Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'], "Ancestral Eko: " + ANNUAL_LITURGY['ancestral_higan']]}
    if m == 4 and d == 8:
        return {"name": "HANA-MATSURI (Buddha's Birthday)", "step": 2, "action": "Place a single fresh flower (or a bowl of water with a flower) on the altar.", "liturgy": ["Morning Chant (Heart Sutra Mantra 7x)", "Birth Eko: " + ANNUAL_LITURGY['hana_matsuri']]}
    
    # Summer
    if (m == 1 or m == 5 or m == 9) and d == 16:
        return {"name": "ZENGETSU KITO-E (Month of Good Cultivation)", "step": 9, "action": "Ensure the altar is clean. Sit Zazen with a specific intention toward ethical renewal.", "liturgy": ["Ten Buddha Names: " + CHANTS['ten_names'], "Zengetsu Eko: " + ANNUAL_LITURGY['zengetsu']]}
    if m == 6 and d == 18:
        return {"name": "WOMEN'S ANCESTORS COMMEMORATION", "step": 9, "action": "Light a special candle on the home altar to honor the maternal lineage and female ancestors.", "liturgy": ["Ten-Line Kannon Sutra: " + CHANTS['jukku_kannon_gyo'], "Women's Lineage Eko: " + ANNUAL_LITURGY['women_ancestors']]}
    if (m == 7 or m == 8) and d == 15:
        return {"name": "O-BON & SEJIKI-E (Festival of Remembrance)", "step": 9, "action": "Place a small bowl of water and a pinch of dinner (saba) on the altar or outside.", "liturgy": ["Great Compassion Dharani: " + CHANTS['daihishin_darani'], "Sejiki Eko: " + ANNUAL_LITURGY['sejiki']]}
    
    # Autumn
    if m == 9 and d == 21:
        return {"name": "HIGAN-E (Autumn Equinox)", "step": 9, "action": "Place a photograph of deceased family members on the altar. Offer water or rice.", "liturgy": ["Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'], "Ancestral Eko: " + ANNUAL_LITURGY['ancestral_higan']]}
    if m == 9 and d == 29:
        return {"name": "RYOSOKI (Two Ancestors Memorial)", "step": 2, "action": "Brew a fresh cup of tea and place a small sweet or piece of fruit on the altar.", "liturgy": ["Surangama Heart Mantra (7x): " + CHANTS['surangama_heart_mantra'], "Ryosoki Eko: " + ANNUAL_LITURGY['ryosoki']]}
    if m == 10 and d == 1:
        return {"name": "ROFUJI (Hearth Closure)", "step": 11, "action": "When turning on the heating or securing the house, take a moment of mindfulness regarding fire safety.", "liturgy": ["Silent Intention: " + ANNUAL_LITURGY['rofuji']]}
    if m == 10 and d == 5:
        return {"name": "DARUMAKI (Bodhidharma Memorial)", "step": 2, "action": "Offer a fresh cup of tea to the altar.", "liturgy": ["Heart of Great Perfect Wisdom Sutra (English): " + CHANTS['heart_sutra_english'], "Daruma Eko: " + ANNUAL_LITURGY['darumaki']]}
    if m == 10 and 10 <= d <= 16:
        return {"name": "YUIMA-E (Vimalakirti Assembly)", "step": 9, "action": "Period of specialized study. Replace standard readings with the Vimalakirti Sutra.", "liturgy": ["Reading: Vimalakirti Nirdesa Sutra (5 Minutes)", "Standard Evening Eko"]}

    # Early Winter
    if m == 12 and d == 8:
        return {"name": "ROHATSU & JODO-E (Buddha's Awakening)", "step": 12, "action": "Cancel evening leisure. Extend Zazen until midnight. Place a candle and tea on the altar.", "liturgy": ["Surangama Heart Mantra (7x): " + CHANTS['surangama_heart_mantra'], "Jodo-e Eko: " + ANNUAL_LITURGY['jodo_e']]}
    if m == 12 and (d == 9 or d == 10):
        return {"name": "DANPI HO-ON SESSHIN (Memorial for Huike)", "step": 2, "action": "Offer a fresh cup of tea. Reflect on the sacrifices made by the ancestors.", "liturgy": ["Great Compassion Dharani: " + CHANTS['daihishin_darani'], "Eka Eko: " + ANNUAL_LITURGY['eka_eko']]}
    if m == 12 and d == 31:
        return {"name": "O-MISOKA (Year-End Purification)", "step": 12, "action": "Clean altar (Step 11). Place food pinch on altar. Strike bell 108 times at end of Zazen.", "liturgy": ["Great Compassion Dharani: " + CHANTS['daihishin_darani'], "Year-End Eko: " + ANNUAL_LITURGY['year_end']]}

    return None

def generate_daily_schedule(target_date):
    """Determines the chronological flow of the day based on the date."""
    day_of_week = target_date.strftime('%A')
    day_val = target_date.day
    is_last_day = day_val == calendar.monthrange(target_date.year, target_date.month)[1]
    is_maintenance_day = day_val % 10 in [4, 9]
    is_weekend = day_of_week in ["Saturday", "Sunday"]
    annual = get_annual_event(target_date)
    
    schedule = []

    # Step 1: Waking
    schedule.append(("Waking & Morning Purification", [VERSES['waking'], VERSES['toothbrush'], VERSES['brushing'], VERSES['rinsing'], VERSES['face']]))
    
    # Step 2: Morning Service
    m_items = []
    if annual and annual['step'] == 2:
        m_items.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        m_items.append(f"ACTION: {annual['action']}")
        m_items.extend(annual['liturgy'])
        schedule.append(("Dawn Zazen & Annual Morning Service", m_items))
    elif is_weekend:
        m_items = ["Extended 45-minute Dawn Zazen", "WEEKLY HOME SUTRA CHANTING SERVICE:"]
        if is_maintenance_day: m_items.append("Shaving Verse: " + VERSES['tonsure'])
        m_items.extend(get_weekly_home_service())
        schedule.append(("Dawn Zazen & Weekly Home Service", m_items))
    elif is_maintenance_day:
        schedule.append(("Maintenance & Self-Care Day", ["[DAWN ZAZEN & SERVICE CANCELLED]", "Focus on physical maintenance, grooming, and household care.", "Shaving Verse: " + VERSES['tonsure']]))
    else:
        morning_dedication = DEDICATIONS['morning']
        if day_val in [1, 15]: morning_dedication = DEDICATIONS['earth']
        if day_val in [2, 16]: morning_dedication = DEDICATIONS['local']
        schedule.append(("Dawn Zazen & Morning Service", ["Dawn Zazen", "Verse of the Kesa (3x): " + VERSES['kesa'], "Heart Sutra Mantra (Chant 7x): " + CHANTS['heart_sutra_mantra'], "Dedication: " + morning_dedication, DEDICATIONS['closing']]))

    # Step 3: Bathroom
    schedule.append(("Bathroom", [VERSES['toilet'], VERSES['hands']]))

    # Step 4: Breakfast
    b_items = []
    if annual and annual['step'] == 4:
        b_items.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        b_items.append(f"ACTION: {annual['action']}")
        b_items.extend(annual['liturgy'])
    b_items.extend(["Five Contemplations:"] + MEALS['five_contemplations'])
    if not is_weekend: b_items.append(MEALS['purity_lotus'])
    schedule.append(("Breakfast", b_items))

    # Step 5: Showering
    schedule.append(("Showering & Getting Ready", [VERSES['bathing']]))

    # Step 6: Work
    if is_weekend:
        schedule.append(("Household Work & Family Time", ["Engage in chores, errands, or rest as temple work."]))
    else:
        schedule.append(("Commute & Morning Work", [VERSES['road_start'], VERSES['right_livelihood']]))

    # Step 7: Midday
    if is_weekend:
        schedule.append(("Lunch", ["[MIDDAY SERVICE CANCELLED] - Family Time", "Five Contemplations Only:"] + MEALS['five_contemplations']))
    else:
        schedule.append(("Midday Pause", ["Midday Zazen", "Victor's Heart Mantra (Chant 7x): " + CHANTS['victor_heart_mantra'], "Dedication: " + DEDICATIONS['midday'], "Five Contemplations:"] + MEALS['five_contemplations'] + [MEALS['purity_lotus']]))

    # Step 8: Afternoon
    if not is_weekend:
        schedule.append(("Afternoon Work Practice & Return Home", []))

    # Step 9: Evening Service
    e_items = []
    if annual and annual['step'] == 9:
        e_items.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        e_items.append(f"ACTION: {annual['action']}")
        e_items.extend(annual['liturgy'])
        schedule.append(("Late Afternoon Zazen & Annual Evening Service", e_items))
    elif day_of_week == "Friday":
        schedule.append(("Evening Transition", ["[LATE AFTERNOON ZAZEN & SERVICE CANCELLED]", "Transition from secular work to spiritual refuge."]))
    elif is_weekend:
        schedule.append(("Afternoon & Evening", ["[LATE AFTERNOON SERVICE CANCELLED] - Undivided family time and rest."]))
    else:
        readings = {1: "Zazen Yojinki", 5: "Shushogi Ch 1", 10: "Shushogi Ch 2", 15: "Shushogi Ch 3", 20: "Shushogi Ch 4", 25: "Shushogi Ch 5"}
        if day_val in readings: e_items.append("READING (Lay Exhortation): " + readings[day_val])
        e_items.extend(["Late Afternoon Zazen", "Surangama Heart Mantra (Chant 7x): " + CHANTS['surangama_heart_mantra']])
        evening_dedication = DEDICATIONS['evening']
        if day_val in [3, 13, 23]: evening_dedication = DEDICATIONS['peace']
        if day_val == 28: evening_dedication = DEDICATIONS['memorial']
        e_items.append("Dedication: " + evening_dedication)
        if day_val in [8, 18, 28]: e_items.append("Admonition of Impermanence: " + CHANTS['impermanence'])
        if day_val == 18:
            e_items.append("Ten-Line Kannon Sutra (Enmei Jukku Kannon Gyō): " + CHANTS['jukku_kannon_gyo'])
            e_items.append("Kannon Dedication (Keizan): " + DEDICATIONS['kannon_dedication'])
        has_ten_names = day_val in [3, 13, 23, 8, 18, 28]
        if has_ten_names: e_items.append("Ten Buddha Names: " + CHANTS['ten_names'])
        if not has_ten_names: e_items.append(DEDICATIONS['closing'])
        if day_val == 15 or is_last_day: e_items.extend(get_uposatha_ceremony())
        schedule.append(("Late Afternoon Zazen & Evening Service", e_items))

    # Step 10: Dinner
    if day_of_week == "Friday":
        schedule.append(("Communal Time", ["Relaxed, celebratory family dinner or social time to mark the end of the week."]))
    elif not is_weekend:
        schedule.append(("Dinner & Free Time", []))

    # Step 11: Evening Purification
    p_items = [VERSES['toothbrush'], VERSES['brushing'], VERSES['flossing'], VERSES['rinsing'], VERSES['face']]
    if annual and annual['step'] == 11:
        p_items.insert(0, f"ANNUAL OBSERVANCE: {annual['name']}")
        p_items.insert(1, f"ACTION: {annual['action']}")
        p_items.insert(2, f"LITURGY: {annual['liturgy'][0]}")
    schedule.append(("Evening Purification", p_items))

    # Step 12: Night Zazen
    n_items = []
    if annual and annual['step'] == 12:
        n_items.append(f"ANNUAL OBSERVANCE: {annual['name']}")
        n_items.append(f"ACTION: {annual['action']}")
        n_items.extend(annual['liturgy'])
        n_items.append("Going to Sleep: " + VERSES['sleep'])
        schedule.append(("Night Zazen & Annual Observance", n_items))
    elif day_of_week == "Friday":
        n_items = ["Extended 45-minute Zazen", "Four Great Vows:"] + CHANTS['vows']
        n_items.append("HOSAN (Calling-Off the Week): Ring bell 3 times. Perform a single bow and say: " + WEEKEND_RITUALS['hosan_greeting'])
        n_items.append("Going to Sleep: " + VERSES['sleep'])
        schedule.append(("Night Zazen (Hosan)", n_items))
    elif day_of_week == "Sunday":
        n_items = ["Extended 45-minute Night Zazen to ground for Monday morning", "Four Great Vows:"] + CHANTS['vows']
        n_items.append("KAISEI (Retreat-Ending Reset): Strike the final 'Settling Bell'. Recite: " + WEEKEND_RITUALS['kaisei_salutation'])
        n_items.append("Going to Sleep: " + VERSES['sleep'])
        schedule.append(("Night Zazen (Kaisei)", n_items))
    else:
        zazen_time = "45-minute Zazen" if day_of_week == "Saturday" else "Night Zazen"
        schedule.append(("Night Zazen & Sleep", [zazen_time, "Four Great Vows:"] + CHANTS['vows'] + ["Going to Sleep: " + VERSES['sleep']]))

    return schedule