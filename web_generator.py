"""
WEB_GENERATOR.PY
Generates a ritual-centered, accessible Markdown post for the Keizan Society.

PURPOSE:
    Converts structured schedule data into a production-ready digital service book.
    Implements dyslexia-aware typography, ritual-action cues, and 
    progressive disclosure for long liturgical texts.

REVISION HISTORY:
    2026-06-06: Initial creation of the web generator.
    2026-06-06: Graphic redesign for dyslexia-aware ritual use.
                - Implemented "Service Mode" UI with line-tracking for chants.
                - Added mobile-first responsive CSS with 20px base font.
                - Fixed duplicated header/footer logic.
                - Implemented specific labeling for all collapsible sections.
                - Added distinct styling for ritual action cues (bells/bows).

MAINTAINER:
    Senior Full-Stack Developer / Keizan Society Technical Editor
"""

import os
from datetime import date
from everyday_shingi_schedule import generate_daily_schedule

def generate_css():
    """Returns the CSS block optimized for dyslexia and ritual use."""
    return """
<style>
    :root {
        --bg: #fdfcf8;
        --surface: #f4f1ea;
        --text: #2d2d2d;
        --muted: #6b665f;
        --accent: #4a5d6e;
        --border: #e0dbd1;
        --focus: #d4af37;
        --ritual: #856404;
        --max-width: 70ch;
    }

    /* Dyslexia-Aware Typography */
    body {
        background-color: var(--bg);
        color: var(--text);
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        line-height: 1.7;
        font-size: 20px; /* Large base for mobile/iPad */
        margin: 0;
        padding: 0;
        text-align: left;
    }

    .container {
        max-width: var(--max-width);
        margin: 0 auto;
        padding: 1.5rem;
    }

    h1, h2, h3, h4 {
        line-height: 1.3;
        margin-top: 2rem;
        font-weight: 600;
        text-align: left;
    }

    h2 { font-size: 1.8rem; color: var(--accent); border-bottom: 2px solid var(--border); padding-bottom: 0.5rem; }
    h3 { font-size: 1.4rem; margin-top: 1.5rem; }

    /* Service Mode Components */
    .glance-card {
        background: var(--surface);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        border-left: 6px solid var(--accent);
    }

    .glance-list { list-style: none; padding: 0; margin: 0; font-size: 0.9rem; }
    .glance-label { font-weight: bold; color: var(--accent); display: inline-block; width: 80px; }

    .ritual-cue {
        background: #fff;
        border: 2px solid var(--border);
        border-left: 5px solid var(--focus);
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 8px;
        font-weight: 500;
        color: var(--ritual);
    }

    /* Chant Line Viewer */
    .chant-container {
        margin: 1.5rem 0;
        padding-left: 0.5rem;
    }

    .chant-line {
        margin-bottom: 0.75rem;
        padding: 0.2rem 0.5rem;
        border-left: 3px solid transparent;
        transition: background 0.2s;
    }

    /* Tap-to-highlight support for place-keeping */
    .chant-line:active, .chant-line:hover {
        background: #f0ede4;
        border-left: 3px solid var(--focus);
    }

    /* Collapsibles */
    details {
        margin: 1rem 0;
        border: 2px solid var(--border);
        border-radius: 12px;
        background: #fff;
        overflow: hidden;
    }

    summary {
        padding: 1rem;
        cursor: pointer;
        font-weight: bold;
        color: var(--accent);
        list-style: none;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    summary::-webkit-details-marker { display: none; }
    summary::after { content: "＋"; font-size: 1.2rem; }
    details[open] summary::after { content: "－"; }
    summary:focus { background: var(--surface); outline: none; }

    .step-header {
        display: flex;
        align-items: baseline;
        gap: 0.75rem;
    }

    .step-number {
        background: var(--accent);
        color: #fff;
        font-size: 0.9rem;
        width: 1.8rem;
        height: 1.8rem;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
        flex-shrink: 0;
    }

    @media (max-width: 600px) {
        body { font-size: 18px; }
        .container { padding: 1rem; }
    }
</style>
"""

def render_item(item):
    """Renders a single liturgical or instructional item into HTML."""
    # Handle simple strings (Verses)
    if isinstance(item, str):
        return f'<div class="action-item">{item}</div>'

    # Handle structured dictionaries
    item_type = item.get("type")
    
    # 1. Ritual Action Cues (Bells, Bows, Instructions)
    if item_type in ["instruction", "ritual", "transition"]:
        return f'<div class="ritual-cue">{item.get("content")}</div>'

    # 2. Annual Observance
    if item_type == "annual":
        return f'<div class="ritual-cue" style="border-color: var(--accent);"><strong>{item.get("content")}</strong></div>'

    # 3. Chants and Dedications (Collapsible)
    if "chant_lines" in item or "data" in item:
        # Extract data if nested
        data = item.get("data", item)
        label = data.get("label", "Show Text")
        title = data.get("title", "")
        lines = data.get("chant_lines", [])
        
        # Build the header
        header_html = ""
        if "step" in item:
            header_html = f'<div class="step-header"><span class="step-number">{item["step"]}</span> <h3>{title or label.replace("Show ", "")}</h3></div>'
        elif title:
            header_html = f'<h3>{title}</h3>'

        # Build the collapsible content
        content_html = '<div class="chant-container">'
        for line in lines:
            content_html += f'<div class="chant-line">{line}</div>'
        content_html += '</div>'

        return f'{header_html}<details><summary>{label}</summary>{content_html}</details>'

    return ""

def format_as_markdown(target_date, data):
    """Converts schedule data into the final Service Mode Markdown."""
    post_title = target_date.strftime('%A · %B %d')
    
    md = [
        "---",
        f"title: \"{post_title}\"",
        f"date: {target_date.isoformat()}",
        "layout: post",
        "---\n",
        generate_css(),
        '<div class="container">',
        f'<h2 class="daily-title">{post_title} · Daily Practice</h2>',
        
        # At a Glance
        '<section class="glance-card">',
        '    <ul class="glance-list">',
        f'        <li><span class="glance-label">Morning</span> {data["summary"]["morning"]}</li>',
        f'        <li><span class="glance-label">Midday</span> {data["summary"]["midday"]}</li>',
        f'        <li><span class="glance-label">Evening</span> {data["summary"]["evening"]}</li>',
        f'        <li><span class="glance-label">Night</span> {data["summary"]["night"]}</li>',
        '    </ul>',
        '</section>',

        '<main id="service-mode">'
    ]

    for block_name, sections in data["blocks"]:
        md.append(f'<section class="time-block">')
        md.append(f'  <h2>{block_name}</h2>')
        
        for section_name, actions in sections:
            md.append(f'  <article class="practice-section">')
            md.append(f'    <h3>{section_name}</h3>')
            
            for action in actions:
                md.append(render_item(action))
            
            md.append(f'  </article>')
        md.append(f'</section>')

    md.append('</main>')
    
    # Unified Footer (No duplication)
    md.append('<footer style="margin-top: 4rem; padding-top: 2rem; border-top: 2px solid var(--border); color: var(--muted); font-size: 0.9rem;">')
    md.append('  <p><em>May this practice benefit all beings throughout the triple world.</em></p>')
    md.append('  <nav><a href="/" style="color: var(--accent);">Return to Today</a> · <a href="/archive" style="color: var(--accent);">Past Observances</a></nav>')
    md.append('</footer>')
    md.append('</div>')
    
    return "\n".join(md)

def main():
    today = date.today()
    schedule_data = generate_daily_schedule(today)
    markdown_content = format_as_markdown(today, schedule_data)
    
    output_dir = "_posts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    file_name = f"{output_dir}/{today.isoformat()}-daily-practice.md"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"[Success] Generated Service Mode post: {file_name}")

if __name__ == "__main__":
    main()
