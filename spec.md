# Course Companion FTE - Specification Document

## 1. Executive Summary

The Course Companion FTE is a Digital Full-Time Equivalent Educational Tutor designed to serve as a 24/7 educational companion, operating 168 hours per week with 85-90% cost savings compared to human tutors. This project implements the Agent Factory Architecture to create an AI-Native Course Companion that teaches, explains, quizzes, tracks, and adapts to learners.

## 2. Project Objectives

### Primary Goals
- Build a production-ready Digital FTE that can tutor thousands of students simultaneously
- Operate 24/7 without fatigue while maintaining 99%+ consistency in educational delivery
- Scale from 10 to 100,000 users without linear cost increase
- Support both ChatGPT App and standalone Web App frontends

### Success Metrics
- Zero-Backend-LLM compliance (Phase 1)
- All 6 required features implemented
- User experience quality
- Cost efficiency metrics
- Clear separation between free and premium features

## 3. Architecture Overview

### 3.1 Zero-Backend-LLM Architecture (Phase 1)
- Backend performs ZERO LLM inference
- ChatGPT handles ALL explanation, tutoring, and adaptation
- System is production-viable and can scale to 100k+ users cheaply
- Backend responsibilities: Serve content, track progress, enforce rules
- ChatGPT responsibilities: Explain concepts, provide analogies, answer questions, adapt tone

### 3.2 Technical Stack
- **Frontend (Phase 1)**: ChatGPT App using OpenAI Apps SDK
- **Frontend (Phase 3)**: Next.js/React web application
- **Backend**: FastAPI (Python) for content APIs, quiz APIs, progress APIs
- **Storage**: Cloudflare R2 for course content, media assets, quiz banks
- **Phase 2**: Hybrid backend with FastAPI + LLM API Calls for premium features

### 3.3 Agent Factory Architecture Implementation
- **L0**: Agent Sandbox (gVisor) - Secure execution (Phase 2 and 3)
- **L1**: Apache Kafka - Event backbone (Phase 2 and 3)
- **L2**: Dapr + Workflows - Infrastructure + Durability (Phase 2 and 3)
- **L3**: FastAPI - HTTP interface + A2A (Phase 1, 2, and 3)
- **L4**: OpenAI Agents SDK - High-level orchestration (Phase 2 and 3)
- **L5**: Claude Agent SDK - Agentic execution (Phase 2 and 3)
- **L6**: Runtime Skills + MCP - Domain knowledge + Tools (Phase 1, 2, and 3)
- **L7**: A2A Protocol - Multi-FTE collaboration (Phase 2 and 3)

## 4. Feature Specifications

### 4.1 Phase 1 Required Features

#### 1. Content Delivery
- **Backend**: Serve content verbatim from R2 storage
- **ChatGPT**: Explain concepts at learner's level, provide analogies and examples
- **APIs**: GET /courses, GET /courses/{id}/chapters, GET /chapters/{id}

#### 2. Navigation
- **Backend**: Return next/previous chapters based on course structure
- **ChatGPT**: Suggest optimal learning path based on user progress and preferences
- **APIs**: GET /chapters/{id}/next, GET /chapters/{id}/previous

#### 3. Grounded Q&A
- **Backend**: Return relevant sections from course content
- **ChatGPT**: Answer questions using only provided content, ensure factual accuracy
- **APIs**: GET /search?q={query}

#### 4. Rule-Based Quizzes
- **Backend**: Grade with predefined answer key, calculate scores based on rules
- **ChatGPT**: Present questions, encourage participation, explain incorrect answers
- **APIs**: POST /quizzes/{id}/submit, GET /quizzes/{id}

#### 5. Progress Tracking
- **Backend**: Store completion status, streaks, quiz scores, last accessed times
- **ChatGPT**: Celebrate achievements, maintain motivation, acknowledge progress
- **APIs**: GET /progress/{user_id}/courses/{course_id}, POST /progress/{user_id}/courses/{course_id}/chapters/{chapter_id}

#### 6. Freemium Gate
- **Backend**: Check access rights, enforce feature limitations, manage subscriptions
- **ChatGPT**: Explain premium features gracefully, suggest upgrade paths
- **APIs**: GET /access/check, GET /pricing

### 4.2 Phase 2 Hybrid Features (Choose Up to 2)

#### A. Adaptive Learning Path
- **Function**: Analyze learning patterns, generate personalized recommendations
- **Why LLM Needed**: Requires reasoning over complex learning data patterns
- **Premium Feature**: Available to Pro tier subscribers only
- **Cost**: $0.018 per request (Claude Sonnet, 2K tokens)

#### B. LLM-Graded Assessments
- **Function**: Evaluate free-form written answers with detailed feedback
- **Why LLM Needed**: Rule-based systems cannot evaluate reasoning or creativity
- **Premium Feature**: Available to Pro tier subscribers only
- **Cost**: $0.014 per request (Claude Sonnet, 1.5K tokens)

#### C. Cross-Chapter Synthesis
- **Function**: Connect concepts across chapters, generate "big picture" insights
- **Why LLM Needed**: Requires multi-document reasoning and synthesis
- **Premium Feature**: Available to Pro tier subscribers only
- **Cost**: $0.027 per request (Claude Sonnet, 3K tokens)

#### D. AI Mentor Agent
- **Function**: Long-running agent for complex tutoring workflows
- **Why LLM Needed**: Multi-turn problem solving and contextual understanding
- **Premium Feature**: Available to Team tier subscribers only
- **Cost**: $0.090 per session (Claude Sonnet, 10K tokens)

### 4.3 Phase 3 Web App Features
- Complete standalone web application
- Full LMS dashboard with progress visualization
- Administrative features for content management
- All features from Phase 1 and 2 available via web interface

## 5. API Specifications

### 5.1 Course Management APIs
```
GET /courses - Retrieve all available courses
GET /courses/{course_id} - Retrieve specific course details
GET /courses/{course_id}/chapters - Retrieve all chapters for a course
```

### 5.2 Chapter Management APIs
```
GET /chapters/{chapter_id} - Retrieve specific chapter content
GET /chapters/{chapter_id}/next - Retrieve next chapter
GET /chapters/{chapter_id}/previous - Retrieve previous chapter
```

### 5.3 Progress Tracking APIs
```
GET /progress/{user_id}/courses/{course_id} - Get user progress in course
POST /progress/{user_id}/courses/{course_id}/chapters/{chapter_id} - Mark chapter complete
```

### 5.4 Quiz Management APIs
```
POST /quizzes/{quiz_id}/submit - Submit quiz answers
GET /quizzes/{quiz_id} - Get quiz details
```

### 5.5 Search APIs
```
GET /search?query={search_term} - Search across all content
```

### 5.6 Access Control APIs
```
GET /access/check - Check user access rights
GET /pricing - Get pricing information
```

## 6. Data Models

### 6.1 Course Model
```typescript
interface Course {
  id: string;
  title: string;
  description: string;
  chapters: Chapter[];
  prerequisites: string[];
}
```

### 6.2 Chapter Model
```typescript
interface Chapter {
  id: string;
  title: string;
  content: string;
  next_chapter_id: string | null;
  prev_chapter_id: string | null;
}
```

### 6.3 User Progress Model
```typescript
interface UserProgress {
  user_id: string;
  course_id: string;
  completed_chapters: string[];
  quiz_scores: Record<string, any>;
  last_accessed: Date;
  streak_days: number;
}
```

## 7. Agent Skills Design

### 7.1 Required Runtime Skills

#### concept-explainer
- **Purpose**: Explain concepts at various complexity levels
- **Trigger Keywords**: "explain", "what is", "how does"
- **Workflow**: Determine user's current level → Find relevant content → Generate explanation → Provide examples

#### quiz-master
- **Purpose**: Guide students through quizzes with encouragement
- **Trigger Keywords**: "quiz", "test me", "practice"
- **Workflow**: Present questions → Validate answers → Provide feedback → Track scores

#### socratic-tutor
- **Purpose**: Guide learning through questions, not answers
- **Trigger Keywords**: "help me think", "I'm stuck"
- **Workflow**: Identify knowledge gap → Ask guiding questions → Allow student discovery → Confirm understanding

#### progress-motivator
- **Purpose**: Celebrate achievements, maintain motivation
- **Trigger Keywords**: "my progress", "streak", "how am I doing"
- **Workflow**: Retrieve progress data → Identify achievements → Provide positive reinforcement → Suggest next steps

### 7.2 Skill Structure Template
Each skill SKILL.md file contains:
1. **Metadata**: Name, description, trigger keywords
2. **Purpose**: What this skill accomplishes
3. **Workflow**: Step-by-step procedure
4. **Response Templates**: Example outputs
5. **Key Principles**: Guidelines and constraints

## 8. Implementation Guidelines

### 8.1 Phase 1 Compliance Rules
- ❌ No LLM API calls in backend
- ❌ No AI inference in backend
- ✅ All intelligent processing in ChatGPT
- ✅ Deterministic backend operations only
- ✅ Strict separation between intelligence and data

### 8.2 Phase 2 Implementation Rules
- ✅ Hybrid intelligence MUST be feature-scoped
- ✅ User-initiated (user requests it)
- ✅ Premium-gated (paid users only)
- ✅ Isolated (separate API routes)
- ✅ Cost-tracked (monitor per-user cost)
- ❌ No auto-triggering of hybrid features
- ❌ No making hybrid required for core UX
- ❌ No hiding hybrid costs from analysis

### 8.3 Phase 3 Implementation
- Complete standalone web application
- All features available via web interface
- Full LMS functionality
- Administrative dashboard

## 9. Quality Assurance

### 9.1 Testing Requirements
- Unit tests for all backend functions
- Integration tests for API endpoints
- UI tests for web application components
- Performance tests for scalability
- Security tests for data protection

### 9.2 Performance Benchmarks
- API response time: < 500ms for 95% of requests
- Frontend load time: < 3 seconds on 3G connection
- Concurrent users: Support 10,000+ simultaneous users
- Uptime: 99.9% availability

### 9.3 Security Standards
- Authentication and authorization for all endpoints
- Input validation and sanitization
- Rate limiting to prevent abuse
- Encryption for data at rest and in transit
- Regular security audits

## 10. Deployment & Operations

### 10.1 Infrastructure Requirements
- Cloud hosting with auto-scaling capabilities
- CDN for content delivery
- Database with backup and recovery
- Monitoring and alerting systems
- Load balancing for high availability

### 10.2 Maintenance Procedures
- Automated backups of user data
- Regular security updates
- Performance monitoring and optimization
- User feedback collection and analysis
- Feature usage analytics

## 11. Success Criteria

### 11.1 Technical Success
- All 6 Phase 1 features implemented and functional
- Zero-Backend-LLM compliance verified
- API performance benchmarks met
- Security standards achieved
- Scalability targets reached

### 11.2 Business Success
- Cost efficiency targets achieved
- User engagement metrics met
- Premium conversion rates achieved
- Customer satisfaction scores maintained
- Competitive advantages demonstrated

## 12. Future Enhancements

### 12.1 Short-term Roadmap
- Additional course content areas
- Enhanced personalization algorithms
- Improved mobile experience
- Social learning features
- Offline content access

### 12.2 Long-term Vision
- Multi-language support
- VR/AR learning experiences
- Advanced AI tutoring capabilities
- Institutional partnerships
- Global expansion

This specification provides a comprehensive blueprint for the Course Companion FTE implementation, ensuring all requirements are met while maintaining the core principles of cost efficiency and educational excellence.