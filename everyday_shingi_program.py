"""
EVERYDAY_SHINGI_PROGRAM.PY
The primary entry point for the Keizan Society Daily Schedule (CLI).

PURPOSE:
    Provides a local terminal interface to view the daily practice schedule.
    Reflects the three-level hierarchy (Time Block > Section > Action) 
    and provides a high-readability layout for practitioners.

REVISION HISTORY:
    2026-06-06: Initial creation of the CLI program.
    2026-06-06: Refactored for structured data compatibility.
                - Added support for dictionary-based liturgical items.
                - Implemented line-by-line rendering for chants.
                - Added ritual-cue highlighting for terminal use.
                - Integrated step-numbering into the terminal display.

MAINTAINER:
    Senior Full-Stack Developer / Keizan Society Technical Editor
"""

import sys
import textwrap
from datetime import datetime, date, timedelta
from everyday_shingi_schedule import generate_daily_schedule

def print_liturgy(item, indent=6, width=72):
    """
    Prints structured liturgical items (chants/dedications) 
    line-by-line for ritual pacing.
    """
    # Extract data if nested in a 'data' key
    data = item.get("data", item)
    lines = data.get("chant_lines", [])
    label = data.get("label", "Liturgical Text")
    
    print(f"\n{' ' * indent}--- {label} ---")
    for line in lines:
        # Hanging indent for long lines within a chant
        wrapper = textwrap.TextWrapper(
            width=width,
            initial_indent=" " * (indent + 2),
            subsequent_indent=" " * (indent + 4)
        )
        print(wrapper.fill(line))
    print(' ' * indent + "-" * (len(label) + 8) + "\n")

def print_action(action, indent=4, width=72):
    """
    Prints a single action item, handling both strings and structured dicts.
    """
    # 1. Handle Step Numbering
    prefix = "· "
    if isinstance(action, dict) and "step" in action:
        prefix = f"[{action['step']}] "

    # 2. Handle Structured Content
    if isinstance(action, dict):
        item_type = action.get("type")
        
        # Ritual Cues / Instructions
        if item_type in ["instruction", "ritual", "transition", "annual"]:
            content = action.get("content", "")
            marker = ">>> " if item_type == "ritual" else "[!] "
            print(f"\n{' ' * indent}{marker}{content.upper()}")
            
        # Chants / Dedications
        elif "chant_lines" in action or "data" in action:
            print_liturgy(action, indent=indent+2, width=width)
            
    # 3. Handle Simple Strings (Verses)
    else:
        wrapper = textwrap.TextWrapper(
            width=width, 
            initial_indent=" " * indent + prefix, 
            subsequent_indent=" " * (indent + len(prefix))
        )
        print(wrapper.fill(action))

def main():
    print("\nKeizan Society · Lay Zen Practice Planner")
    print("=" * 42)
    user_input = input("Enter date (YYYY-MM-DD) or press [Enter] for today: ").strip()
    
    try:
        current_date = datetime.strptime(user_input, "%Y-%m-%d").date() if user_input else date.today()
    except ValueError:
        print("\n[!] Invalid date format. Defaulting to today.")
        current_date = date.today()

    while True:
        data = generate_daily_schedule(current_date)
        
        print(f"\n\n{'#'*80}")
        print(f" SERVICE BOOK: {current_date.strftime('%A, %B %d, %Y')}")
        print(f"{'#'*80}")

        # 1. AT A GLANCE SUMMARY
        print("\nTODAY AT A GLANCE")
        print("-" * 20)
        for period, desc in data["summary"].items():
            print(f"  {period.capitalize():<10} : {desc}")

        # 2. MAIN CONTENT HIERARCHY
        for block_name, sections in data["blocks"]:
            print(f"\n\n{block_name.upper()}")
            print("=" * len(block_name))
            
            for section_name, actions in sections:
                print(f"\n  {section_name}")
                print("  " + "-" * len(section_name))
                
                if not actions:
                    print("    (Standard mindful activity)")
                    continue
                
                for action in actions:
                    print_action(action)

        print(f"\n\n{'='*80}")
        print(" OPTIONS: [Enter] Tomorrow | [YYYY-MM-DD] Specific Date | [Q] Quit")
        nav = input(" >> ").strip().lower()
        
        if nav == 'q': 
            break
        elif not nav: 
            current_date += timedelta(days=1)
        else:
            try: 
                current_date = datetime.strptime(nav, "%Y-%m-%d").date()
            except ValueError: 
                print("\n[!] Invalid date format. Please use YYYY-MM-DD.")

if __name__ == "__main__":
    main()
