"""
ZEN MISSAL GENERATOR
--------------------
DESCRIPTION:
This script assembles a liturgical missal based on the Keizan Shingi. 
It handles date-based substitutions, rest days, and sutra injections.

ENVIRONMENTS:
1. LOCAL (Mac/Thonny): Uses absolute paths to your project folder.
2. CLOUD (GitHub Actions): Uses relative paths within the repository.
"""

import os
import yaml
import pytz
import calendar
import re
import sys
from datetime import datetime

# --- SMART CONFIGURATION ---
TIMEZONE = "America/New_York"

if os.getenv('GITHUB_ACTIONS') == 'true':
    # CLOUD CONFIGURATION
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")
else:
    # LOCAL CONFIGURATION
    # Update this path if you move your project folder on your Mac
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal" 
    OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")

# PATH RESOLUTION
CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def check_time_gate():
    """
    Prevents the script from running outside of the midnight window.
    
    This allows the GitHub Action to be scheduled hourly (to avoid delays)
    while ensuring the website only updates once per day.
    """
    if os.getenv('GITHUB_ACTIONS') != 'true':
        return # Skip this check if running locally on your Mac

    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    
    # If it is NOT the midnight hour (0), exit the script silently
    if now.hour != 0:
        print(f"Current hour is {now.hour}. Skipping update until midnight window.")
        sys.exit(0)
    
    print("Midnight window detected. Proceeding with update...")

def simple_markdown(text):
    """
    Converts basic markdown syntax to HTML tags.
    
    Args:
        text (str): The raw text from a YAML body field.
    Returns:
        list: A list of strings, where each string is an HTML paragraph.
    """
    if not text: return []
    # Convert *text* to <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Split by double newlines to create paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def get_meta():
    """
    Calculates liturgical metadata based on the current date and timezone.
    
    Returns:
        dict: Contains date strings and boolean flags for liturgical rules.
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    dom = now.day
    month = now.month
    
    last_day = calendar.monthrange(now.year, now.month)[1]
    is_last_day = (dom == last_day)
    
    return {
        "date_str": now.strftime("%A, %B %d, %Y"),
        "day_of_week": now.strftime("%A"),
        "dom": dom,
        "month": month,
        "is_last_day": is_last_day,
        "is_weekend": now.weekday() >= 5, # 5 is Saturday, 6 is Sunday
        "is_rest_day": dom in [4, 9, 14, 19, 24] or is_last_day,
        "is_uposatha": dom == 15 or is_last_day
    }

def transform_schedule(section_name, activity_ids, meta):
    """
    Applies Keizan Shingi substitution rules to a list of activities.
    
    Args:
        section_name (str): The name of the liturgical period (e.g., "EARLY HOURS").
        activity_ids (list): The list of IDs from the template.
        meta (dict): The date metadata.
    Returns:
        list: The transformed list of activity IDs.
    """
    new_ids = []
    dom = meta["dom"]

    # RULE: Rest Day - Replace Early Hours with Shaving
    if meta["is_rest_day"] and section_name.upper() == "EARLY HOURS":
        return ["shaving"] 

    for act_id in activity_ids:
        
        # --- SPECIAL OBSERVANCES RULE ---
        # Removed the 'month == 12' restriction so this shows every weekend.
        if act_id == "special_observances":
            new_ids.append(act_id)
        
        # --- EXISTING SUBSTITUTION RULES ---
        elif act_id == "morning_chant":
            if dom in [1, 15]: new_ids.append("morning_chant_earth")
            elif dom in [2, 16]: new_ids.append("morning_chant_local_spirits")
            else: new_ids.append(act_id)
            
        else:
            new_ids.append(act_id)
            
    return new_ids

def assemble():
    """
    Loads templates and activity files to build the final data structure.
    
    Returns:
        tuple: (metadata dictionary, list of section dictionaries)
    """
    meta = get_meta()
    
    # 1. Determine template
    t_name = "weekday.yaml"
    if meta["day_of_week"] == "Friday": 
        t_name = "friday.yaml"
    elif meta["is_weekend"]: 
        t_name = "weekend.yaml"
    
    template_path = os.path.join(TEMPLATE_DIR, t_name)
    
    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}")
        return meta, []

    with open(template_path, 'r', encoding='utf-8') as f:
        template = yaml.safe_load(f)

    # 2. Process sections
    final_sections = []
    for sec in template['sections']:
        active_ids = transform_schedule(sec['period'], sec['activity_ids'], meta)
        
        activities = []
        for act_id in active_ids:
            # Note: Ensure your file is named 'special_observances.yaml' to match the ID
            path = os.path.join(CONTENT_DIR, f"{act_id}.yaml")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    try:
                        activities.append(yaml.safe_load(f))
                    except yaml.YAMLError as exc:
                        print(f"Error parsing YAML in {path}: {exc}")
            else:
                print(f"Warning: Activity file missing: {path}")
                
        final_sections.append({"period": sec['period'], "activities": activities})
        
    return meta, final_sections

def render(meta, sections):
    """
    Generates the final HTML file with CSS styling.
    
    Args:
        meta (dict): Date metadata.
        sections (list): The assembled activity data.
    """
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
    body { font-family: 'Libre Baskerville', serif; max-width: 7.5in; margin: 1in auto; line-height: 1.6; text-align: justify; font-size: 11.5pt; color: #000; }
    h1 { text-align: center; font-size: 26pt; border-bottom: 1px solid #000; padding-bottom: 15px; margin-bottom: 40px; }
    h2 { text-align: center; text-transform: uppercase; letter-spacing: 0.5em; font-size: 14pt; margin: 60px 0 30px 0; font-weight: normal; }
    .activity { margin-bottom: 1.8em; clear: both; }
    .activity p { text-indent: 2.5em; margin: 0; padding: 0; }
    .activity-title { font-weight: bold; text-transform: uppercase; }
    .activity-title::after { content: ". "; }
    i { font-style: italic; }
    """
    html = f"<html><head><style>{css}</style></head><body>"
    html += f"<h1>{meta['date_str']}</h1>"
    for s in sections:
        if not s['activities']: continue
        html += f"<h2>{s['period']}</h2>"
        for a in s['activities']:
            paragraphs = simple_markdown(a.get('body', ''))
            html += f"<div class='activity'>"
            if paragraphs:
                first_p = paragraphs[0]
                title_html = f"<span class='activity-title'>{a.get('title', 'Untitled')}</span>"
                html += f"<p>{title_html}{first_p}</p>"
                for other_p in paragraphs[1:]:
                    html += f"<p>{other_p}</p>"
            else:
                html += f"<p><span class='activity-title'>{a.get('title', 'Untitled')}</span></p>"
            html += f"</div>"
    html += "</body></html>"
    
    out_dir = os.path.dirname(OUTPUT_FILE)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    # 1. Check if we are allowed to run at this hour
    check_time_gate()
    
    # 2. Assemble and Render
    metadata, final_sections = assemble()
    render(metadata, final_sections)
    print(f"Generated Missal for {metadata['date_str']}")
