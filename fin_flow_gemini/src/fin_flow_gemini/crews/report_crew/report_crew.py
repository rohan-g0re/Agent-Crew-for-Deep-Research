from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from crewai_tools import FileWriterTool, FileReadTool
file_writer = FileWriterTool()
file_reader = FileReadTool()

from dotenv import load_dotenv
load_dotenv()

@CrewBase
class ReportCrew():
    """ReportCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def visualization_eloborator(self) -> Agent:
        return Agent(
            config=self.agents_config['visualization_eloborator'], # type: ignore[index]
            tools=[file_reader, file_writer],
            verbose=True,
            multimodal=True,
            max_retry_limit=5
        )

    @agent
    def news_merger_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['news_merger_agent'], # type: ignore[index]
            tools=[file_reader, file_writer],
            verbose=True,
            max_retry_limit=5
        )

    @task
    def visualization_eloborator_task(self) -> Task:
        return Task(
            config=self.tasks_config['visualization_eloborator_task'], # type: ignore[index]
            output_file='/assets/report/intermediate_report.md'
        )

    @task
    def news_merger_task(self) -> Task:
        return Task(
            config=self.tasks_config['news_merger_task'], # type: ignore[index]
            depends_on=['visualization_eloborator_task'],
            output_file='/assets/report/final_report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the ReportCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
