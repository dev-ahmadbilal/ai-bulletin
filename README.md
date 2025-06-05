# 🧠 AI Bulletin

**Let the AI read the news — You read the bulletin.**  
A weekly, AI-generated tech newsletter that summarizes the top stories, dives deep into trending topics, and delivers them straight to your inbox.

---

## 🚀 Project Overview

AI Bulletin is an automated newsletter system built with:

- 🤖 **CrewAI** agents for content generation
- ⚡ **FastAPI** for backend APIs
- 📨 **Email delivery** with Resend or SendGrid
- 📅 **Automated scheduling** for weekly runs

The goal is to provide tech enthusiasts with a high-quality, AI-curated bulletin every week — generated and delivered end-to-end without human input.

---

## 🧩 Current Status: MVP Phase

The MVP includes:

- ✅ Email subscription API (`POST /subscribe`)
- ✅ SQLite integration for storing emails
- ✅ Minimal FastAPI setup using `uv`
- 🛠️ (In Progress) CrewAI-based newsletter generation

---

## 📁 Folder Structure

```

ai-bulletin/
├── main.py              # FastAPI app entry point
├── database.py          # SQLite engine + session config
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas for validation
├── requirements.txt     # Project dependencies
└── subscribers.db       # SQLite DB (auto-created)

````

---

## ⚙️ Getting Started

### 📦 Prerequisites

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv): a faster package/dependency manager

Install `uv`:
```bash
curl -Ls https://astral.sh/uv/install.sh | bash
````

---

### 🛠️ Setup

```bash
# Clone repo
git clone https://github.com/yourname/ai-bulletin.git
cd ai-bulletin

# Create virtual environment
uv venv .venv
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

---

### 🚀 Run the App

```bash
uvicorn main:app --reload
```

Test it using `curl` or Postman:

```bash
curl -X POST http://localhost:8000/subscribe \
  -H "Content-Type: application/json" \
  -d '{"email": "example@domain.com"}'
```

---

## 📌 API Endpoints

| Method | Route        | Description          |
| ------ | ------------ | -------------------- |
| POST   | `/subscribe` | Subscribe with email |
| GET    | `/health`    | Health check         |

---

## 📬 What's Next

* 🧠 Integrate CrewAI agents for newsletter generation
* 📨 Email delivery using Resend API
* 🗓️ Weekly automation with APScheduler or GitHub Actions
* 🗃️ Archive past newsletters
* 🌐 Serve a minimal HTML subscription form

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## ✨ Tagline Reminder

> **Let the AI read the news — You read the bulletin.**

