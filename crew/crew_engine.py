# crew_engine.py
import json
from datetime import datetime
from crew.ai_bulletin_crew import AIBulletinCrew
from crew.newsletter_storage import store_newsletter_data

def run_newsletter_pipeline():
    print("🚀 Starting AI Bulletin Crew")
    
    # Kick off the crew
    crew = AIBulletinCrew().crew()
    result = crew.kickoff(inputs={})
    
    print("\n📊 Crew Execution Result:")
    print(f"Result type: {type(result)}")
    print(f"Result attributes: {dir(result)}")

    # Try extracting output
    if hasattr(result, 'output'):
        print("✅ Newsletter generated successfully via 'output'")
        newsletter_topics = result.output
    elif hasattr(result, 'raw_output'):
        print("✅ Newsletter generated successfully via 'raw_output'")
        newsletter_topics = result.raw_output
    else:
        print("⚠️ No usable output found in result.")
        newsletter_topics = {}

    # Current week
    current_date = datetime.now()
    week_number = current_date.isocalendar()[1]
    week = f"{current_date.year}-W{week_number:02d}"

    # Read generated HTML from file
    try:
        with open("outputs/10_newsletter_final.html", "r") as f:
            final_html = f.read()
    except FileNotFoundError:
        print("⚠️ Could not find final HTML file at outputs/10_newsletter_final.html")
        final_html = ""

    # Store newsletter in DB
    topics_json = json.dumps(newsletter_topics)
    store_result = store_newsletter_data(week, topics_json, final_html)
    print("💾 Store Result:", store_result)

    return {
        "week": week,
        "topics_json": topics_json,
        "final_html": final_html
    }