from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool
from crewai.memory import LongTermMemory
from crew.schemas.newsletter_topics import NewsletterTopics

@CrewBase
class AIBulletinCrew():
    """AI Bulletin Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def topic_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['topic_planner'], # type: ignore[index]
            verbose=True,
            tools=[SerperDevTool()],
            memory=LongTermMemory(path="memory/topic_planner_memory.db"),
            output_pydantic=NewsletterTopics,
        )

    @task
    def plan_newsletter(self) -> Task:
        return Task(
            config=self.tasks_config['plan_newsletter'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the content writing crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
        )
