# Test Plan Management Tool

## Overview
This is a minimal AI-based test plan management tool. 

## Architecture & Technical Choices

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
- **Local Mixtral**: Privacy-focused, no API costs, works offline, 7B works well for relatively complex tasks like summarizing a long description into test steps

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Node.js & npm
- Ollama installed and running
- Mistral model installed (`ollama pull mistral`)
- This application requires adequate system resources, especially for AI-powered features. On systems with limited RAM (e.g., 8GB or less), performance may be significantly slower or unusable due to the computational demands of the Mistral 7B model via Ollama.


### Installation & Setup

#### Install
```bash
git clone https://github.com/reknahs/test-plan-management-tool.git
```

#### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create Python virtual environment
python3 -m venv venv

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

#### Step 1: Start Ollama AI Service
```bash
ollama serve
```
If you navigate to `http://localhost:11434/` and it says `Ollama`, you're good to go. 
*Note: Ollama must be running for AI suggestions to work*

#### Step 2: Start Backend Server (Terminal 1)
```bash
# Navigate to project root directory
cd [project-directory]
source backend/venv/bin/activate  # Activate virtual environment
uvicorn backend.main:app --reload
```
API Documentation: `http://localhost:8000/docs`

#### Step 3: Start Frontend Application (Terminal 2)
```bash
cd frontend
npm start
```
Frontend will be available at: `http://localhost:3000`

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

#### 4. AI-Based Test Suggestions
- Enter document text (requirements, specifications, etc.)
- Click "Get Suggestions"
- AI generates title, description, and test steps
- Click "Import Suggestions as New Plan" to create plan from AI output
- Click "Create" to save to list of test plans

### Example Document Input
```
Feature: File Processing Service

The system should allow users to upload CSV files via an API endpoint. 
Uploaded files should be validated to ensure they have the required columns: "name", "email", and "age". 
The backend should parse the CSV, transform the data by normalizing names to title case, and filtering out rows with invalid email addresses. 
Processed data should be saved to a database. 
Users should be able to request a summary report that counts the number of valid and invalid rows in each file. 
Errors during processing should be logged and returned to the user with meaningful messages.
```

### AI Output
**Title**: File Processing Service API Test Plan

**Description**: This test plan focuses on validating the functionality and error handling of the File Processing Service API, ensuring proper upload, validation, parsing, normalization, filtering, saving, and reporting of CSV data, as well as logging errors.

**Steps**:
1. Set up test environment, including the API endpoint, test database, and test files with valid and invalid data.
2. Test successful file upload by sending a valid CSV file via the API endpoint and verifying its presence in the database.
3. Test validation of required columns "name", "email", and "age" by providing CSV files with missing or incorrect column names.
4. Test normalization of names to title case by comparing the saved data with the original test files.
5. Test email address filtering by sending a CSV file containing both valid and invalid email addresses, and verifying that only the valid emails are saved in the database.
6. Generate and verify summary reports, counting the number of valid and invalid rows in each processed file.
7. Test error handling by intentionally introducing various errors (e.g., incorrect data types, corrupted CSV files) and ensuring that meaningful error messages are returned to the user.
8. Log and review API response logs to validate that errors during processing have been logged as expected.

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
- **VSCode**: Used for running project
- **Cline (free x-ai/grok-code-fast-1)**: Used for planning structure of project, generating most of the frontend, and generating most of the code for database models
- **ChatGPT-4**: Used for helping with generating the REST API parts of the backend 

### Specific AI-Assisted Features
1. Database Relationship Setup
2. React State Management
3. Error Handling Patterns
4. CORS Configuration
5. API Request Formatting 

## Testing

### Manual Testing Performed
- Test plan CRUD operations
- AI suggestion generation with different document types
- Frontend-backend communication
- Error handling

### Performance Notes
- **AI Generation**: 5+ seconds 
- **API Response**: <100ms for standard CRUD operations

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

## Examples


![1](images/homepage.png)




![2](images/ai.png)




![3](images/aigenerated.png)



