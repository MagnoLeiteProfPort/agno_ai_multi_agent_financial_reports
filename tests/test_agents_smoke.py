import asyncio
from agents.equity_analyst import equity_analyst
from agents.market_researcher import market_researcher

def test_agents_exist():
    assert equity_analyst is not None
    assert market_researcher is not None
