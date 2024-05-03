from youtube_yapper_trapper.tools.custom_tool import YouTubeCommentsTool
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from agentops.agent import track_agent
import agentops
import os


agentops.init()


@CrewBase
class YoutubeCommentsCrew:
    """YoutubeCommentsCrew crew for analyzing comments on tech-related YouTube videos."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self) -> None:
        # Groq
        self.groq_llm = ChatGroq(
            temperature=0,
            groq_api_key=os.environ.get("GROQ_API_KEY"),
            model_name="llama3-70b-8192",
        )

        # Ollama
        self.ollama_llm = ChatOpenAI(
            model="mistral",
            base_url="http://localhost:11434/v1",
            api_key="ollama",  # something random
            temperature=0,
        )

    @track_agent(name="comment_fetcher")
    @agent
    def comment_fetcher(self) -> Agent:
        """Agent responsible for fetching YouTube comments."""
        return Agent(
            config=self.agents_config["comment_fetcher"],
            tools=[YouTubeCommentsTool()],
            allow_delegation=False,
            llm=self.ollama_llm,
            verbose=True,
        )

    @track_agent(name="insights_analyst")
    @agent
    def insights_analyst(self) -> Agent:
        """Agent responsible for analyzing comments and generating insights."""
        return Agent(
            config=self.agents_config["insights_analyst"],
            llm=self.ollama_llm,
            allow_delegation=False,
            verbose=True,
        )

    @track_agent(name="report_writer")
    @agent
    def report_writer(self) -> Agent:
        """Agent responsible for writing detailed reports based on the analysis."""
        return Agent(
            config=self.agents_config["report_writer"],
            llm=self.ollama_llm,
            allow_delegation=False,
            verbose=True,
        )

    @task
    def fetch_comments_task(self) -> Task:
        """Task to fetch comments from YouTube videos."""
        return Task(
            config=self.tasks_config["fetch_comments_task"],
            agent=self.comment_fetcher(),
            output_file="comments.md",
        )

    @task
    def analyze_insights_task(self) -> Task:
        """Task to analyze comments and generate insights."""
        return Task(
            config=self.tasks_config["insights_task"],
            agent=self.insights_analyst(),
            human_input=True,
        )

    @task
    def generate_report_task(self) -> Task:
        """Task to generate the final report."""
        return Task(
            config=self.tasks_config["reporting_task"],
            agent=self.report_writer(),
            output_file="report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the YoutubeCommentsCrew crew"""
        return Crew(
            agents=[
                self.comment_fetcher(),
                self.insights_analyst(),
                self.report_writer(),
            ],
            tasks=[
                self.fetch_comments_task(),
                self.analyze_insights_task(),
                self.generate_report_task(),
            ],
            process=Process.sequential,
            memory=False,
            max_rpm=2,
            verbose=2,
        )
