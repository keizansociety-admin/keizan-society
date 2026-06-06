"""
EVERYDAY_SHINGI_PROGRAM.PY
The primary entry point for the Keizan Society Daily Schedule (CLI).

PURPOSE:
    Provides a local terminal interface to view the daily practice schedule.
    Reflects the three-level hierarchy (Time Block > Section > Action) 
    and provides a high-readability layout for practitioners.

REVISION HISTORY:
    2025-01-24: Refactored to support the new structured data dictionary.
                - Added 'At a Glance' summary display.
                - Added Ritual Symbol Legend display.
                - Implemented nested loops for Block/Section/Action hierarchy.
                - Optimized terminal spacing for dyslexia-friendly reading.

MAINTAINER:
    Senior Full-Stack Developer / Keizan Society Technical Editor
"""

import sys
import textwrap
from datetime import datetime, date, timedelta
from everyday_shingi_schedule import generate_daily_schedule

def print_bullet(text, bullet="- ", indent=4, width=72):
    """
    Prints text with a hanging indent. 
    Handles multi-line strings (chants) by preserving their internal line breaks.
    """
    lines = text.split('\n')
    initial_indent = " " * indent + bullet
    subsequent_indent = " " * (indent + len(bullet))
    
    wrapper = textwrap.TextWrapper(
        width=width, 
        initial_indent=initial_indent, 
        subsequent_indent=subsequent_indent,
        replace_whitespace=False # Preserves our ritual line breaks
    )
    
    for line in lines:
        if line.strip():
            print(wrapper.fill(line))

def main():
    print("\nSoto Zen Lay Practice Planner")
    print("=" * 30)
    user_input = input("Enter date (YYYY-MM-DD) or press [Enter] for today: ").strip()
    
    try:
        current_date = datetime.strptime(user_input, "%Y-%m-%d").date() if user_input else date.today()
    except ValueError:
        print("\n[!] Invalid date format. Defaulting to today.")
        current_date = date.today()

    while True:
        data = generate_daily_schedule(current_date)
        
        print(f"\n\n{'#'*80}")
        print(f" LAY ZEN DAILY PRACTICE: {current_date.strftime('%A, %B %d, %Y')}")
        print(f"{'#'*80}")

        # 1. AT A GLANCE SUMMARY
        print("\nTODAY AT A GLANCE")
        print("-" * 20)
        for period, desc in data["summary"].items():
            print(f"  {period.capitalize():<10} : {desc}")

        # 2. RITUAL LEGEND
        print("\nRITUAL SYMBOLS")
        print("-" * 20)
        for sym, desc in data["legend"]:
            print(f"  {sym}  {desc}")

        # 3. MAIN CONTENT HIERARCHY
        for block_name, sections in data["blocks"]:
            print(f"\n\n{block_name.upper()}")
            print("=" * len(block_name))
            
            for section_name, actions in sections:
                print(f"\n  {section_name}")
                print("  " + "-" * len(section_name))
                
                if not actions:
                    print("    (Standard activity)")
                    continue
                
                for action in actions:
                    # Highlight Annual Observances
                    if action.startswith("ANNUAL OBSERVANCE:"):
                        print(f"\n    *** {action} ***")
                    # Highlight specific Ritual Actions
                    elif action.startswith("ACTION:"):
                        print_bullet(action, bullet="[!] ", indent=4)
                    # Standard Actions or Chants
                    else:
                        # If it's a long chant (multi-line), give it more space
                        if "\n" in action:
                            print("\n")
                            print_bullet(action, bullet="  ", indent=6)
                            print("\n")
                        else:
                            print_bullet(action, bullet="· ", indent=6)

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
