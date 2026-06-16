from google import genai
from google.adk.agents import LlmAgent
from typing import Dict
from google.adk.tools.agent_tool import AgentTool
from investment_plan_agent.agent import investment_plan_agent
from google.adk.models import google_llm
from config_secrets import get_secret
import os

os.environ["GOOGLE_API_KEY"] = get_secret("GOOGLE_API_KEY")



def get_user_finance_details(user_id: str = "default") -> Dict:
    """
    Get user personal finance details including salary, expenses, investments,
    debts, savings capacity, and financial goals.

    Args:
        user_id: The unique identifier for the user. Defaults to 'default'.
    """
    # Simulated user profiles — replace with DB/API call as needed
    profiles = {
        "default": {
            "user_id": "default",
            "monthly_salary": 50000,
            "other_income": 5000,
            "expenses": {
                "emi": 15000,
                "rent": 10000,
                "essentials": 5000,
                "entertainment": 3000,
                "travel": 2000,
            },
            "existing_investments": {
                "mutual_funds": 100000,
                "stocks": 50000,
                "fixed_deposits": 200000,
                "ppf": 75000,
            },
            "debts": {
                "home_loan_outstanding": 1500000,
                "personal_loan_outstanding": 50000,
            },
            "monthly_savings_capacity": 20000,
            "risk_appetite": "moderate",  # low | moderate | high
            "financial_goals": [
                {"goal": "retirement", "target_amount": 10000000, "years": 25},
                {"goal": "child_education", "target_amount": 2000000, "years": 10},
            ],
        }
    }
    return profiles.get(user_id, profiles["default"])

# native_client = genai.Client(api_key=getenv("GOOGLE_API_KEY"))
# gemini_model = google_llm.Gemini(model="gemini-2.5-flash")
# gemini_model.client = native_client
finance_assistant_agent = LlmAgent(
    name="finance_assistant_agent",
    model="gemini-2.5-flash",
    description="An agent that can answer questions about finance and investments",
    instruction="""You are a finance assistant agent.
        You can answer questions about finance and investments.

        You have three tools use to complete your task:
        1. get_user_finance_details: This tool will provide you with the user's personal finance details like salary, expenses, investments and savings capacity. You should use this tool to get the user's financial details before providing any investment advice.
        2. investment_plan_agent: This tool is an agent that can provide investment advice based on the user's financial details. You should use this tool to get the best investment options for the user based on their financial details.

        ALWAYS use the investment_plan_agent tool to get the best investment options for the user based on their financial details. Do not provide any investment advice without using the investment_plan_agent tool first.
    """,
    tools=[AgentTool(investment_plan_agent), get_user_finance_details],
)

root_agent = finance_assistant_agent