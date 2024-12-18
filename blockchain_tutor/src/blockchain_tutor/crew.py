import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from tools.custom_tool import CustomSerperDevTool
from langchain_groq import ChatGroq
from crewai import LLM
from composio_crewai import ComposioToolSet, Action, App
from crewai_tools import TXTSearchTool, PDFSearchTool, DirectorySearchTool

from dotenv import load_dotenv
load_dotenv()

completion_state = {"completed": False}

llm = LLM(
    model="gemini/gemini-1.5-pro-002",
    api_key=os.environ["GOOGLE_API_KEY"]
)

# llm = ChatGroq(model="groq/llama3-8b-8192", api_key=os.environ["GROQ_API_KEY"])

composio_toolset = ComposioToolSet()
Image_Analyzer_tool = composio_toolset.get_tools(actions=['IMAGE_ANALYSER_ANALYSE'])
Code_tool = composio_toolset.get_tools(actions=['GREPTILE_CODE_QUERY'])

Reader_tool = TXTSearchTool(
    txt="/Users/dharmanshusingh/Downloads/ai_tutor/blockchain_text.txt",
    config={
        "llm": {
            "provider": "groq",  
            "config": {
                "model": "groq/mixtral-8x7b-32768",
            },
        },
        "embedder": {
            "provider": "cohere",
            "config": {
                "model": "embed-english-v3.0",
                "api_key": os.environ["COHERE_API_KEY"],
            }
        },
    }
)

# PDF_tool = DirectorySearchTool(
#     directory='/Users/dharmanshusingh/Downloads/ai_tutor/docs',
#     config={
#         "llm": {
#             "provider": "groq",
#             "config": {
#                 "model": "groq/mixtral-8x7b-32768",
#             },
#         },
#         "embedder": {
#             "provider": "cohere",
#             "config": {
#                 "model": "embed-english-v3.0",
#                 "api_key": os.environ["COHERE_API_KEY"],
#             }
#         },
#     }
# )

def add_embedding(embedding_id, embedding_data, db):
    if db.contains(embedding_id):
        print(f"Embedding {embedding_id} already exists. Skipping addition.")
    else:
        db.add(embedding_id, embedding_data)

@CrewBase
class BlockchainTutorCrew:
    """BlockchainTutorCrew"""
    agents_config = '/Users/dharmanshusingh/Downloads/ai_tutor/blockchain_tutor/src/blockchain_tutor/config/agents.yaml'
    tasks_config = '/Users/dharmanshusingh/Downloads/ai_tutor/blockchain_tutor/src/blockchain_tutor/config/tasks.yaml'
    
    @agent
    def knowledge_retrieval_agent(self) -> Agent:
        agent_config = self.agents_config['knowledge_retrieval_agent']
        return Agent(
            config=agent_config, 
            tools=[Reader_tool],
            #SerperDevTool(), ScrapeWebsiteTool(), CustomSerperDevTool(), 
            allow_delegation=True,
            # max_iter=1,
            verbose=True,
            llm=llm,
        )

    @agent
    def query_responder_agent(self) -> Agent:
        agent_config = self.agents_config['query_responder_agent']
        return Agent(
            config=agent_config, 
            allow_delegation=True,
            verbose=True,
            # max_iter=1,
            llm=llm,
        )

    @agent
    def summariser_agent(self) -> Agent:
        agent_config = self.agents_config['summariser_agent']
        return Agent(
            config=agent_config, 
            allow_delegation=True,
            verbose=True,
            # max_iter=1,
            llm=llm,
        )

    @agent
    def blockchain_ai_tutor(self) -> Agent:
        agent_config = self.agents_config['blockchain_ai_tutor']
        return Agent(
            config=agent_config, 
            allow_delegation=True,
            verbose=True,
            # max_iter=1,
            llm=llm,
        )

    @agent
    def image_analyzer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['image_analyzer_agent'],
            tools=[Image_Analyzer_tool[0]],
            allow_delegation=True,
            verbose=True,
            # max_iter=1,
            llm=llm,
        )

    @agent
    def code_query_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['code_query_agent'],
            tools=[Code_tool[0]],
            allow_delegation=True,
            verbose=True,
            # max_iter=1,
            llm=llm,
        )

    # Tasks
    @task
    def knowledge_retrieval_task(self) -> Task:
        task_config = self.tasks_config['knowledge_retrieval_task']
        return Task(
            config=task_config,
            output_file='output/knowledge_retrieval_results.json',
            tools=[Reader_tool],
            llm=llm,
        )

    @task
    def query_response_task(self) -> Task:
        task_config = self.tasks_config['query_response_task']
        return Task(
            config=task_config,
            output_file='output/query_response_results.json',
            llm=llm,
        )

    @task
    def text_summarization_task(self) -> Task:
        task_config = self.tasks_config['text_summarization_task']
        return Task(
            config=task_config,
            output_file='output/text_summarization_results.json',
            llm=llm,
        )

    @task
    def blockchain_tutoring_task(self) -> Task:
        task_config = self.tasks_config['blockchain_tutoring_task']
        return Task(
            config=task_config,
            output_file='output/blockchain_tutoring_results.json',
            llm=llm,
        )

    @task
    def image_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['image_analysis_task'],
            output_file='output/image_analysis_results.json',
            tools=[Image_Analyzer_tool[0]],
            llm=llm,
        )

    @task
    def code_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['code_analysis_task'],
            output_file='output/code_analysis_results.json',
            tools=[Code_tool[0]],
            llm=llm,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the BlockchainTutorCrew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            # process=Process.sequential,
            process=Process.hierarchical,
            planning=True,
            planning_llm=ChatGroq(model="groq/llama3-70b-8192", api_key=os.environ["GROQ_API_KEY"]),
            manager_llm=ChatGroq(model="groq/llama3-70b-8192", api_key=os.environ["GROQ_API_KEY"]),
            verbose=True,
        )
