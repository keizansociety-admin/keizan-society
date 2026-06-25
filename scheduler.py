"""
scheduler.py
============
A dedicated module for calculating Zen liturgical schedules.
UX FIX: "Fuzzy Matching" allows hyphens or underscores to work interchangeably.
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
    Uses normalization so 'late-afternoon' matches 'late_afternoon'.
    """
    dom = meta["dom"]
    month = meta["month"]
    day_of_week = meta["day_of_week"]
    is_last_day = meta["is_last_day"]
    is_shaving_day = meta.get("is_shaving_day", False)
    
    new_ids = activity_ids.copy()

    def normalize(s):
        """Standardizes strings: 'Late-Afternoon ' -> 'late_afternoon'"""
        return str(s).strip().lower().replace("-", "_")

    def find_anchor_index(target_id):
        """Finds the index of an ID regardless of hyphens/underscores."""
        norm_target = normalize(target_id)
        for i, act_id in enumerate(new_ids):
            if normalize(act_id) == norm_target:
                return i
        return None

    # --- RULE I: SHAVING & MAINTENANCE (4/9) ---
    if is_shaving_day and section_name == "EARLY HOURS":
        idx = find_anchor_index("face_washing_morning")
        if idx is not None:
            new_ids.insert(idx + 1, "shaving_verse")
            new_ids.insert(idx + 2, "shower_and_dress")
        
        z_idx = find_anchor_index("dawn_zazen")
        if z_idx is not None: new_ids.pop(z_idx)
        new_ids = [act for act in new_ids if "morning_chant" not in normalize(act)]

    # --- MORNING RULES (Memorial Chants) ---
    m_idx = find_anchor_index("morning_chant")
    if m_idx is not None:
        if dom in [1, 15]: new_ids[m_idx] = "morning_chant_health_of_the_earth"
        if dom in [2, 16]: new_ids[m_idx] = "morning_chant_local_spirits"

    # --- EVENING RULES (Memorial Additions) ---
    e_idx = find_anchor_index("late_afternoon_zazen")
    if e_idx is not None:
        if dom in [3, 13, 23]: new_ids.insert(e_idx, "prayers_for_supporters")
        if (dom == 29) or (month == 2 and is_last_day): new_ids.insert(e_idx, "two_ancestors_memorial")
        if dom in [8, 18, 28]: new_ids.insert(e_idx, "admonition_of_impermanence")

    # --- RULE J: STUDY & READING (1, 5, 10, 15, 20, 25) ---
    reading_days = {1: "sutra_reading_01", 5: "sutra_reading_05", 10: "sutra_reading_10", 
                    15: "sutra_reading_15", 20: "sutra_reading_20", 25: "sutra_reading_25"}
    
    if dom in reading_days:
        reading_id = reading_days[dom]
        
        if day_of_week in ["Monday", "Tuesday", "Wednesday", "Thursday"]:
            idx = find_anchor_index("late_afternoon_zazen")
            if idx is not None: new_ids.insert(idx, reading_id)
        
        elif day_of_week == "Friday":
            idx = find_anchor_index("evening_chant")
            if idx is not None: new_ids.insert(idx, reading_id)
        
        else: # Weekend
            idx = find_anchor_index("special_observances")
            if idx is not None: new_ids.insert(idx + 1, reading_id)
            
    return new_ids
