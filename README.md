# Course Companion FTE - Phase 1

## Overview
This is a Digital Full-Time Equivalent Educational Tutor that serves as a 24/7 educational companion. This Phase 1 implementation follows the Zero-Backend-LLM architecture where all intelligent processing happens in ChatGPT, while our backend provides deterministic services like content delivery, progress tracking, and quiz grading.

## Architecture
- **Frontend**: ChatGPT App (will be integrated with OpenAI's platform)
- **Backend**: FastAPI server with deterministic functions only (no LLM calls in Phase 1)
- **Storage**: In-memory mock database (for demonstration, replace with real DB in production)

## Features Implemented

### 1. Content Delivery
- Serve course materials verbatim from the backend
- Chapter navigation (next/previous)

### 2. Progress Tracking
- Track user completion of chapters
- Calculate course completion percentage
- Track quiz scores

### 3. Quiz System
- Rule-based quiz grading
- Pass/fail determination based on predefined thresholds

### 4. Search Functionality
- Search across courses and chapters

### 5. Freemium Access Control
- Basic access control mechanisms

## API Endpoints

### Courses
- `GET /courses` - Get all available courses
- `GET /courses/{course_id}` - Get specific course details
- `GET /courses/{course_id}/chapters` - Get all chapters for a course

### Chapters
- `GET /chapters/{chapter_id}` - Get specific chapter content
- `GET /chapters/{chapter_id}/next` - Get next chapter
- `GET /chapters/{chapter_id}/previous` - Get previous chapter

### Progress Tracking
- `POST /progress/{user_id}/courses/{course_id}/chapters/{chapter_id}` - Mark chapter as completed
- `GET /progress/{user_id}/courses/{course_id}` - Get user progress in a course

### Quizzes
- `POST /quizzes/{quiz_id}/submit` - Submit quiz answers and get results

### Search
- `GET /search?query={search_term}` - Search across all content

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory: `cd backend`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the server: `uvicorn main:app --reload`
4. The API will be available at `http://localhost:8000`

### API Documentation
- Interactive documentation at `http://localhost:8000/docs`
- Alternative documentation at `http://localhost:8000/redoc`

## Phase 1 Compliance
This implementation strictly adheres to the Zero-Backend-LLM principle:
- ❌ No LLM API calls in the backend
- ❌ No AI inference in the backend
- ✅ All intelligent processing delegated to ChatGPT
- ✅ Backend only handles deterministic operations (content delivery, progress tracking, rule-based grading)

## Course Content
The system comes with a sample course on "Introduction to Modern Python" with chapters covering:
1. Getting Started with Python
2. Python Basics
3. Functions and Typing

## Technologies Used
- Python 3.8+
- FastAPI
- Pydantic
- Uvicorn