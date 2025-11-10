from typing import Literal, TypedDict

Mode = Literal["collaborate", "auto", "manual"]

class ReportResult(TypedDict):
    content_markdown: str
    session_id: str | None
