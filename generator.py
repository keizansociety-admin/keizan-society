"""
ZEN MISSAL GENERATOR (Version 2.3)
----------------------------------
Meticulously debugged for GitHub Actions pathing and liturgical accuracy.
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

# Determine the base directory and ensure the output path is consistent
if os.getenv('GITHUB_ACTIONS') == 'true':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    # Local path for development
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal" 

# FIX: Both environments now point to the 'output' folder as per the file tree
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def check_time_gate():
    """
    Prevents the script from running outside the midnight window on GitHub.
    Note: GitHub Actions can be delayed. If this script runs at 12:15 AM, 
    it will still proceed.
    """
    if os.getenv('GITHUB_ACTIONS') != 'true':
        return 
    
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    
    # We allow the script to run during the 0 hour (12:00 AM - 12:59 AM)
    if now.hour != 0:
        print(f"Current hour is {now.hour}. Skipping update until midnight window.")
        sys.exit(0) 
    print("Midnight window detected. Proceeding with update...")

def simple_markdown(text):
    """
    Converts *italics* and **bold** to HTML and splits text into 
    clean paragraph lists.
    """
    if not text: return []
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def get_meta():
    """
    Calculates the current date and identifies special liturgical 
    conditions like rest days or the end of the month.
    """
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    dom = now.day
    
    # calendar.monthrange returns (first_day_of_week, number_of_days_in_month)
    # We need the second value [1] to get the last day of the month.
    last_day = calendar.monthrange(now.year, now.month)[1]
    
    # FIX: Added 29 to the rest day list and fixed the last_day comparison
    is_rest_day = dom in [4, 9, 14, 19, 24, 29] or (dom == last_day)
    
    return {
        "date_str": now.strftime("%A, %B %d, %Y"),
        "day_of_week": now.strftime("%A"),
        "dom": dom,
        "is_weekend": now.weekday() >= 5,
        "is_rest_day": is_rest_day,
    }

def transform_schedule(section_name, activity_ids, meta):
    """
    Applies substitution rules. On rest days, early morning zazen 
    is replaced by the shaving verse.
    """
    new_ids = []
    dom = meta["dom"]
    
    # FIX: Changed 'shaving' to 'shaving_verse' to match the file tree
    if meta["is_rest_day"] and section_name.upper() == "EARLY HOURS":
        return ["shaving_verse"] 
        
    for act_id in activity_ids:
        if act_id == "morning_chant":
            if dom in [1, 15]: new_ids.append("morning_chant_earth")
            elif dom in [2, 16]: new_ids.append("morning_chant_local_spirits")
            else: new_ids.append(act_id)
        else:
            new_ids.append(act_id)
    return new_ids

def assemble():
    """
    Loads the appropriate template based on the day of the week 
    and fetches the content for each activity.
    """
    meta = get_meta()
    
    # Select template
    if meta["day_of_week"] == "Friday": 
        t_name = "friday.yaml"
    elif meta["is_weekend"]: 
        t_name = "weekend.yaml"
    else:
        t_name = "weekday.yaml"
    
    template_path = os.path.join(TEMPLATE_DIR, t_name)
    with open(template_path, 'r', encoding='utf-8') as f:
        template = yaml.safe_load(f)

    final_sections = []
    for sec in template['sections']:
        active_ids = transform_schedule(sec['period'], sec['activity_ids'], meta)
        activities = []
        for act_id in active_ids:
            path = os.path.join(CONTENT_DIR, f"{act_id}.yaml")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    activities.append(yaml.safe_load(f))
            else:
                print(f"Warning: Missing file for activity '{act_id}'")
                
        final_sections.append({"period": sec['period'], "activities": activities})
    return meta, final_sections

def render(meta, sections):
    """
    Generates the final HTML file with embedded CSS for 
    liturgical formatting.
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
    
    .chant { max-width: 85%; margin: 2em auto; text-align: left; }
    .chant p { text-indent: 0 !important; margin-bottom: 0.8em; }
    """
    html = f"<!DOCTYPE html><html><head><meta charset='UTF-8'><style>{css}</style></head><body>"
    html += f"<h1>{meta['date_str']}</h1>"
    
    for s in sections:
        if not s['activities']: continue
        html += f"<h2>{s['period']}</h2>"
        for a in s['activities']:
            is_chant = a.get('display') == 'chant'
            div_class = "activity chant" if is_chant else "activity"
            paragraphs = simple_markdown(a.get('body', ''))
            
            html += f"<div class='{div_class}'>"
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
    
    # Ensure the output directory exists before writing
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    check_time_gate()
    metadata, final_sections = assemble()
    render(metadata, final_sections)
    print(f"Successfully generated Missal for {metadata['date_str']}")
