from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

app = FastAPI(
    title="Course Companion FTE - Phase 1",
    description="Zero-Backend-LLM Educational Platform",
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

# Mock database (in production, use a real database)
courses_db = {}
users_db = {}
progress_db = {}
quizzes_db = {}

# Data models
class Course(BaseModel):
    id: str
    title: str
    description: str
    chapters: list
    prerequisites: list = []

class Chapter(BaseModel):
    id: str
    title: str
    content: str
    next_chapter_id: Optional[str] = None
    prev_chapter_id: Optional[str] = None

class UserProgress(BaseModel):
    user_id: str
    course_id: str
    completed_chapters: list
    quiz_scores: dict
    last_accessed: datetime
    streak_days: int = 0

class QuizSubmission(BaseModel):
    user_id: str
    quiz_id: str
    answers: dict

class QuizResult(BaseModel):
    quiz_id: str
    score: float
    passed: bool
    feedback: str

# Initialize sample data
def init_sample_data():
    global courses_db, quizzes_db

    # Sample course
    sample_course = Course(
        id="course-python-intro",
        title="Introduction to Modern Python",
        description="Learn modern Python with typing and best practices",
        prerequisites=[],
        chapters=[
            {
                "id": "ch1-intro",
                "title": "Getting Started with Python",
                "content": "# Getting Started\n\nPython is a versatile programming language...",
                "next_chapter_id": "ch2-basics",
                "prev_chapter_id": None
            },
            {
                "id": "ch2-basics",
                "title": "Python Basics",
                "content": "# Python Basics\n\nVariables, data types, and operators...",
                "next_chapter_id": "ch3-functions",
                "prev_chapter_id": "ch1-intro"
            },
            {
                "id": "ch3-functions",
                "title": "Functions and Typing",
                "content": "# Functions and Type Hints\n\nModern Python uses type hints...",
                "next_chapter_id": None,
                "prev_chapter_id": "ch2-basics"
            }
        ]
    )

    courses_db[sample_course.id] = sample_course

    # Sample quiz
    quizzes_db["quiz-python-basics"] = {
        "id": "quiz-python-basics",
        "course_id": "course-python-intro",
        "chapter_id": "ch2-basics",
        "questions": [
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
        "passing_score": 0.7
    }

@app.on_event("startup")
async def startup_event():
    init_sample_data()

# API Endpoints

@app.get("/")
async def root():
    return {"message": "Course Companion FTE - Phase 1 API", "status": "running"}

@app.get("/courses")
async def get_courses():
    """Get all available courses"""
    return {"courses": [course.dict() for course in courses_db.values()]}

@app.get("/courses/{course_id}")
async def get_course(course_id: str):
    """Get a specific course by ID"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    return courses_db[course_id]

@app.get("/courses/{course_id}/chapters")
async def get_course_chapters(course_id: str):
    """Get all chapters for a specific course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    course = courses_db[course_id]
    return {"chapters": course.chapters}

@app.get("/chapters/{chapter_id}")
async def get_chapter(chapter_id: str):
    """Get a specific chapter by ID"""
    for course in courses_db.values():
        for chapter_data in course.chapters:
            if chapter_data["id"] == chapter_id:
                return chapter_data
    raise HTTPException(status_code=404, detail="Chapter not found")

@app.get("/chapters/{chapter_id}/next")
async def get_next_chapter(chapter_id: str):
    """Get the next chapter after the specified one"""
    for course in courses_db.values():
        for chapter_data in course.chapters:
            if chapter_data["id"] == chapter_id:
                next_id = chapter_data.get("next_chapter_id")
                if next_id:
                    return await get_chapter(next_id)
                return {"message": "No next chapter available"}
    raise HTTPException(status_code=404, detail="Chapter not found")

@app.get("/chapters/{chapter_id}/previous")
async def get_prev_chapter(chapter_id: str):
    """Get the previous chapter before the specified one"""
    for course in courses_db.values():
        for chapter_data in course.chapters:
            if chapter_data["id"] == chapter_id:
                prev_id = chapter_data.get("prev_chapter_id")
                if prev_id:
                    return await get_chapter(prev_id)
                return {"message": "No previous chapter available"}
    raise HTTPException(status_code=404, detail="Chapter not found")

@app.post("/progress/{user_id}/courses/{course_id}/chapters/{chapter_id}")
async def mark_chapter_completed(user_id: str, course_id: str, chapter_id: str):
    """Mark a chapter as completed for a user"""
    key = f"{user_id}:{course_id}"

    if key not in progress_db:
        progress_db[key] = UserProgress(
            user_id=user_id,
            course_id=course_id,
            completed_chapters=[],
            quiz_scores={},
            last_accessed=datetime.now(),
            streak_days=0
        )

    user_progress = progress_db[key]

    # Add chapter to completed if not already there
    if chapter_id not in user_progress.completed_chapters:
        user_progress.completed_chapters.append(chapter_id)
        user_progress.last_accessed = datetime.now()

    return {"message": "Chapter marked as completed", "progress": user_progress.dict()}

@app.get("/progress/{user_id}/courses/{course_id}")
async def get_user_progress(user_id: str, course_id: str):
    """Get a user's progress in a specific course"""
    key = f"{user_id}:{course_id}"

    if key not in progress_db:
        return {
            "user_id": user_id,
            "course_id": course_id,
            "completed_chapters": [],
            "quiz_scores": {},
            "completion_percentage": 0,
            "streak_days": 0
        }

    progress = progress_db[key]
    course = courses_db.get(course_id)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    total_chapters = len(course.chapters)
    completed_count = len(progress.completed_chapters)
    completion_percentage = (completed_count / total_chapters) * 100 if total_chapters > 0 else 0

    return {
        "user_id": progress.user_id,
        "course_id": progress.course_id,
        "completed_chapters": progress.completed_chapters,
        "quiz_scores": progress.quiz_scores,
        "completion_percentage": completion_percentage,
        "streak_days": progress.streak_days
    }

@app.post("/quizzes/{quiz_id}/submit")
async def submit_quiz(quiz_id: str, submission: QuizSubmission):
    """Submit quiz answers and get results"""
    if quiz_id not in quizzes_db:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz = quizzes_db[quiz_id]
    correct_answers = 0
    total_questions = len(quiz["questions"])

    for question in quiz["questions"]:
        question_id = question["id"]
        if question_id in submission.answers:
            if submission.answers[question_id] == question["correct_answer"]:
                correct_answers += 1

    score = correct_answers / total_questions if total_questions > 0 else 0
    passed = score >= quiz["passing_score"]

    # Save quiz result to user progress
    progress_key = f"{submission.user_id}:{quiz['course_id']}"
    if progress_key not in progress_db:
        progress_db[progress_key] = UserProgress(
            user_id=submission.user_id,
            course_id=quiz['course_id'],
            completed_chapters=[],
            quiz_scores={},
            last_accessed=datetime.now(),
            streak_days=0
        )

    progress_db[progress_key].quiz_scores[quiz_id] = {
        "score": score,
        "passed": passed,
        "date": datetime.now().isoformat()
    }

    feedback = "Great job!" if passed else "Keep studying, you'll get it next time!"

    return QuizResult(
        quiz_id=quiz_id,
        score=score,
        passed=passed,
        feedback=feedback
    )

@app.get("/search")
async def search_content(query: str):
    """Search for content across courses and chapters"""
    results = []

    for course in courses_db.values():
        # Search in course title and description
        if query.lower() in course.title.lower() or query.lower() in course.description.lower():
            results.append({
                "type": "course",
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "relevance": 0.9
            })

        # Search in chapter titles and content
        for chapter in course.chapters:
            if query.lower() in chapter["title"].lower() or query.lower() in chapter["content"].lower():
                relevance = 0.8 if query.lower() in chapter["title"].lower() else 0.6
                results.append({
                    "type": "chapter",
                    "id": chapter["id"],
                    "title": chapter["title"],
                    "course_id": course.id,
                    "course_title": course.title,
                    "relevance": relevance
                })

    # Sort by relevance
    results.sort(key=lambda x: x["relevance"], reverse=True)

    return {"results": results[:10]}  # Return top 10 results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)