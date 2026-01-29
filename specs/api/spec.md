# API Specifications for Course Companion FTE

## Overview
The Course Companion FTE API provides a comprehensive set of RESTful endpoints for educational content management, progress tracking, quiz administration, and search functionality. The API follows REST principles with JSON request/response payloads and standard HTTP status codes.

## Base URL
```
Production: https://api.coursecompanionfte.com/api/v1
Staging: https://staging-api.coursecompanionfte.com/api/v1
Development: http://localhost:8000/api/v1
```

## Versioning
- **Version Strategy**: URI versioning (v1 in the path)
- **Backward Compatibility**: Maintained for minor version updates
- **Deprecation Policy**: 6 months advance notice for breaking changes
- **Future Versions**: v2 planned with enhanced features

## Authentication
### JWT Token Authentication
- **Header**: `Authorization: Bearer <jwt_token>`
- **Token Format**: JWT with HS256 algorithm
- **Expiration**: 30 minutes for access tokens
- **Refresh Token**: Available for extended sessions

### API Key Authentication (Future)
- **Header**: `X-API-Key: <api_key>`
- **Rate Limits**: Higher limits for API key users
- **Usage Tracking**: Per-key usage analytics

## Common Headers
```
Content-Type: application/json
Accept: application/json
User-Agent: CourseCompanionFTE/v1
```

## Rate Limiting
- **Public Endpoints**: 100 requests per minute per IP
- **Authenticated Endpoints**: 200 requests per minute per user
- **Quiz Submissions**: 10 submissions per hour per user
- **Premium Features**: 5 requests per day per user
- **Burst Limit**: 10 requests per second per IP

## Error Handling
### Error Response Format
```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_ERROR_CODE",
  "timestamp": "2026-01-29T10:30:00.123456Z",
  "request_id": "unique-request-id"
}
```

### Common HTTP Status Codes
- **200**: OK - Request successful
- **201**: Created - New resource created
- **204**: No Content - Request successful, no content to return
- **400**: Bad Request - Invalid request format
- **401**: Unauthorized - Authentication required
- **403**: Forbidden - Insufficient permissions
- **404**: Not Found - Resource does not exist
- **409**: Conflict - Resource conflict (e.g., duplicate)
- **422**: Unprocessable Entity - Validation error
- **429**: Too Many Requests - Rate limit exceeded
- **500**: Internal Server Error - Server error

## Response Format Standards
### Successful Responses
```json
{
  "data": { /* resource data */ },
  "meta": { /* pagination, links, etc. */ },
  "links": { /* related links */ }
}
```

### List Responses
```json
{
  "data": [ /* array of resources */ ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 5,
      "per_page": 10,
      "total": 50
    }
  }
}
```

## Course Management Endpoints

### GET /courses
**Description**: Retrieve all available courses
**Authentication**: Public
**Rate Limit**: 100 requests/minute per IP
**Parameters**:
- `limit` (optional): Number of courses to return (default: 10, max: 100)
- `offset` (optional): Offset for pagination (default: 0)
- `sort` (optional): Sort field (default: created_at, options: created_at, title)
- `order` (optional): Sort order (default: desc, options: asc, desc)

**Response**:
```json
{
  "data": [
    {
      "id": "course-python-intro",
      "title": "Introduction to Modern Python",
      "description": "Learn modern Python with typing and best practices",
      "prerequisites": ["basic-programming", "math-fundamentals"],
      "chapters_count": 8,
      "created_at": "2026-01-28T10:30:00Z",
      "updated_at": "2026-01-28T10:30:00Z"
    }
  ],
  "meta": {
    "pagination": {
      "page": 1,
      "pages": 1,
      "per_page": 10,
      "total": 1
    }
  }
}
```

### GET /courses/{course_id}
**Description**: Retrieve a specific course by ID
**Authentication**: Public
**Rate Limit**: 100 requests/minute per IP
**Parameters**: None
**Response**:
```json
{
  "data": {
    "id": "course-python-intro",
    "title": "Introduction to Modern Python",
    "description": "Learn modern Python with typing and best practices",
    "prerequisites": ["basic-programming", "math-fundamentals"],
    "chapters": [
      {
        "id": "ch1-intro",
        "title": "Getting Started with Python",
        "content": "# Getting Started\n\nPython is a versatile programming language...",
        "next_chapter_id": "ch2-basics",
        "prev_chapter_id": null,
        "order": 1
      }
    ],
    "created_at": "2026-01-28T10:30:00Z",
    "updated_at": "2026-01-28T10:30:00Z"
  }
}
```

### GET /courses/{course_id}/chapters
**Description**: Retrieve all chapters for a specific course
**Authentication**: Public
**Rate Limit**: 100 requests/minute per IP
**Parameters**:
- `sort` (optional): Sort field (default: order, options: order, created_at)
- `order` (optional): Sort order (default: asc, options: asc, desc)

**Response**:
```json
{
  "data": [
    {
      "id": "ch1-intro",
      "title": "Getting Started with Python",
      "content": "# Getting Started\n\nPython is a versatile programming language...",
      "next_chapter_id": "ch2-basics",
      "prev_chapter_id": null,
      "order": 1,
      "created_at": "2026-01-28T10:30:00Z",
      "updated_at": "2026-01-28T10:30:00Z"
    }
  ]
}
```

## Chapter Management Endpoints

### GET /chapters/{chapter_id}
**Description**: Retrieve a specific chapter by ID
**Authentication**: Public
**Rate Limit**: 100 requests/minute per IP
**Parameters**: None
**Response**:
```json
{
  "data": {
    "id": "ch1-intro",
    "course_id": "course-python-intro",
    "title": "Getting Started with Python",
    "content": "# Getting Started\n\nPython is a versatile programming language...",
    "next_chapter_id": "ch2-basics",
    "prev_chapter_id": null,
    "order": 1,
    "created_at": "2026-01-28T10:30:00Z",
    "updated_at": "2026-01-28T10:30:00Z"
  }
}
```

### GET /chapters/{chapter_id}/next
**Description**: Get the next chapter after the specified one
**Authentication**: Public
**Rate Limit**: 100 requests/minute per IP
**Parameters**: None
**Response**:
```json
{
  "data": {
    "id": "ch2-basics",
    "course_id": "course-python-intro",
    "title": "Python Basics",
    "content": "# Python Basics\n\nVariables, data types, and operators...",
    "next_chapter_id": "ch3-functions",
    "prev_chapter_id": "ch1-intro",
    "order": 2,
    "created_at": "2026-01-28T10:30:00Z",
    "updated_at": "2026-01-28T10:30:00Z"
  }
}
```

### GET /chapters/{chapter_id}/previous
**Description**: Get the previous chapter before the specified one
**Authentication**: Public
**Rate Limit**: 100 requests/minute per IP
**Parameters**: None
**Response**:
```json
{
  "data": {
    "id": "ch1-intro",
    "course_id": "course-python-intro",
    "title": "Getting Started with Python",
    "content": "# Getting Started\n\nPython is a versatile programming language...",
    "next_chapter_id": "ch2-basics",
    "prev_chapter_id": null,
    "order": 1,
    "created_at": "2026-01-28T10:30:00Z",
    "updated_at": "2026-01-28T10:30:00Z"
  }
}
```

## Quiz Management Endpoints

### GET /quizzes/{quiz_id}
**Description**: Retrieve a specific quiz by ID
**Authentication**: Required for premium quizzes
**Rate Limit**: 50 requests/minute per user
**Parameters**: None
**Response**:
```json
{
  "data": {
    "id": "quiz-python-basics",
    "course_id": "course-python-intro",
    "chapter_id": "ch2-basics",
    "title": "Python Basics Quiz",
    "questions": [
      {
        "id": "q1",
        "question": "What is the correct way to declare a variable in Python?",
        "options": ["int x = 5", "var x = 5", "x = 5", "declare x = 5"],
        "correct_answer": "x = 5"
      }
    ],
    "passing_score": 0.7,
    "created_at": "2026-01-28T10:30:00Z",
    "updated_at": "2026-01-28T10:30:00Z"
  }
}
```

### POST /quizzes/submit
**Description**: Submit quiz answers for grading
**Authentication**: Required
**Rate Limit**: 10 submissions/hour per user
**Request Body**:
```json
{
  "user_id": "user-12345",
  "quiz_id": "quiz-python-basics",
  "answers": {
    "q1": "x = 5",
    "q2": "def my_func():"
  }
}
```

**Response**:
```json
{
  "data": {
    "quiz_id": "quiz-python-basics",
    "score": 1.0,
    "passed": true,
    "feedback": "Great job! You passed the quiz.",
    "completed_at": "2026-01-29T10:30:00Z"
  }
}
```

### GET /quizzes/attempts/{user_id}/{quiz_id}
**Description**: Get user's attempts for a specific quiz
**Authentication**: Required (user must match user_id)
**Rate Limit**: 20 requests/minute per user
**Parameters**:
- `limit` (optional): Number of attempts to return (default: 10, max: 50)
- `offset` (optional): Offset for pagination (default: 0)

**Response**:
```json
{
  "data": [
    {
      "id": 123,
      "user_id": "user-12345",
      "quiz_id": "quiz-python-basics",
      "answers": {
        "q1": "x = 5",
        "q2": "def my_func():"
      },
      "score": 1.0,
      "passed": true,
      "completed_at": "2026-01-29T10:30:00Z"
    }
  ]
}
```

### GET /quizzes/user/{user_id}/course/{course_id}
**Description**: Get all quizzes for a course that user can access
**Authentication**: Required (user must match user_id)
**Rate Limit**: 50 requests/minute per user
**Parameters**: None
**Response**:
```json
{
  "data": [
    {
      "id": "quiz-python-basics",
      "course_id": "course-python-intro",
      "chapter_id": "ch2-basics",
      "title": "Python Basics Quiz",
      "questions_count": 10,
      "passing_score": 0.7
    }
  ]
}
```

## Progress Tracking Endpoints

### POST /progress/{user_id}/courses/{course_id}/chapters/{chapter_id}
**Description**: Mark a chapter as completed for a user
**Authentication**: Required (user must match user_id)
**Rate Limit**: 100 completions/day per user
**Parameters**: None
**Request Body**: None
**Response**:
```json
{
  "data": {
    "message": "Chapter marked as completed",
    "progress": {
      "user_id": "user-12345",
      "course_id": "course-python-intro",
      "completed_chapters": ["ch1-intro", "ch2-basics"],
      "quiz_scores": {},
      "last_accessed": "2026-01-29T10:30:00Z",
      "streak_days": 7
    }
  }
}
```

### GET /progress/{user_id}/courses/{course_id}
**Description**: Get user's progress in a specific course
**Authentication**: Required (user must match user_id)
**Rate Limit**: 200 requests/minute per user
**Parameters**: None
**Response**:
```json
{
  "data": {
    "user_id": "user-12345",
    "course_id": "course-python-intro",
    "completed_chapters": ["ch1-intro", "ch2-basics"],
    "quiz_scores": {
      "quiz-python-basics": {
        "score": 1.0,
        "passed": true,
        "date": "2026-01-29T10:30:00Z"
      }
    },
    "completion_percentage": 25.0,
    "streak_days": 7,
    "last_accessed": "2026-01-29T10:30:00Z"
  }
}
```

### GET /progress/{user_id}/courses
**Description**: Get user's progress across all courses
**Authentication**: Required (user must match user_id)
**Rate Limit**: 100 requests/minute per user
**Parameters**: None
**Response**:
```json
{
  "data": [
    {
      "course_id": "course-python-intro",
      "course_title": "Introduction to Modern Python",
      "completed_chapters": 2,
      "total_chapters": 8,
      "completion_percentage": 25.0,
      "quiz_scores": {"quiz-python-basics": {"score": 1.0, "passed": true}},
      "streak_days": 7,
      "last_accessed": "2026-01-29T10:30:00Z"
    }
  ]
}
```

### PUT /progress/{user_id}/streak/reset
**Description**: Reset user's learning streak
**Authentication**: Required (user must match user_id)
**Rate Limit**: 1 request/day per user
**Parameters**: None
**Request Body**: None
**Response**:
```json
{
  "data": {
    "message": "Streak reset successfully",
    "user_id": "user-12345"
  }
}
```

## Search Endpoints

### GET /search
**Description**: Search across all content (courses and chapters)
**Authentication**: Public
**Rate Limit**: 50 requests/minute per IP
**Parameters**:
- `q` (required): Search query string
- `limit` (optional): Number of results to return (default: 10, max: 20)
- `type` (optional): Filter by type (options: course, chapter, all)

**Response**:
```json
{
  "data": [
    {
      "type": "course",
      "id": "course-python-intro",
      "title": "Introduction to Modern Python",
      "description": "Learn modern Python with typing and best practices",
      "relevance": 0.9
    },
    {
      "type": "chapter",
      "id": "ch1-intro",
      "title": "Getting Started with Python",
      "course_id": "course-python-intro",
      "course_title": "Introduction to Modern Python",
      "relevance": 0.8
    }
  ]
}
```

### GET /search/courses
**Description**: Search specifically for courses
**Authentication**: Public
**Rate Limit**: 50 requests/minute per IP
**Parameters**:
- `q` (required): Search query string
- `limit` (optional): Number of results to return (default: 10, max: 20)

**Response**:
```json
{
  "data": [
    {
      "type": "course",
      "id": "course-python-intro",
      "title": "Introduction to Modern Python",
      "description": "Learn modern Python with typing and best practices",
      "relevance": 0.9
    }
  ]
}
```

### GET /search/chapters
**Description**: Search specifically for chapters
**Authentication**: Public
**Rate Limit**: 50 requests/minute per IP
**Parameters**:
- `q` (required): Search query string
- `limit` (optional): Number of results to return (default: 10, max: 20)

**Response**:
```json
{
  "data": [
    {
      "type": "chapter",
      "id": "ch1-intro",
      "title": "Getting Started with Python",
      "course_id": "course-python-intro",
      "course_title": "Introduction to Modern Python",
      "relevance": 0.8
    }
  ]
}
```

## Hybrid Intelligence Endpoints (Premium Features)

### POST /hybrid/adaptive-learning
**Description**: Generate personalized learning path based on user performance
**Authentication**: Required (premium subscription)
**Rate Limit**: 5 requests/day per user
**Request Body**:
```json
{
  "user_id": "user-12345",
  "course_id": "course-python-intro",
  "current_chapter_id": "ch2-basics",
  "quiz_performance": {
    "quiz-python-basics": 0.85,
    "quiz-functions": 0.65
  },
  "time_spent": {
    "ch1-intro": 1200,
    "ch2-basics": 1800
  }
}
```

**Response**:
```json
{
  "data": {
    "recommended_next_chapter": "ch3-functions",
    "confidence": 0.85,
    "learning_style": "visual",
    "improvement_areas": ["quiz-functions"],
    "estimated_time_to_mastery": "2-3 weeks"
  }
}
```

### POST /hybrid/llm-assessment
**Description**: LLM-based assessment with detailed feedback
**Authentication**: Required (premium subscription)
**Rate Limit**: 10 requests/day per user
**Request Body**:
```json
{
  "user_id": "user-12345",
  "quiz_id": "quiz-python-basics",
  "question_id": "q1",
  "user_response": "The variable is declared as x = 5 in Python",
  "correct_answer": "x = 5",
  "question_context": "Variables and declarations in Python"
}
```

**Response**:
```json
{
  "data": {
    "score": 0.8,
    "feedback": "Good job identifying the key concept!",
    "misconceptions_identified": [],
    "recommended_study_topics": ["Review fundamental concepts"],
    "confidence_level": "high"
  }
}
```

### POST /hybrid/synthesis
**Description**: Connect concepts across chapters and generate insights
**Authentication**: Required (premium subscription)
**Rate Limit**: 3 requests/day per user
**Request Body**:
```json
{
  "user_id": "user-12345",
  "course_id": "course-python-intro",
  "chapter_ids": ["ch1-intro", "ch2-basics", "ch3-functions"],
  "learning_goals": ["understand basics", "learn functions"]
}
```

**Response**:
```json
{
  "data": {
    "synthesized_concepts": ["Getting Started", "Python Basics", "Functions and Typing"],
    "connections_identified": [
      "The concept of 'Getting Started' builds upon 'Python Basics' in important ways."
    ],
    "big_picture_insights": [
      "These concepts form a foundational understanding of the subject."
    ],
    "practical_applications": [
      "Apply these concepts in real-world scenarios to reinforce learning."
    ]
  }
}
```

### POST /hybrid/mentor-session
**Description**: Long-running AI mentor for complex tutoring workflows
**Authentication**: Required (premium subscription)
**Rate Limit**: 2 requests/day per user
**Request Body**:
```json
{
  "user_id": "user-12345",
  "course_id": "course-python-intro",
  "chapter_id": "ch3-functions",
  "question": "I'm having trouble understanding how functions work in Python",
  "context": "We're learning about functions and type hints"
}
```

**Response**:
```json
{
  "data": {
    "response": "I understand you're asking about functions in Python...",
    "teaching_points": [
      "Break complex problems into smaller parts",
      "Apply concepts learned in previous chapters"
    ],
    "follow_up_questions": [
      "Can you think of any real-world applications for this concept?"
    ],
    "related_concepts": [
      "Foundational concepts from earlier chapters"
    ]
  }
}
```

### GET /hybrid/usage/{user_id}
**Description**: Get usage statistics for hybrid intelligence features for cost tracking
**Authentication**: Required (user must match user_id)
**Rate Limit**: 10 requests/minute per user
**Parameters**: None
**Response**:
```json
{
  "data": {
    "adaptive_learning": 3,
    "llm_assessment": 7,
    "synthesis": 2,
    "mentor_sessions": 1
  }
}
```

## Data Models

### Course Model
```json
{
  "id": "string (required)",
  "title": "string (required)",
  "description": "string (required)",
  "prerequisites": "array of strings (optional)",
  "created_at": "ISO 8601 datetime (required)",
  "updated_at": "ISO 8601 datetime (nullable)"
}
```

### Chapter Model
```json
{
  "id": "string (required)",
  "course_id": "string (required)",
  "title": "string (required)",
  "content": "string (required)",
  "next_chapter_id": "string (nullable)",
  "prev_chapter_id": "string (nullable)",
  "order": "integer (required)",
  "created_at": "ISO 8601 datetime (required)",
  "updated_at": "ISO 8601 datetime (nullable)"
}
```

### Quiz Model
```json
{
  "id": "string (required)",
  "course_id": "string (required)",
  "chapter_id": "string (required)",
  "title": "string (required)",
  "questions": [
    {
      "id": "string (required)",
      "question": "string (required)",
      "options": "array of strings (required)",
      "correct_answer": "string (required)"
    }
  ],
  "passing_score": "float (default: 0.7)",
  "created_at": "ISO 8601 datetime (required)",
  "updated_at": "ISO 8601 datetime (nullable)"
}
```

### Quiz Submission Model
```json
{
  "user_id": "string (required)",
  "quiz_id": "string (required)",
  "answers": "object (required) - map of question_id to selected answer"
}
```

### Quiz Result Model
```json
{
  "quiz_id": "string (required)",
  "score": "float (required)",
  "passed": "boolean (required)",
  "feedback": "string (required)",
  "completed_at": "ISO 8601 datetime (required)"
}
```

### User Progress Model
```json
{
  "user_id": "string (required)",
  "course_id": "string (required)",
  "completed_chapters": "array of strings (required)",
  "quiz_scores": "object (required) - map of quiz_id to score object",
  "last_accessed": "ISO 8601 datetime (required)",
  "streak_days": "integer (required)",
  "completion_percentage": "float (computed)"
}
```

## Security Headers
All API responses include:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

## CORS Policy
- **Allowed Origins**: Production domain, staging domain, localhost:3000
- **Allowed Methods**: GET, POST, PUT, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization, X-Requested-With
- **Credentials**: Allowed from trusted origins

## Monitoring and Logging
### Request Logging
- **Request ID**: Unique identifier for each request
- **Timestamp**: ISO 8601 formatted timestamp
- **Method and Path**: HTTP method and requested path
- **Response Time**: Time taken to process request
- **Status Code**: HTTP status code returned
- **User ID**: Authenticated user (when available)

### Performance Metrics
- **Response Times**: 95th percentile tracking
- **Error Rates**: Percentage of requests resulting in errors
- **Throughput**: Requests per second
- **Database Query Times**: Average query execution time
- **Cache Hit Ratios**: API caching effectiveness

## Rate Limiting Implementation
### Implementation Details
- **Storage**: Redis for distributed rate limiting
- **Algorithm**: Sliding window counter
- **Granularity**: Per-user and per-IP tracking
- **Buckets**: 1-minute sliding windows

### Rate Limit Headers
- `X-RateLimit-Limit`: Maximum requests allowed in the current window
- `X-RateLimit-Remaining`: Remaining requests in the current window
- `X-RateLimit-Reset`: Unix timestamp for when the current window resets

## Error Codes Reference
- `COURSE_NOT_FOUND`: Requested course does not exist
- `CHAPTER_NOT_FOUND`: Requested chapter does not exist
- `QUIZ_NOT_FOUND`: Requested quiz does not exist
- `USER_NOT_AUTHENTICATED`: Authentication required but not provided
- `INSUFFICIENT_PERMISSIONS`: User lacks required permissions
- `VALIDATION_ERROR`: Request data validation failed
- `RATE_LIMIT_EXCEEDED`: Request rate limit has been exceeded
- `INTERNAL_SERVER_ERROR`: Unexpected server error occurred
- `SUBSCRIPTION_REQUIRED`: Premium feature requires subscription
- `QUIZ_SUBMISSION_LIMIT_EXCEEDED`: Daily quiz submission limit reached

## API Documentation
- **Interactive Documentation**: Available at `/docs` (Swagger UI)
- **Alternative Documentation**: Available at `/redoc` (ReDoc)
- **OpenAPI Specification**: Available at `/openapi.json`
- **SDK Generation**: OpenAPI spec supports SDK generation for multiple languages