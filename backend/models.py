"""
Database Models and Session Management for Test Plan Management Tool

This module defines the SQLAlchemy ORM models for test plans and their associated test steps.
It includes database connection setup, session management, and automatic table creation.

Database: SQLite (test_plans.db)
Relationships: TestPlan (1) -> (many) TestStep (cascade delete enabled)
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database Configuration
# Using SQLite for simplicity - ideal for development and single-user applications
DATABASE_URL = "sqlite:///./test_plans.db"

# Create SQLAlchemy engine with SQLite-specific settings
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)

# Session factory for database connections
# autocommit=False: Manual transaction control
# autoflush=False: Manual flushing control
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

class TestPlan(Base):
    """
    SQLAlchemy model representing a test plan in the database.

    A test plan contains basic information about testing objectives and
    has multiple associated test steps (one-to-many relationship).
    """
    __tablename__ = "test_plans"

    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)

    # Test plan title - indexed for faster searches
    title = Column(String, index=True)

    # Optional description of the test plan
    description = Column(String)

    # Relationship to TestStep - bidirectional with cascading delete
    # When a TestPlan is deleted, all associated TestSteps are also deleted
    steps = relationship("TestStep", back_populates="plan", cascade="all, delete-orphan")


class TestStep(Base):
    """
    SQLAlchemy model representing individual test steps within a test plan.

    Each test step belongs to exactly one test plan (many-to-one relationship).
    Test steps can be managed independently while maintaining plan association.
    """
    __tablename__ = "test_steps"

    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)

    # Description of what this test step involves
    description = Column(String)

    # Foreign key linking to parent TestPlan
    # When the plan is deleted, steps are deleted (cascade from TestPlan)
    plan_id = Column(Integer, ForeignKey("test_plans.id"))

    # Back-reference to the parent TestPlan
    plan = relationship("TestPlan", back_populates="steps")


# Database Table Creation
# Automatically create all tables in the database if they don't exist
# This runs on application startup and ensures schema is up to date
Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency function for FastAPI that provides database sessions.

    This function is used as a dependency in API endpoints to get a database session.
    It automatically handles session lifecycle (creation, cleanup) using Python generators.

    Yields:
        Session: SQLAlchemy database session for database operations

    Note: Sessions are automatically closed after the request completes
    """
    db = SessionLocal()  # Create new session
    try:
        yield db  # Provide session to endpoint function
    finally:
        db.close()  # Ensure session is always closed
