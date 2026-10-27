"""
NAAN MUDHALVAN - NM1130 AI AND DIGITAL SKILLS
EX.NO: 8  |  Career Essentials
------------------------------------------------------------------
Department  : CSE (AI & ML)
College     : University College of Engineering (BIT Campus), Anna University, Tiruchirappalli

Aim
---
To build a Career Skills Planner covering the career essentials in the notes:

1. Skill self-assessment  (communication, teamwork, problem solving, time management,
                           leadership, adaptability, critical thinking,
                           emotional intelligence, digital literacy)
2. Skill-gap analysis and a radar chart
3. SMART goal builder       (setting clear goals)
4. Time management          (Eisenhower priority matrix)

Libraries : standard library (matplotlib + numpy optional, for the radar chart)
Run       : python career_essentials.py                 -> uses sample ratings
            python career_essentials.py --interactive   -> enter your own ratings
"""

import argparse
from datetime import date, timedelta
from pathlib import Path

TARGET_LEVEL = 4  # we aim for at least 4 out of 5 in every skill

SKILLS = {
    "Communication": "Practise presentations, join a debate or technical-paper club, write a weekly summary.",
    "Teamwork": "Take part in group projects and hackathons; share responsibilities and give feedback.",
    "Problem Solving": "Solve one coding or aptitude problem daily (LeetCode, HackerRank).",
    "Time Management": "Plan the week every Sunday; use time-blocking and the Eisenhower matrix.",
    "Leadership": "Lead a project team or a student-club event from planning to completion.",
    "Adaptability": "Learn one new tool or technology every month and try different roles.",
    "Critical Thinking": "Question assumptions, compare two solutions before choosing one.",
    "Emotional Intelligence": "Reflect after conflicts, listen actively, ask for peer feedback.",
    "Digital Literacy": "Build projects with Python, GitHub and Power BI; keep certifications updated.",
}

SAMPLE_RATINGS = {
    "Communication": 3, "Teamwork": 4, "Problem Solving": 4, "Time Management": 2,
    "Leadership": 2, "Adaptability": 4, "Critical Thinking": 3,
    "Emotional Intelligence": 3, "Digital Literacy": 5,
}


def heading(title: str) -> None:
    print("\n" + "=" * 64)
    print(title)
    print("=" * 64)


# ---------------------------------------------------------------------------
# 1. Self-assessment
# ---------------------------------------------------------------------------
def ask_ratings() -> dict[str, int]:
    print("Rate yourself from 1 (beginner) to 5 (expert) in each skill.")
    ratings = {}
    for skill in SKILLS:
        while True:
            answer = input(f"  {skill:<24}: ").strip()
            if answer in {"1", "2", "3", "4", "5"}:
                ratings[skill] = int(answer)
                break
            print("    Please enter a number between 1 and 5.")
    return ratings


def bar(value: int) -> str:
    return "#" * value + "." * (5 - value)


def show_assessment(ratings: dict[str, int]) -> None:
    for skill, value in ratings.items():
        status = "OK" if value >= TARGET_LEVEL else "improve"
        print(f"  {skill:<24} [{bar(value)}] {value}/5  {status}")
    average = sum(ratings.values()) / len(ratings)
    print(f"\n  Overall career-readiness score: {average:.1f}/5 ({average / 5:.0%})")


# ---------------------------------------------------------------------------
# 2. Skill-gap analysis
# ---------------------------------------------------------------------------
def gap_analysis(ratings: dict[str, int]) -> list[str]:
    gaps = sorted(((TARGET_LEVEL - v, s) for s, v in ratings.items() if v < TARGET_LEVEL), reverse=True)
    if not gaps:
        print("  Excellent! All skills meet the target level. Keep learning new technologies.")
        return []
    print("  Priority skills to develop (largest gap first):")
    for rank, (gap, skill) in enumerate(gaps, start=1):
        print(f"   {rank}. {skill} (gap {gap}) -> {SKILLS[skill]}")
    return [skill for _, skill in gaps]


def radar_chart(ratings: dict[str, int]) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print("  (matplotlib not installed - radar chart skipped)")
        return

    labels = list(ratings)
    values = list(ratings.values())
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw={"polar": True})
    ax.plot(angles, values, color="#118DFF", linewidth=2, label="Your level")
    ax.fill(angles, values, color="#118DFF", alpha=0.25)
    ax.plot(angles, [TARGET_LEVEL] * len(angles), color="#2e8b57", linestyle="--", label=f"Target ({TARGET_LEVEL})")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([label.replace(" ", "\n") for label in labels], fontsize=9)
    ax.set_ylim(0, 5)
    ax.set_yticks([1, 2, 3, 4, 5])
    ax.set_title("Career Skills Radar", fontsize=15, fontweight="bold", pad=24)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.12))
    out = Path(__file__).with_name("career_skills_radar.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Radar chart saved: {out.name}")


# ---------------------------------------------------------------------------
# 3. SMART goal builder - Specific, Measurable, Achievable, Relevant, Time-bound
# ---------------------------------------------------------------------------
def smart_goal(skill: str, action: str, measure: str, weeks: int) -> dict:
    deadline = date.today() + timedelta(weeks=weeks)
    return {
        "Specific": f"Improve my {skill.lower()} by {action}",
        "Measurable": measure,
        "Achievable": f"Spend 3 hours per week for {weeks} weeks",
        "Relevant": f"{skill} is needed in every profession and for placements",
        "Time-bound": f"Complete by {deadline:%d %B %Y}",
    }


# ---------------------------------------------------------------------------
# 4. Time management - Eisenhower matrix
# ---------------------------------------------------------------------------
def eisenhower(tasks: list[tuple[str, bool, bool]]) -> dict[str, list[str]]:
    """tasks = (name, urgent, important)"""
    matrix = {"DO NOW (urgent + important)": [], "SCHEDULE (important, not urgent)": [],
              "DELEGATE (urgent, not important)": [], "ELIMINATE (neither)": []}
    for name, urgent, important in tasks:
        if urgent and important:
            matrix["DO NOW (urgent + important)"].append(name)
        elif important:
            matrix["SCHEDULE (important, not urgent)"].append(name)
        elif urgent:
            matrix["DELEGATE (urgent, not important)"].append(name)
        else:
            matrix["ELIMINATE (neither)"].append(name)
    return matrix


def main() -> None:
    parser = argparse.ArgumentParser(description="Career Essentials skill planner")
    parser.add_argument("--interactive", action="store_true", help="enter your own skill ratings")
    args = parser.parse_args()

    print("NM1130 - EX.NO: 8 - CAREER ESSENTIALS PLANNER")

    heading("1. SKILL SELF-ASSESSMENT")
    ratings = ask_ratings() if args.interactive else SAMPLE_RATINGS
    if not args.interactive:
        print("  (sample ratings shown - run with --interactive to enter yours)\n")
    show_assessment(ratings)

    heading("2. SKILL-GAP ANALYSIS")
    priorities = gap_analysis(ratings)
    radar_chart(ratings)

    heading("3. SMART GOAL FOR THE TOP PRIORITY SKILL")
    skill = priorities[0] if priorities else "Digital Literacy"
    goal = smart_goal(skill, "completing one structured activity every week",
                      "Track progress weekly and self-rate again at the end", weeks=8)
    for key, value in goal.items():
        print(f"  {key:<11}: {value}")

    heading("4. TIME MANAGEMENT - EISENHOWER MATRIX")
    tasks = [
        ("Submit record for practical exam", True, True),
        ("Prepare for internal test tomorrow", True, True),
        ("Build GitHub portfolio project", False, True),
        ("Update LinkedIn profile", False, True),
        ("Reply to non-essential group chats", True, False),
        ("Scroll social media", False, False),
    ]
    for quadrant, items in eisenhower(tasks).items():
        print(f"  {quadrant}")
        for item in items:
            print(f"     - {item}")

    print("\nResult: Career skills assessed and an improvement plan generated.")


if __name__ == "__main__":
    main()
