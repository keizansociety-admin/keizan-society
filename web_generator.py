"""
WEB_GENERATOR.PY
Generates a Markdown blog post for the Keizan Society website.
This script is designed to be run automatically by GitHub Actions.
"""

import os
from datetime import date
from everyday_shingi_schedule import generate_daily_schedule

def format_as_markdown(target_date, schedule_data):
    """
    Converts the schedule logic into a clean Markdown blog post.
    Includes Jekyll-compatible front matter.
    """
    post_title = target_date.strftime('%A, %B %d, %Y')
    
    # Front Matter for the website
    md = [
        "---",
        f"title: \"Daily Practice: {post_title}\"",
        f"date: {target_date.isoformat()}",
        "layout: post",
        "---\n",
        f"# {post_title}\n",
        "Welcome to today's practice. Follow the steps below to align your day with the Keizan Shingi.\n"
    ]

    for title, items in schedule_data:
        md.append(f"## {title.upper()}")
        if not items:
            md.append("*Standard activity*\n")
            continue
            
        for item in items:
            # Apply CSS-ready classes for the hanging indent on the web
            if item.startswith("ANNUAL OBSERVANCE:"):
                md.append(f"\n> ### {item}\n")
            elif item.startswith("ACTION:") or "HOSAN" in item or "KAISEI" in item:
                md.append(f"<div class='ritual-action'><strong>{item}</strong></div>")
            elif item.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.")):
                md.append(f"<div class='liturgy-step'>{item}</div>")
            else:
                md.append(f"<div class='verse-item'>{item}</div>")
        md.append("") # Spacer between sections

    md.append("\n---\n")
    md.append("*May this practice benefit all beings throughout the triple world.*")
    
    return "\n".join(md)

def main():
    # 1. Determine the date (Today)
    today = date.today()
    
    # 2. Generate the schedule using the core logic engine
    schedule = generate_daily_schedule(today)
    
    # 3. Convert to Markdown format
    markdown_content = format_as_markdown(today, schedule)
    
    # 4. Ensure the output directory exists (standard for Jekyll/Hugo)
    output_dir = "_posts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 5. Save the file with the standard naming convention: YYYY-MM-DD-title.md
    file_name = f"{output_dir}/{today.isoformat()}-daily-practice.md"
    
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"[Success] Generated web post: {file_name}")

if __name__ == "__main__":
    main()