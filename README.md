# NM1130 - AI and Digital Skills (Naan Mudhalvan)

**University College of Engineering (BIT Campus), Anna University, Tiruchirappalli**
Department of CSE (AI & ML) | Academic Year 2026-2027 | Semester III

This repository contains one Python program for each experiment in the NM1130 record.
Every program is self-contained, prints a clear step-by-step output, and ends with a *Result* line.

## Experiments

| Ex.No | Experiment | Program | What it demonstrates |
|------:|------------|---------|----------------------|
| 1 | AI Fluency | [`ex01_ai_fluency/ai_fluency.py`](ex01_ai_fluency/ai_fluency.py) | AI timeline, classification, regression, clustering, optimization, neural network, NLP sentiment analysis |
| 2 | AI Productivity | [`ex02_ai_productivity/ai_productivity.py`](ex02_ai_productivity/ai_productivity.py) | Copilot-style assistant: email drafting, summaries, action items, proposals, sales insights (optional real LLM call) |
| 3 | AI Applications | [`ex03_ai_applications/ai_applications.py`](ex03_ai_applications/ai_applications.py) | Healthcare, banking fraud detection, recommendation engine, agriculture yield prediction |
| 4 | LinkedIn: Building Your Professional Brand | [`ex04_linkedin_branding/linkedin_profile_analyzer.py`](ex04_linkedin_branding/linkedin_profile_analyzer.py) | Profile scoring, common-mistake detection, headline generator, before/after chart |
| 5 | Cybersecurity | [`ex05_cybersecurity/cybersecurity_toolkit.py`](ex05_cybersecurity/cybersecurity_toolkit.py) | Password strength, secure generator, salted hashing, phishing URL detector, 2FA (TOTP), data integrity |
| 6 | GitHub Foundations | [`ex06_github_foundations/mini_git.py`](ex06_github_foundations/mini_git.py) | Mini Git: commit, branch, merge, conflict, clone, push, pull request, review |
| 7 | Power BI | [`ex07_power_bi/power_bi_dashboard.py`](ex07_power_bi/power_bi_dashboard.py) | Get data, clean (Power Query), KPIs (DAX), dashboard image, CSV export for Power BI Desktop |
| 8 | Career Essentials | [`ex08_career_essentials/career_essentials.py`](ex08_career_essentials/career_essentials.py) | Skill self-assessment, gap analysis, radar chart, SMART goals, Eisenhower matrix |

## How to run

```bash
# 1. (optional) create a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # macOS / Linux

# 2. install the libraries
pip install -r requirements.txt

# 3. run any experiment
python ex01_ai_fluency/ai_fluency.py
python ex08_career_essentials/career_essentials.py --interactive
```

Requires Python 3.10 or newer. Experiments 2, 5 and 6 need no extra libraries.
Charts and CSV files are created in the same folder as the program that makes them.

## Output files

- `ex04_linkedin_branding/profile_improvement.png`
- `ex07_power_bi/sales_dashboard.png`, `sales_clean.csv` (import into Power BI Desktop)
- `ex08_career_essentials/career_skills_radar.png`
