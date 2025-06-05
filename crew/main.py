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

        # Extract structured topics from result
        output = result.output if hasattr(result, "output") else None

        if output and hasattr(output, "topics"):
            print("✅ Newsletter topics generated:")
            print(output)
            self.state.newsletter_topics = output
        else:
            print("⚠️ No topics returned or format mismatch.")
            self.state.newsletter_topics = []

    @listen(kickoff_newsletter_generation)
    def save_topics_to_file(self):
        print("💾 Saving newsletter content to 'newsletter_output.json'...")
        with open("newsletter_output.json", "w") as f:
            json.dump(self.state.newsletter_topics, f, indent=2)
        print("📁 File saved.")


def kickoff():
    AIBulletinFlow().kickoff()


def plot():
    AIBulletinFlow().plot()


if __name__ == "__main__":
    kickoff()