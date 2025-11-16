# Test Plan Management Tool

A minimal AI-based test plan management tool that suggests test steps from documents and provides CRUD operations for test plans.

## 🏗️ Architecture

**Backend**: FastAPI with SQLite/SQLAlchemy
**Frontend**: React with basic CSS styling
**AI**: Local Ollama with Mistral model for test step generation
**Communication**: REST API with CORS enabled

## 🚀 Quick Start

### Prerequisites
- Python 3.13+, Node.js, Ollama (`ollama serve`, `ollama pull mistral`)

### Setup & Run
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
uvicorn backend.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm start
```

## 📖 Usage
- Visit `http://localhost:3000` to access the web interface
- Create/view/edit/delete test plans with titles, descriptions, and test steps
- Use "Suggest Test Steps" to generate AI recommendations from document text
- Import AI suggestions directly into new test plans

## Technical Implementation Details

### Database Schema
```python
# backend/models.py
TestPlan:
  - id: Primary Key (Integer)
  - title: Indexed String
  - description: String

TestStep:
  - id: Primary Key (Integer)
  - description: String
  - plan_id: Foreign Key → TestPlan.id
```

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/plans` | List all test plans |
| POST | `/plans` | Create new test plan |
| GET | `/plans/{id}` | Get specific test plan |
| PUT | `/plans/{id}` | Update test plan |
| DELETE | `/plans/{id}` | Delete test plan |
| POST | `/suggest` | Generate AI test plan from document |

### AI Integration
- **Model**: Mistral 7B (local via Ollama)
- **Task**: Structured test plan generation
- **Input**: Free-form document text
- **Output**: Title, description, and numbered test steps

## 🤖 AI Assistance Used

### Development Tools & Libraries
- **Cline**: Frontend React code generation and optimization
- **GitHub Copilot**: FastAPI boilerplate, SQLAlchemy model setup, CORS configuration
- **ChatGPT-4**: Backend code implementation, API endpoint logic, AI integration patterns

*All code logic was implemented or modified to fit specific requirements*

## 🎯 Assignment Deliverables
- **Repository**: Self-contained with setup scripts
- **Documentation**: This README covers approach, AI citation, and usage
- **Code Quality**: Clean separation between backend/frontend, documented code

**Built with**: FastAPI, React, SQLAlchemy, Ollama/Mistral, and modern Python/JavaScript practices.
