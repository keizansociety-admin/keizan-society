"""
ZEN MISSAL GENERATOR (Version 2.5 - Uposatha & Heartbeat)
--------------------------------------------------
1. Injects Uposatha Confession on the 15th and last day.
2. Injects Two Ancestors Memorial on the 15th.
3. Includes Heartbeat logic for GitHub priority.
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
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")
else:
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal" 
    OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")

CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def simple_markdown(text):
    """Converts *italics* and **bold** to HTML and splits paragraphs."""
    if not text: return []
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def get_meta():
    """Calculates date and liturgical flags."""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    dom = now.day
    last_day = calendar.monthrange(now.year, now.month)[1]
    return {
        "date_str": now.strftime("%A, %B %d, %Y"),
        "day_of_week": now.strftime("%A"),
        "dom": dom,
        "is_weekend": now.weekday() >= 5,
        "is_rest_day": dom in [4, 9, 14, 19, 24] or (dom == last_day),
        "is_uposatha": dom == 15 or (dom == last_day)
    }

def transform_schedule(section_name, activity_ids, meta):
    """
    Applies Keizan Shingi substitution and injection rules.
    """
    new_ids = []
    dom = meta["dom"]
    is_uposatha = meta["is_uposatha"]
    
    # RULE: Rest Day - Replace Early Hours with Shaving
    if meta["is_rest_day"] and section_name.upper() == "EARLY HOURS":
        return ["shaving"] 

    for act_id in activity_ids:
        
        # RULE: Morning Chant Substitutions (1st and 15th)
        if act_id == "morning_chant":
            if dom in [1, 15]:
                new_ids.append("morning_chant_earth")
            elif dom in [2, 16]:
                new_ids.append("morning_chant_local_spirits")
            else:
                new_ids.append(act_id)

        # RULE: 15th Day - Memorial Service (Before Breakfast)
        elif act_id == "morning_meal" and dom == 15:
            new_ids.append("two_ancestors_memorial")
            new_ids.append(act_id)
            
        # RULE: Uposatha Confession (15th and Last Day)
        # Injected before the evening chant as per lay instructions
        elif act_id == "evening_chant" and is_uposatha:
            new_ids.append("uposatha_confession")
            new_ids.append(act_id)
            
        else:
            new_ids.append(act_id)
            
    return new_ids

def assemble():
    """Loads templates and activity files."""
    meta = get_meta()
    t_name = "weekday.yaml"
    if meta["day_of_week"] == "Friday": t_name = "friday.yaml"
    elif meta["is_weekend"]: t_name = "weekend.yaml"
    
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
        final_sections.append({"period": sec['period'], "activities": activities})
    return meta, final_sections

def render(meta, sections):
    """Generates HTML and updates the heartbeat file."""
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
    html = f"<html><head><style>{css}</style></head><body>"
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
    
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(html)

    # --- HEARTBEAT LOGIC ---
    heartbeat_path = os.path.join(BASE_DIR, "heartbeat.txt")
    with open(heartbeat_path, "w", encoding='utf-8') as f:
        f.write(f"Last Pulse: {datetime.now(pytz.timezone(TIMEZONE))}")

if __name__ == "__main__":
    metadata, final_sections = assemble()
    render(metadata, final_sections)
    print(f"Generated Missal for {metadata['date_str']}")
