"""
scheduler.py
============
A dedicated module for calculating Zen liturgical schedules.
Updated: Added Rule J for Study/Reading days (1st, 5th, 10th, 15th, 20th, 25th).
"""

from datetime import datetime
import calendar
import pytz

def get_meta(timezone_str: str = "America/New_York") -> dict:
    """
    Calculates temporal milestones used for liturgical logic.
    
    Returns:
        dict: Contains day of week, day of month (dom), and boolean flags 
              for shaving days and month-end observances.
    """
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
    Determines which YAML template to load based on the day of the week.
    """
    if day_of_week in ["Saturday", "Sunday"]:
        return "weekend"
    elif day_of_week == "Friday":
        return "friday"
    else:
        return "weekday"
    
def transform_schedule(section_name: str, activity_ids: list, meta: dict) -> list:
    """
    Applies liturgical rules to modify the activity list for a specific section.
    
    This function handles:
    - Shaving/Maintenance (4/9)
    - Memorial Chants (1, 2, 15, 16)
    - Evening Additions (3, 8, 13, 18, 23, 28, 29)
    - Study/Reading Days (1, 5, 10, 15, 20, 25)
    """
    dom = meta["dom"]
    month = meta["month"]
    day_of_week = meta["day_of_week"]
    is_last_day = meta["is_last_day"]
    is_shaving_day = meta.get("is_shaving_day", False)
    
    # Work on a copy to avoid mutating the original template list
    new_ids = activity_ids.copy()

    # --- RULE I: SHAVING & MAINTENANCE (Days ending in 4 or 9) ---
    if is_shaving_day and section_name == "EARLY HOURS":
        if "face_washing_morning" in new_ids:
            idx = new_ids.index("face_washing_morning")
            new_ids.insert(idx + 1, "shaving_verse")
            new_ids.insert(idx + 2, "shower_and_dress")
        if "dawn_zazen" in new_ids:
            new_ids.remove("dawn_zazen")
        chant_variants = ["morning_chant", "morning_chant_health_of_the_earth", "morning_chant_local_spirits"]
        new_ids = [act for act in new_ids if act not in chant_variants]

    # --- MORNING RULES (D & E: Memorial Chants) ---
    if dom in [1, 15] and "morning_chant" in new_ids:
        new_ids[new_ids.index("morning_chant")] = "morning_chant_health_of_the_earth"
    if dom in [2, 16] and "morning_chant" in new_ids:
        new_ids[new_ids.index("morning_chant")] = "morning_chant_local_spirits"

    # --- EVENING RULES (F, G, & H: Memorial Additions) ---
    if "late_afternoon_zazen" in new_ids:
        idx = new_ids.index("late_afternoon_zazen")
        if dom in [3, 13, 23]:
            new_ids.insert(idx, "prayers_for_supporters")
        if (dom == 29) or (month == 2 and is_last_day):
            new_ids.insert(idx, "two_ancestors_memorial")
        if dom in [8, 18, 28]:
            new_ids.insert(idx, "admonition_of_impermanence")

    # --- RULE J: STUDY & READING (Days ending in 5 or 0, plus the 1st) ---
    # We map the specific days to their corresponding activity IDs.
    reading_days = {1: "sutra_reading_01", 5: "sutra_reading_05", 10: "sutra_reading_10", 
                    15: "sutra_reading_15", 20: "sutra_reading_20", 25: "sutra_reading_25"}
    
    if dom in reading_days:
        reading_id = reading_days[dom]
        
        # WEEKDAY LOGIC: Insert before late-afternoon zazen
        if day_of_week in ["Monday", "Tuesday", "Wednesday", "Thursday"]:
            if "late_afternoon_zazen" in new_ids:
                idx = new_ids.index("late_afternoon_zazen")
                new_ids.insert(idx, reading_id)
        
        # FRIDAY LOGIC: Insert before evening chant
        elif day_of_week == "Friday":
            if "evening_chant" in new_ids:
                idx = new_ids.index("evening_chant")
                new_ids.insert(idx, reading_id)
        
        # WEEKEND LOGIC: Insert after special observances
        else:
            if "special_observances" in new_ids:
                idx = new_ids.index("special_observances")
                # We use idx + 1 to place it AFTER the anchor
                new_ids.insert(idx + 1, reading_id)
            
    return new_ids
