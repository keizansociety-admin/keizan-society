"""
ZEN MISSAL GENERATOR (Version 3.1)
----------------------------------
Meticulously debugged for liturgical formatting and GitHub Actions.
Fix: Ensures Activity Titles and Body text are inline (no line breaks).
"""

import os
import yaml
import re
import sys
import scheduler  # Externalized liturgical logic module

# --- SMART CONFIGURATION ---
# Determine the base directory and ensure the output path is consistent
if os.getenv('GITHUB_ACTIONS') == 'true':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
else:
    # Local path for development (Thonny / Dropbox)
    BASE_DIR = "/Users/jocorsoesquivel/Dropbox/zen_missal"

# Pathing aligned with the provided file tree
OUTPUT_FILE = os.path.join(BASE_DIR, "output", "index.html")
CONTENT_DIR = os.path.join(BASE_DIR, "content", "activities")
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

def check_time_gate():
    """
    Placeholder for time-based execution logic. 
    Currently allows execution to proceed for debugging and manual triggers.
    """
    if os.getenv('GITHUB_ACTIONS') != 'true':
        return

def simple_markdown(text):
    """
    Converts *italics* and **bold** to HTML and splits text into 
    a list of clean paragraphs.
    """
    if not text:
        return []
    # Bold: **text** -> <b>text</b>
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
    # Italics: *text* -> <i>text</i>
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
    # Split by double newlines into a list of paragraphs
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    return paragraphs

def assemble():
    """
    Loads the appropriate template and fetches activity content.
    Relies on scheduler.py for temporal metadata and substitution rules.
    """
    # 1. Fetch temporal metadata (Day of week, rest day status, etc.)
    meta = scheduler.get_meta()
    day_of_week = meta.get("day_of_week", "Monday")
    
    # 2. Determine and load the base template (weekday, weekend, or friday)
    template_name = scheduler.get_base_template_name(day_of_week)
    template_path = os.path.join(TEMPLATE_DIR, f"{template_name}.yaml")
    
    if not os.path.exists(template_path):
        print(f"Error: Template {template_name}.yaml not found.")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        base_template = yaml.safe_load(f)
        
    final_sections = []
    
    # 3. Process sections and apply liturgical substitutions
    for section in base_template.get("sections", []):
        section_name = section.get("period")
        activity_ids = section.get("activity_ids", [])
        
        # Delegate substitution logic to scheduler.py
        transformed_ids = scheduler.transform_schedule(section_name, activity_ids, meta)
        
        activities_content = []
        for act_id in transformed_ids:
            # Check for both .yaml and .yml extensions
            path_yaml = os.path.join(CONTENT_DIR, f"{act_id}.yaml")
            path_yml = os.path.join(CONTENT_DIR, f"{act_id}.yml")
            
            target_path = None
            if os.path.exists(path_yaml):
                target_path = path_yaml
            elif os.path.exists(path_yml):
                target_path = path_yml
            
            if target_path:
                with open(target_path, 'r', encoding='utf-8') as act_f:
                    act_data = yaml.safe_load(act_f)
                    # Convert raw body string into a list of HTML-formatted paragraphs
                    act_data['body'] = simple_markdown(act_data.get('body', ''))
                    activities_content.append(act_data)
            else:
                # Fallback if a content file is missing
                activities_content.append({
                    "title": act_id.replace("_", " ").title(), 
                    "body": [f"[Missing content file for {act_id}]"]
                })
                
        final_sections.append({
            "period": section_name,
            "activities": activities_content
        })
        
    return meta, final_sections

def render(meta, sections):
    """
    Generates the final HTML file.
    UX FIX: Injects the activity title into the first paragraph tag 
    to ensure they stay on the same line.
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
    
    html_parts = []
    html_parts.append("<!DOCTYPE html>")
    html_parts.append("<html><head><meta charset='utf-8'>")
    html_parts.append(f"<style>{css}</style>")
    html_parts.append(f"<title>Zen Missal - {meta.get('day_of_week', 'Today')}</title>")
    html_parts.append("</head><body>")
    
    # Header Section
    date_display = f"{meta.get('day_of_week', '')}, {meta.get('date_str', '')}"
    html_parts.append(f"<h1>Zen Missal<br><span style='font-size: 14pt'>{date_display}</span></h1>")
    
    # Content Sections
    for section in sections:
        if not section['activities']:
            continue
            
        html_parts.append(f"<h2>{section['period']}</h2>")
        
        for act in section['activities']:
            html_parts.append("<div class='activity'>")
            
            paragraphs = act.get('body', [])
            title_html = f"<span class='activity-title'>{act.get('title', 'Untitled')}</span>"
            
            if paragraphs:
                # CRITICAL FORMATTING FIX:
                # Place the title span INSIDE the first <p> tag to keep them inline.
                first_p = paragraphs[0]
                html_parts.append(f"<p>{title_html}{first_p}</p>")
                
                # Render any remaining paragraphs normally
                for other_p in paragraphs[1:]:
                    html_parts.append(f"<p>{other_p}</p>")
            else:
                # Fallback if body is empty
                html_parts.append(f"<p>{title_html}</p>")
                
            html_parts.append("</div>")
            
    html_parts.append("</body></html>")
    
    # Ensure output directory exists and write file
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
        out_f.write("\n".join(html_parts))

if __name__ == "__main__":
    # 1. Check if we are allowed to run
    check_time_gate()
    
    # 2. Build the data structure
    metadata, final_sections = assemble()
    
    # 3. Generate the HTML file
    render(metadata, final_sections)
    
    # 4. Confirmation for local debugging (Thonny)
    print(f"Successfully generated Missal for {metadata.get('day_of_week', 'Today')}")
