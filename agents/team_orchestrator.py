# agents/team_orchestrator.py
"""
Team Orchestrator

Purpose:
- Coordinates multiple specialized agents (e.g., Equity Analyst and Market Researcher)
  to perform collaborative financial or market analysis.
- Acts as the central controller that delegates tasks and combines insights from
  multiple agents into a unified result.

Usage:
- The orchestrator can be used programmatically or run locally for testing.
- The asynchronous `run_team()` method provides an interactive way to test the team’s
  end-to-end analysis behavior directly from this module.
"""

import asyncio
from dotenv import load_dotenv

# Load environment variables (e.g., model keys, config paths)
load_dotenv()

from agno.models.openai import OpenAIChat
from agno.team import Team

from agents.equity_analyst import equity_analyst
from agents.market_researcher import market_researcher
from core.prompts import TEAM_ORCHESTRATOR_INSTRUCTIONS

# Build a multi-agent team responsible for financial and market research collaboration.
# Explanation of parameters:
# - name: human-readable identifier for the team.
# - model: shared model used for coordination and synthesis of agent outputs.
# - members: a list of preconfigured specialized agents to be orchestrated.
# - instructions: system-level directives defining how collaboration occurs.
# - markdown: ensures outputs are human-readable and well-formatted.
team = Team(
    name="Equity Analysis Team",
    model=OpenAIChat(id="gpt-4o"),
    members=[equity_analyst, market_researcher],
    instructions=TEAM_ORCHESTRATOR_INSTRUCTIONS,
    markdown=True,
)

# Helper function for local, manual testing.
# It runs the team asynchronously and prints the streamed response in real time.
async def run_team(message: str):
    """
    Executes a test query through the full team pipeline.

    Args:
        message (str): The user query or analysis request to process.

    Returns:
        str: The team’s full analytical response.
    """
    # Streamed output for interactive local testing (e.g., during development)
    return await team.aprint_response(message=message, stream=True)


# Allows direct execution of this script for debugging or standalone runs.
if __name__ == "__main__":
    # Example: Trigger an end-to-end analysis for a given company.
    asyncio.run(run_team("Analyze Banco do Brasil S.A. (BBAS3.SA) end-to-end."))
