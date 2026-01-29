# Course Companion FTE - Complete Specification Document

## Table of Contents
1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [Architecture Overview](#architecture-overview)
4. [Backend Specifications](#backend-specifications)
5. [Frontend Specifications](#frontend-specifications)
6. [API Specifications](#api-specifications)
7. [Database Schema](#database-schema)
8. [User Interface Specifications](#user-interface-specifications)
9. [Performance Requirements](#performance-requirements)
10. [Security Requirements](#security-requirements)
11. [Testing Strategy](#testing-strategy)
12. [Deployment Specifications](#deployment-specifications)

## Executive Summary

The Course Companion FTE is a revolutionary Digital Full-Time Equivalent Educational Tutor designed to operate 24/7, delivering world-class tutoring at 1% of traditional costs while maintaining exceptional quality. The system combines deterministic backend logic with AI-powered tutoring capabilities through ChatGPT integration.

### Key Benefits:
- **Cost Efficiency**: 99% cost reduction compared to human tutors
- **Availability**: 24/7 operation (168 hours/week vs 40 hours/week)
- **Scalability**: Supports unlimited concurrent students
- **Consistency**: 99%+ consistency in educational delivery
- **Multi-language Support**: 50+ languages supported

## Project Overview

### Mission Statement
To create a production-ready Digital FTE that can tutor thousands of students simultaneously, operating 24/7 without fatigue while maintaining 99%+ consistency in educational delivery.

### Target Audience
- Students seeking personalized tutoring
- Educational institutions looking for scalable solutions
- Organizations wanting cost-effective training programs

### Core Principles
1. **Zero-Backend-LLM Architecture** (Phase 1): Backend performs ZERO LLM inference
2. **Deterministic Logic**: Content delivery, progress tracking, and quiz grading are deterministic
3. **AI-Powered Enhancement**: ChatGPT handles explanation, tutoring, and adaptation
4. **Scalable Architecture**: Designed to scale from 10 to 100,000 users without linear cost increase
5. **Cost Optimization**: Target $0.002-$0.004 per user per month for 10K users

## Architecture Overview

### System Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ChatGPT       │    │   Course        │    │   Cloudflare    │
│   Integration   │    │   Companion     │    │   R2 Storage    │
│                 │    │   FTE Backend   │    │                 │
│ - Explanations  │◄──►│ - Content APIs  │◄──►│ - Course        │
│ - Tutoring      │    │ - Quiz APIs     │    │   Content       │
│ - Adaptation    │    │ - Progress APIs │    │ - Media Assets  │
│ - Motivation    │    │ - Search APIs   │    │ - Quiz Banks    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   (PostgreSQL/  │
                       │   SQLite)       │
                       │ - Courses       │
                       │ - Chapters      │
                       │ - Users         │
                       │ - Progress      │
                       │ - Quizzes       │
                       └─────────────────┘
```

### Technology Stack
- **Backend**: FastAPI (Python 3.9+)
- **Frontend**: Next.js 16.1.6 (React/TypeScript)
- **Database**: SQLAlchemy ORM (PostgreSQL/SQLite)
- **Storage**: Cloudflare R2
- **AI Integration**: OpenAI API (ChatGPT)
- **Authentication**: JWT Tokens
- **Styling**: Tailwind CSS

## Backend Specifications

### Core Components
- **FastAPI Application**: Main application entry point
- **Models**: SQLAlchemy database models
- **Schemas**: Pydantic request/response schemas
- **Routers**: API route handlers
- **Config**: Database and application configuration
- **Utils**: Helper functions and utilities

### Key Features Implementation
1. **Content Delivery System**
   - Course management and retrieval
   - Chapter navigation (next/previous)
   - Content serving without LLM processing

2. **Progress Tracking System**
   - Chapter completion tracking
   - Streak management
   - Progress visualization

3. **Quiz Management System**
   - Rule-based quiz delivery
   - Automated grading with answer keys
   - Performance tracking

4. **Search Functionality**
   - Cross-content search
   - Relevance ranking
   - Fast indexing

5. **Hybrid Intelligence (Premium)**
   - Adaptive Learning Paths
   - LLM-graded Assessments
   - Cross-Chapter Synthesis
   - AI Mentor Sessions

### Database Models
- **Course**: Course information and metadata
- **Chapter**: Individual course chapters
- **User**: User accounts and profiles
- **UserProgress**: Progress tracking per user/course
- **Quiz**: Quiz definitions and questions
- **QuizAttempt**: Individual quiz attempts
- **Subscription**: Premium feature access control
- **HybridUsage**: Usage tracking for cost analysis

## Frontend Specifications

### Application Structure
```
frontend/
├── app/                    # Next.js 13+ app directory
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── courses/           # Course management
│   │   └── [id]/         # Dynamic course pages
│   ├── progress/          # Progress tracking
│   ├── quiz/              # Quiz system
│   ├── search/            # Search functionality
│   └── globals.css        # Global styles
├── components/            # Reusable components
│   ├── Header.tsx         # Navigation header
│   ├── Footer.tsx         # Page footer
│   └── CourseCard.tsx     # Course display component
├── types/                 # TypeScript definitions
│   └── course.ts          # Course type definitions
├── lib/                   # Utility functions
│   └── api.ts             # API helper functions
└── public/                # Static assets
```

### User Interface Features
1. **Dashboard Views**
   - Course catalog with progress indicators
   - Personalized learning paths
   - Achievement tracking

2. **Course Management**
   - Chapter navigation
   - Content display
   - Progress tracking

3. **Quiz System**
   - Interactive quizzes
   - Real-time scoring
   - Performance feedback

4. **Progress Tracking**
   - Visual progress indicators
   - Streak tracking
   - Achievement badges

5. **Search Functionality**
   - Content search across courses
   - Relevance ranking
   - Quick access to materials

### Responsive Design
- Mobile-first approach
- Tablet and desktop optimized layouts
- Touch-friendly interactions
- Accessible design patterns

## API Specifications

### Base URL
`http://localhost:8000/api/v1` (development)
`https://api.coursecompanionfte.com/api/v1` (production)

### Authentication
Most endpoints require authentication via JWT token in Authorization header:
```
Authorization: Bearer <token>
```

### Content APIs

#### GET /courses
Retrieve all available courses
- **Response**: Array of Course objects
- **Example Response**:
```json
{
  "courses": [
    {
      "id": "course-python-intro",
      "title": "Introduction to Modern Python",
      "description": "Learn modern Python with typing and best practices",
      "prerequisites": [],
      "chapters": []
    }
  ]
}
```

#### GET /courses/{course_id}
Retrieve a specific course
- **Parameters**: course_id (path parameter)
- **Response**: Single Course object

#### GET /courses/{course_id}/chapters
Retrieve all chapters for a course
- **Parameters**: course_id (path parameter)
- **Response**: Array of Chapter objects

#### GET /chapters/{chapter_id}
Retrieve a specific chapter
- **Parameters**: chapter_id (path parameter)
- **Response**: Single Chapter object

#### GET /chapters/{chapter_id}/next
Get the next chapter after specified chapter
- **Parameters**: chapter_id (path parameter)
- **Response**: Single Chapter object or error

#### GET /chapters/{chapter_id}/previous
Get the previous chapter before specified chapter
- **Parameters**: chapter_id (path parameter)
- **Response**: Single Chapter object or error

### Quiz APIs

#### GET /quizzes/{quiz_id}
Retrieve a specific quiz
- **Parameters**: quiz_id (path parameter)
- **Response**: Single Quiz object

#### POST /quizzes/submit
Submit quiz answers for grading
- **Request Body**:
```json
{
  "user_id": "user-123",
  "quiz_id": "quiz-456",
  "answers": {
    "question-1": "answer-option-a",
    "question-2": "answer-option-b"
  }
}
```
- **Response**: QuizResult object

#### GET /quizzes/attempts/{user_id}/{quiz_id}
Get user's attempts for a specific quiz
- **Parameters**: user_id, quiz_id (path parameters)
- **Response**: Array of QuizAttempt objects

#### GET /quizzes/user/{user_id}/course/{course_id}
Get all quizzes for a course that user can access
- **Parameters**: user_id, course_id (path parameters)
- **Response**: Array of Quiz objects

### Progress APIs

#### POST /progress/{user_id}/courses/{course_id}/chapters/{chapter_id}
Mark a chapter as completed for a user
- **Parameters**: user_id, course_id, chapter_id (path parameters)
- **Response**: Success message with updated progress

#### GET /progress/{user_id}/courses/{course_id}
Get user's progress in a specific course
- **Parameters**: user_id, course_id (path parameters)
- **Response**: UserProgress object

#### GET /progress/{user_id}/courses
Get user's progress across all courses
- **Parameters**: user_id (path parameter)
- **Response**: Array of course progress objects

#### PUT /progress/{user_id}/streak/reset
Reset user's learning streak
- **Parameters**: user_id (path parameter)
- **Response**: Success message

### Search APIs

#### GET /search
Search across all content
- **Query Parameters**: q (query string), limit (number)
- **Response**: SearchResponse object

#### GET /search/courses
Search specifically for courses
- **Query Parameters**: q (query string), limit (number)
- **Response**: SearchResponse object with course results

#### GET /search/chapters
Search specifically for chapters
- **Query Parameters**: q (query string), limit (number)
- **Response**: SearchResponse object with chapter results

### Hybrid Intelligence APIs (Premium Features)

#### POST /hybrid/adaptive-learning
Generate personalized learning path based on user performance
- **Request Body**: AdaptiveLearningRequest
- **Response**: AdaptiveLearningResponse
- **Cost**: $0.018 per request
- **Requires**: Premium subscription

#### POST /hybrid/llm-assessment
LLM-based assessment with detailed feedback
- **Request Body**: LLMAssessmentRequest
- **Response**: LLMAssessmentResponse
- **Cost**: $0.014 per request
- **Requires**: Premium subscription

#### POST /hybrid/synthesis
Connect concepts across chapters and generate insights
- **Request Body**: CrossChapterSynthesisRequest
- **Response**: CrossChapterSynthesisResponse
- **Cost**: $0.027 per request
- **Requires**: Premium subscription

#### POST /hybrid/mentor-session
Long-running AI mentor for complex tutoring workflows
- **Request Body**: MentorSessionRequest
- **Response**: MentorSessionResponse
- **Cost**: $0.090 per session
- **Requires**: Premium subscription

#### GET /hybrid/usage/{user_id}
Get usage statistics for hybrid intelligence features for cost tracking
- **Parameters**: user_id (path parameter)
- **Response**: Usage statistics object

## Database Schema

### Course Table
```sql
CREATE TABLE courses (
    id VARCHAR PRIMARY KEY,
    title VARCHAR NOT NULL,
    description TEXT,
    prerequisites JSON DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Chapter Table
```sql
CREATE TABLE chapters (
    id VARCHAR PRIMARY KEY,
    course_id VARCHAR REFERENCES courses(id),
    title VARCHAR NOT NULL,
    content TEXT,
    next_chapter_id VARCHAR,
    prev_chapter_id VARCHAR,
    order INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### User Table
```sql
CREATE TABLE users (
    id VARCHAR PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### UserProgress Table
```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    course_id VARCHAR REFERENCES courses(id),
    completed_chapters JSON DEFAULT '[]',
    quiz_scores JSON DEFAULT '{}',
    last_accessed TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    streak_days INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Quiz Table
```sql
CREATE TABLE quizzes (
    id VARCHAR PRIMARY KEY,
    course_id VARCHAR REFERENCES courses(id),
    chapter_id VARCHAR REFERENCES chapters(id),
    title VARCHAR NOT NULL,
    questions JSON NOT NULL,  -- Stores questions in JSON format
    passing_score FLOAT DEFAULT 0.7,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### QuizAttempt Table
```sql
CREATE TABLE quiz_attempts (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    quiz_id VARCHAR REFERENCES quizzes(id),
    answers JSON,  -- Stores user answers in JSON format
    score FLOAT,
    passed BOOLEAN,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Subscription Table
```sql
CREATE TABLE subscriptions (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    plan_type VARCHAR DEFAULT 'free',  -- free, premium, pro, team
    start_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### HybridUsage Table
```sql
CREATE TABLE hybrid_usage (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR REFERENCES users(id),
    month_year VARCHAR,  -- Format: YYYY-MM
    adaptive_learning INTEGER DEFAULT 0,
    llm_assessment INTEGER DEFAULT 0,
    synthesis INTEGER DEFAULT 0,
    mentor_sessions INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## User Interface Specifications

### Color Palette
- **Primary**: Emerald 600 (#059669)
- **Secondary**: Emerald 500 (#10B981)
- **Accent**: Indigo 600 (#4F46E5)
- **Background**: White / Gray 900 (dark mode)
- **Text**: Gray 900 / White (dark mode)

### Typography
- **Font Family**: Inter (system font stack)
- **Heading Sizes**:
  - H1: 2.5rem (40px)
  - H2: 2rem (32px)
  - H3: 1.5rem (24px)
- **Body Text**: 1rem (16px) with 1.5 line height

### Layout Grid
- **Container Width**: 1208px max-width
- **Grid System**: 12-column responsive grid
- **Spacing Scale**: 0.25rem (4px) base unit
- **Breakpoints**:
  - sm: 640px
  - md: 768px
  - lg: 1024px
  - xl: 1280px

### Component Specifications

#### Course Card Component
- **Dimensions**: Variable height, fixed width (320px)
- **Elements**: Title, description, progress bar, action button
- **States**: Hover, active, completed
- **Interactions**: Click to view course details

#### Progress Bar Component
- **Height**: 8px
- **Border Radius**: 4px
- **Colors**: Background light gray, filled emerald
- **Animation**: Smooth transition on progress change

#### Quiz Question Component
- **Layout**: Question text, multiple choice options
- **Interaction**: Radio button selection
- **Feedback**: Immediate visual feedback on selection

## Performance Requirements

### Backend Performance
- **API Response Time**: < 200ms for 95% of requests
- **Database Queries**: < 50ms average
- **Concurrent Users**: Support 10,000+ simultaneous users
- **Throughput**: Handle 1,000+ requests per second

### Frontend Performance
- **Initial Load**: < 3 seconds on 3G connection
- **Page Transitions**: < 300ms
- **Interactive**: < 100ms input response
- **Bundle Size**: < 200KB JavaScript

### Scalability Targets
- **Horizontal Scaling**: Auto-scale based on demand
- **Database Connection Pooling**: Efficient connection management
- **Caching Strategy**: Redis for frequently accessed data
- **CDN Integration**: Cloudflare for static asset delivery

## Security Requirements

### Authentication & Authorization
- **JWT Tokens**: Stateless authentication
- **Token Expiration**: 30-minute access tokens
- **Role-based Access**: Different permissions for user types
- **Password Security**: Bcrypt hashing with salt

### Data Protection
- **Encryption at Rest**: Database encryption
- **Encryption in Transit**: HTTPS/TLS 1.3
- **PII Handling**: Minimal personal data collection
- **Data Retention**: Automatic cleanup policies

### API Security
- **Rate Limiting**: Per-user request limits
- **Input Validation**: Sanitization and validation
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Output encoding

### Audit & Monitoring
- **Access Logging**: All user actions logged
- **Security Events**: Suspicious activity detection
- **Compliance**: GDPR/CCPA compliance measures

## Testing Strategy

### Unit Testing
- **Backend**: Pytest for API endpoints and business logic
- **Frontend**: Jest/React Testing Library for components
- **Coverage Target**: 80%+ code coverage
- **CI/CD Integration**: Automated testing pipeline

### Integration Testing
- **API Testing**: End-to-end API workflows
- **Database Testing**: CRUD operations validation
- **Authentication Testing**: Security flow validation

### Performance Testing
- **Load Testing**: Simulate concurrent user load
- **Stress Testing**: System breaking point analysis
- **Soak Testing**: Long-duration stability testing

### User Acceptance Testing
- **Scenario Testing**: Real-world usage scenarios
- **Accessibility Testing**: WCAG 2.1 AA compliance
- **Cross-browser Testing**: Chrome, Firefox, Safari, Edge

## Deployment Specifications

### Infrastructure Requirements
- **Compute**: Containerized deployment (Docker/Kubernetes)
- **Database**: Managed PostgreSQL (AWS RDS/Google Cloud SQL)
- **Storage**: Cloudflare R2 for static assets
- **CDN**: Cloudflare for global content delivery

### Environment Configuration
- **Development**: Local setup with SQLite
- **Staging**: Pre-production testing environment
- **Production**: Production environment with full features

### Deployment Pipeline
1. **Build**: Compile and optimize assets
2. **Test**: Run automated test suite
3. **Deploy**: Deploy to staging environment
4. **Verify**: Automated smoke tests
5. **Promote**: Deploy to production

### Monitoring & Observability
- **Application Monitoring**: APM with error tracking
- **Infrastructure Monitoring**: Resource utilization
- **User Analytics**: Usage patterns and engagement
- **Alerting**: Critical issue notifications

### Rollback Strategy
- **Blue-Green Deployment**: Zero-downtime deployments
- **Feature Flags**: Safe feature toggling
- **Health Checks**: Automated rollback triggers

---

**Document Version**: 1.0
**Last Updated**: January 2026
**Approved By**: Course Companion FTE Development Team