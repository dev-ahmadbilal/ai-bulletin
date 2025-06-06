import json
from pydantic import BaseModel
from crewai.flow import Flow, listen, start

from crew.ai_bulletin_crew import AIBulletinCrew


class AIBulletinState(BaseModel):
    newsletter_topics: dict = {}


class AIBulletinFlow(Flow[AIBulletinState]):

    @start()
    def kickoff_newsletter_generation(self):
        print("🚀 Starting AI Bulletin Crew")
        result = (
            AIBulletinCrew()
            .crew()
            .kickoff(inputs={})
        )

        # Extract output from result
        if hasattr(result, 'output'):
            print("✅ Newsletter generated successfully")
            self.state.newsletter_topics = result.output
        else:
            print("⚠️ No output returned.")
            self.state.newsletter_topics = {}

    @listen(kickoff_newsletter_generation)
    def save_final_output(self):
        print("💾 Saving final newsletter output...")
        with open("newsletter_final.json", "w") as f:
            json.dump(self.state.newsletter_topics, f, indent=2, default=str)
        print("📁 Final output saved to newsletter_final.json")


def kickoff():
    AIBulletinFlow().kickoff()


def plot():
    AIBulletinFlow().plot()


if __name__ == "__main__":
    kickoff()