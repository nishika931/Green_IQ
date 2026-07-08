# 🌱 GreenIQ - AI Powered Plant Care Assistant

GreenIQ is an AI-powered Plant Care Assistant that helps users take better care of their plants using Artificial Intelligence, live weather data, and plant information APIs.

The application combines **LangGraph Multi-Agent Architecture**, **LangChain**, **Groq LLM**, **FastAPI**, **React**, and **PostgreSQL** to provide personalized plant care recommendations.

---

# 🚀 Features

- 🔐 User Authentication (JWT)
- 🌱 Plant Library
- 🔍 Search Plants using Perenual API
- 🤖 AI Plant Doctor
- 🌦️ Live Weather-Based Plant Advice
- 🦠 Plant Disease Detection Agent
- 💬 Chat History
- 📍 Location-based Plant Care
- 🧠 Multi-Agent AI using LangGraph
- ⚡ FastAPI Backend
- ⚛️ React Frontend
- 🐘 PostgreSQL Database

---

# 🧠 AI Agents

## Supervisor Agent
Routes the user query to the correct specialized AI agent.

## Plant Care Agent
Provides watering, sunlight, fertilizer, soil, humidity, and seasonal care recommendations.

Uses:
- Plant Database
- Weather API
- Groq LLM

## Disease Agent
Analyzes plant disease symptoms and provides:

- Possible Disease
- Cause
- Treatment
- Prevention

---

# 🌦 APIs Used

## OpenWeather API

Provides:

- Temperature
- Humidity
- Weather Condition
- Wind Speed

Used to generate weather-aware plant care advice.

---

## Perenual Plant API

Provides:

- Plant Information
- Scientific Name
- Family
- Watering Needs
- Sunlight
- Soil
- Maintenance
- Growth Rate
- Hardiness
- Images
- Description

---

# 🛠 Tech Stack

## Frontend

- React
- React Router
- Axios
- Tailwind CSS

## Backend

- FastAPI
- LangChain
- LangGraph
- Groq LLM
- SQLAlchemy
- JWT Authentication

## Database

- PostgreSQL

---

# 📂 Project Structure

```
backend
│
├── agents
├── graph
├── models
├── routes
├── schema
├── services
├── tools
├── db
├── core
└── main.py

frontend
│
├── src
│   ├── components
│   ├── pages
│   ├── api
│   ├── context
│   └── App.jsx
```

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/nishika931/GreenIQ.git
```

---

## Backend

```bash
cd backend
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
uvicorn main:app --reload
```

---

## Frontend

```bash
cd frontend
npm install
npm run dev
```

---

# Environment Variables

Create a `.env` file.

```
GROQ_API_KEY=your_key

OPENWEATHER_API_KEY=your_key

PERENUAL_API_KEY=your_key

DATABASE_URL=postgresql://username:password@host/database

JWT_SECRET_KEY=your_secret
```

---

# AI Workflow

```
User Question
      │
      ▼
Supervisor Agent
      │
      ▼
───────────────
│        │          
▼        ▼          
Plant   Disease   
Agent    Agent     
│
▼
Weather API
│
▼
Plant Database
│
▼
Groq LLM
│
▼
AI Response
│
▼
Save Chat History
```

---

# Database

## Users

- Register
- Login
- JWT Authentication

## Plants

Stores:

- Plant Information
- Care Details
- Location

## Chat History

Stores:

- User Question
- AI Response
- Plant
- Timestamp

# Screenshots

./ScreenShots

---

Live Link :- https://green-iq-bice.vercel.app/

# Author

**Nishika Sahu**

Agentic AI | Full Stack Developer

---

# License

This project is developed for educational and learning purposes.
