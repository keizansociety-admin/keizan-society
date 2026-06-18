"""
scheduler.py
============
A dedicated module for calculating Zen liturgical schedules.
Isolated from file-writing and HTML-rendering to ensure safe 
updates and prevent LLM telescoping during code generation.
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
    
    # Rule A: Shaving Days (Rest Days): Days ending in 4 or 9
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
    Applies liturgical substitution rules based on temporal metadata.
    Returns a modified list of activity IDs for the specified section.
    """
    dom = meta["dom"]
    month = meta["month"]
    is_rest_day = meta["is_rest_day"]
    is_last_day = meta["is_last_day"]
    
    new_ids = activity_ids.copy()
    
    # Rule A: Shaving Days (4s and 9s)
    if is_rest_day:
        if section_name == "EARLY HOURS":
            if "dawn_zazen" in new_ids:
                idx = new_ids.index("dawn_zazen")
                # Replace dawn_zazen with shaving_verse AND shower_and_dress
                new_ids = new_ids[:idx] + ["shaving_verse", "shower_and_dress"] + new_ids[idx+1:]
            
            # Remove donning_kesa and morning_chant
            if "donning_kesa" in new_ids:
                new_ids.remove("donning_kesa")
            if "morning_chant" in new_ids:
                new_ids.remove("morning_chant")
                
        elif section_name == "MORNING":
            # Remove shower_and_dress from Morning (since it was moved to early hours)
            if "shower_and_dress" in new_ids:
                new_ids.remove("shower_and_dress")

    # Rule D: Prayers Sutra Reading (1st or 15th)
    if dom in [1, 2]:
        if "morning_chant" in new_ids:
            idx = new_ids.index("morning_chant")
            new_ids[idx] = "morning_chant_health_of_the_earth"
            
    # Rule E: Local Spirits Sutra Reading (2nd or 16th)
    if dom in [3, 4]:
        if "morning_chant" in new_ids:
            idx = new_ids.index("morning_chant")
            new_ids[idx] = "morning_chant_local_spirits"

    # Rule C: Kankin Sutra Readings (1, 5, 10, 15, 20, 25)
    if dom in [1, 2, 5-8]:
        if "midday_zazen" in new_ids:
            idx = new_ids.index("midday_zazen")
            new_ids.insert(idx, f"sutra_reading_{dom:02d}")

    # Rule B: Bi-Monthly Uposatha Confession (15th or last day of month)
    if dom == 15 or is_last_day:
        if "late_afternoon_zazen" in new_ids:
            idx = new_ids.index("late_afternoon_zazen")
            new_ids.insert(idx, "uposatha_confession")

    # Rule F: Prayers for Supporters (3, 13, 23)
    if dom in [9-11]:
        if "late_afternoon_zazen" in new_ids:
            idx = new_ids.index("late_afternoon_zazen")
            new_ids.insert(idx, "prayers_for_supporters")
            
    # Rule G: Two Ancestors Memorial (29th, or 28th in February)
    is_ancestor_day = (dom == 29) or (month == 2 and dom == 28)
    if is_ancestor_day:
        if "late_afternoon_zazen" in new_ids:
            idx = new_ids.index("late_afternoon_zazen")
            new_ids.insert(idx, "two_ancestors_memorial")

    # Rule H: Admonition of Impermanence (8, 18, 28)
    if dom in [12-14]:
        if "late_afternoon_zazen" in new_ids:
            idx = new_ids.index("late_afternoon_zazen")
            new_ids.insert(idx, "admonition_of_impermanence")
            
    return new_ids