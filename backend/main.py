from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
"""
Test Plan Management Tool - Backend (FastAPI)

This module provides a REST API for managing test plans with CRUD operations
and AI-powered test step suggestions using local Ollama models.

Core Features:
- Test Plan CRUD operations (Create, Read, Update, Delete)
- Individual test step management within plans
- AI-generated test plan suggestions from documents
- SQLite database with SQLAlchemy ORM
"""

import requests
import json
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from .models import TestPlan, TestStep, get_db

# Initialize FastAPI application
app = FastAPI(
    title="Test Plan Management Tool",
    description="AI-powered test plan management with REST API",
    version="1.0.0"
)

# Enable CORS for frontend communication
# Allows requests from React dev server running on localhost:3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React development server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Pydantic models for API request/response validation and serialization

class TestStepBase(BaseModel):
    """Base model for test step data"""
    description: str

class TestPlanBase(BaseModel):
    """Base model containing common test plan fields"""
    title: str
    description: str

class TestPlanCreate(TestPlanBase):
    """Model for creating new test plans (includes steps)"""
    steps: List[TestStepBase] = []

class TestPlanResponse(TestPlanBase):
    """Response model for test plan data (includes ID from database)"""
    id: int
    steps: List[TestStepBase] = []

    class Config:
        # Pydantic v2: use from_attributes instead of orm_mode
        from_attributes = True  # Allow conversion from SQLAlchemy models

class SuggestRequest(BaseModel):
    """Input model for AI suggestion requests"""
    document: str

class SuggestResponse(BaseModel):
    """Response model for AI-generated test plan suggestions"""
    title: str          # AI-generated title
    description: str    # AI-generated description
    steps: List[str]    # AI-generated test steps

# API Endpoints for Test Plan Management

@app.get("/plans", response_model=List[TestPlanResponse])
def read_plans(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    """
    Retrieve all test plans with pagination support.

    - **skip**: Number of plans to skip (for pagination)
    - **limit**: Maximum number of plans to return (default: 10)
    - **Returns**: List of TestPlanResponse objects
    """
    plans = db.query(TestPlan).offset(skip).limit(limit).all()
    return plans

@app.post("/plans", response_model=TestPlanResponse)
def create_plan(plan: TestPlanCreate, db: Session = Depends(get_db)):
    """
    Create a new test plan with its associated test steps.

    - **plan**: TestPlanCreate object containing title, description, and steps
    - **Returns**: Created TestPlanResponse with generated ID
    """
    # Create the test plan
    db_plan = TestPlan(title=plan.title, description=plan.description)
    db.add(db_plan)
    db.flush()  # Get the generated ID before committing

    # Add associated test steps
    for step in plan.steps:
        db_step = TestStep(description=step.description, plan_id=db_plan.id)
        db.add(db_step)

    db.commit()  # Persist to database
    db.refresh(db_plan)  # Refresh to get all data
    return db_plan

@app.get("/plans/{plan_id}", response_model=TestPlanResponse)
def read_plan(plan_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single test plan by its ID.

    - **plan_id**: Unique identifier of the test plan
    - **Returns**: TestPlanResponse object or 404 if not found
    """
    plan = db.query(TestPlan).filter(TestPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@app.put("/plans/{plan_id}", response_model=TestPlanResponse)
def update_plan(plan_id: int, plan: TestPlanCreate, db: Session = Depends(get_db)):
    """
    Update an existing test plan and replace all its test steps.

    - **plan_id**: ID of the test plan to update
    - **plan**: Updated TestPlanCreate data
    - **Returns**: Updated TestPlanResponse or 404 if not found
    """
    db_plan = db.query(TestPlan).filter(TestPlan.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # Update basic fields
    db_plan.title = plan.title
    db_plan.description = plan.description

    # Delete existing steps and add new ones
    db.query(TestStep).filter(TestStep.plan_id == plan_id).delete()
    for step in plan.steps:
        db_step = TestStep(description=step.description, plan_id=plan_id)
        db.add(db_step)

    db.commit()
    db.refresh(db_plan)
    return db_plan

@app.delete("/plans/{plan_id}")
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    """
    Delete a test plan and all its associated test steps.

    - **plan_id**: ID of the test plan to delete
    - **Returns**: Confirmation message or 404 if not found
    """
    plan = db.query(TestPlan).filter(TestPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # SQLAlchemy cascade delete will handle test steps automatically
    db.delete(plan)
    db.commit()
    return {"detail": "Plan deleted"}

@app.post("/plans/{plan_id}/steps", response_model=TestStepBase)
def create_step(plan_id: int, step: TestStepBase, db: Session = Depends(get_db)):
    """
    Add a new test step to an existing test plan.

    - **plan_id**: ID of the parent test plan
    - **step**: TestStepBase object with step description
    - **Returns**: Created TestStepBase or 404 if plan not found
    """
    plan = db.query(TestPlan).filter(TestPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    db_step = TestStep(description=step.description, plan_id=plan_id)
    db.add(db_step)
    db.commit()
    db.refresh(db_step)
    return db_step

@app.put("/steps/{step_id}", response_model=TestStepBase)
def update_step(step_id: int, step: TestStepBase, db: Session = Depends(get_db)):
    """
    Update an existing test step's description.

    - **step_id**: ID of the test step to update
    - **step**: Updated TestStepBase data
    - **Returns**: Updated TestStepBase or 404 if not found
    """
    db_step = db.query(TestStep).filter(TestStep.id == step_id).first()
    if not db_step:
        raise HTTPException(status_code=404, detail="Step not found")

    db_step.description = step.description
    db.commit()
    db.refresh(db_step)
    return db_step

@app.delete("/steps/{step_id}")
def delete_step(step_id: int, db: Session = Depends(get_db)):
    """
    Delete an individual test step.

    - **step_id**: ID of the test step to delete
    - **Returns**: Confirmation message or 404 if not found
    """
    step = db.query(TestStep).filter(TestStep.id == step_id).first()
    if not step:
        raise HTTPException(status_code=404, detail="Step not found")

    db.delete(step)
    db.commit()
    return {"detail": "Step deleted"}

def suggest_plan(document: str) -> dict:
    """
    Generate AI-powered test plan suggestions from a document using Ollama (Mistral model).

    This function creates a structured prompt asking the AI to generate:
    - A concise title for the test plan
    - A brief description
    - A numbered list of practical test steps

    Args:
        document (str): The input document text to generate suggestions from

    Returns:
        dict: Contains 'title', 'description', and 'steps' (list of strings)
              Returns error values if AI generation fails
    """
    # Create a structured prompt for the AI model
    # Instructions ask for specific format: TITLE, DESCRIPTION, STEPS
    prompt = f"""Based on this document, generate a complete test plan with:

1. A concise, descriptive Title for the test plan (max 50 characters)
2. A brief Description (max 100 words)
3. Practical test steps in checklist format (numbered list)

Document:
{document}

Format your response exactly like this:

TITLE: [title here]
DESCRIPTION: [description here]
STEPS:
1. [step 1]
2. [step 2]
etc."""

    # Prepare API request for Ollama
    payload = {
        "model": "mistral",      # AI model to use (installed locally)
        "prompt": prompt,        # Generated prompt with document
        "stream": False          # Non-streaming response
    }

    try:
        # Send request to local Ollama API
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        text = data.get("response", "")

        # Parse AI response using expected format
        lines = text.strip().split('\n')
        title = ""
        description = ""
        steps = []

        section = None  # Track which section we're parsing

        for line in lines:
            line = line.strip()
            if line.startswith('TITLE:'):
                title = line.replace('TITLE:', '').strip()
                section = None
            elif line.startswith('DESCRIPTION:'):
                description = line.replace('DESCRIPTION:', '').strip()
                section = None
            elif line.startswith('STEPS:'):
                section = 'steps'  # Enter steps parsing mode
            elif section == 'steps' and (line.startswith(('1.', '2.', '3.')) or line[0].isdigit()):
                # Remove numbering from steps and clean them up
                clean_step = line.split('.', 1)[1].strip() if '.' in line[:3] else line.strip()
                if clean_step:
                    steps.append(clean_step)

        # Provide fallback values if parsing failed
        if not title:
            title = "Generated Test Plan"
        if not description:
            description = f"Test plan generated from document with {len(steps)} steps"

        return {
            "title": title,
            "description": description,
            "steps": steps[:10]  # Limit to first 10 steps for UI
        }

    except Exception as e:
        # Handle any errors gracefully with fallback content
        return {
            "title": "Error Generating Plan",
            "description": "Error generating suggestions: " + str(e),
            "steps": ["Error generating suggestions"]
        }

@app.post("/suggest", response_model=SuggestResponse)
def suggest(req: SuggestRequest):
    """
    AI Test Plan Generation API Endpoint.

    Accepts document text and uses Ollama AI to generate:
    - Intelligent test plan title
    - Descriptive summary
    - Practical test steps from document content

    - **req**: SuggestRequest containing document text
    - **Returns**: Generated SuggestResponse with title, description, and steps
    """
    result = suggest_plan(req.document)
    return result
