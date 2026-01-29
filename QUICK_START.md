# Course Companion FTE - Quick Start Guide

## 🚀 Quick Launch

### Start Backend Server
```bash
cd backend
python -m uvicorn main:app --reload
```
Backend will be available at: `http://localhost:8000`

### Start Frontend Server
```bash
cd frontend
npm run dev
```
Frontend will be available at: `http://localhost:3000`

### Or use the Windows script:
```bash
start.bat
```

---

## 📋 API Endpoints (Backend: http://localhost:8000)

### Phase 1: Zero-Backend-LLM
- `GET /courses` - Get all available courses
- `GET /courses/{course_id}` - Get specific course
- `GET /courses/{course_id}/chapters` - Get course chapters
- `GET /chapters/{chapter_id}` - Get chapter content
- `GET /chapters/{chapter_id}/next` - Get next chapter
- `GET /chapters/{chapter_id}/previous` - Get previous chapter
- `POST /progress/{user_id}/courses/{course_id}/chapters/{chapter_id}` - Mark chapter complete
- `GET /progress/{user_id}/courses/{course_id}` - Get user progress
- `POST /quizzes/{quiz_id}/submit` - Submit quiz
- `GET /search?query={search_term}` - Search content

### Phase 2: Hybrid Intelligence (Premium Features)
- `POST /hybrid/adaptive-learning` - Adaptive learning path
- `POST /hybrid/llm-assessment` - LLM-graded assessment
- `POST /hybrid/synthesis` - Cross-chapter synthesis
- `POST /hybrid/mentor-session` - AI mentor session
- `GET /hybrid/usage/{user_id}` - Usage tracking

### API Documentation
- Interactive docs: `http://localhost:8000/docs`
- Alternative: `http://localhost:8000/redoc`

---

## 🌐 Web Application (Frontend: http://localhost:3000)

### Available Pages:
- `/` - Home page with course listings
- `/courses/[id]` - Course detail page
- `/progress` - Progress tracking dashboard
- `/quiz` - Quiz system
- `/search` - Content search

---

## 🧪 Testing

### Test Phase 1 APIs:
```bash
python test_api.py
```

### Test Phase 2 Hybrid Features:
```bash
python test_hybrid_features.py
```

### Run Complete Demo:
```bash
python demo.py
```

---

## 📁 Project Structure

```
├── backend/                 # Phase 1 & 2 Backend
│   ├── main.py            # FastAPI application
│   └── requirements.txt   # Dependencies
├── frontend/              # Phase 3 Web App
│   ├── app/              # Next.js pages
│   ├── components/       # Reusable components
│   └── types/            # TypeScript definitions
├── frontend-chatgpt/      # ChatGPT App manifest
├── architecture.md        # Architecture diagram
├── cost-analysis.md       # Cost breakdown
├── spec.md               # Specification
├── README.md             # Main docs
├── start.bat             # Windows startup script
├── test_*.py             # Test scripts
└── demo.py               # Complete demo
```

---

## 🎯 Features Overview

### Phase 1: Zero-Backend-LLM
✅ Content Delivery
✅ Navigation
✅ Grounded Q&A
✅ Rule-Based Quizzes
✅ Progress Tracking
✅ Freemium Gate

### Phase 2: Hybrid Intelligence
✅ Adaptive Learning Path
✅ LLM-Graded Assessments
✅ Cross-Chapter Synthesis
✅ AI Mentor Agent
✅ Usage Tracking

### Phase 3: Web Application
✅ Complete UI/UX
✅ Course Browser
✅ Progress Dashboard
✅ Quiz System
✅ Search Functionality
✅ Responsive Design

---

## 💰 Business Metrics

- **Cost:** $16-41/month (Phase 1) vs $2,000-5,000 for human tutors
- **Availability:** 168 hours/week vs 40 hours
- **Scalability:** 100K+ users with minimal cost increase
- **Consistency:** 99%+ vs 85-95% human variance
- **Languages:** 50+ vs 1-3 for humans

---

## 🏆 Ready for Submission!

All hackathon requirements completed:
- ✅ Phase 1: Zero-Backend-LLM - Complete
- ✅ Phase 2: Hybrid Intelligence - Complete
- ✅ Phase 3: Web App - Complete
- ✅ Documentation - Complete
- ✅ Testing - Complete
- ✅ Demo - Complete

**Project is 100% ready for hackathon submission! 🚀**