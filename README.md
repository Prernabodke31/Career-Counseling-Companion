# 🎓 Agentic Career Counseling Companion
### Powered by IBM Granite on WatsonX.ai

> **Problem Statement #15** — An intelligent, autonomous AI agent that continuously monitors student performance, evolving interests, and real-time labor market trends to deliver tailored career pathway suggestions.

---

## 🏗️ Architecture

```
career-counseling-companion/
├── backend/                     # FastAPI Python Backend
│   ├── main.py                  # Application entry point
│   ├── config.py                # Settings (reads .env)
│   ├── database.py              # SQLAlchemy + SQLite setup
│   ├── .env                     # IBM Cloud credentials (root level)
│   ├── requirements.txt         # Python dependencies
│   ├── agents/
│   │   └── career_agent.py      # 🤖 IBM Granite Agentic Orchestrator
│   ├── services/
│   │   ├── granite_service.py   # IBM WatsonX.ai / Granite SDK integration
│   │   ├── market_service.py    # Labor market intelligence (JSearch API)
│   │   └── auth_service.py      # JWT authentication
│   ├── models/
│   │   └── models.py            # SQLAlchemy ORM models
│   └── routes/
│       ├── auth.py              # Register / Login
│       ├── students.py          # Student profile & academic records
│       ├── assessment.py        # Interest / Aptitude / Personality tests
│       ├── career.py            # AI career recommendations & chat
│       └── market.py            # Labor market data endpoints
│
└── frontend/                    # React + Vite Frontend
    ├── src/
    │   ├── App.jsx              # Router + Layout Shell
    │   ├── AuthContext.jsx      # Auth state management
    │   ├── api.js               # Axios instance + interceptors
    │   ├── index.css            # IBM Carbon-inspired styles
    │   └── pages/
    │       ├── Login.jsx
    │       ├── Register.jsx
    │       ├── Dashboard.jsx    # Stats + market overview
    │       ├── Profile.jsx      # Academic profile + grades
    │       ├── Assessment.jsx   # Self-assessment quizzes
    │       ├── CareerPlan.jsx   # IBM Granite recommendations
    │       ├── Chat.jsx         # Conversational AI counselor
    │       └── Market.jsx       # Live job market data
    └── package.json
```

---

## ⚙️ IBM Cloud Services Used

| Service | Purpose |
|---|---|
| **IBM WatsonX.ai** | Hosts IBM Granite LLM |
| **IBM Granite 3 8B Instruct** | Generates career recommendations, chat responses, skill gap analysis |
| **IBM IAM** | API key authentication |

---

## 🚀 Quick Start

### 1. Configure IBM Granite Credentials

Edit `.env` in the project root:

```env
IBM_WATSONX_API_KEY=your_api_key_here
IBM_WATSONX_PROJECT_ID=your_project_id_here
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
IBM_GRANITE_MODEL_ID=ibm/granite-3-8b-instruct
```

**Get credentials:**
1. Sign up at [IBM Cloud](https://cloud.ibm.com) (Free Lite account)
2. Create a **WatsonX.ai** service instance
3. Create a **Project** in WatsonX.ai Studio
4. Generate an **API Key** in IBM Cloud IAM

### 2. Start the Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```

Backend available at: `http://localhost:8000`  
API Docs: `http://localhost:8000/api/docs`

### 3. Start the Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend available at: `http://localhost:3000`

---

## 🤖 Agentic Workflow

```
Student Input
    │
    ▼
┌─────────────────────────────────────────────┐
│           Career Counseling Agent           │
│  (backend/agents/career_agent.py)           │
│                                             │
│  1. Read academic profile + GPA + grades    │
│  2. Load assessment scores (interest/       │
│     aptitude/personality)                   │
│  3. Fetch real-time labor market data       │
│  4. Build context-rich prompt               │
│  5. Call IBM Granite on WatsonX.ai          │
│  6. Parse + structure the response          │
│  7. Store career plan in database           │
└─────────────────────────────────────────────┘
    │
    ▼
Personalized Career Pathways + Action Plan
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Create student account |
| POST | `/api/auth/login` | Login and get JWT token |

### Student Profile
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/me` | Get my profile + academic records |
| PUT | `/api/students/me` | Update profile |
| POST | `/api/students/me/academic-records` | Add subject/grade |
| DELETE | `/api/students/me/academic-records/{id}` | Remove record |

### Assessment
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/assessment/questions/{type}` | Get questions (interest/aptitude/personality) |
| POST | `/api/assessment/submit` | Submit assessment answers |
| GET | `/api/assessment/history` | View past assessments |

### Career Guidance (IBM Granite)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/career/recommend` | 🤖 Generate AI career plan |
| GET | `/api/career/plans` | View all career plans |
| POST | `/api/career/chat` | Chat with AI counselor |
| GET | `/api/career/chat/history` | Get chat history |
| POST | `/api/career/skills-gap` | Analyze skill gaps for a target career |

### Labor Market
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/market/overview` | Market trends + hot roles |
| GET | `/api/market/jobs?role=X&location=Y` | Live job listings |
| GET | `/api/market/in-demand-skills` | Top skills in demand |
| GET | `/api/market/salary/{role}` | Salary data for a role |

---

## 🔑 Environment Variables

See [`.env`](.env) for the full list. Key variables:

| Variable | Description |
|---|---|
| `IBM_WATSONX_API_KEY` | Your IBM Cloud API key |
| `IBM_WATSONX_PROJECT_ID` | WatsonX.ai project ID |
| `IBM_GRANITE_MODEL_ID` | Model ID (default: `ibm/granite-3-8b-instruct`) |
| `DATABASE_URL` | SQLite (default) or PostgreSQL |
| `SECRET_KEY` | JWT secret key |
| `RAPID_API_KEY` | Optional: RapidAPI key for live job listings |

---

## 🎯 Features

- ✅ **Student Registration & Authentication** (JWT)
- ✅ **Academic Profile Management** (GPA, subjects, grades)
- ✅ **3-Part Self-Assessment** (Interest, Aptitude, Personality)
- ✅ **AI Career Pathway Recommendations** powered by IBM Granite
- ✅ **Conversational AI Career Counselor** (chat interface)
- ✅ **Skills Gap Analyzer** for target careers
- ✅ **Real-time Labor Market Intelligence**
- ✅ **Live Job Listings** via JSearch API
- ✅ **Salary Range Data** by role
- ✅ **Career Plan History** tracking
- ✅ **IBM Carbon Design** inspired UI

---

## 🧠 IBM Granite Integration

The system uses **IBM Granite 3 8B Instruct** via the `ibm-watsonx-ai` SDK:

```python
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

model = ModelInference(
    model_id="ibm/granite-3-8b-instruct",
    credentials=Credentials(url=URL, api_key=API_KEY),
    project_id=PROJECT_ID,
)
response = model.generate_text(prompt=career_prompt)
```

**Note:** The app runs in **mock mode** if credentials are not configured — ideal for development and demos.

---

## 📦 Tech Stack

| Layer | Technology |
|---|---|
| **AI/LLM** | IBM Granite 3 8B Instruct (WatsonX.ai) |
| **Backend** | FastAPI (Python 3.11+) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **ORM** | SQLAlchemy 2.0 |
| **Auth** | JWT (python-jose + passlib bcrypt) |
| **Frontend** | React 18 + Vite |
| **Styling** | Custom CSS (IBM Carbon inspired) |
| **Market Data** | JSearch API (RapidAPI) |
