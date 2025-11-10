# agents/equity_analyst.py
"""
Equity Analyst agent.

Purpose:
- Analyze publicly listed companies and produce investor-focused insights.
- Uses a finance toolkit for market data and a reasoning toolkit for structured analysis.
- Persists context and user memories across runs via an application database.

Required environment/config:
- API keys and app settings are read from environment variables (.env supported).
"""

from dotenv import load_dotenv

# Load variables from a local .env file (e.g., API keys, DB paths)
load_dotenv()

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools

from core.prompts import ANALYST_SYSTEM
from core.memory import build_db
from core.config import get_settings

# Initialize application settings (validates env/config on import)
_settings = get_settings()  # underscore indicates local use / side-effects only

# Build a persistent database connection used by the agent for sessions & memories
_db = build_db()

# Configure the analysis agent.
# Notes on key parameters:
# - name/role: human-readable metadata shown in logs/UX.
# - model: language model backend; the id can be changed via configuration if needed.
# - tools: capabilities the agent can call (market data, reasoning utilities).
# - instructions: system-level directives that shape analysis style and outputs.
# - db / enable_user_memories: enables long-term memory across conversations.
# - markdown: format responses in Markdown for readable output.
equity_analyst = Agent(
    name="Equity Analyst",
    role="Analyze listed companies and produce investor-grade insights",
    model=OpenAIChat(id="gpt-4o"),
    tools=[
        YFinanceTools(),                  # Financial data: prices, fundamentals, etc.
        ReasoningTools(add_instructions=True),  # Structured reasoning helpers
    ],
    instructions=ANALYST_SYSTEM,         # Domain-specific analysis directives
    db=_db,                              # Persistent storage for sessions & memories
    enable_user_memories=True,           # Remember user preferences and context
    markdown=True,                       # Return nicely formatted Markdown
)