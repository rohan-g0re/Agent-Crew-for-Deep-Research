from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from crewai_tools import SerperDevTool, ScrapeWebsiteTool, FileWriterTool, FileReadTool

scrape_website = ScrapeWebsiteTool()
serper_dev = SerperDevTool()
json_file_writer_urls = FileWriterTool(file_path="\assets\news\news_urls.json")
json_file_writer_scraped = FileWriterTool(file_path="\assets\news\news_scraped.json")
md_file_writer_news = FileWriterTool(file_path="\assets\news\news_article.md")
file_reader = FileReadTool()

from dotenv import load_dotenv
load_dotenv()


@CrewBase
class NewsCrew():
    """NewsCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
    
    @agent
    def retrieve_news(self) -> Agent:
        return Agent(
            config=self.agents_config['retrieve_news'], # type: ignore[index]
            tools=[serper_dev, json_file_writer_urls],
            verbose=True,
            allow_delegation=True,
            max_retry_limit=5
        )
    
    
    @agent
    def website_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['website_scraper'], # type: ignore[index]
            tools=[file_reader, scrape_website, json_file_writer_scraped],
            verbose=True,
            allow_delegation=True,
            max_retry_limit=5
        )

    @agent
    def ai_news_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['ai_news_writer'], # type: ignore[index]
            tools=[file_reader, md_file_writer_news],
            verbose=True,
            allow_delegation=True,
            max_retry_limit=5
        )

    @task
    def retrieve_news_task(self) -> Task:
        return Task(
            config=self.tasks_config['retrieve_news_task'], # type: ignore[index]
            output_file="/assets/news/news_urls.json"
        )

    @task
    def website_scrape_task(self) -> Task:
        return Task(
            config=self.tasks_config['website_scrape_task'], # type: ignore[index]
                output_file="/assets/news/news_scraped.json",
            depends_on=["retrieve_news_task"]
        )
    
    @task
    def ai_news_write_task(self) -> Task:
        return Task(
            config=self.tasks_config['ai_news_write_task'], # type: ignore[index]
            output_file="/assets/news/news_article.md",
            depends_on=["website_scrape_task"]
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the NewsCrew crew"""

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
