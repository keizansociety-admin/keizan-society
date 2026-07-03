"""
ZEN MISSAL GENERATOR (Version 4.0.1)
----------------------------------
A human-centered tool for generating liturgical schedules.
"""

import os
import yaml
import re
import sys
import scheduler 

# --- 1. SMART CONFIGURATION ---
if os.getenv('GITHUB_ACTIONS') == 'true':
    # This finds the folder where this script lives
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # We added "output" here so it matches your local setup!
    # os.path.join safely glues folder names together
    OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")
else:
    # This is your local path for when you run it on your own computer
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal"
    OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")

CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def simple_markdown(text):
    """Converts basic markdown into HTML."""
    if not text:
        return []
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def fetch_activity_data(act_id):
    """Finds the YAML file for an activity, handling naming variations."""
    variations = [act_id, act_id.replace("-", "_"), act_id.replace("_", "-")]
    
    for var in variations:
        for ext in [".yaml", ".yml"]:
            path = os.path.join(CONTENT_DIR, f"{var}{ext}")
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    data['body'] = simple_markdown(data.get('body', ''))
                    return data
    
    clean_title = act_id.replace("_", " ").replace("-", " ").title()
    return {
        "title": clean_title, 
        "body": [f"<i>[Missing content file for {act_id}]</i>"]
    }

def assemble():
    """Loads the template and runs it through the scheduler pipeline."""
    meta = scheduler.get_meta()
    template_name = scheduler.get_base_template_name(meta["day_of_week"])
    template_path = os.path.join(TEMPLATE_DIR, f"{template_name}.yaml")
    
    if not os.path.exists(template_path):
        print(f"Error: Template {template_name}.yaml not found.")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        base_template = yaml.safe_load(f)
        
    final_sections = []
    for section in base_template.get("sections", []):
        section_name = section.get("period", "UNNAMED PERIOD")
        activity_ids = section.get("activity_ids", [])
        
        transformed_ids = scheduler.transform_schedule(section_name, activity_ids, meta)
        activities_content = [fetch_activity_data(aid) for aid in transformed_ids]
        
        final_sections.append({
            "period": section_name,
            "activities": activities_content
        })
        
    return meta, final_sections

def render(meta, sections, target_path):
    """
    Takes the processed schedule data and draws the final HTML file.
    
    Args:
        meta (dict): Date and special day info.
        sections (list): The list of activities for the day.
        target_path (str): Exactly where to save the finished file.
    """
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
    html_parts.append(f"<title>Householder's Shingi - {meta.get('date_str')}</title>")
    html_parts.append("</head><body>")
    
    shaving_html = ""
    if meta.get("is_shaving_day"):
        shaving_html = f"<span class='shaving-label'>Shaving & Maintenance Day</span>"
    
    date_header = f"{meta.get('day_of_week')}, {meta.get('date_str')}"
    
    html_parts.append(f"""
    <h1>
        Householder's Shingi<br>
        <span class='sub-header'>{date_header}</span>
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
    
    # Ensure the folder exists before we try to save the file
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    
    # Write the file to the specific path provided to the function
    with open(target_path, 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(html_parts))

if __name__ == "__main__":
    # 1. Prepare the data
    metadata, final_sections = assemble()
    
    # 2. Determine where we are (GitHub vs Local) to set the base folder
    if os.getenv('GITHUB_ACTIONS') == 'true':
        current_dir = os.path.dirname(os.path.abspath(__file__))
    else:
        current_dir = "/Users/jocorsoesquivel/Dropbox/zen_missal"

    # 3. Define our two delivery locations
    path_root = os.path.join(current_dir, "index.html")
    path_output = os.path.join(current_dir, "output", "index.html")
    
    # 4. Run the render function twice!
    render(metadata, final_sections, path_root)
    render(metadata, final_sections, path_output)
    
    print(f"Successfully generated Missal in both locations for {metadata.get('date_str')}")
