"""
scheduler.py
============
A dedicated module for calculating Zen liturgical schedules.
FIX: Robust anchor detection (handles hyphens and underscores).
"""

from datetime import datetime
import calendar
import pytz

def get_meta(timezone_str: str = "America/New_York") -> dict:
    """Calculates temporal milestones for liturgical logic."""
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]
    is_last_day = (now.day == last_day_of_month)
    is_shaving_day = (now.day % 10 == 4) or (now.day % 10 == 9)
    
    return {
        "day_of_week": now.strftime("%A"),
        "dom": now.day,
        "month": now.month,
        "year": now.year,
        "is_last_day": is_last_day,
        "is_shaving_day": is_shaving_day,
        "date_str": now.strftime("%B %d, %Y")
    }

def get_base_template_name(day_of_week: str) -> str:
    """Determines which YAML template to load."""
    if day_of_week in ["Saturday", "Sunday"]:
        return "weekend"
    elif day_of_week == "Friday":
        return "friday"
    else:
        return "weekday"

def transform_schedule(section_name: str, activity_ids: list, meta: dict) -> list:
    """
    Applies liturgical rules. 
    Updated with robust anchor matching for Study Days and Memorials.
    """
    dom = meta["dom"]
    month = meta["month"]
    day_of_week = meta["day_of_week"]
    is_last_day = meta["is_last_day"]
    is_shaving_day = meta.get("is_shaving_day", False)
    
    new_ids = activity_ids.copy()

    # Helper to find index of any anchor in a list of possibilities
    def get_anchor_idx(possibilities):
        for p in possibilities:
            if p in new_ids:
                return new_ids.index(p)
        return None

    # --- RULE I: SHAVING & MAINTENANCE (4/9) ---
    if is_shaving_day and section_name == "EARLY HOURS":
        idx = get_anchor_idx(["face_washing_morning", "face-washing-morning"])
        if idx is not None:
            new_ids.insert(idx + 1, "shaving_verse")
            new_ids.insert(idx + 2, "shower_and_dress")
        if "dawn_zazen" in new_ids: new_ids.remove("dawn_zazen")
        new_ids = [act for act in new_ids if "morning_chant" not in act]

    # --- MORNING RULES (Memorial Chants) ---
    if dom in [1, 15] and "morning_chant" in new_ids:
        new_ids[new_ids.index("morning_chant")] = "morning_chant_health_of_the_earth"
    if dom in [2, 16] and "morning_chant" in new_ids:
        new_ids[new_ids.index("morning_chant")] = "morning_chant_local_spirits"

    # --- EVENING RULES (Memorial Additions) ---
    idx = get_anchor_idx(["late_afternoon_zazen", "late-afternoon_zazen"])
    if idx is not None:
        if dom in [3, 13, 23]: new_ids.insert(idx, "prayers_for_supporters")
        if (dom == 29) or (month == 2 and is_last_day): new_ids.insert(idx, "two_ancestors_memorial")
        if dom in [8, 18, 28]: new_ids.insert(idx, "admonition_of_impermanence")

    # --- RULE J: STUDY & READING (1, 5, 10, 15, 20, 25) ---
    reading_days = {1: "sutra_reading_01", 5: "sutra_reading_05", 10: "sutra_reading_10", 
                    15: "sutra_reading_15", 20: "sutra_reading_20", 25: "sutra_reading_25"}
    
    if dom in reading_days:
        reading_id = reading_days[dom]
        
        # WEEKDAY: Before Late Afternoon Zazen
        if day_of_week in ["Monday", "Tuesday", "Wednesday", "Thursday"]:
            idx = get_anchor_idx(["late_afternoon_zazen", "late-afternoon_zazen"])
            if idx is not None:
                new_ids.insert(idx, reading_id)
        
        # FRIDAY: Before Evening Chant
        elif day_of_week == "Friday":
            idx = get_anchor_idx(["evening_chant", "evening-chant"])
            if idx is not None:
                new_ids.insert(idx, reading_id)
        
        # WEEKEND: After Special Observances
        else:
            idx = get_anchor_idx(["special_observances", "special-observances"])
            if idx is not None:
                new_ids.insert(idx + 1, reading_id)
            
    return new_ids
