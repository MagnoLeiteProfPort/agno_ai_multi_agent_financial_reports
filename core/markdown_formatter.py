# core/markdown_formatter.py
import re

def prettify_report(md: str) -> str:
    """
    Enhance the LLM's markdown for human readability and UI polish.
    """
    if not md:
        return ""

    # Normalize section headers spacing
    md = re.sub(r"(?m)^## (.+)", r"## 🟦 \1", md)
    md = re.sub(r"(?m)^### (.+)", r"### 🔹 \1", md)

    # Add spacing after tables
    md = re.sub(r"(\|[^\n]+\|)\n(\|[-:]+[-|:]+\|)", r"\1\n\2\n", md)

    # Highlight numeric/financial cues
    md = re.sub(r"\b([0-9]+\.[0-9]+)\b", r"**\1**", md)  # bold numbers
    md = re.sub(r"📉", "📉 (Decline)", md)
    md = re.sub(r"📈", "📈 (Growth)", md)
    md = re.sub(r"📊", "📊 (Data)", md)

    # Highlight key keywords
    keywords = {
        "Risk": "⚠️ **Risk**",
        "Catalyst": "🚀 **Catalyst**",
        "Opportunity": "💡 **Opportunity**",
        "Valuation": "💰 **Valuation**",
        "Summary": "🧭 **Summary**",
    }
    for word, decorated in keywords.items():
        md = re.sub(rf"\b{word}\b", decorated, md, flags=re.IGNORECASE)

    # Section dividers for readability
    md = md.replace("---", "\n\n---\n\n")

    return md.strip()
