# FitBuddy – AI Fitness Plan Generator using Gemini Models

FitBuddy is an AI-powered fitness web application that generates personalized 7-day workout routines and tailored nutrition/recovery tips based on a user's unique goals, intensity preferences, and physical stats. Built with **FastAPI**, **SQLite (SQLAlchemy)**, and **Google Gemini AI models** (**Gemini 1.5 Pro** & **Gemini 1.5 Flash**).

---

## 🚀 Key Features & Scenarios

- **Scenario 1: Personalized 7-Day Workout Generation**
  - Users input their Name, User ID, Age, Weight, Fitness Goal (e.g., *muscle gain*, *weight loss*, *flexibility*), and Workout Intensity (*Low*, *Medium*, *High*).
  - The system generates a structured day-by-day plan (Warm-up, Main Workout with sets & reps, and Cooldown) using **Gemini 1.5 Pro**.
- **Scenario 2: Dynamic Feedback & Iterative Plan Refinement**
  - Users can submit feedback (e.g., *"more focus on cardio"*, *"add yoga & core exercises"*, *"include more rest days"*).
  - **Gemini 1.5 Pro** refines the original workout routine while preserving the structured layout and updates the database.
  - A confirmation message banner (*"Your plan has been updated based on your feedback!"*) is displayed alongside the updated plan.
- **Scenario 3: AI Nutrition & Recovery Tips**
  - Instant, actionable dietary advice (e.g., protein recommendations, hydration, micronutrients) generated via **Gemini 1.5 Flash**.
- **Scenario 4: Coach & Admin Dashboard (`/view-all-users`)**
  - Centralized dashboard displaying all registered users, their demographic info, fitness goals, intensity, original plans, and updated plans in a formatted table.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** FastAPI, Python 3.11+, Uvicorn (ASGI)
- **AI Layer:** Google Generative AI SDK (`google-generativeai`)
  - `gemini-1.5-pro`: Structured 7-day workout plans & feedback-based revisions
  - `gemini-1.5-flash`: Fast, concise nutrition and recovery tips
- **Database:** SQLite with SQLAlchemy ORM (`fitbuddy.db`)
- **Frontend & Templating:** Jinja2 templates, HTML5, Vanilla CSS with modern glassmorphism, responsive grid & flexbox layouts, Google Fonts (*Outfit* & *Roboto*)
- **Data Validation:** Pydantic models (`UserInput`, `FeedbackRequest`, `WorkoutRequest`)

---

## 📁 Project Structure

```
fitbuddy/
│
├── requirements.txt            # Project dependencies
├── .env                        # Environment variables (Google Gemini API key)
├── .env.example                # Example environment configuration
├── fitbuddy.db                 # Local SQLite database (auto-generated)
├── main.py                     # Root entry point
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application instance & static mount
│   ├── routes.py               # Route handlers (HTML & REST APIs)
│   ├── database.py             # SQLAlchemy models & database CRUD operations
│   ├── schemas.py              # Pydantic validation schemas
│   ├── gemini_generator.py     # Gemini 1.5 Pro workout generator
│   ├── gemini_flash_generator.py # Gemini 1.5 Flash nutrition tip generator
│   ├── updated_plan.py         # Feedback-based plan updater (Gemini 1.5 Pro)
│   └── nutrition.py            # Nutrition profile helper utilities
│
├── templates/
│   ├── index.html              # Homepage with user input form
│   ├── result.html             # Workout plan, nutrition tip & feedback form
│   └── all_users.html          # Admin dashboard with user & plan table
│
├── static/
│   └── images/
│       └── gym-bg.jpg          # Fitness-themed background asset
│
└── test_app.py                 # End-to-end automated test suite
```

---

## ⚙️ Installation & Setup

### 1. Clone or Open Workspace
```bash
cd fitbuddy
```

### 2. Create and Activate Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Google Gemini API Key
Create or edit the `.env` file in the project root:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
```
> **Note:** If no API key is provided or the API is unreachable, FitBuddy includes a fallback generation engine to ensure the UI and workflows function seamlessly.

---

## 🏃 Running the Application

Start the FastAPI development server with Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
Or simply:
```bash
python main.py
```

- **Web Application:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Admin Dashboard:** [http://127.0.0.1:8000/view-all-users](http://127.0.0.1:8000/view-all-users)
- **Interactive Swagger Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Alternative ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints Reference

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Renders homepage with user intake form |
| `POST` | `/generate-workout` | Processes form submission, generates plan & tip, renders `result.html` |
| `POST` | `/submit-feedback` | Refines workout plan using user feedback, renders `result.html` |
| `GET` | `/view-all-users` | Renders admin dashboard listing all users and plans |
| `POST` | `/delete-user/{user_id}` | Removes a user and their workout plans |
| `POST` | `/generate-workout/gemini` | REST API: Generates workout JSON via Gemini Pro |
| `GET` | `/nutrition-tip` | REST API: Generates nutrition tip JSON via Gemini Flash |
| `POST` | `/generate-plan` | REST API: Creates user and saves generated plan |
| `POST` | `/update-plan/{user_id}` | REST API: Updates existing plan based on feedback |
| `GET` | `/api/users` | REST API: Returns all users and plan status in JSON |
| `GET` | `/health` | Health check endpoint |

---

## 🧪 Testing

Run the automated test suite covering all 10 core integration scenarios:

```bash
python test_app.py
```

All tests validate:
- Homepage rendering and form inputs
- Form-based workout generation and database persistence
- Feedback-based plan refinement and alert confirmation
- Admin dashboard rendering and table view
- All REST API endpoints and data schemas
- User deletion and cascade handling
