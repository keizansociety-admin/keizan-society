"""
EVERYDAY_SHINGI_PROGRAM.PY
The primary entry point for the Keizan Society Daily Schedule.
"""

import sys
import textwrap
from datetime import datetime, date, timedelta
from everyday_shingi_schedule import generate_daily_schedule

def print_bullet(text, bullet="- ", indent=3, width=75):
    """
    Prints text with a hanging indent. 
    The first line gets the bullet; subsequent lines align with the start of the text.
    """
    initial_indent = " " * indent + bullet
    subsequent_indent = " " * (indent + len(bullet))
    wrapper = textwrap.TextWrapper(
        width=width, 
        initial_indent=initial_indent, 
        subsequent_indent=subsequent_indent
    )
    print(wrapper.fill(text))

def main():
    print("\nSoto Zen Lay Practice Planner")
    print("-" * 30)
    user_input = input("Enter date (YYYY-MM-DD) or press [Enter] for today: ").strip()
    
    try:
        current_date = datetime.strptime(user_input, "%Y-%m-%d").date() if user_input else date.today()
    except ValueError:
        print("\n[!] Invalid date format. Defaulting to today.")
        current_date = date.today()

    while True:
        print(f"\n{'='*80}")
        print(f"LAY ZEN DAILY PRACTICE SHEET: {current_date.strftime('%A, %B %d, %Y')}")
        print(f"{'='*80}")

        daily_steps = generate_daily_schedule(current_date)
        
        for title, items in daily_steps:
            print(f"\n{title.upper()}")
            if not items:
                print("   (Standard activity)")
            for item in items:
                # Check if the item is a numbered list item for specific formatting
                if item.strip().startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "10.", "11.")): 
                    print_bullet(item, bullet="  ", indent=5)
                # Highlight Annual Observance headers
                elif item.startswith("ANNUAL OBSERVANCE:"):
                    print(f"\n    *** {item} ***")
                # Highlight specific Actions (including Hosan/Kaisei instructions)
                elif item.startswith("ACTION:") or "HOSAN" in item or "KAISEI" in item:
                    print_bullet(item, bullet="[!] ", indent=3)
                else: 
                    print_bullet(item)

        print(f"\n{'='*80}")
        print("OPTIONS: [Enter] for tomorrow | [YYYY-MM-DD] for specific date | [Q] to quit")
        nav = input(">> ").strip().lower()
        
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