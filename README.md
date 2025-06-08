# 📰 AI Bulletin

**Let the AI read the news — You read the bulletin.**

A fully autonomous, AI-powered weekly tech newsletter that summarizes the top stories, dives deep into trends, and delivers beautifully formatted content straight to your inbox.

---

## 🚀 Overview

**AI Bulletin** is a self-operating newsletter system designed to:

* 🧠 Use **CrewAI** agents to generate insightful, structured content
* 📨 Deliver formatted newsletters via **SendGrid**
* ⚡ Run on a lightweight **FastAPI** backend
* 🗓️ Schedule and automate weekly generation and delivery using **APScheduler**

Built for AI-curious hackers who want to stay informed.

---

## 🎯 Project Goal

To automate every part of a newsletter workflow:

1. ✍️ Curate and plan relevant content
2. 🔍 Summarize and analyze top stories
3. 🖋️ Format a professional-grade newsletter
4. 📤 Email it to all subscribers

Without any human in the loop. Just subscribe and enjoy.

---

## 🧠 Agents & Responsibilities

| Agent                        | Responsibility                                   |
| ---------------------------- | ------------------------------------------------ |
| **TopicPlannerAgent**        | Plans weekly theme and outlines subtopics        |
| **TopStoriesAgent**          | Summarizes the top 3 tech/AI stories             |
| **DeepDiveAgent**            | Provides in-depth analysis on a major topic      |
| **ToolOfTheWeekAgent**       | Recommends trending AI tool with summary         |
| **QuoteAgent**               | Picks a relevant quote or tweet                  |
| **AIInTheWildAgent**         | Highlights a real-world AI use case              |
| **HotTakesAgent**            | Adds quick, opinionated commentary               |
| **EditorsNoteAgent**         | Writes a personalized closing note               |
| **NewsletterEditorAgent**    | Edits and compiles all section drafts            |
| **HTMLFormatterAgent**       | Styles and formats final HTML for email delivery |

---

## 🧱 Architecture

### 🔁 System Flow

1. `PlanTopicsTask` ← Done by TopicPlannerAgent
2. `[Parallel]` TopStoriesTask, DeepDiveTask, ToolTask, QuoteTask, AIWildTask, HotTakesTask, EditorsNoteTask
3. `EditNewsletterTask` ← NewsletterEditorAgent
4. `FormatHTMLTask` ← HTMLFormatterAgent
5. 🚀 Email is sent via SendGrid

### 📊 Architectural Diagram (Textual)

```
CrewManagerAgent
  │
  ▼
TopicPlannerAgent
       │
       ▼
┌────────────────────────────────────────────────────┐
│    Runs in Parallel                                │
│ ┌────────────┬────────────┬────────────┬─────────┐ │
│ │TopStories  │ DeepDive   │ ToolOfWeek │ Quote   │ │
│ │Agent       │ Agent      │ Agent      │ Agent   │ │
│ └────────────┴────────────┴────────────┴─────────┘ │
│ ┌────────────┬────────────┐                        │
│ │ AIWild     │ HotTakes   │                        │
│ │ Agent      │ Agent      │                        │
│ └────────────┴────────────┘                        │
└────────────────────────────────────────────────────┘
       │
       ▼
NewsletterEditorAgent
       │
       ▼
HTMLFormatterAgent
```

---

## 🧩 Tech Stack

* **Language**: Python 3.12+
* **Framework**: FastAPI + Jinja2 templates
* **Task Automation**: APScheduler
* **Agents & LLM**: CrewAI (GPT-4 or Deepseek)
* **Database**: SQLite (via SQLAlchemy ORM)
* **Email Services**: SendGrid or any other service (configurable)

---

## 📁 Folder Structure

```
ai-bulletin/
├── main.py              # FastAPI app entry point
├── database.py          # SQLite engine + session config
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas for validation
├── admin.py             # Admin interface or manual overrides
├── newsletter/          # CrewAI agents, tasks, orchestration
├── crew/                # Crew definitions and configuration
├── jobs/                # APScheduler jobs (weekly trigger)
├── utils/               # Email sender wrappers
├── templates/           # HTML pages for subscription/unsubscribe
├── requirements.txt     # Project dependencies
└── subscribers.db       # SQLite DB (auto-created)
```

---

## ⚙️ Getting Started

### 📦 Prerequisites

* Python 3.10+
* [`uv`](https://github.com/astral-sh/uv): ultra-fast package manager

```bash
curl -Ls https://astral.sh/uv/install.sh | bash
```

### 🛠️ Setup & Installation

```bash
# Clone the repo
$ git clone https://github.com/dev-ahmadbilal/ai-bulletin.git
$ cd ai-bulletin

# Create virtual environment
$ uv venv .venv
$ source .venv/bin/activate

# Install dependencies
$ uv pip install -r requirements.txt
```

### 🚀 Run Locally

```bash
uvicorn main:app --reload
```

### 🌐 Test Email Subscription

```bash
curl -X POST http://localhost:8000/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "example@domain.com"}'
```

---

## 📬 API Endpoints

| Method | Route          | Description             |
| ------ | -------------- | ----------------------- |
| POST   | `/subscribe`   | Subscribe a new email   |
| GET    | `/health`      | Check API health status |
| GET    | `/unsubscribe` | Show unsubscribe form   |
| POST   | `/unsubscribe` | Unsubscribe from list   |

---

## 🗓️ Automation with APScheduler

* The `newsletter_job` is triggered every Sunday at 10 AM:

```python
CronTrigger(day_of_week="sun", hour=10, minute=0)
```

* You can change the schedule in `jobs/newsletter_job.py`

---

## 🧹 How It Works for Subscribers

* ✉️ When a new user subscribes, they **instantly receive the latest edition** of the newsletter.  
* 📫 We recommend checking your **spam or junk folder** if you don’t see the email.  
* 🗓️ After that, new editions are delivered to all subscribers **automatically every week**.  

---

## 🎁 Sponsors

**AI Bulletin is currently looking for sponsors!**

If you're a company or individual who believes in the power of open-source, agentic AI systems, and automated media — let's collaborate.

Want to sponsor AI Bulletin?  
➡️ [ahmadbilal.3491@gmail.com](mailto:ahmadbilal.3491@gmail)

---

## ☕ Support Ahmad

If you enjoy AI Bulletin, consider buying me a coffee:

➡️ [https://buymeacoffee.com/ahmad.bilal](https://buymeacoffee.com/ahmad.bilal)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE)

---

## 🤝 Contributing

Feel free to fork and submit PRs for enhancements, fixes, or new agent ideas.

---

## 🙌 Acknowledgements
* Shoutout to Ed Donner for an amazing Agentic ai course. 
* CrewAI by Vercel & LangChain community
* APScheduler for painless job scheduling
* SendGrid for simple transactional email delivery


