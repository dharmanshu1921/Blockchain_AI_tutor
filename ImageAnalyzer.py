from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from composio_crewai import ComposioToolSet, Action, App
import os
from langchain_groq import ChatGroq

os.environ["GROQ_API_KEY"] = ""

llm=ChatGroq(model="groq/llama3-8b-8192", api_key="")


# Initialize the composio toolset with API key
composio_toolset = ComposioToolSet()
weather_tool = composio_toolset.get_tools(actions=['IMAGE_ANALYSER'])

# Define the agent with tools and goal
crewai_agent = Agent(
    role="Sample Agent",
    goal="You are an AI agent that is responsible for taking actions based on the tools you have",
    backstory="You are an AI agent that is responsible for taking actions based on the tools you have.",
    verbose=True,
    tools=tools,
    llm=llm,
)

# Define the task description and expected output
task = Task(
    description="Analyse the image and provide insights based on the analysis.",
    agent=crewai_agent,
    expected_output="A detailed analysis of the image with relevant information.",
)

# Initialize the crew with the agent and task
my_crew = Crew(agents=[crewai_agent], tasks=[task])

# Kick off the task and print the result
result = my_crew.kickoff()
print(result)
