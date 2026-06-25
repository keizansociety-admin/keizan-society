"""
ZEN MISSAL GENERATOR (Version 3.4)
----------------------------------
Meticulously debugged for liturgical formatting and GitHub Actions.
UX FIX: Robust file discovery (handles hyphen/underscore mismatches).
"""

import os
import yaml
import re
import sys
import scheduler 

# --- SMART CONFIGURATION ---
if os.getenv('GITHUB_ACTIONS') == 'true':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")
else:
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal"
    OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")

CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def check_time_gate():
    if os.getenv('GITHUB_ACTIONS') != 'true':
        return

def simple_markdown(text):
    if not text:
        return []
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def assemble():
    """
    Loads the template and fetches activity content.
    UX FIX: Now tries multiple filename variations (hyphens vs underscores)
    to ensure content is found even if the template and file system differ.
    """
    meta = scheduler.get_meta()
    day_of_week = meta.get("day_of_week", "Monday")
    
    template_name = scheduler.get_base_template_name(day_of_week)
    template_path = os.path.join(TEMPLATE_DIR, f"{template_name}.yaml")
    
    if not os.path.exists(template_path):
        print(f"Error: Template {template_name}.yaml not found.")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        base_template = yaml.safe_load(f)
        
    final_sections = []
    
    for section in base_template.get("sections", []):
        section_name = section.get("period")
        activity_ids = section.get("activity_ids", [])
        
        transformed_ids = scheduler.transform_schedule(section_name, activity_ids, meta)
        
        activities_content = []
        for act_id in transformed_ids:
            # --- ROBUST FILE DISCOVERY ---
            # We try the ID exactly as written, then try it with underscores.
            # This allows "late-afternoon" in templates to find "late_afternoon" files.
            variations = [act_id, act_id.replace("-", "_"), act_id.replace("_", "-")]
            
            target_path = None
            for var in variations:
                for ext in [".yaml", ".yml"]:
                    test_path = os.path.join(CONTENT_DIR, f"{var}{ext}")
                    if os.path.exists(test_path):
                        target_path = test_path
                        break
                if target_path: break
            
            if target_path:
                with open(target_path, 'r', encoding='utf-8') as act_f:
                    act_data = yaml.safe_load(act_f)
                    act_data['body'] = simple_markdown(act_data.get('body', ''))
                    activities_content.append(act_data)
            else:
                # Fallback: Generate a readable title from the ID
                # We replace underscores with spaces but KEEP hyphens for grammar.
                clean_title = act_id.replace("_", " ").title()
                activities_content.append({
                    "title": clean_title, 
                    "body": [f"[Missing content file for {act_id}]"]
                })
                
        final_sections.append({
            "period": section_name,
            "activities": activities_content
        })
        
    return meta, final_sections

def render(meta, sections):
    """Generates the final HTML file with CSS styling."""
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
    .sub-header {
        font-size: 14pt;
        display: block;
        margin-top: 10px;
    }
    .shaving-label {
        font-size: 13pt;
        font-style: italic;
        color: #444;
        display: block;
        margin-top: 5px;
    }
    """
    
    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append("<html><head><meta charset='utf-8'>")
    html_parts.append(f"<style>{css}</style>")
    html_parts.append(f"<title>Householder's Shingi - {meta.get('day_of_week', 'Today')}</title>")
    html_parts.append("</head><body>")
    
    shaving_html = ""
    if meta.get("is_shaving_day"):
        shaving_html = f"<span class='shaving-label'>Shaving & Maintenance Day</span>"
    
    date_str = f"{meta.get('day_of_week', '')}, {meta.get('date_str', '')}"
    
    html_parts.append(f"""
    <h1>
        Householder's Shingi<br>
        <span class='sub-header'>{date_str}</span>
        {shaving_html}
    </h1>
    """)
    
    for section in sections:
        if not section['activities']:
            continue
        html_parts.append(f"<h2>{section['period']}</h2>")
        for act in section['activities']:
            html_parts.append("<div class='activity'>")
            paragraphs = act.get('body', [])
            title_html = f"<span class='activity-title'>{act.get('title', 'Untitled')}</span>"
            if paragraphs:
                first_p = paragraphs[0]
                html_parts.append(f"<p>{title_html}{first_p}</p>")
                for other_p in paragraphs[1:]:
                    html_parts.append(f"<p>{other_p}</p>")
            else:
                html_parts.append(f"<p>{title_html}</p>")
            html_parts.append("</div>")
            
    html_parts.append("</body></html>")
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(html_parts))

if __name__ == "__main__":
    check_time_gate()
    metadata, final_sections = assemble()
    render(metadata, final_sections)
    print(f"Successfully generated Missal for {metadata.get('day_of_week', 'Today')}")
