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
    """Calculates temporal milestones (rest days, month ends)."""
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    
    # Calculate if today is the last day of the current month
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]
    is_last_day = (now.day == last_day_of_month)
    
    # Rule: Shaving Days (Rest Days): Days ending in 4 or 9
    is_rest_day = (now.day % 10 == 4) or (now.day % 10 == 9)
    
    return {
        "day_of_week": now.strftime("%A"),
        "dom": now.day,
        "month": now.month,
        "year": now.year,
        "is_last_day": is_last_day,
        "is_rest_day": is_rest_day,
        "date_str": now.strftime("%B %d, %Y")
    }

def get_base_template_name(day_of_week: str) -> str:
    """Determines which base template to load based on the day of the week."""
    if day_of_week in ["Saturday", "Sunday"]:
        return "weekend"
    elif day_of_week == "Friday":
        return "friday"
    else:
        return "weekday"

def transform_schedule(section_name: str, activity_ids: list, meta: dict) -> list:
    """
    Applies liturgical substitution rules D through H.
    """
    dom = meta["dom"]
    month = meta["month"]
    is_last_day = meta["is_last_day"]
    
    # Work on a copy of the list to avoid modifying the original template
    new_ids = activity_ids.copy()
    
    # --- MORNING RULES (D & E) ---
    
    # Rule D: Prayers Sutra Reading (1 or 15)
    if dom in [1, 15]:
        if "morning_chant" in new_ids:
            idx = new_ids.index("morning_chant")
            new_ids[idx] = "morning_chant_health_of_the_earth"
            
    # Rule E: Local Spirits Sutra Reading (2 or 16)
    if dom in [2, 16]:
        if "morning_chant" in new_ids:
            idx = new_ids.index("morning_chant")
            new_ids[idx] = "morning_chant_local_spirits"

    # --- EVENING RULES (F, G, & H) ---
    # Note: These all insert BEFORE late_afternoon_zazen.
    # We check them in reverse order of importance so they appear in the correct sequence.

    if "late_afternoon_zazen" in new_ids:
        
        # Rule F: Prayers for Supporters (3, 13, 23)
        if dom in [3, 13, 23]:
            idx = new_ids.index("late_afternoon_zazen")
            new_ids.insert(idx, "prayers_for_supporters")

        # Rule G: Two Ancestors Memorial (29, or 28 in Feb)
        # Logic: If it's the 29th OR (it's Feb and it's the last day of the month)
        is_ancestor_day = (dom == 29) or (month == 2 and is_last_day)
        if is_ancestor_day:
            idx = new_ids.index("late_afternoon_zazen")
            new_ids.insert(idx, "two_ancestors_memorial")

        # Rule H: Admonition of Impermanence (8, 18, 28)
        if dom in [8, 18, 28]:
            idx = new_ids.index("late_afternoon_zazen")
            new_ids.insert(idx, "admonition_of_impermanence")
            
    return new_ids
