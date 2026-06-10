import os
import yaml
import pytz
import calendar
import re
from datetime import datetime

# --- GITHUB CONFIGURATION ---
TIMEZONE = "America/New_York"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# These must match your folder names exactly
CONTENT_DIR = os.path.join(BASE_DIR, "content/activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")

def simple_markdown(text):
    if not text: return []
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def get_meta():
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    dom = now.day
    last_day = calendar.monthrange(now.year, now.month)[1]
    is_last_day = (dom == last_day)
    return {
        "date_str": now.strftime("%A, %B %d, %Y"),
        "day_of_week": now.strftime("%A"),
        "dom": dom,
        "is_last_day": is_last_day,
        "is_weekend": now.weekday() >= 5,
        "is_rest_day": dom in [4, 9, 14, 19, 24] or is_last_day,
        "is_uposatha": dom == 15 or is_last_day
    }

def transform_schedule(section_name, activity_ids, meta):
    new_ids = []
    dom = meta["dom"]
    if meta["is_rest_day"] and section_name.upper() == "EARLY HOURS":
        return ["shaving"] 
    for act_id in activity_ids:
        if meta["is_rest_day"] and act_id == "shower_and_dress":
            continue
        if dom == 28 and act_id == "evening_zazen":
            new_ids.append("two_ancestors_memorial")
        sutra_days = [1, 5, 10, 15, 20, 25]
        if dom in sutra_days and act_id == "late_afternoon_zazen":
            new_ids.append(f"sutra_reading_{dom}")
        target_id = act_id
        if act_id == "morning_chant":
            if dom in [1, 15]: target_id = "morning_chant_earth"
            elif dom in [2, 16]: target_id = "morning_chant_local_spirits"
        if act_id == "evening_chant":
            if dom in [3, 13, 23]: target_id = "evening_chant_supporters"
            elif dom in [8, 18, 28]: target_id = "evening_chant_impermanence"
            elif meta["is_uposatha"]: target_id = "uposatha"
        new_ids.append(target_id)
    return new_ids

def assemble():
    meta = get_meta()
    t_name = "weekday.yaml"
    if meta["day_of_week"] == "Friday": t_name = "friday.yaml"
    elif meta["is_weekend"]: t_name = "weekend.yaml"
    
    template_path = os.path.join(TEMPLATE_DIR, t_name)
    if not os.path.exists(template_path):
        print(f"DEBUG: Template not found at {template_path}")
        return meta, []

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
                print(f"DEBUG: Activity file not found at {path}")
        final_sections.append({"period": sec['period'], "activities": activities})
    return meta, final_sections

def render(meta, sections):
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
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    metadata, final_sections = assemble()
    render(metadata, final_sections)
