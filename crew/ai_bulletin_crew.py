import os
import json
from typing import List, Dict, Any
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool
from crewai.memory import LongTermMemory
from crew.schemas.newsletter_topics import NewsletterTopics

@CrewBase
class AIBulletinCrew():
    """AI Bulletin Crew for generating autonomous newsletters"""

    agents: List[BaseAgent]
    tasks: List[Task]

    def __init__(self):
        super().__init__()
        # Ensure output directories exist
        os.makedirs("outputs", exist_ok=True)
        os.makedirs("memory", exist_ok=True)

    # Define Agents
    @agent
    def topic_planner(self) -> Agent:
        return Agent(
            config=self.agents_config['topic_planner'],
            verbose=True,
            tools=[SerperDevTool()],
            memory=LongTermMemory(path="memory/topic_planner_memory.db"),
            output_pydantic=NewsletterTopics
        )

    @agent
    def top_stories_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['top_stories_writer'], 
            verbose=True, 
            tools=[SerperDevTool()],
            allow_delegation=False,
            memory=False
        )

    @agent
    def deep_dive_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['deep_dive_writer'], 
            verbose=True, 
            tools=[SerperDevTool()],
            allow_delegation=False,
            memory=False
        )

    @agent
    def tool_of_the_week_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['tool_of_the_week_writer'], 
            verbose=True, 
            tools=[SerperDevTool()],
            allow_delegation=False,
            memory=False
        )

    @agent
    def quote_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['quote_writer'], 
            verbose=True, 
            tools=[SerperDevTool()],
            allow_delegation=False,
            memory=False
        )

    @agent
    def ai_in_the_wild_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_in_the_wild_writer'], 
            verbose=True, 
            tools=[SerperDevTool()],
            allow_delegation=False,
            memory=False
        )

    @agent
    def hot_takes_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['hot_takes_writer'], 
            verbose=True, 
            tools=[SerperDevTool()],
            allow_delegation=False,
            memory=False
        )

    @agent
    def editors_note_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['editors_note_writer'], 
            verbose=True,
            allow_delegation=False,
            memory=False
        )

    @agent
    def newsletter_editor(self) -> Agent:
        return Agent(
            config=self.agents_config['newsletter_editor'], 
            verbose=True,
            allow_delegation=False,
            memory=False
        )

    @agent
    def html_formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['html_formatter'], 
            verbose=True,
            memory=LongTermMemory(path="memory/html_formatter_memory.db")
        )

    # Define Tasks
    @task
    def plan_newsletter(self) -> Task:
        return Task(
            config=self.tasks_config['plan_newsletter'],
            output_file="outputs/01_newsletter_topics.json",
            return_output=True
        )

    @task
    def top_stories(self) -> Task:
        return Task(
            config=self.tasks_config['top_stories_task'],
            context=[self.plan_newsletter()],
            output_file="outputs/02_top_stories.md"
        )

    @task
    def deep_dive(self) -> Task:
        return Task(
            config=self.tasks_config['deep_dive_task'],
            context=[self.plan_newsletter()],
            output_file="outputs/03_deep_dive.md"
        )

    @task
    def tool_of_the_week(self) -> Task:
        return Task(
            config=self.tasks_config['tool_task'],
            context=[self.plan_newsletter()],
            output_file="outputs/04_tool_of_week.md"
        )

    @task
    def quote(self) -> Task:
        return Task(
            config=self.tasks_config['quote_task'],
            context=[self.plan_newsletter()],
            output_file="outputs/05_quote.md"
        )

    @task
    def ai_in_the_wild(self) -> Task:
        return Task(
            config=self.tasks_config['ai_in_the_wild_task'],
            context=[self.plan_newsletter()],
            output_file="outputs/06_ai_wild.md"
        )

    @task
    def hot_takes(self) -> Task:
        return Task(
            config=self.tasks_config['hot_takes_task'],
            context=[self.plan_newsletter()],
            output_file="outputs/07_hot_takes.md"
        )

    @task
    def editors_note(self) -> Task:
        return Task(
            config=self.tasks_config['editors_note_task'],
            context=[self.plan_newsletter()],
            output_file="outputs/08_editors_note.md"
        )

    @task
    def edit_newsletter(self) -> Task:
        return Task(
            config=self.tasks_config['newsletter_editing_task'],
            context=[
                self.top_stories(),
                self.deep_dive(),
                self.tool_of_the_week(),
                self.quote(),
                self.ai_in_the_wild(),
                self.hot_takes(),
                self.editors_note()
            ],
            output_file="outputs/09_newsletter_edited.md"
        )

    @task
    def format_html(self) -> Task:
        return Task(
            config=self.tasks_config['html_formatting_task'],
            context=[self.edit_newsletter()],
            output_file="outputs/10_newsletter_final.html"
        )

    def save_task_output(self, task_name: str, output: Any, file_path: str):
        """Save individual task output to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                if isinstance(output, dict):
                    json.dump(output, f, indent=2, ensure_ascii=False)
                else:
                    f.write(str(output))
            print(f"✅ Saved {task_name} output to {file_path}")
        except Exception as e:
            print(f"❌ Error saving {task_name} output: {e}")

    # Build Crew
    @crew
    def crew(self) -> Crew:
        """Build and return the crew with proper task dependencies for parallel execution"""
        
        return Crew(
            agents=[
                self.topic_planner(),
                self.top_stories_writer(),
                self.deep_dive_writer(),
                self.tool_of_the_week_writer(),
                self.quote_writer(),
                self.ai_in_the_wild_writer(),
                self.hot_takes_writer(),
                self.editors_note_writer(),
                self.newsletter_editor(),
                self.html_formatter()
            ],
            tasks=[
                self.plan_newsletter(),
                self.top_stories(),
                self.deep_dive(),
                self.tool_of_the_week(),
                self.quote(),
                self.ai_in_the_wild(),
                self.hot_takes(),
                self.editors_note(),
                self.edit_newsletter(),
                self.format_html()
            ],
            process=Process.hierarchical,
            manager_llm="deepseek/deepseek-chat",
            verbose=True,
            memory=True,
            full_output=True
        )