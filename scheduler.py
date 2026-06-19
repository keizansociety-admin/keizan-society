"""
scheduler.py
============
A dedicated module for calculating Zen liturgical schedules.
Fixed: Corrected list syntax and aligned dates with Rule D-H.
"""

from datetime import datetime
import calendar
import pytz

def get_meta(timezone_str: str = "America/New_York") -> dict:
    """Calculates temporal milestones (shaving days, month ends)."""
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    
    # Calculate if today is the last day of the current month
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]
    is_last_day = (now.day == last_day_of_month)
    
    # Rule: Shaving Days (Maintenance Days): Days ending in 4 or 9
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
    """
    STRUCTURAL RULES
    Rule A: Weekday/Weekend
    Rule B: Friday
    """
    if day_of_week in ["Saturday", "Sunday"]:
        return "weekend"
    elif day_of_week == "Friday":
        return "friday"
    else:
        return "weekday"
    
def transform_schedule(section_name: str, activity_ids: list, meta: dict) -> list:
    """
    Applies liturgical rules including Friday template logic and 
    Shaving/Maintenance Day (4/9) modifications.
    """
    dom = meta["dom"]
    month = meta["month"]
    is_last_day = meta["is_last_day"]
    is_shaving_day = meta.get("is_shaving_day", False)
    
    new_ids = activity_ids.copy()

    # --- RULE I: SHAVING & MAINTENANCE (Days ending in 4 or 9) ---
    if is_shaving_day and section_name == "EARLY HOURS":
        # 1. INSERT shaving_verse and shower_and_dress AFTER face_washing_morning
        if "face_washing_morning" in new_ids:
            idx = new_ids.index("face_washing_morning")
            # We insert in reverse order or increment the index to maintain sequence
            new_ids.insert(idx + 1, "shaving_verse")
            new_ids.insert(idx + 2, "shower_and_dress")
        
        # 2. DELETE dawn_zazen
        if "dawn_zazen" in new_ids:
            new_ids.remove("dawn_zazen")
            
        # 3. DELETE morning_chant (and any variants)
        chant_variants = [
            "morning_chant", 
            "morning_chant_health_of_the_earth", 
            "morning_chant_local_spirits"
        ]
        new_ids = [act for act in new_ids if act not in chant_variants]

    # --- MORNING RULES (D & E) ---
    # (Only apply if not already removed by Shaving Day logic)
    if dom in [1, 15] and "morning_chant" in new_ids:
        new_ids[new_ids.index("morning_chant")] = "morning_chant_health_of_the_earth"
    if dom in [2, 16] and "morning_chant" in new_ids:
        new_ids[new_ids.index("morning_chant")] = "morning_chant_local_spirits"

    # --- EVENING RULES (F, G, & H) ---
    if "late_afternoon_zazen" in new_ids:
        idx = new_ids.index("late_afternoon_zazen")
        if dom in [3, 13, 23]:
            new_ids.insert(idx, "prayers_for_supporters")
        if (dom == 29) or (month == 2 and is_last_day):
            new_ids.insert(idx, "two_ancestors_memorial")
        if dom in [8, 18, 28]:
            new_ids.insert(idx, "admonition_of_impermanence")
            
    return new_ids
