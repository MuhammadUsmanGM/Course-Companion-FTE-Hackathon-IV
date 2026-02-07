from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from sqlalchemy.orm import Session

from config.database import engine, get_db, Base
from routers import courses, progress, quizzes, search, hybrid
import models

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Course Companion FTE API",
    description="Digital Full-Time Equivalent Educational Tutor API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with API versioning
app.include_router(courses.router, prefix="/api/v1/courses", tags=["courses"])
app.include_router(progress.router, prefix="/api/v1/progress", tags=["progress"])
app.include_router(quizzes.router, prefix="/api/v1/quizzes", tags=["quizzes"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(hybrid.router, prefix="/api/v1/hybrid", tags=["hybrid"])

# Legacy routes for current frontend compatibility (unversioned)
app.include_router(courses.router, prefix="/courses", tags=["legacy"])
app.include_router(progress.router, prefix="/progress", tags=["legacy"])
app.include_router(quizzes.router, prefix="/quizzes", tags=["legacy"])
app.include_router(search.router, prefix="/search", tags=["legacy"])
app.include_router(hybrid.router, prefix="/hybrid", tags=["legacy"])

@app.get("/")
async def root():
    return {
        "message": "Course Companion FTE API",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs"
    }

@app.get("/api/v1/access/check")
async def check_access(user_id: str, db: Session = Depends(get_db)):
    """
    Feature 6: Freemium Gate / Access Control
    Checks if a user has active premium access.
    """
    subscription = db.query(models.Subscription).filter(
        models.Subscription.user_id == user_id,
        models.Subscription.is_active == True
    ).first()
    
    if subscription:
        return {
            "user_id": user_id,
            "has_premium": True,
            "plan_type": subscription.plan_type,
            "expires_at": subscription.end_date
        }
    
    return {
        "user_id": user_id,
        "has_premium": False,
        "plan_type": "free",
        "message": "Upgrade to Premium for advanced features like AI mentoring and adaptive learning paths."
    }

@app.get("/api/v1/pricing")
async def get_pricing():
    """Information for the Freemium Gate presentation"""
    return {
        "tiers": [
            {"name": "Free", "price": "$0", "features": ["First 3 chapters", "Basic quizzes", "ChatGPT tutoring"]},
            {"name": "Premium", "price": "$9.99/mo", "features": ["All chapters", "All quizzes", "Progress tracking"]},
            {"name": "Pro", "price": "$19.99/mo", "features": ["Premium + Adaptive Path + LLM Assessments"]},
            {"name": "Team", "price": "$49.99/mo", "features": ["Pro + Analytics + Multiple seats"]}
        ]
    }

# Seed sample data on startup if empty
@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    try:
        # Check if we already have courses
        if db.query(models.Course).count() == 0:
            logger.info("Seeding initial course data...")
            
            # Create a sample course
            course_id = "course-python-intro"
            course = models.Course(
                id=course_id,
                title="Introduction to Modern Python",
                description="Learn modern Python with typing and best practices",
                prerequisites=[]
            )
            db.add(course)
            
            # Create chapters
            chapters = [
                models.Chapter(
                    id="ch1-intro",
                    course_id=course_id,
                    title="Getting Started with Python",
                    content="# Getting Started\n\nPython is a versatile programming language...",
                    next_chapter_id="ch2-basics",
                    prev_chapter_id=None,
                    order=1
                ),
                models.Chapter(
                    id="ch2-basics",
                    course_id=course_id,
                    title="Python Basics",
                    content="# Python Basics\n\nVariables, data types, and operators...",
                    next_chapter_id="ch3-functions",
                    prev_chapter_id="ch1-intro",
                    order=2
                ),
                models.Chapter(
                    id="ch3-functions",
                    course_id=course_id,
                    title="Functions and Typing",
                    content="# Functions and Type Hints\n\nModern Python uses type hints...",
                    next_chapter_id=None,
                    prev_chapter_id="ch2-basics",
                    order=3
                )
            ]
            for chapter in chapters:
                db.add(chapter)
            
            # Create a sample quiz
            quiz = models.Quiz(
                id="quiz-python-basics",
                course_id=course_id,
                chapter_id="ch2-basics",
                title="Python Basics Quiz",
                questions=[
                    {
                        "id": "q1",
                        "question": "What is the correct way to declare a variable in Python?",
                        "options": ["int x = 5", "var x = 5", "x = 5", "declare x = 5"],
                        "correct_answer": "x = 5"
                    },
                    {
                        "id": "q2",
                        "question": "Which of these is a valid Python function declaration?",
                        "options": ["function my_func():", "def my_func():", "func my_func():", "void my_func():"],
                        "correct_answer": "def my_func():"
                    }
                ],
                passing_score=0.7
            )
            db.add(quiz)
            
            db.commit()
            logger.info("Successfully seeded course data.")
    except Exception as e:
        logger.error(f"Error seeding data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)