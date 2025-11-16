# Test Plan Management Tool

## 📋 Assignment Overview
As part of our ongoing efforts to streamline validation workflows, we introduce a minimal AI-based test plan management tool. This exercise assesses proficiency in AI, Python, web development fundamentals, and the ability to implement simple yet logical features. The assignment is intentionally scoped to be completed within a few hours.

## 🎯 Objective
Develop a basic AI-powered test plan management tool that suggests test steps based on input documents and allows users to create, view, edit, and delete test plans.

## 🏗️ Architecture & Technical Choices

### Backend (FastAPI - Python)
- **Framework**: FastAPI for REST API development with automatic OpenAPI documentation
- **Database**: SQLite with SQLAlchemy ORM (lightweight, file-based)
- **AI Integration**: Local Ollama service with Mistral 7B model
- **Validation**: Pydantic models for request/response validation
- **CORS**: Enabled for frontend-backend communication

### Frontend (React)
- **Framework**: Create React App with hooks-based state management
- **HTTP Client**: Axios for API communication
- **Styling**: Basic CSS with minimal responsive design
- **Loading States**: Real-time feedback during AI generation

### Why These Choices?
- **FastAPI**: Modern, async-ready, automatic documentation, strong typing
- **SQLite**: Zero configuration, suitable for development/demos
- **React**: Industry standard, component-based, efficient for this scale
- **Local AI**: Privacy-focused, no API costs, works offline

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js & npm
- Ollama installed and running
- Mistral model installed (`ollama pull mistral`)

### Installation & Setup

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # (Linux/Mac)
# or venv\Scripts\activate  # (Windows)

# Install dependencies
pip install -r requirements.txt
```

#### Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

### Running the Application

#### Step 1: Start Ollama AI Service (Terminal 1)
```bash
ollama serve
```
*Note: Ollama must be running for AI suggestions to work*

#### Step 2: Start Backend Server (Terminal 2)
```bash
cd backend
source venv/bin/activate  # Activate virtual environment
uvicorn backend.main:app --reload
```
Backend will be available at: `http://localhost:8000`
API Documentation: `http://localhost:8000/docs`

#### Step 3: Start Frontend Application (Terminal 3)
```bash
cd frontend
npm start
```
Frontend will be available at: `http://localhost:3000` (opens automatically)

## 📖 Usage Guide

### Core Features

#### 1. View Test Plans
- All test plans are listed on the main page
- Each plan shows title, description, and associated test steps
- Edit/Delete buttons for each plan

#### 2. Create New Test Plan
- Click "Create Plan" section
- Fill in title and description
- Add test steps by clicking "Add Step"
- Click "Create" to save

#### 3. Edit Existing Plan
- Click "Edit" button on any existing plan
- Modify title, description, or test steps
- Click "Save" to update

#### 4. AI-Powered Test Suggestions
- Enter document text (requirements, specifications, etc.)
- Click "Get Suggestions"
- AI generates: Intelligent title, description, and test steps
- Click "Import Suggestions as New Plan" to create plan from AI output

### Example Document Input
```
Our login system requires users to authenticate with email and password.
Users should be able to reset their password via email link.
The system must validate input formats and prevent brute force attacks.
```

### Expected AI Output
**Title**: User Authentication System Testing
**Description**: Comprehensive testing for login, registration, and security features
**Steps**:
1. Verify email/password login functionality
2. Test password reset via email link
3. Validate input format requirements
4. Check brute force attack prevention
5. Test session management and logout

## 🔧 Technical Implementation Details

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
- **GitHub Copilot**: Code completion and suggestions throughout development
- **ChatGPT-4**: Initial project planning and architecture decisions
- **Claude**: Code review and optimization suggestions (specifically for React component structure)
- **Perplexity**: Research on FastAPI-SQLAlchemy integration patterns

### Specific AI-Assisted Features
1. **Database Relationship Setup**: Copilot suggested optimal SQLAlchemy relationship configuration
2. **React State Management**: Claude provided best practices for handling complex form states
3. **Error Handling Patterns**: ChatGPT recommended comprehensive try-catch blocks and user feedback mechanisms
4. **CORS Configuration**: Copilot assisted with proper FastAPI CORS middleware setup
5. **API Request Formatting**: Claude suggested optimal Axios configuration for the frontend

### AI-Generated Content vs Original Code
- **AI Generated**: ~40% of code (boilerplate, configuration, standard patterns)
- **Original Implementation**: ~60% of code (business logic, custom features, integration logic)
- **AI Refinement**: Used AI suggestions but adapted them to fit specific requirements

## ⚠️ Known Limitations & Future Enhancements

### Current Limitations
- **Database**: SQLite (not suitable for production multi-user scenarios)
- **AI**: Requires local Ollama installation and sufficient hardware
- **UI**: Basic styling, non-responsive design
- **Authentication**: No user authentication or authorization
- **Validation**: Basic frontend validation only

### Potential Enhancements
- **Database**: PostgreSQL with connection pooling
- **AI**: Cloud-based alternatives (OpenAI, Claude API) for better reliability
- **UI**: Modern design system (Material-UI, Tailwind CSS)
- **Features**: Test execution tracking, reports, team collaboration
- **Security**: User authentication, data encryption, API rate limiting

## 🧪 Testing & Validation

### Manual Testing Performed
- ✅ Test plan CRUD operations
- ✅ AI suggestion generation with various document types
- ✅ Frontend-backend communication
- ✅ Error handling and loading states
- ✅ Database relationships and constraints

### Performance Notes
- **AI Generation**: 5+ seconds (normal for local LLM inference)
- **API Response**: <100ms for standard CRUD operations
- **Frontend Load**: Instant with local development server

## 📁 Project Structure
```
test-plan-management-tool/
├── backend/
│   ├── __init__.py          # Python package marker
│   ├── main.py             # FastAPI application & routes
│   ├── models.py           # SQLAlchemy database models
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   ├── index.html      # React HTML template
│   │   └── manifest.json   # PWA manifest
│   └── src/
│       ├── App.js          # Main React component
│       ├── App.css         # Component styles
│       ├── index.js        # React entry point
│       └── index.css       # Global styles
└── README.md               # This documentation
```

## 🏆 Development Highlights

### Clean Architecture
- Clear separation between frontend and backend
- RESTful API design
- Proper error handling and user feedback
- Responsive state management

### AI Integration
- Local, privacy-focused AI approach
- Structured prompt engineering for consistent results
- Graceful fallbacks when AI is unavailable

### User Experience
- Real-time loading indicators during AI generation
- Intuitive import workflow for AI suggestions
- Optimized for quick test plan creation and management

---

## 📞 Support & Contact

This tool demonstrates fundamental concepts in modern web development with AI integration. For questions or feedback, please refer to the codebase and implementation patterns.

**Built with**: FastAPI, React, SQLAlchemy, Ollama/Mistral, and modern Python/JavaScript practices.
