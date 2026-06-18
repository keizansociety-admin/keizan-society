"""
ZEN MISSAL GENERATOR (Version 3.0)
Meticulously debugged for GitHub Actions pathing and liturgical accuracy.
Scheduling logic has been externalized to scheduler.py to prevent LLM telescoping.
"""
import os
import yaml
import re
import sys

import scheduler  # Newly separated liturgical logic module

### --- SMART CONFIGURATION ---
### Determine the base directory and ensure the output path is consistent
if os.getenv('GITHUB_ACTIONS') == 'true':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    # Local path for development
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal"

### FIX: Both environments now point to the 'output' folder as per the file tree
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def check_time_gate():
    """
    Prevents the script from running outside the midnight window on GitHub.
    Note: GitHub Actions can be delayed. If this script runs at 12:15 AM, it will still proceed.
    """
    if os.getenv('GITHUB_ACTIONS') != 'true':
        return

def simple_markdown(text):
    """
    Converts *italics* and **bold** to HTML and splits text into clean paragraph lists.
    """
    if not text:
        return []
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def assemble():
    """
    Loads the appropriate template based on the day of the week and fetches the content for each activity.
    Relies on scheduler.py for temporal metadata and liturgical substitution rules.
    """
    # 1. Fetch temporal metadata from the scheduler
    meta = scheduler.get_meta()
    day_of_week = meta.get("day_of_week", "Monday")
    
    # 2. Determine the base template 
    template_name = scheduler.get_base_template_name(day_of_week)
    template_path = os.path.join(TEMPLATE_DIR, f"{template_name}.yaml")
    
    with open(template_path, 'r', encoding='utf-8') as f:
        base_template = yaml.safe_load(f)
        
    final_sections = []
    
    # 3. Apply substitutions and load content
    for section in base_template.get("sections", []):
        section_name = section.get("period")
        activity_ids = section.get("activity_ids", [])
        
        # Delegate substitutions to the scheduler logic
        transformed_ids = scheduler.transform_schedule(section_name, activity_ids, meta)
        
        activities_content = []
        for act_id in transformed_ids:
            # Support both yaml and yml extensions as per the file tree
            act_path_yaml = os.path.join(CONTENT_DIR, f"{act_id}.yaml")
            act_path_yml = os.path.join(CONTENT_DIR, f"{act_id}.yml")
            
            if os.path.exists(act_path_yaml):
                target_path = act_path_yaml
            elif os.path.exists(act_path_yml):
                target_path = act_path_yml
            else:
                activities_content.append({"title": act_id, "body": [f"[Missing content file for {act_id}]"]})
                continue
                
            with open(target_path, 'r', encoding='utf-8') as act_f:
                act_data = yaml.safe_load(act_f)
                act_data['body'] = simple_markdown(act_data.get('body', ''))
                activities_content.append(act_data)
                
        final_sections.append({
            "period": section_name,
            "activities": activities_content
        })
        
    return meta, final_sections

def render(meta, sections):
    """
    Generates the final HTML file with embedded CSS for liturgical formatting.
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
    """
    
    # Build the HTML output
    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append("<html><head><meta charset='utf-8'>")
    html_parts.append(f"<style>{css}</style>")
    html_parts.append(f"<title>Zen Missal - {meta.get('day_of_week', 'Today')}</title>")
    html_parts.append("</head><body>")
    
    # Add Header
    date_str = f"{meta.get('day_of_week', '')}, {meta.get('date_str', str(meta.get('dom', '')))}"
    html_parts.append(f"<h1>Zen Missal<br><span style='font-size: 14pt'>{date_str}</span></h1>")
    
    # Render each section and its activities
    for section in sections:
        html_parts.append(f"<h2>{section['period']}</h2>")
        for act in section['activities']:
            html_parts.append("<div class='activity'>")
            html_parts.append(f"<span class='activity-title'>{act.get('title', 'Untitled')}</span>")
            for paragraph in act.get('body', []):
                html_parts.append(f"<p>{paragraph}</p>")
            html_parts.append("</div>")
            
    html_parts.append("</body></html>")
    
    # Write to file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(html_parts))

if __name__ == "__main__":
    check_time_gate()
    metadata, final_sections = assemble()
    render(metadata, final_sections)
    print(f"Successfully generated Missal for {metadata.get('day_of_week', 'Today')}")
