"""
ZEN MISSAL GENERATOR
--------------------
DESCRIPTION:
This script assembles a liturgical missal based on the Keizan Shingi. 
It handles date-based substitutions, rest days, and sutra injections.

ENVIRONMENTS:
1. LOCAL (Mac/Thonny): Uses absolute paths to your Dropbox folder.
2. CLOUD (GitHub Actions): Uses relative paths within the repository.

WORKFLOW:
1. Edit YAML files in 'content/activities' or 'templates' on your Mac.
2. Run this script in Thonny to preview changes in 'output/index.html'.
3. Upload (Push) changes to GitHub. The 'daily_missal.yml' workflow 
   will run this same script automatically at midnight.

MAINTENANCE:
- To change the local path, update the BASE_DIR in the 'else' block below.
- To add new rules, update the 'transform_schedule' function.
"""

import os
import yaml
import pytz
import calendar
import re
from datetime import datetime

# --- SMART CONFIGURATION ---
TIMEZONE = "America/New_York"

if os.getenv('GITHUB_ACTIONS') == 'true':
    # CLOUD CONFIGURATION
    # Detects the folder where the GitHub Action is running
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")
else:
    # LOCAL CONFIGURATION
    # Update this path if you move your project folder on your Mac
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal" 
    OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")

# PATH RESOLUTION
# These remain consistent across both platforms
CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def simple_markdown(text):
    """Converts *italics* to HTML and splits text into paragraphs."""
    if not text: return []
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def get_meta():
    """Calculates date and adds a placeholder for holidays."""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    dom = now.day
    month = now.month # Added month for holiday tracking
    
    last_day = calendar.monthrange(now.year, now.month)[1]
    is_last_day = (dom == last_day)
    
    return {
        "date_str": now.strftime("%A, %B %d, %Y"),
        "day_of_week": now.strftime("%A"),
        "dom": dom,
        "month": month,
        "is_last_day": is_last_day,
        "is_weekend": now.weekday() >= 5,
        "is_rest_day": dom in [4, 9, 14, 19, 24] or is_last_day,
        "is_uposatha": dom == 15 or is_last_day
    }

def transform_schedule(section_name, activity_ids, meta):
    """
    Applies Keizan Shingi rules and handles conditional 
    activities like Special Observances.
    """
    new_ids = []
    dom = meta["dom"]
    month = meta["month"]

    # RULE: Rest Day - Wipe Early Hours and replace with Shaving
    # (This stays from your original code)
    if meta["is_rest_day"] and section_name.upper() == "EARLY HOURS":
        return ["shaving"] 

    for act_id in activity_ids:
        
        # --- SPECIAL OBSERVANCES RULE ---
        if act_id == "special_observances":
            # For now, let's say it only shows up in December (Month 12)
            # You can change this logic later!
            if month == 12:
                new_ids.append(act_id)
            else:
                continue # This skips it if it's not December
        
        # --- EXISTING SUBSTITUTION RULES ---
        elif act_id == "morning_chant":
            if dom in [1, 15]: new_ids.append("morning_chant_earth")
            elif dom in [2, 16]: new_ids.append("morning_chant_local_spirits")
            else: new_ids.append(act_id)
            
        # (Add your other existing rules for evening_chant here...)
        
        else:
            # If no special rule applies, just add the activity normally
            new_ids.append(act_id)
            
    return new_ids

def assemble():
    """
    Determines the correct template based on the date, loads the 
    YAML configuration, and assembles the activity data.
    """
    meta = get_meta()
    
    # 1. Determine which template file to use
    t_name = "weekday.yaml"
    if meta["day_of_week"] == "Friday": 
        t_name = "friday.yaml"
    elif meta["is_weekend"]: 
        t_name = "weekend.yaml"
    
    template_path = os.path.join(TEMPLATE_DIR, t_name)
    
    # 2. Check if the template file actually exists
    if not os.path.exists(template_path):
        print(f"Error: Template not found at {template_path}")
        return meta, []

    # 3. LOAD THE TEMPLATE (This is the part that was likely missing or broken)
    with open(template_path, 'r', encoding='utf-8') as f:
        template = yaml.safe_load(f)

    # 4. Process the sections defined in the template
    final_sections = []
    for sec in template['sections']:
        # Apply the Keizan Shingi rules to get the list of activity IDs
        active_ids = transform_schedule(sec['period'], sec['activity_ids'], meta)
        
        activities = []
        for act_id in active_ids:
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
    """Generates the final HTML file with CSS typesetting."""
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
    
    # Ensure output directory exists for local testing
    out_dir = os.path.dirname(OUTPUT_FILE)
    if out_dir and not os.path.exists(out_dir):
        os.makedirs(out_dir)
        
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    metadata, final_sections = assemble()
    render(metadata, final_sections)
    print(f"Generated Missal for {metadata['date_str']}")