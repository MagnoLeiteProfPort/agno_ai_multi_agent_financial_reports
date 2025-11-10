# agents/market_researcher.py
"""
Market Researcher agent.

Purpose:
- Collect and analyze up-to-date, reliable market intelligence and news.
- Combines web search and reasoning capabilities for contextual insights.
- Persists session and user-specific data across runs using a memory database.

Environment:
- Loads environment variables (e.g., API keys, configuration) from a .env file.
"""

from dotenv import load_dotenv

# Load environment variables from the local .env file
load_dotenv()

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools

from core.prompts import RESEARCHER_SYSTEM
from core.memory import build_db
from core.config import get_settings

# Initialize and validate global settings for the application
_settings = get_settings()  # variable kept local, mainly to ensure configuration is loaded

# Build the shared persistent memory database
_db = build_db()

# Configure the Market Researcher agent.
# Explanation of main arguments:
# - name/role: identifies the purpose of the agent and its scope of analysis.
# - model: the natural language processing backend.
# - tools: external resources and logic modules available to the agent.
#   * DuckDuckGoTools: allows the agent to perform live web searches.
#   * ReasoningTools: supports structured reasoning and critique-based thinking.
# - instructions: system-level behavior prompts (e.g., tone, depth, structure).
# - db / enable_user_memories: persist memory and context across sessions.
# - markdown: ensures outputs are formatted for better readability.
market_researcher = Agent(
    name="Market Researcher",
    role="Fetch dated, trustworthy market intel and news",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        DuckDuckGoTools(),                # Enables web search for current and historical data
        ReasoningTools(add_instructions=True),  # Adds reasoning structure for analysis quality
    ],
    instructions=RESEARCHER_SYSTEM,       # Behavior and analytical directives
    db=_db,                               # Persistent database for user context and sessions
    enable_user_memories=True,            # Maintains continuity across user interactions
    markdown=True,                        # Formats responses for readable presentation
)
