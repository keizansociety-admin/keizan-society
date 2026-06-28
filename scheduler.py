"""
scheduler.py
============
The 'Liturgical Engine' for the Zen Missal. 
This module organizes the day by passing the schedule through a series 
of 'Pipeline' stations: Structural shifts, Substitutions, and Additions.
"""

from datetime import datetime
import calendar
import pytz

# --- 1. THE LITURGICAL CALENDAR (Rule Maps) ---
# Edit these dictionaries to change what happens on specific days.

# Swaps: { (Days of Month): "New Activity ID" }
MORNING_SUBSTITUTIONS = {
    (1, 15): "morning_chant_health_of_the_earth",
    (2, 16): "morning_chant_local_spirits"
}

# Additions: { (Days of Month): "Activity to Add" }
# These are inserted BEFORE 'late_afternoon_zazen' on weekdays.
EVENING_ADDITIONS = {
    (3, 13, 23): "prayers_for_supporters",
    (8, 18, 28): "admonition_of_impermanence",
    (29,): "two_ancestors_memorial"
}

# Sutra Readings: { Day: "Filename" }
SUTRA_MAP = {
    1: "sutra_reading_01", 5: "sutra_reading_05", 10: "sutra_reading_10", 
    15: "sutra_reading_15", 20: "sutra_reading_20", 25: "sutra_reading_25"
}

def get_meta(timezone_str: str = "America/New_York") -> dict:
    """Calculates the current date and special Zen milestones."""
    tz = pytz.timezone(timezone_str)
    now = datetime.now(tz)
    
    # calendar.monthrange handles Leap Years (Feb 29) automatically
    last_day_of_month = calendar.monthrange(now.year, now.month)[1]
    
    day_of_week = now.strftime("%A")
    
    return {
        "day_of_week": day_of_week,
        "dom": now.day,
        "month": now.month,
        "is_last_day": (now.day == last_day_of_month),
        "is_shaving_day": (now.day % 10 in [4, 9]),
        "is_weekend": day_of_week in ["Saturday", "Sunday"],
        "date_str": now.strftime("%B %d, %Y")
    }

def get_base_template_name(day_of_week: str) -> str:
    """Selects the foundation layout for the day."""
    if day_of_week in ["Saturday", "Sunday"]:
        return "weekend"
    return "friday" if day_of_week == "Friday" else "weekday"

def find_activity_index(activity_ids, target_id):
    """Helper to find an activity ID regardless of hyphens/underscores."""
    norm_target = str(target_id).lower().replace("-", "_")
    for i, act_id in enumerate(activity_ids):
        if str(act_id).lower().replace("-", "_") == norm_target:
            return i
    return None

# --- 2. THE PIPELINE STATIONS ---
def apply_structural_rules(section_name, activity_ids, meta):
    """Handles major shifts like Shaving Day (4/9)."""
    if meta["is_shaving_day"] and section_name == "EARLY HOURS":
        # 1. Add Shaving Verse AFTER face washing
        idx = find_activity_index(activity_ids, "face_washing_morning")
        if idx is not None:
            activity_ids.insert(idx + 1, "shaving_verse")
            activity_ids.insert(idx + 2, "shower_and_dress")
        
        # 2. Remove meditation, chants, and Kesa donning
        z_idx = find_activity_index(activity_ids, "dawn_zazen")
        if z_idx is not None: activity_ids.pop(z_idx)
        
        # --- NEW: Remove Donning Kesa ---
        k_idx = find_activity_index(activity_ids, "donning_kesa")
        if k_idx is not None: activity_ids.pop(k_idx)
        
        # Remove any activity that looks like a morning chant
        activity_ids = [a for a in activity_ids if "morning_chant" not in a]
        
    return activity_ids

def apply_substitution_rules(activity_ids, meta):
    """Swaps standard chants for special ones."""
    dom = meta["dom"]
    m_idx = find_activity_index(activity_ids, "morning_chant")
    if m_idx is not None:
        for days, new_id in MORNING_SUBSTITUTIONS.items():
            if dom in days:
                activity_ids[m_idx] = new_id
    return activity_ids

def apply_addition_rules(activity_ids, meta):
    """Tucks memorial reminders into the evening schedule."""
    dom = meta["dom"]
    e_idx = find_activity_index(activity_ids, "late_afternoon_zazen")
    if e_idx is not None:
        for days, new_id in EVENING_ADDITIONS.items():
            if dom in days:
                activity_ids.insert(e_idx, new_id)
        # Special case for February Leap Year
        if meta["is_last_day"] and meta["month"] == 2:
            if "two_ancestors_memorial" not in activity_ids:
                activity_ids.insert(e_idx, "two_ancestors_memorial")
    return activity_ids

def apply_sutra_rules(activity_ids, meta):
    """Adds Sutra readings based on Weekday vs Weekend logic."""
    dom = meta["dom"]
    if dom not in SUTRA_MAP:
        return activity_ids

    sutra_id = SUTRA_MAP[dom]
    
    if meta["is_weekend"]:
        idx = find_activity_index(activity_ids, "special_observances")
        if idx is not None:
            activity_ids.insert(idx + 1, sutra_id)
    else:
        idx = find_activity_index(activity_ids, "midday_zazen")
        if idx is not None:
            activity_ids.insert(idx, sutra_id)
            
    return activity_ids

def apply_uposatha_rules(activity_ids, meta):
    """Adds Confession on the 15th and Last Day."""
    if not (meta["dom"] == 15 or meta["is_last_day"]):
        return activity_ids

    confession_id = "uposatha_confession"
    
    if meta["is_weekend"]:
        idx = find_activity_index(activity_ids, "special_observances")
        if idx is not None:
            # We insert at idx + 1. If a Sutra was already added at idx + 1, 
            # this pushes the Sutra down, putting Confession first.
            activity_ids.insert(idx + 1, confession_id)
    else:
        idx = find_activity_index(activity_ids, "late_afternoon_zazen")
        if idx is not None:
            activity_ids.insert(idx, confession_id)
            
    return activity_ids

# --- 3. THE MAIN PIPELINE ---

def transform_schedule(section_name, activity_ids, meta):
    """The assembly line that processes the day's activities."""
    new_ids = list(activity_ids) # Work on a copy
    
    new_ids = apply_structural_rules(section_name, new_ids, meta)
    new_ids = apply_substitution_rules(new_ids, meta)
    new_ids = apply_addition_rules(new_ids, meta)
    new_ids = apply_sutra_rules(new_ids, meta)
    new_ids = apply_uposatha_rules(new_ids, meta)
    
    return new_ids
