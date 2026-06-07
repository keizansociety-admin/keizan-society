"""
EVERYDAY_SHINGI_SCHEDULE.PY
The logic engine for the Keizan Society.

REVISION HISTORY:
    2026-06-06: Initial creation.
    2026-06-06: BUGFIX: Corrected Night Block nesting and section order.
                Purification is now a distinct section preceding Zazen.
"""

import calendar
from everyday_shingi_liturgy import VERSES, MEALS, CHANTS, DEDICATIONS, ANNUAL_LITURGY, WEEKEND_RITUALS

def get_ritual_legend():
    return [("◎", "Strike large bowl-bell"), ("●", "Strike small bowl-bell"), ("▲", "Muffle hand-bell")]

def get_uposatha_ceremony():
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
        MEALS['purity_lotus'],
        {"type": "instruction", "content": "Three Refuges Prayer (Prostrate after each)"},
        CHANTS['three_refuges_prayer'],
        {"type": "ritual", "content": "Closing: 3 Prostrations"},
        DEDICATIONS['final_closing']
    ]

def get_weekly_home_service():
    return [
        {"type": "instruction", "content": "PREPARATION: Light candle and incense."},
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
    m, d = target_date.month, target_date.day
    if m == 10 and d == 1:
        return {"name": "ROFUJI (Hearth Closure)", "step": "evening_purification", "action": "Mindfulness of fire safety.", "liturgy": [ANNUAL_LITURGY['rofuji']]}
    return None

def generate_daily_schedule(target_date):
    day_of_week = target_date.strftime('%A')
    day_val = target_date.day
    is_last_day = day_val == calendar.monthrange(target_date.year, target_date.month)[1]
    is_weekend = day_of_week in ["Saturday", "Sunday"]
    annual = get_annual_event(target_date)
    
    blocks = []

    # --- MORNING ---
    morning_sections = [
        ("Waking & Morning Purification", [VERSES['waking'], VERSES['toothbrush'], VERSES['brushing'], VERSES['rinsing'], VERSES['face']])
    ]
    
    m_actions = []
    if annual and annual['step'] == "morning_service":
        m_actions.append({"type": "annual", "content": f"ANNUAL OBSERVANCE: {annual['name']}"})
        m_actions.extend(annual['liturgy'])
        morning_sections.append(("Dawn Zazen & Annual Service", m_actions))
    elif is_weekend:
        m_actions = [{"type": "instruction", "content": "Extended 45-minute Dawn Zazen"}]
        m_actions.extend(get_weekly_home_service())
        morning_sections.append(("Dawn Zazen & Weekly Home Service", m_actions))
    else:
        morning_sections.append(("Dawn Zazen & Morning Service", [
            {"type": "instruction", "content": "Dawn Zazen"}, VERSES['kesa'], CHANTS['heart_sutra_sino'], DEDICATIONS['morning'], DEDICATIONS['final_closing']
        ]))
    
    morning_sections.append(("Breakfast", [MEALS['five_contemplations']]))
    morning_sections.append(("Showering & Preparation", [VERSES['bathing']]))
    blocks.append(("Morning", morning_sections))

    # --- MIDDAY ---
    midday_sections = []
    if is_weekend:
        midday_sections.append(("Household Work & Family Time", [{"type": "instruction", "content": "Engage in chores or rest as temple work."}]))
    else:
        midday_sections.append(("Commute & Work", [VERSES['road_start'], VERSES['right_livelihood']]))
        midday_sections.append(("Midday Pause", [DEDICATIONS['midday'], MEALS['five_contemplations']]))
    blocks.append(("Midday", midday_sections))

    # --- AFTERNOON & EVENING ---
    evening_sections = []
    if is_weekend or day_of_week == "Friday":
        evening_sections.append(("Evening Transition", [{"type": "instruction", "content": "Transition to rest and family time."}]))
    else:
        e_actions = [DEDICATIONS['evening']]
        if day_val == 15 or is_last_day: e_actions.extend(get_uposatha_ceremony())
        e_actions.append(DEDICATIONS['final_closing'])
        evening_sections.append(("Late Afternoon Zazen & Evening Service", e_actions))
    blocks.append(("Afternoon & Evening", evening_sections))

    # --- NIGHT (FIXED NESTING) ---
    night_sections = []
    
    # Section 1: Purification
    p_actions = []
    if annual and annual['step'] == "evening_purification":
        p_actions.append({"type": "annual", "content": f"ANNUAL OBSERVANCE: {annual['name']}"})
        p_actions.append({"type": "instruction", "content": annual['action']})
    p_actions.extend([VERSES['toothbrush'], VERSES['brushing'], VERSES['flossing'], VERSES['rinsing'], VERSES['face']])
    night_sections.append(("Evening Purification", p_actions))

    # Section 2: Zazen
    n_actions = [{"type": "instruction", "content": "Night Zazen"}]
    if day_of_week == "Friday": n_actions.append({"type": "ritual", "content": "HOSAN: " + WEEKEND_RITUALS['hosan_greeting']})
    elif day_of_week == "Sunday": n_actions.append({"type": "ritual", "content": "KAISEI: " + WEEKEND_RITUALS['kaisei_salutation']})
    n_actions.append(CHANTS['vows'])
    n_actions.append(VERSES['sleep'])
    night_sections.append(("Night Zazen & Sleep", n_actions))
    
    blocks.append(("Night", night_sections))

    summary = {"morning": "purification · zazen", "midday": "household work", "evening": "rest", "night": "purification · vows"}
    return {"summary": summary, "legend": get_ritual_legend(), "blocks": blocks}
