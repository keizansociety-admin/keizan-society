"""
WEB_GENERATOR.PY
Generates a ritual-centered, accessible Markdown post for the Keizan Society.

PURPOSE:
    Converts the structured schedule data into a production-ready web page.
    Implements dyslexia-aware typography, semantic HTML5, and a calm, 
    spacious visual hierarchy.

REVISION HISTORY:
    2025-01-24: Complete redesign for accessibility and ritual pacing.
                - Added 'At a Glance' summary card.
                - Implemented collapsible <details> for long chants.
                - Added comprehensive CSS for dyslexia support.
                - Standardized three-level hierarchy (Block > Section > Action).
                - Added Ritual Symbol Legend.

MAINTAINER:
    Senior Full-Stack Developer / Keizan Society Technical Editor
"""

import os
from datetime import date
from everyday_shingi_schedule import generate_daily_schedule

def generate_css():
    """Returns the CSS block for the practice page."""
    return """
<style>
    :root {
        --bg: #fdfcf8;        /* Warm off-white */
        --surface: #f4f1ea;   /* Subtle card background */
        --text: #2d2d2d;      /* Near-black */
        --muted: #6b665f;     /* Muted temple-gray */
        --accent: #4a5d6e;    /* Muted indigo */
        --border: #e0dbd1;
        --focus: #d4af37;     /* Gold focus state */
        --max-width: 70ch;
    }

    body {
        background-color: var(--bg);
        color: var(--text);
        font-family: system-ui, -apple-system, sans-serif;
        line-height: 1.65;
        font-size: 1.2rem;
        margin: 0;
        padding: 2rem 1rem;
        display: flex;
        justify-content: center;
    }

    .container {
        max-width: var(--max-width);
        width: 100%;
    }

    /* Typography */
    h1, h2, h3, h4 {
        color: var(--text);
        line-height: 1.2;
        margin-top: 2.5rem;
        font-weight: 600;
    }

    h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.8rem; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; color: var(--accent); }
    h3 { font-size: 1.4rem; margin-top: 2rem; }

    .site-header {
        text-align: left;
        margin-bottom: 3rem;
    }

    .site-header p {
        color: var(--muted);
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-size: 0.9rem;
        margin: 0;
    }

    /* At a Glance Card */
    .glance-card {
        background: var(--surface);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 2rem 0;
        border-left: 4px solid var(--accent);
    }

    .glance-card h4 { margin-top: 0; font-size: 1rem; text-transform: uppercase; color: var(--muted); }
    .glance-list { list-style: none; padding: 0; margin: 0; }
    .glance-list li { margin-bottom: 0.5rem; font-size: 1.1rem; }
    .glance-label { font-weight: bold; color: var(--accent); width: 100px; display: inline-block; }

    /* Ritual Legend */
    .legend {
        font-size: 0.95rem;
        color: var(--muted);
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        margin-bottom: 2rem;
        padding: 1rem;
        background: #fff;
        border: 1px solid var(--border);
        border-radius: 4px;
    }

    /* Practice Sections */
    .time-block { margin-bottom: 4rem; }
    .practice-section { margin-bottom: 2.5rem; }
    
    .action-item { margin-bottom: 1rem; }
    .ritual-text {
        white-space: pre-wrap;
        background: #fff;
        padding: 1.2rem;
        border-radius: 4px;
        border: 1px solid var(--border);
        margin: 1rem 0;
        font-family: inherit;
    }

    .status-note {
        color: var(--muted);
        font-style: italic;
        border-left: 2px solid var(--border);
        padding-left: 1rem;
    }

    /* Collapsible Chants */
    details {
        margin: 1rem 0;
        border: 1px solid var(--border);
        border-radius: 4px;
        background: #fff;
    }

    summary {
        padding: 0.8rem 1.2rem;
        cursor: pointer;
        font-weight: bold;
        color: var(--accent);
        outline: none;
    }

    summary:focus { box-shadow: 0 0 0 3px var(--focus); }

    .annual-observance {
        background: #fdf8e4;
        padding: 1rem;
        border: 1px solid #e6dbac;
        border-radius: 4px;
        margin: 1rem 0;
    }

    .ritual-action {
        font-weight: bold;
        color: #856404;
    }

    /* Accessibility */
    .skip-link {
        position: absolute;
        top: -40px;
        left: 0;
        background: var(--accent);
        color: white;
        padding: 8px;
        z-index: 100;
    }
    .skip-link:focus { top: 0; }

    @media (max-width: 600px) {
        body { font-size: 1.1rem; padding: 1rem; }
        h1 { font-size: 2rem; }
        .glance-label { display: block; margin-bottom: 0.2rem; }
    }
</style>
"""

def format_as_markdown(target_date, data):
    """Converts schedule data into a styled HTML/Markdown hybrid."""
    
    # Date formatting: Saturday · June 6 · Daily Practice
    post_title = target_date.strftime('%A · %B %d · Daily Practice')
    
    md = [
        "---",
        f"title: \"{post_title}\"",
        f"date: {target_date.isoformat()}",
        "layout: post",
        "---\n",
        generate_css(),
        '<a class="skip-link" href="#practice-content">Skip to today’s practice</a>',
        '<header class="site-header">',
        '    <p>Keizan Society</p>',
        '    <h1>Daily Home Practice</h1>',
        '</header>',
        f'<h2 class="daily-title">{post_title}</h2>',
        
        # At a Glance Card
        '<section class="glance-card">',
        '    <h4>Today at a Glance</h4>',
        '    <ul class="glance-list">',
        f'        <li><span class="glance-label">Morning</span> {data["summary"]["morning"]}</li>',
        f'        <li><span class="glance-label">Midday</span> {data["summary"]["midday"]}</li>',
        f'        <li><span class="glance-label">Evening</span> {data["summary"]["evening"]}</li>',
        f'        <li><span class="glance-label">Night</span> {data["summary"]["night"]}</li>',
        '    </ul>',
        '</section>',

        # Legend
        '<div class="legend">',
        *[f'<span><strong>{sym}</strong> {desc}</span>' for sym, desc in data["legend"]],
        '</div>',

        '<main id="practice-content">'
    ]

    for block_name, sections in data["blocks"]:
        md.append(f'<section class="time-block">')
        md.append(f'  <h2>{block_name}</h2>')
        
        for section_name, actions in sections:
            md.append(f'  <div class="practice-section">')
            
            # Handle Cancelled Services
            if "Cancelled" in section_name:
                md.append(f'    <h3 class="status-note">{section_name}</h3>')
            else:
                md.append(f'    <h3>{section_name}</h3>')
            
            for action in actions:
                # Annual Observance Styling
                if action.startswith("ANNUAL OBSERVANCE:"):
                    md.append(f'    <div class="annual-observance"><strong>{action}</strong></div>')
                elif action.startswith("ACTION:"):
                    md.append(f'    <div class="ritual-action">{action}</div>')
                
                # Long Chants / Liturgy (Collapsible)
                elif "\n" in action or len(action) > 200:
                    # Extract first line or title for the summary
                    summary_text = "Show Full Text"
                    if "Maka han-nya" in action: summary_text = "Show Heart Sutra (Sino-Japanese)"
                    elif "Daihishin" in action: summary_text = "Show Great Compassion Dharani"
                    elif "Heart of Great" in action: summary_text = "Show Heart Sutra (English)"
                    elif "Dedication" in action: summary_text = "Show Dedication"
                    
                    md.append(f'    <details>')
                    md.append(f'      <summary>{summary_text}</summary>')
                    md.append(f'      <div class="ritual-text">{action}</div>')
                    md.append(f'    </details>')
                
                # Standard Action Items
                else:
                    md.append(f'    <div class="action-item">{action}</div>')
            
            md.append(f'  </div>')
        md.append(f'</section>')

    md.append('</main>')
    md.append('<footer style="margin-top: 5rem; color: var(--muted); font-size: 0.9rem; border-top: 1px solid var(--border); padding-top: 2rem;">')
    md.append('  <p><em>May this practice benefit all beings throughout the triple world.</em></p>')
    md.append('  <nav><a href="/archive" style="color: var(--accent); text-decoration: none;">View Past Observances</a></nav>')
    md.append('</footer>')
    
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
    
    print(f"[Success] Generated accessible web post: {file_name}")

if __name__ == "__main__":
    main()
