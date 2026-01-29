# Backend Specifications for Course Companion FTE

## Overview
The backend is built using FastAPI, a modern Python web framework that provides high performance and automatic API documentation. The architecture follows the Zero-Backend-LLM principle where the backend handles deterministic operations while ChatGPT manages AI-powered features.

## Technology Stack
- **Framework**: FastAPI (0.104.1)
- **Programming Language**: Python 3.9+
- **Database ORM**: SQLAlchemy (2.0.23)
- **Database Support**: PostgreSQL/SQLite
- **Environment Management**: python-dotenv
- **Data Validation**: Pydantic (2.5.0)
- **Authentication**: JWT tokens
- **Database Migration**: Alembic (1.13.1)

## Project Structure
```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── models/                 # SQLAlchemy database models
│   └── __init__.py        # All model definitions
├── schemas/                # Pydantic schemas for validation
│   └── __init__.py        # All schema definitions
├── routers/                # API route handlers
│   ├── courses.py         # Course management endpoints
│   ├── quizzes.py         # Quiz management endpoints
│   ├── progress.py        # Progress tracking endpoints
│   └── search.py          # Search functionality endpoints
├── config/                 # Configuration files
│   └── database.py        # Database configuration
└── utils/                  # Utility functions (to be added)
```

## Core Architecture

### FastAPI Application
The main application is configured with:
- CORS middleware for cross-origin requests
- Automatic API documentation (Swagger UI and ReDoc)
- Event handlers for startup/shutdown
- Centralized exception handling

### Database Configuration
- **Connection Pooling**: Configured for optimal performance
- **Async Support**: Ready for async database operations
- **Migration Ready**: Alembic configured for schema evolution
- **Multiple DB Support**: Configurable for PostgreSQL/SQLite

### Dependency Injection
- **Database Sessions**: Automatic session management via dependency
- **Authentication**: JWT token validation
- **Validation**: Request/response schema validation
- **Configuration**: Environment-based settings

## API Endpoints Specification

### Course Management (/api/v1/courses)

#### GET /
- **Purpose**: Retrieve all available courses
- **Response**: Array of Course objects
- **Authentication**: Optional (public content)
- **Rate Limit**: 100 requests/minute per IP

#### GET /{course_id}
- **Purpose**: Retrieve a specific course by ID
- **Parameters**: course_id (path parameter)
- **Response**: Single Course object
- **Authentication**: Optional (public content)
- **Rate Limit**: 100 requests/minute per IP

#### GET /{course_id}/chapters
- **Purpose**: Retrieve all chapters for a specific course
- **Parameters**: course_id (path parameter)
- **Response**: Array of Chapter objects ordered by sequence
- **Authentication**: Optional (public content)
- **Rate Limit**: 100 requests/minute per IP

### Chapter Management (/api/v1/chapters)

#### GET /{chapter_id}
- **Purpose**: Retrieve a specific chapter by ID
- **Parameters**: chapter_id (path parameter)
- **Response**: Single Chapter object
- **Authentication**: Optional (public content)
- **Rate Limit**: 100 requests/minute per IP

#### GET /{chapter_id}/next
- **Purpose**: Get the next chapter in sequence
- **Parameters**: chapter_id (path parameter)
- **Response**: Single Chapter object or 404 if none
- **Authentication**: Optional (public content)
- **Rate Limit**: 100 requests/minute per IP

#### GET /{chapter_id}/previous
- **Purpose**: Get the previous chapter in sequence
- **Parameters**: chapter_id (path parameter)
- **Response**: Single Chapter object or 404 if none
- **Authentication**: Optional (public content)
- **Rate Limit**: 100 requests/minute per IP

### Quiz Management (/api/v1/quizzes)

#### GET /{quiz_id}
- **Purpose**: Retrieve a specific quiz by ID
- **Parameters**: quiz_id (path parameter)
- **Response**: Single Quiz object
- **Authentication**: Required for premium quizzes
- **Rate Limit**: 50 requests/minute per user

#### POST /submit
- **Purpose**: Submit quiz answers for grading
- **Request Body**: QuizSubmission object
- **Response**: QuizResult object
- **Authentication**: Required
- **Rate Limit**: 10 submissions/hour per user

#### GET /attempts/{user_id}/{quiz_id}
- **Purpose**: Get user's attempts for a specific quiz
- **Parameters**: user_id, quiz_id (path parameters)
- **Response**: Array of QuizAttempt objects
- **Authentication**: Required (user must match user_id)
- **Rate Limit**: 20 requests/minute per user

#### GET /user/{user_id}/course/{course_id}
- **Purpose**: Get all quizzes for a course that user can access
- **Parameters**: user_id, course_id (path parameters)
- **Response**: Array of Quiz objects
- **Authentication**: Required
- **Rate Limit**: 50 requests/minute per user

### Progress Tracking (/api/v1/progress)

#### POST /{user_id}/courses/{course_id}/chapters/{chapter_id}
- **Purpose**: Mark a chapter as completed for a user
- **Parameters**: user_id, course_id, chapter_id (path parameters)
- **Response**: Success message with updated progress
- **Authentication**: Required (user must match user_id)
- **Rate Limit**: 100 completions/day per user

#### GET /{user_id}/courses/{course_id}
- **Purpose**: Get user's progress in a specific course
- **Parameters**: user_id, course_id (path parameters)
- **Response**: UserProgress object
- **Authentication**: Required (user must match user_id)
- **Rate Limit**: 200 requests/minute per user

#### GET /{user_id}/courses
- **Purpose**: Get user's progress across all courses
- **Parameters**: user_id (path parameter)
- **Response**: Array of course progress summaries
- **Authentication**: Required (user must match user_id)
- **Rate Limit**: 100 requests/minute per user

#### PUT /{user_id}/streak/reset
- **Purpose**: Reset user's learning streak
- **Parameters**: user_id (path parameter)
- **Response**: Success confirmation
- **Authentication**: Required (user must match user_id)
- **Rate Limit**: 1 request/day per user

### Search Functionality (/api/v1/search)

#### GET /
- **Purpose**: Search across all content (courses and chapters)
- **Query Parameters**: q (query string), limit (number, default 10)
- **Response**: SearchResponse object with results
- **Authentication**: Optional
- **Rate Limit**: 50 requests/minute per IP

#### GET /courses
- **Purpose**: Search specifically for courses
- **Query Parameters**: q (query string), limit (number, default 10)
- **Response**: SearchResponse object with course results
- **Authentication**: Optional
- **Rate Limit**: 50 requests/minute per IP

#### GET /chapters
- **Purpose**: Search specifically for chapters
- **Query Parameters**: q (query string), limit (number, default 10)
- **Response**: SearchResponse object with chapter results
- **Authentication**: Optional
- **Rate Limit**: 50 requests/minute per IP

### Hybrid Intelligence APIs (Premium Features)

#### POST /hybrid/adaptive-learning
- **Purpose**: Generate personalized learning path based on user performance
- **Request Body**: AdaptiveLearningRequest object
- **Response**: AdaptiveLearningResponse object
- **Authentication**: Required (premium subscription)
- **Rate Limit**: 5 requests/day per user
- **Cost**: $0.018 per request

#### POST /hybrid/llm-assessment
- **Purpose**: LLM-based assessment with detailed feedback
- **Request Body**: LLMAssessmentRequest object
- **Response**: LLMAssessmentResponse object
- **Authentication**: Required (premium subscription)
- **Rate Limit**: 10 requests/day per user
- **Cost**: $0.014 per request

#### POST /hybrid/synthesis
- **Purpose**: Connect concepts across chapters and generate insights
- **Request Body**: CrossChapterSynthesisRequest object
- **Response**: CrossChapterSynthesisResponse object
- **Authentication**: Required (premium subscription)
- **Rate Limit**: 3 requests/day per user
- **Cost**: $0.027 per request

#### POST /hybrid/mentor-session
- **Purpose**: Long-running AI mentor for complex tutoring workflows
- **Request Body**: MentorSessionRequest object
- **Response**: MentorSessionResponse object
- **Authentication**: Required (premium subscription)
- **Rate Limit**: 2 requests/day per user
- **Cost**: $0.090 per session

#### GET /hybrid/usage/{user_id}
- **Purpose**: Get usage statistics for hybrid intelligence features
- **Parameters**: user_id (path parameter)
- **Response**: Usage statistics object
- **Authentication**: Required (user must match user_id)
- **Rate Limit**: 10 requests/minute per user

## Database Models

### Course Model
```python
class Course(Base):
    __tablename__ = "courses"

    id: str (Primary Key, Index)
    title: str (Index)
    description: str
    prerequisites: List[str] (JSON)
    created_at: DateTime
    updated_at: DateTime
```

### Chapter Model
```python
class Chapter(Base):
    __tablename__ = "chapters"

    id: str (Primary Key, Index)
    course_id: str (Foreign Key -> courses.id)
    title: str (Index)
    content: str
    next_chapter_id: str (Nullable)
    prev_chapter_id: str (Nullable)
    order: int
    created_at: DateTime
    updated_at: DateTime
```

### User Model
```python
class User(Base):
    __tablename__ = "users"

    id: str (Primary Key, Index)
    email: str (Unique, Index)
    username: str (Unique, Index)
    is_active: bool (Default: True)
    created_at: DateTime
    updated_at: DateTime
```

### UserProgress Model
```python
class UserProgress(Base):
    __tablename__ = "user_progress"

    id: int (Primary Key, Index)
    user_id: str (Foreign Key -> users.id)
    course_id: str (Foreign Key -> courses.id)
    completed_chapters: List[str] (JSON, Default: [])
    quiz_scores: Dict (JSON, Default: {})
    last_accessed: DateTime
    streak_days: int (Default: 0)
    created_at: DateTime
    updated_at: DateTime
```

### Quiz Model
```python
class Quiz(Base):
    __tablename__ = "quizzes"

    id: str (Primary Key, Index)
    course_id: str (Foreign Key -> courses.id)
    chapter_id: str (Foreign Key -> chapters.id)
    title: str
    questions: List[Dict] (JSON)
    passing_score: float (Default: 0.7)
    created_at: DateTime
    updated_at: DateTime
```

### QuizAttempt Model
```python
class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id: int (Primary Key, Index)
    user_id: str (Foreign Key -> users.id)
    quiz_id: str (Foreign Key -> quizzes.id)
    answers: Dict (JSON)
    score: float
    passed: bool
    completed_at: DateTime
```

### Subscription Model
```python
class Subscription(Base):
    __tablename__ = "subscriptions"

    id: int (Primary Key, Index)
    user_id: str (Foreign Key -> users.id)
    plan_type: str (Default: "free")
    start_date: DateTime
    end_date: DateTime (Nullable)
    is_active: bool (Default: True)
    created_at: DateTime
    updated_at: DateTime
```

### HybridUsage Model
```python
class HybridUsage(Base):
    __tablename__ = "hybrid_usage"

    id: int (Primary Key, Index)
    user_id: str (Foreign Key -> users.id)
    month_year: str (Format: YYYY-MM)
    adaptive_learning: int (Default: 0)
    llm_assessment: int (Default: 0)
    synthesis: int (Default: 0)
    mentor_sessions: int (Default: 0)
    created_at: DateTime
    updated_at: DateTime
```

## Security Measures

### Authentication
- **JWT Tokens**: Stateless authentication with expiration
- **Token Refresh**: Automatic refresh token handling
- **Password Hashing**: Bcrypt with salt rounds

### Rate Limiting
- **Per Endpoint**: Configurable rate limits
- **Per User/IP**: Account-based and IP-based limits
- **Redis Integration**: Distributed rate limiting

### Input Validation
- **Pydantic Schemas**: Automatic request validation
- **Sanitization**: Input cleaning and validation
- **Size Limits**: Request size constraints

### Error Handling
- **Standardized Errors**: Consistent error response format
- **Logging**: Comprehensive error logging
- **Monitoring**: Error tracking and alerting

## Performance Optimizations

### Caching Strategy
- **Redis Cache**: Frequently accessed data caching
- **CDN Integration**: Static content delivery
- **Database Indexing**: Optimized query performance

### Database Optimization
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Indexed searches and queries
- **Lazy Loading**: On-demand data loading

### API Optimization
- **Pagination**: Large dataset handling
- **Compression**: Response compression (gzip)
- **CORS Configuration**: Optimized cross-origin policies

## Monitoring and Logging

### Application Logs
- **Structured Logging**: JSON-formatted logs
- **Log Levels**: Debug, Info, Warning, Error
- **Request Tracing**: End-to-end request tracking

### Performance Metrics
- **Response Times**: API performance tracking
- **Error Rates**: Failure rate monitoring
- **Resource Usage**: CPU, memory, database metrics

### Business Metrics
- **User Engagement**: Learning progress tracking
- **Content Consumption**: Course completion rates
- **Feature Usage**: Premium feature adoption

## Deployment Configuration

### Environment Variables
```
DATABASE_URL=postgresql://user:password@host:port/dbname
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
REDIS_URL=redis://localhost:6379
LOG_LEVEL=INFO
```

### Container Configuration (Docker)
```
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### Health Checks
- **Liveness**: API availability check
- **Readiness**: Database connectivity check
- **Custom Checks**: Business logic validation

## Error Handling and Recovery

### Error Response Format
```json
{
  "detail": "Error message",
  "error_code": "ERROR_CODE",
  "timestamp": "ISO 8601 timestamp",
  "request_id": "unique request identifier"
}
```

### Retry Mechanisms
- **Database Retries**: Automatic retry for transient failures
- **External API Retries**: Configurable retry policies
- **Circuit Breaker**: Fail-fast for persistent issues

### Backup and Recovery
- **Database Backups**: Automated daily backups
- **Point-in-Time Recovery**: Transaction log backups
- **Disaster Recovery**: Multi-region backup strategy

## Future Extensions

### Scalability Enhancements
- **Microservices**: Potential service decomposition
- **Message Queues**: Async processing for heavy operations
- **Load Balancing**: Horizontal scaling support

### Feature Additions
- **Real-time Updates**: WebSocket support for live updates
- **Analytics Engine**: Advanced learning analytics
- **Content Management**: Admin panel for content creators

### Integration Points
- **Third-party SSO**: OAuth providers support
- **Payment Gateways**: Subscription management
- **Notification Systems**: Email and push notifications