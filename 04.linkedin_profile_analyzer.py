"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 4  |  LinkedIn: Building Your Professional Brand
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To build a LinkedIn Profile Analyzer that scores a profile against the
checklist from the notes (photo, headline, summary, education, skills,
certifications, projects, network, activity), points out common mistakes and
suggests improvements. A "before" and "after" profile are compared to show how
a strong professional brand is built.

Libraries : standard library (matplotlib optional, for the comparison chart)
Run       : python linkedin_profile_analyzer.py
"""

import re
from pathlib import Path

# Each rule: (key, label, weight in points)
CHECKLIST = [
    ("photo", "Professional profile photo", 10),
    ("headline", "Clear, informative headline", 15),
    ("summary", "Well-written summary (About)", 15),
    ("education", "Education details", 10),
    ("skills", "Technical skills (at least 5)", 15),
    ("certifications", "Certifications added", 10),
    ("projects", "Project details", 10),
    ("connections", "Network of 100+ connections", 8),
    ("activity", "Posts / engagement every month", 7),
]
MAX_SCORE = sum(weight for _, _, weight in CHECKLIST)

CLICHES = ["hardworking", "passionate", "team player", "go-getter", "result-oriented", "dynamic", "self-motivated"]


def evaluate(profile: dict) -> dict:
    """Return {rule_key: points_earned} for a profile."""
    headline_words = len(profile.get("headline", "").split())
    summary_words = len(profile.get("summary", "").split())

    passed = {
        "photo": profile.get("photo", False),
        "headline": 4 <= headline_words <= 25 and "student" != profile.get("headline", "").strip().lower(),
        "summary": summary_words >= 30,
        "education": bool(profile.get("education")),
        "skills": len(profile.get("skills", [])) >= 5,
        "certifications": len(profile.get("certifications", [])) >= 1,
        "projects": len(profile.get("projects", [])) >= 1,
        "connections": profile.get("connections", 0) >= 100,
        "activity": profile.get("posts_last_3_months", 0) >= 3,
    }
    return {key: (weight if passed[key] else 0) for key, _, weight in CHECKLIST}


def common_mistakes(profile: dict) -> list[str]:
    mistakes = []
    if not profile.get("photo"):
        mistakes.append("No profile photo - profiles with a clear photo get far more views.")
    if len(profile.get("headline", "").split()) < 4:
        mistakes.append("Headline is too short - mention your field, skills and goal.")
    if len(profile.get("summary", "").split()) < 30:
        mistakes.append("Summary is incomplete - describe skills, goals and achievements.")
    found = [c for c in CLICHES if c in profile.get("summary", "").lower()]
    if found:
        mistakes.append(f"Overused buzzwords in summary ({', '.join(found)}) - show proof with examples instead.")
    if profile.get("posts_last_3_months", 0) == 0:
        mistakes.append("No activity - share posts, learning or project updates regularly.")
    if re.search(r"[!]{2,}|[A-Z]{12,}", profile.get("summary", "")):
        mistakes.append("Unprofessional tone - avoid shouting (ALL CAPS) and repeated '!!'.")
    return mistakes


def generate_headline(role: str, skills: list[str], goal: str) -> str:
    """Headline formula: Role | Top skills | Goal"""
    return f"{role} | {' - '.join(skills[:3])} | {goal}"


def report(name: str, profile: dict) -> int:
    scores = evaluate(profile)
    total = sum(scores.values())
    percent = total / MAX_SCORE * 100
    rating = "All-Star" if percent >= 90 else "Strong" if percent >= 70 else "Intermediate" if percent >= 40 else "Beginner"

    print(f"\n--- {name} ---")
    for key, label, weight in CHECKLIST:
        tick = "[x]" if scores[key] else "[ ]"
        print(f"  {tick} {label:<34} {scores[key]:>2}/{weight}")
    print(f"  Profile strength : {total}/{MAX_SCORE}  ({percent:.0f}%)  ->  {rating}")

    issues = common_mistakes(profile)
    if issues:
        print("  Mistakes to fix:")
        for issue in issues:
            print("    -", issue)
    return total


def save_comparison_chart(before: int, after: int) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("\n(matplotlib not installed - chart skipped)")
        return

    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(["Before", "After"], [before, after], color=["#d9534f", "#2e8b57"])
    ax.set_ylim(0, MAX_SCORE)
    ax.set_ylabel("Profile strength score")
    ax.set_title("LinkedIn Profile Improvement")
    for bar, value in zip(bars, [before, after]):
        ax.text(bar.get_x() + bar.get_width() / 2, value + 1, str(value), ha="center", fontweight="bold")
    out = Path(__file__).with_name("profile_improvement.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"\nChart saved: {out.name}")


def main() -> None:
    print("NM1130 - EX.NO: 4 - LINKEDIN PROFILE ANALYZER")

    before = {
        "photo": False,
        "headline": "Student",
        "summary": "I am a hardworking and passionate student!!",
        "education": "",
        "skills": ["Python"],
        "certifications": [],
        "projects": [],
        "connections": 25,
        "posts_last_3_months": 0,
    }

    after = {
        "photo": True,
        "headline": generate_headline(
            "ECE Student", ["Python", "AI/ML", "Power BI"], "Seeking AI & Data internships"
        ),
        "summary": (
            "Electrical and Computer Engineering student at University College of "
            "Engineering (BIT Campus), Anna University. I build small AI and data projects in Python, "
            "completed the Naan Mudhalvan AI and Digital Skills programme, and I am looking for an "
            "internship where I can apply machine learning to real business problems."
        ),
        "education": "B.E. Electrical and Computer Engineering, Anna University",
        "skills": ["Python", "Machine Learning", "Power BI", "GitHub", "Cybersecurity basics", "Communication"],
        "certifications": ["Naan Mudhalvan - AI and Digital Skills", "GitHub Foundations"],
        "projects": ["Sales dashboard in Power BI", "Mini version-control simulator in Python"],
        "connections": 180,
        "posts_last_3_months": 4,
    }

    before_score = report("BEFORE: unoptimised profile", before)
    after_score = report("AFTER: optimised professional brand", after)

    print("\nGenerated headline example:")
    print("  ", after["headline"])

    print(f"\nImprovement: {before_score} -> {after_score} points (+{after_score - before_score})")
    save_comparison_chart(before_score, after_score)

    print("\nResult: Profile analysed and professional branding tips generated.")


if __name__ == "__main__":
    main()
