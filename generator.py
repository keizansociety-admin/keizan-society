import os
import yaml
import pytz
import calendar
import re
from datetime import datetime

# --- CONFIGURATION ---
TIMEZONE = "America/New_York"
BASE_DIR = os.path.dirname(__file__)
CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def simple_markdown(text):
    """Converts *italics* to HTML and splits text into paragraphs."""
    if not text: return []
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def get_meta():
    """Determines the date and liturgical triggers."""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    dom = now.day
    
    # Calculate if today is the last day of the month
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
    """
    Applies the Rules RTF logic and Sutra Injection to the list of activity IDs.
    This is the 'Rule Pipeline' that modifies the schedule before loading files.
    """
    new_ids = []
    dom = meta["dom"]

    # RULE: Rest Day - Wipe Early Hours and replace with Shaving
    if meta["is_rest_day"] and section_name.upper() == "EARLY HOURS":
        return ["shaving"] 

    for act_id in activity_ids:
        # RULE: Rest Day - Remove Shower from Morning
        if meta["is_rest_day"] and act_id == "shower_and_dress":
            continue

        # RULE: Day 28 Memorial (Injection before Evening Zazen)
        if dom == 28 and act_id == "evening_zazen":
            new_ids.append("two_ancestors_memorial")

        # RULE: Kankin Sutra Reading (Injection before Late-Afternoon Zazen)
        sutra_days = [1, 5, 10, 15, 20, 25]
        if dom in sutra_days and act_id == "late_afternoon_zazen":
            new_ids.append(f"sutra_reading_{dom}")
        
        # RULE: Substitutions (The 'Swap' Logic)
        target_id = act_id
        
        # Morning Chant Swaps (Days 1, 15, 2, 16)
        if act_id == "morning_chant":
            if dom in [1, 15]: target_id = "morning_chant_earth"
            elif dom in [2, 16]: target_id = "morning_chant_local_spirits"
            
        # Evening Chant Swaps (3/13/23, 8/18/28, Uposatha)
        if act_id == "evening_chant":
            if dom in [3, 13, 23]: target_id = "evening_chant_supporters"
            elif dom in [8, 18, 28]: target_id = "evening_chant_impermanence"
            elif meta["is_uposatha"]: target_id = "uposatha"

        new_ids.append(target_id)
        
    return new_ids

def assemble():
    """Gathers the correct YAML files based on the template and rule pipeline."""
    meta = get_meta()
    
    # 1. Select Template based on Day of Week
    t_name = "weekday.yaml"
    if meta["day_of_week"] == "Friday": t_name = "friday.yaml"
    elif meta["is_weekend"]: t_name = "weekend.yaml"
    
    template_path = os.path.join(TEMPLATE_DIR, t_name)
    if not os.path.exists(template_path):
        print(f"Error: Template {t_name} not found in {TEMPLATE_DIR}")
        return meta, []

    with open(template_path, 'r', encoding='utf-8') as f:
        template = yaml.safe_load(f)

    final_sections = []
    for sec in template['sections']:
        # Apply the Rule Pipeline to the activity list for this section
        active_ids = transform_schedule(sec['period'], sec['activity_ids'], meta)
        
        activities = []
        for act_id in active_ids:
            path = os.path.join(CONTENT_DIR, f"{act_id}.yaml")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    activities.append(yaml.safe_load(f))
            else:
                print(f"Warning: Missing file {act_id}.yaml")
                
        final_sections.append({"period": sec['period'], "activities": activities})
        
    return meta, final_sections

def render(meta, sections):
    """Typesets the missal using CSS to match the liturgical design."""
    css = """
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&display=swap');
    
    body { 
        font-family: 'Libre Baskerville', serif; 
        max-width: 7.5in; 
        margin: 1in auto; 
        line-height: 1.6; 
        text-align: justify; 
        font-size: 11.5pt; 
        color: #000;
    }
    
    h1 { 
        text-align: center; 
        font-size: 26pt; 
        border-bottom: 1px solid #000; 
        padding-bottom: 15px; 
        margin-bottom: 40px; 
    }
    
    h2 { 
        text-align: center; 
        text-transform: uppercase; 
        letter-spacing: 0.5em; 
        font-size: 14pt; 
        margin: 60px 0 30px 0; 
        font-weight: normal; 
    }
    
    .activity { 
        margin-bottom: 1.8em; 
        clear: both;
    }
    
    .activity p { 
        text-indent: 2.5em; 
        margin: 0; 
        padding: 0;
    }

    .activity-title { 
        font-weight: bold; 
        text-transform: uppercase; 
    }
    
    .activity-title::after { 
        content: ". "; 
    }

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
                # Inject the title into the first paragraph for the run-in effect
                first_p = paragraphs[0]
                title_html = f"<span class='activity-title'>{a.get('title', 'Untitled')}</span>"
                html += f"<p>{title_html}{first_p}</p>"
                
                for other_p in paragraphs[1:]:
                    html += f"<p>{other_p}</p>"
            else:
                html += f"<p><span class='activity-title'>{a.get('title', 'Untitled')}</span></p>"
            html += f"</div>"
            
    html += "</body></html>"
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    out_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(out_path, "w", encoding='utf-8') as f:
        f.write(html)

if __name__ == "__main__":
    metadata, final_sections = assemble()
    render(metadata, final_sections)
    print(f"Generated Missal for {metadata['date_str']}")