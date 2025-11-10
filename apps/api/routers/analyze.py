# apps/api/routers/analyze.py
from fastapi import APIRouter, HTTPException
from io import StringIO
import contextlib
from typing import Any

from apps.api.schemas import AnalyzeIn, AnalyzeOut
from core.guardrails import AnalyzeRequest
from agents.team_orchestrator import team

from core.markdown_formatter import prettify_report

router = APIRouter()


def _to_text(obj: Any) -> str:
    """
    Best-effort conversion of various Agno return types to text.
    """
    if obj is None:
        return ""
    # Agno responses often have `.content`
    content = getattr(obj, "content", None)
    if isinstance(content, str) and content.strip():
        return content
    # Some may be dict-like
    if isinstance(obj, dict):
        for k in ("content", "text", "message", "output"):
            if k in obj and isinstance(obj[k], str) and obj[k].strip():
                return obj[k]
    # Fallback to string
    return str(obj)


async def _call_with_variants(fn, message: str) -> str:
    """
    Try common calling conventions:
    - fn(message=...)
    - fn(input=...)
    - fn(prompt=...)
    - fn(message)  (positional)
    - fn(input)    (positional)
    """
    # Try keyword variants
    for kwargs in ({"message": message}, {"input": message}, {"prompt": message}):
        try:
            result = await fn(**kwargs)  # type: ignore[misc]
            return _to_text(result)
        except TypeError:
            pass

    # Try positional variants
    try:
        result = await fn(message)  # type: ignore[misc]
        return _to_text(result)
    except TypeError:
        pass

    try:
        result = await fn(message)  # type: ignore[misc]
        return _to_text(result)
    except TypeError:
        pass

    raise TypeError("No compatible signature for async team method.")


async def _call_team(message: str) -> str:
    """
    Compatible execution across Agno versions.
    Tries several async methods and finally captures stdout from streaming.
    """
    # Newer/common async entry points (try in order)
    if hasattr(team, "aresponse"):
        try:
            return await _call_with_variants(team.aresponse, message)  # type: ignore[attr-defined]
        except TypeError:
            pass

    if hasattr(team, "arun"):
        try:
            return await _call_with_variants(team.arun, message)  # type: ignore[attr-defined]
        except TypeError:
            pass

    if hasattr(team, "achat"):
        try:
            return await _call_with_variants(team.achat, message)  # type: ignore[attr-defined]
        except TypeError:
            pass

    if hasattr(team, "aplan"):
        try:
            return await _call_with_variants(team.aplan, message)  # type: ignore[attr-defined]
        except TypeError:
            pass

    # Streaming printer – capture stdout and return it
    if hasattr(team, "aprint_response"):
        buf = StringIO()
        with contextlib.redirect_stdout(buf):
            try:
                # Prefer keyword; some builds require/accept it
                await team.aprint_response(message=message, stream=False)  # type: ignore[attr-defined]
            except TypeError:
                try:
                    await team.aprint_response(message=message)  # type: ignore[attr-defined]
                except TypeError:
                    # Last resort: positional only
                    try:
                        await team.aprint_response(message)  # type: ignore[attr-defined]
                    except TypeError:
                        await team.aprint_response(message)  # type: ignore[attr-defined]
        text = buf.getvalue().strip()
        return text or "Analysis completed."

    # Synchronous fallbacks (very old builds)
    for name in ("response", "run", "chat", "plan"):
        if hasattr(team, name):
            fn = getattr(team, name)
            # Try common keyword signatures
            for kwargs in ({"message": message}, {"input": message}, {"prompt": message}):
                try:
                    result = fn(**kwargs)
                    return _to_text(result)
                except TypeError:
                    pass
            # Positional fallback
            try:
                result = fn(message)
                return _to_text(result)
            except TypeError:
                pass

    raise RuntimeError("No compatible Team execution method found on this Agno version.")


@router.post("/analyze", response_model=AnalyzeOut)
async def analyze(body: AnalyzeIn):
    # Guardrails + normalization
    req = AnalyzeRequest(**body.model_dump())
    message = (
        f"Target: {req.ticker}\n\n"
        f"User goal: {req.prompt}\n\n"
        f"Deliver the orchestrated, sourced equity report."
    )
    try:
        content_text = await _call_team(message)
        # 🎨 Enhance markdown for readability
        content_text = prettify_report(content_text)
        return AnalyzeOut(
            session_id=str(getattr(team, "session_id", None)),
            content_markdown=content_text or "(no content returned)",
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Analysis failed: {e}")
