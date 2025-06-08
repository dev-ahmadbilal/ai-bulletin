import json
from datetime import datetime
from pydantic import BaseModel
from crewai.flow import Flow, listen, start
from crew.ai_bulletin_crew import AIBulletinCrew
from crew.newsletter_storage import store_newsletter_data, get_previous_topics


class AIBulletinState(BaseModel):
    newsletter_topics: dict = {}
    newsletter_html: str = ""


class AIBulletinFlow(Flow[AIBulletinState]):

    @start()
    def kickoff_newsletter_generation(self):
        print("🚀 Starting AI Bulletin Crew")
        
        # Get previous topics using the storage function
        previous_topics = get_previous_topics()
        
        # Start crew with previous topics
        crew = AIBulletinCrew().crew()
        inputs = {
            "previous_topics": previous_topics
        }
        result = crew.kickoff(inputs=inputs)
        
        print("\n📊 Crew Execution Result:")
        print(f"Result type: {type(result)}")
        print(f"Result attributes: {dir(result)}")
        
        # Extract output from result
        if hasattr(result, 'output'):
            print("\n✅ Newsletter generated successfully")
            print(f"Output type: {type(result.output)}")
            print(f"Output content: {result.output}")
            self.state.newsletter_topics = result.output
        elif hasattr(result, 'raw_output'):
            print("\n✅ Newsletter generated successfully (raw output)")
            print(f"Raw output type: {type(result.raw_output)}")
            print(f"Raw output content: {result.raw_output}")
            self.state.newsletter_topics = result.raw_output
        else:
            print("\n⚠️ No output returned.")
            print("Available result data:")
            print(result)
            self.state.newsletter_topics = {}

    @listen(kickoff_newsletter_generation)
    def save_final_output(self):
        print("\n💾 Saving final newsletter output...")
        
        # Generate current week identifier (YYYY-Www format)
        current_date = datetime.now()
        week_number = current_date.isocalendar()[1]
        week = f"{current_date.year}-W{week_number:02d}"
        
        # Read the HTML output from the formatter's output file
        try:
            with open("outputs/01_newsletter_topics.json", "r") as f:
                topics_json = json.load(f)

            with open("outputs/10_newsletter_final.html", "r") as f:
                final_html = f.read()
                
            # Clean HTML by removing markdown code fences
            topics_json = json.dumps(topics_json)
            final_html = final_html.replace("```html", "").replace("```", "").strip()
            
        except FileNotFoundError:
            print("⚠️ HTML output file not found")
            final_html = ""
        
        # Store in SQLite database
        result = store_newsletter_data(week, topics_json, final_html)
        print(result)


def kickoff():
    AIBulletinFlow().kickoff()


def plot():
    AIBulletinFlow().plot()


if __name__ == "__main__":
    kickoff()