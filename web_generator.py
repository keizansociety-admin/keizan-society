"""
WEB_GENERATOR.PY
Generates a ritual-centered, accessible Markdown post for the Keizan Society.

REVISION HISTORY:
    2026-06-06: Initial creation.
    2026-06-06: BUGFIX: Explicit UTC-to-Local conversion for rollover.
    2026-06-06: BUGFIX: Merged Step Numbers into Ritual Action Cards to remove redundancy.
"""

import os
from datetime import datetime, timedelta, timezone
from everyday_shingi_schedule import generate_daily_schedule

# CONFIGURATION: Set to Eastern Time (UTC-4 for June/Daylight Time)
LOCAL_OFFSET = timezone(timedelta(hours=-4))

def generate_css():
    return """
<style>
    :root {
        --bg: #fdfcf8; --surface: #f4f1ea; --text: #2d2d2d; --muted: #6b665f;
        --accent: #4a5d6e; --border: #e0dbd1; --focus: #d4af37; --ritual: #856404;
        --max-width: 70ch;
    }
    body { background-color: var(--bg); color: var(--text); font-family: system-ui, sans-serif; line-height: 1.7; font-size: 20px; margin: 0; padding: 0; }
    .container { max-width: var(--max-width); margin: 0 auto; padding: 1.5rem; }
    
    /* Typography */
    h1 { font-size: 2rem; color: var(--text); margin-bottom: 0.5rem; }
    h2 { font-size: 1.6rem; color: var(--accent); border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; margin-top: 3rem; }
    h3 { font-size: 1.3rem; margin-top: 2rem; color: var(--muted); text-transform: uppercase; letter-spacing: 0.05em; }

    /* Ritual Action Cards */
    .ritual-cue { background: #fff; border: 2px solid var(--border); border-left: 5px solid var(--focus); padding: 1rem; margin: 1rem 0; border-radius: 8px; color: var(--ritual); font-weight: 500; }
    .action-item { margin-bottom: 1.2rem; display: block; }
    
    /* Collapsible Chants (Merged Step + Label) */
    details { margin: 1rem 0; border: 2px solid var(--border); border-radius: 12px; background: #fff; }
    summary { padding: 1rem; cursor: pointer; font-weight: bold; color: var(--accent); display: flex; align-items: center; gap: 1rem; }
    summary:focus { outline: none; background: var(--surface); }
    
    .step-badge { background: var(--accent); color: #fff; font-size: 0.8rem; width: 1.6rem; height: 1.6rem; display: flex; align-items: center; justify-content: center; border-radius: 50%; flex-shrink: 0; }

    .chant-line { margin-bottom: 0.75rem; padding: 0.2rem 0.5rem; border-left: 3px solid transparent; }
    .chant-line:active { background: #f0ede4; border-left: 3px solid var(--focus); }

    /* At a Glance */
    .glance-card { background: var(--surface); padding: 1.5rem; border-radius: 12px; border-left: 6px solid var(--accent); margin: 2rem 0; }
    .glance-list { list-style: none; padding: 0; margin: 0; font-size: 0.95rem; }
    .glance-label { font-weight: bold; color: var(--accent); width: 90px; display: inline-block; }
</style>
"""

def render_item(item):
    if isinstance(item, str):
        return f'<span class="action-item">{item}</span>'

    item_type = item.get("type")
    if item_type in ["instruction", "ritual", "transition", "annual"]:
        return f'<div class="ritual-cue">{item.get("content")}</div>'

    if "chant_lines" in item or "data" in item:
        data = item.get("data", item)
        label = data.get("label", "Show Text")
        title = data.get("title", "")
        lines = data.get("chant_lines", [])
        
        # Merge Step Number and Label into the Summary
        summary_content = ""
        if "step" in item:
            summary_content += f'<span class="step-badge">{item["step"]}</span> '
        
        # Use the most descriptive label available
        display_label = title if title else label.replace("Show ", "").replace("Open ", "")
        summary_content += f'<span>{display_label}</span>'

        content_html = '<div class="chant-container" style="padding: 1rem; border-top: 1px solid var(--border);">'
        for line in lines:
            content_html += f'<div class="chant-line">{line}</div>'
        content_html += '</div>'

        return f'<details><summary>{summary_content}</summary>{content_html}</details>'
    return ""

def format_as_markdown(target_date, data):
    post_title = target_date.strftime('%A · %B %d')
    md = [
        "---",
        f"title: \"{post_title}\"",
        f"date: {target_date.isoformat()}",
        "layout: post",
        "---\n",
        generate_css(),
        '<div class="container">',
        f'<h1>{post_title} · Daily Practice</h1>',
        '<section class="glance-card"><ul class="glance-list">',
        f'<li><span class="glance-label">Morning</span> {data["summary"]["morning"]}</li>',
        f'<li><span class="glance-label">Midday</span> {data["summary"]["midday"]}</li>',
        f'<li><span class="glance-label">Evening</span> {data["summary"]["evening"]}</li>',
        f'<li><span class="glance-label">Night</span> {data["summary"]["night"]}</li></ul></section>',
        '<main>'
    ]
    
    for block_name, sections in data["blocks"]:
        md.append(f'<section><h2>{block_name}</h2>')
        for section_name, actions in sections:
            md.append(f'<article><h3>{section_name}</h3>')
            for action in actions:
                md.append(render_item(action))
            md.append('</article>')
        md.append('</section>')
    
    md.append('</main><footer style="margin-top: 5rem; color: var(--muted); font-style: italic; border-top: 1px solid var(--border); padding-top: 2rem;">May this practice benefit all beings throughout the triple world.</footer></div>')
    return "\n".join(md)

def main():
    # FIX: Explicitly convert UTC now to Local Timezone before extracting the date
    today = datetime.now(timezone.utc).astimezone(LOCAL_OFFSET).date()
    
    schedule_data = generate_daily_schedule(today)
    markdown_content = format_as_markdown(today, schedule_data)
    
    output_dir = "_posts"
    if not os.path.exists(output_dir): os.makedirs(output_dir)
    file_name = f"{output_dir}/{today.isoformat()}-daily-practice.md"
    with open(file_name, "w", encoding="utf-8") as f: f.write(markdown_content)
    print(f"[Success] Generated for {today}: {file_name}")

if __name__ == "__main__": main()
