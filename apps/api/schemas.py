from pydantic import BaseModel, Field, ConfigDict

class AnalyzeIn(BaseModel):
    ticker: str = Field(
        ...,
        description="Ticker symbol (e.g. AAPL or BBAS3.SA). Brazilian tickers usually end with '.SA'.",
        examples=["AAPL", "BBAS3.SA"],
    )
    prompt: str = Field(
        default="Full equity deep-dive with catalysts, risks, and valuation hooks.",
        description="What you want the team to do.",
        examples=["Full deep-dive with catalysts, risks, and valuation hooks."],
    )

    # This example drives the body pre-fill in Swagger UI
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ticker": "BBAS3.SA",
                "prompt": "Full deep-dive with catalysts, risks, and valuation hooks.",
            }
        }
    )

class AnalyzeOut(BaseModel):
    session_id: str | None = None
    content_markdown: str
