"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 2  |  AI Productivity
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To build a small "copilot-style" productivity assistant that automates the
repetitive work described in the experiment: drafting emails, summarising
conversations, extracting action items, writing proposals and finding
insights in sales data.

The core tools work OFFLINE using only the Python standard library.
An optional function (ask_llm) can call a real generative-AI model if you set
an API key - this shows how a true copilot is built.

Run : python ai_productivity.py
"""

import os
import re
from collections import Counter

STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "is", "are", "was", "were", "to", "of", "in", "on",
    "for", "with", "at", "by", "from", "it", "this", "that", "we", "i", "you", "they", "he",
    "she", "be", "will", "as", "our", "your", "their", "has", "have", "had", "so", "if", "then",
}


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ---------------------------------------------------------------------------
# 1. Generative-AI style email drafting (prompt -> first draft)
# ---------------------------------------------------------------------------
def draft_email(feature: str, benefit: str, audience: str = "Customer", tone: str = "friendly") -> str:
    """Create a first draft from a short instruction, like the CRM example in the notes."""
    openings = {
        "friendly": f"Hi {audience},\n\nWe have some exciting news to share!",
        "formal": f"Dear {audience},\n\nWe are pleased to announce an important update.",
    }
    closings = {
        "friendly": "Happy to help if you have any questions!\n\nWarm regards,\nThe Product Team",
        "formal": "Please contact us should you require further information.\n\nSincerely,\nThe Product Team",
    }
    return "\n".join([
        f"Subject: Introducing {feature}",
        "",
        openings[tone],
        "",
        f"Our new {feature} helps you {benefit}. It is available now in your account,",
        "and you can start using it right away - no extra setup needed.",
        "",
        closings[tone],
    ])


# ---------------------------------------------------------------------------
# 2. Summarisation (like Copilot in Outlook / Teams)
# ---------------------------------------------------------------------------
def split_sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def summarize(text: str, max_sentences: int = 2) -> str:
    """Extractive summary: keep the sentences that contain the most frequent keywords."""
    sentences = split_sentences(text)
    words = [w for w in re.findall(r"[a-z']+", text.lower()) if w not in STOP_WORDS]
    frequency = Counter(words)

    def score(sentence: str) -> float:
        tokens = [w for w in re.findall(r"[a-z']+", sentence.lower()) if w not in STOP_WORDS]
        return sum(frequency[t] for t in tokens) / (len(tokens) or 1)

    best = sorted(range(len(sentences)), key=lambda i: score(sentences[i]), reverse=True)[:max_sentences]
    return " ".join(sentences[i] for i in sorted(best))  # keep original order


ACTION_PATTERN = re.compile(
    r"\b(will|needs? to|need to|should|must|please|action|follow up|send|prepare|share|schedule|deadline|by (?:monday|tuesday|wednesday|thursday|friday|tomorrow|next week))\b",
    re.IGNORECASE,
)


def extract_action_items(notes: str) -> list[str]:
    return [s for s in split_sentences(notes) if ACTION_PATTERN.search(s)]


# ---------------------------------------------------------------------------
# 3. Proposal generation from CRM data (like Copilot in Word)
# ---------------------------------------------------------------------------
def generate_proposal(client: dict) -> str:
    total = sum(item["qty"] * item["price"] for item in client["items"])
    lines = "\n".join(
        f"  - {i['name']:<22} {i['qty']:>3} x Rs.{i['price']:>10,.2f} = Rs.{i['qty'] * i['price']:>11,.2f}"
        for i in client["items"]
    )
    return (
        f"PROPOSAL FOR {client['company'].upper()}\n"
        f"Prepared for : {client['contact']}\n"
        f"Challenge    : {client['challenge']}\n\n"
        f"Proposed solution:\n{lines}\n\n"
        f"Total investment : Rs.{total:,.2f}\n"
        f"Expected outcome : {client['outcome']}"
    )


# ---------------------------------------------------------------------------
# 4. Insights from quarterly data (like Copilot in Excel)
# ---------------------------------------------------------------------------
def quarterly_insights(sales: dict[str, list[float]]) -> list[str]:
    insights = []
    totals = {region: sum(values) for region, values in sales.items()}
    best = max(totals, key=totals.get)
    worst = min(totals, key=totals.get)
    insights.append(f"Top region: {best} (Rs.{totals[best]:,.0f}); lowest region: {worst} (Rs.{totals[worst]:,.0f}).")

    for region, values in sales.items():
        growth = (values[-1] - values[0]) / values[0] * 100
        trend = "growing" if growth > 0 else "declining"
        insights.append(f"{region}: {trend} {abs(growth):.1f}% from Q1 to Q{len(values)}.")

    overall = sum(totals.values())
    insights.append(f"Overall sales for the year: Rs.{overall:,.0f}.")
    return insights


# ---------------------------------------------------------------------------
# 5. OPTIONAL - call a real generative AI model
# ---------------------------------------------------------------------------
def ask_llm(prompt: str) -> str:
    """
    Sends a prompt to Claude using the Anthropic API.
    Setup (optional):  pip install anthropic   and   set ANTHROPIC_API_KEY
    If the key or package is missing, a friendly message is returned instead.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        return "[Optional demo skipped: set the ANTHROPIC_API_KEY environment variable to enable it.]"
    try:
        import anthropic
    except ImportError:
        return "[Optional demo skipped: run 'pip install anthropic' to enable it.]"

    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def main() -> None:
    print("NM1130 - EX.NO: 2 - AI PRODUCTIVITY (Copilot-style assistant)")

    heading("1. EMAIL DRAFT FROM A ONE-LINE PROMPT")
    print('Prompt: "Write a friendly email announcing our new CRM feature that helps customers save time."\n')
    print(draft_email("CRM Smart Reminders", "save time by following up with leads automatically"))

    heading("2. SUMMARISE A CUSTOMER CONVERSATION")
    conversation = (
        "The customer reported that invoices are taking too long to generate. "
        "They said the slow invoice process delays payments from their clients. "
        "We explained that the new reporting module will speed up invoice generation. "
        "The customer will test the module next week. "
        "Priya should send the demo link by Friday. "
        "The customer also mentioned they enjoyed the support team's quick replies."
    )
    print("Summary:\n ", summarize(conversation, max_sentences=2))

    heading("3. ACTION ITEMS FROM MEETING NOTES")
    for number, item in enumerate(extract_action_items(conversation), start=1):
        print(f"  {number}. {item}")

    heading("4. PROPOSAL GENERATED FROM CRM DATA")
    client = {
        "company": "Sunrise Textiles",
        "contact": "Mr. Arun Kumar",
        "challenge": "Manual invoicing delays customer payments.",
        "items": [
            {"name": "Reporting module", "qty": 1, "price": 45000},
            {"name": "User licences", "qty": 10, "price": 1200},
            {"name": "Onboarding training", "qty": 2, "price": 7500},
        ],
        "outcome": "Invoices generated 60% faster with fewer errors.",
    }
    print(generate_proposal(client))

    heading("5. INSIGHTS FROM QUARTERLY SALES DATA")
    sales = {
        "North": [120000, 135000, 150000, 162000],
        "South": [98000, 97000, 91000, 88000],
        "East": [76000, 82000, 90000, 99000],
    }
    for line in quarterly_insights(sales):
        print("  *", line)

    heading("6. (OPTIONAL) REAL GENERATIVE AI MODEL")
    print(ask_llm("In two sentences, explain how generative AI improves workplace productivity."))

    print("\nResult: Productivity tasks automated successfully.")


if __name__ == "__main__":
    main()
