from google.adk.agents import LlmAgent
from google.adk.tools import google_search

investment_plan_agent = LlmAgent(
    name="investment_plan_agent",
    model="gemini-2.5-flash",
    description="An investment plan assistant who can use Google Search to find the best investment options for the user based on their financial details.",
    instruction="""You are a friendly and helpful investment plan assistant. You can use Google Search to find the best investment options for the user based on their financial details. 
    You can also ask the user for more information if needed.

    ALWAYS use the google_search tool to find the best investment options for the user based on their financial details. Do not provide any investment advice without using the google_search tool first.
    """,
    tools=[google_search],
)

root_agent = investment_plan_agent