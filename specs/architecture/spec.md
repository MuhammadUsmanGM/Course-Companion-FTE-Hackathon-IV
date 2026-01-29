# Architecture Specifications for Course Companion FTE

## Overview
The Course Companion FTE architecture follows a modern microservices-inspired design with a clear separation between deterministic backend logic and AI-powered tutoring capabilities. The system implements a Zero-Backend-LLM architecture for Phase 1, with optional hybrid intelligence features for Phase 2.

## System Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ChatGPT       │    │   Course        │    │   Cloudflare    │
│   Integration   │    │   Companion     │    │   R2 Storage    │
│                 │    │   FTE Backend   │    │                 │
│ - Explanations  │◄──►│ - Content APIs  │◄──►│ - Course        │
│ - Tutoring      │    │ - Quiz APIs     │    │   Content       │
│ - Adaptation    │    │ - Progress APIs │    │ - Media Assets  │
│ - Motivation    │    │ - Search APIs   │    │ - Quiz Banks    │
│ - Premium       │    │ - Hybrid APIs   │    │ - User Assets   │
│   Features      │    │                 │    │                 │
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
                       │ - Subscriptions │
                       │ - Usage Logs    │
                       └─────────────────┘
```

### Layered Architecture
```
┌─────────────────────────────────────────────────────────────┐
│                    Presentation Layer                       │
│  (Next.js Frontend, React Components, User Interfaces)    │
├─────────────────────────────────────────────────────────────┤
│                    API Gateway Layer                        │
│         (Route Management, Authentication)                 │
├─────────────────────────────────────────────────────────────┤
│                    Service Layer                            │
│  (Business Logic, Validation, Coordination)               │
├─────────────────────────────────────────────────────────────┤
│                    Data Access Layer                        │
│      (Database Operations, Caching, Queries)               │
├─────────────────────────────────────────────────────────────┤
│                    Infrastructure Layer                     │
│    (Database, Storage, Message Queues, Monitoring)        │
└─────────────────────────────────────────────────────────────┘
```

## Component Architecture

### Backend Components
```
Course Companion FTE Backend
├── main.py (Application Entry Point)
├── config/
│   └── database.py (Database Configuration)
├── models/ (Database Models)
│   └── __init__.py (All SQLAlchemy Models)
├── schemas/ (Pydantic Schemas)
│   └── __init__.py (All Request/Response Schemas)
├── routers/ (API Route Handlers)
│   ├── courses.py (Course Management Routes)
│   ├── quizzes.py (Quiz Management Routes)
│   ├── progress.py (Progress Tracking Routes)
│   ├── search.py (Search Functionality Routes)
│   └── __init__.py (Route Registration)
├── services/ (Business Logic - Future Addition)
├── utils/ (Utility Functions - Future Addition)
└── dependencies/ (Dependency Injection - Future Addition)
```

### Frontend Components
```
Course Companion FTE Frontend
├── app/ (Next.js App Directory)
│   ├── layout.tsx (Root Layout)
│   ├── page.tsx (Homepage)
│   ├── courses/ (Course Management Pages)
│   │   └── [id]/ (Dynamic Course Pages)
│   │       └── page.tsx (Course Detail)
│   ├── progress/ (Progress Tracking)
│   │   └── page.tsx (Progress Dashboard)
│   ├── quiz/ (Quiz System)
│   │   └── page.tsx (Quiz Interface)
│   ├── search/ (Search Functionality)
│   │   └── page.tsx (Search Interface)
│   └── globals.css (Global Styles)
├── components/ (Reusable UI Components)
│   ├── Header.tsx (Navigation Header)
│   ├── Footer.tsx (Site Footer)
│   └── CourseCard.tsx (Course Display)
├── types/ (TypeScript Definitions)
│   └── course.ts (Course, Chapter, Progress Types)
├── lib/ (Utility Functions)
│   └── api.ts (API Communication Utilities)
└── public/ (Static Assets - Future Addition)
```

## Technology Stack

### Backend Technologies
- **Framework**: FastAPI (Python 3.9+)
- **Database ORM**: SQLAlchemy 2.0+
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **API Documentation**: Swagger UI / ReDoc
- **Data Validation**: Pydantic 2.0+
- **Authentication**: JWT Tokens
- **Environment Management**: python-dotenv
- **Database Migration**: Alembic

### Frontend Technologies
- **Framework**: Next.js 16.1.6
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **Icons**: Lucide React
- **State Management**: React Hooks
- **API Communication**: Native fetch
- **Build Tool**: Webpack (via Next.js)

### Infrastructure
- **Hosting**: Cloud-based deployment
- **Database**: Managed PostgreSQL/SQLite
- **Storage**: Cloudflare R2
- **CDN**: Cloudflare
- **Caching**: Redis (Planned)
- **Monitoring**: Application Performance Monitoring (Planned)

## Design Patterns

### Backend Patterns
1. **Repository Pattern**: Data access layer abstraction
2. **Dependency Injection**: Service registration and resolution
3. **DTO Pattern**: Data transfer objects for API communication
4. **Factory Pattern**: Object creation abstraction
5. **Strategy Pattern**: Algorithm selection for business logic

### Frontend Patterns
1. **Component Composition**: Building complex UIs from simple components
2. **Container/Presentational**: Separation of concerns in UI
3. **Higher-Order Components**: Component logic reuse
4. **Custom Hooks**: Stateful logic sharing
5. **Provider Pattern**: State management across component tree

## Security Architecture

### Authentication Flow
```
User Login
    ↓
JWT Token Generation
    ↓
Token Storage (Frontend)
    ↓
Token Inclusion in Requests
    ↓
Token Validation (Backend)
    ↓
Authorized API Access
```

### Authorization Strategy
- **Role-Based Access Control**: Different permissions for user types
- **Resource-Based Authorization**: Fine-grained resource access control
- **API Key Authentication**: For third-party integrations (Future)
- **Session Management**: Secure session handling

### Security Measures
- **Input Validation**: Server-side validation for all inputs
- **SQL Injection Prevention**: Parameterized queries
- **XSS Protection**: Content sanitization
- **CSRF Protection**: Cross-site request forgery prevention
- **Rate Limiting**: API abuse prevention
- **Encryption**: Data encryption in transit and at rest

## Performance Architecture

### Caching Strategy
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Browser       │    │   CDN           │    │   Application   │
│   Cache         │    │   Cache         │    │   Cache         │
│                 │    │                 │    │                 │
│ - Static Assets │◄──►│ - Static Assets │◄──►│ - API Response  │
│ - Service       │    │ - Images, CSS,  │    │ - Frequently    │
│   Worker        │    │   JS            │    │   Accessed Data │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Database Optimization
- **Indexing Strategy**: Proper indexing for query performance
- **Connection Pooling**: Efficient database connection management
- **Query Optimization**: Optimized SQL queries
- **Pagination**: Efficient large dataset handling
- **Read Replicas**: Separate read/write operations (Future)

### API Performance
- **Response Compression**: Gzip compression for API responses
- **Pagination**: Default and configurable pagination
- **Rate Limiting**: Prevent API abuse
- **Caching Headers**: Proper cache headers for static content
- **Batch Operations**: Efficient bulk operations

## Scalability Architecture

### Horizontal Scaling
- **Stateless Services**: Services can be scaled independently
- **Load Balancing**: Distribute traffic across multiple instances
- **Auto-scaling**: Automatically adjust capacity based on demand
- **Microservices**: Independent scaling of components (Future)

### Vertical Scaling
- **Database Scaling**: Upgrade database hardware as needed
- **Application Scaling**: Increase instance resources
- **Caching**: Reduce database load through caching
- **CDN**: Offload static content to CDN

### Database Scaling
- **Sharding**: Split data across multiple databases (Future)
- **Partitioning**: Organize data for better performance
- **Read Replicas**: Separate read operations (Future)
- **Connection Pooling**: Efficient connection management

## Deployment Architecture

### Development Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Developer     │    │   Frontend      │    │   Backend       │
│   Machine       │    │   (localhost:   │    │   (localhost:   │
│                 │    │   3000)         │    │   8000)         │
│ - Code Editor   │    │ - Next.js Dev   │    │ - FastAPI Dev   │
│ - Git Client    │    │   Server        │    │   Server        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Production Environment
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client        │    │   Load          │    │   Application   │
│   Browser       │    │   Balancer      │    │   Servers       │
│                 │    │                 │    │                 │
│ - Next.js App   │◄──►│ - Traffic       │◄──►│ - Multiple      │
│ - API Requests  │    │   Distribution  │    │   Instances     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Database      │
                       │   Cluster       │
                       │                 │
                       │ - Master Node   │
                       │ - Slave Nodes   │
                       │   (Future)      │
                       └─────────────────┘
```

### CI/CD Pipeline
```
Code Commit
    ↓
Automated Testing
    ↓
Security Scanning
    ↓
Build & Package
    ↓
Staging Deployment
    ↓
Automated Testing (Staging)
    ↓
Production Deployment
    ↓
Health Monitoring
```

## Data Architecture

### Database Schema
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   courses       │    │   chapters      │    │   users         │
│                 │    │                 │    │                 │
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ title           │    │ course_id (FK)  │    │ email           │
│ description     │    │ title           │    │ username        │
│ prerequisites   │    │ content         │    │ is_active       │
│ created_at      │    │ next_chapter_id │    │ created_at      │
│ updated_at      │    │ prev_chapter_id │    │ updated_at      │
└─────────────────┘    │ order           │    └─────────────────┘
                       │ created_at      │
┌─────────────────┐    │ updated_at      │
│   user_progress │    └─────────────────┘
│                 │
│ id (PK)         │    ┌─────────────────┐    ┌─────────────────┐
│ user_id (FK)    │    │   quizzes       │    │   quiz_attempts │
│ course_id (FK)  │    │                 │    │                 │
│ completed_chap. │    │ id (PK)         │    │ id (PK)         │
│ quiz_scores     │    │ course_id (FK)  │    │ user_id (FK)    │
│ last_accessed   │    │ chapter_id (FK) │    │ quiz_id (FK)    │
│ streak_days     │    │ title           │    │ answers         │
│ created_at      │    │ questions       │    │ score           │
│ updated_at      │    │ passing_score   │    │ passed          │
└─────────────────┘    │ created_at      │    │ completed_at    │
                       │ updated_at      │    └─────────────────┘
                       └─────────────────┘
```

### Data Flow
```
User Interaction
    ↓
API Request
    ↓
Authentication & Validation
    ↓
Business Logic Processing
    ↓
Database Operation
    ↓
Response Generation
    ↓
Client Response
```

## Integration Architecture

### External Integrations
1. **ChatGPT API**: AI-powered tutoring and explanations
2. **Cloudflare R2**: Cloud storage for course content
3. **Payment Gateway**: Subscription management (Future)
4. **Email Service**: Notifications and communications (Future)

### API Contracts
- **RESTful APIs**: Standard HTTP methods and status codes
- **JSON Format**: Standard data exchange format
- **Versioning**: API version management
- **Documentation**: OpenAPI specification

## Monitoring and Observability

### Logging Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Application   │    │   Log Aggregator│    │   Log Viewer    │
│   Logs          │    │   (ELK Stack)   │    │   (Kibana)      │
│                 │    │                 │    │                 │
│ - Structured    │───►│ - Centralized   │───►│ - Search &      │
│   JSON Format   │    │   Collection    │    │   Visualization │
│ - Log Levels    │    │ - Filtering     │    │ - Alerts        │
│ - Context       │    │ - Archiving     │    │ - Dashboards    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Metrics Collection
- **Application Metrics**: Response times, error rates, throughput
- **System Metrics**: CPU, memory, disk usage
- **Business Metrics**: User engagement, course completion
- **Custom Metrics**: Domain-specific measurements

### Health Monitoring
- **Application Health**: Service availability checks
- **Database Health**: Connection and performance monitoring
- **External Service Health**: Third-party service monitoring
- **Resource Utilization**: Infrastructure monitoring

## Error Handling Architecture

### Error Propagation
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Client)      │    │   (API)         │    │   (Queries)     │
│                 │    │                 │    │                 │
│ - Network       │◄──►│ - Business Logic│◄──►│ - Database      │
│   Errors        │    │   Errors        │    │   Errors        │
│ - Validation    │    │ - Authentication│    │ - Connection    │
│   Errors        │    │   Errors        │    │   Errors        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Error Handler                          │
│  - Standardized Error Format                              │
│  - Error Logging                                          │
│  - Error Recovery                                         │
│  - User-Friendly Messages                                 │
└─────────────────────────────────────────────────────────────┘
```

### Error Response Format
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional error details",
    "timestamp": "ISO 8601 timestamp",
    "request_id": "unique request identifier"
  }
}
```

## Deployment Architecture

### Containerization (Future)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   Container     │    │   Container     │    │   Container     │
│   (Docker)      │    │   (Docker)      │    │   (Docker)      │
│                 │    │                 │    │                 │
│ - Next.js App   │    │ - FastAPI App   │    │ - PostgreSQL    │
│ - Dependencies  │    │ - Dependencies  │    │ - Data Volume   │
│ - Configuration │    │ - Environment   │    │ - Backup        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Orchestration (Future)
- **Kubernetes**: Container orchestration
- **Service Discovery**: Automatic service registration
- **Auto-scaling**: Dynamic resource allocation
- **Rolling Updates**: Zero-downtime deployments

## Security Architecture

### Defense in Depth
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Network       │    │   Application   │    │   Data          │
│   Layer         │    │   Layer         │    │   Layer         │
│                 │    │                 │    │                 │
│ - Firewall      │    │ - Authentication│    │ - Encryption    │
│ - VPN           │    │ - Authorization │    │ - Access        │
│ - DDoS          │    │ - Input         │    │   Controls      │
│   Protection    │    │   Validation    │    │ - Backup        │
└─────────────────┘    │ - Rate Limiting │    └─────────────────┘
                       │ - Session       │
┌─────────────────┐    │   Management    │    ┌─────────────────┐
│   Identity      │    │ - Security      │    │   Audit         │
│   Management    │    │   Headers       │    │   Trail         │
│                 │    └─────────────────┘    │                 │
│ - User          │                           │ - Activity      │
│   Management    │    ┌─────────────────┐    │   Logging       │
│ - Role          │    │   Monitoring    │    │ - Compliance    │
│   Management    │    │                 │    │ - Forensics     │
│ - Permission    │    │ - Health        │    └─────────────────┘
│   Management    │    │   Checks        │
└─────────────────┘    │ - Performance   │
                       │   Monitoring    │
                       │ - Error         │
                       │   Tracking      │
                       └─────────────────┘
```

## Future Architecture Considerations

### Microservices Migration (Phase 3)
```
Current Monolith → Future Microservices
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Course        │    │   Course        │    │   Progress      │
│   Service       │    │   Service       │    │   Service       │
│   (Monolith)    │───→│   (Microservice)│───→│   (Microservice)│
│                 │    │                 │    │                 │
│ - All Features  │    │ - Course        │    │ - Progress      │
│   in One App    │    │   Management    │    │   Tracking      │
└─────────────────┘    │ - Chapter       │    │ - User          │
                       │   Navigation    │    │   Analytics     │
┌─────────────────┐    │ - Content       │    └─────────────────┘
│   Quiz &        │    │   Delivery      │
│   Search        │    └─────────────────┘
│   Service       │
│   (Monolith)    │    ┌─────────────────┐    ┌─────────────────┐
│                 │    │   User          │    │   Payment       │
│ - Quiz          │    │   Service       │    │   Service       │
│   Management    │    │   (Microservice)│    │   (Microservice)│
│ - Search        │    │ - User          │    │ - Subscription  │
│   Functionality │    │   Management    │    │   Management    │
└─────────────────┘    │ - Authentication│    │ - Billing       │
                       │ - Authorization │    │ - Invoicing     │
                       └─────────────────┘    └─────────────────┘
```

### Event-Driven Architecture (Future)
- **Message Queues**: RabbitMQ, Apache Kafka
- **Event Streaming**: Real-time data processing
- **CQRS Pattern**: Separate read and write models
- **Event Sourcing**: Immutable event log

## Quality Assurance Architecture

### Testing Strategy
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Unit Tests    │    │   Integration   │    │   End-to-End    │
│   (Backend)     │    │   Tests         │    │   Tests         │
│                 │    │                 │    │                 │
│ - Model Tests   │    │ - API Tests     │    │ - UI Tests      │
│ - Service Tests │    │ - Database      │    │ - Workflow      │
│ - Utility Tests │    │   Tests         │    │   Tests         │
└─────────────────┘    │ - Auth Tests    │    └─────────────────┘
                       └─────────────────┘
┌─────────────────┐                        ┌─────────────────┐
│   Performance   │                        │   Security      │
│   Tests         │                        │   Tests         │
│                 │                        │                 │
│ - Load Tests    │                        │ - Vulnerability │
│ - Stress Tests  │                        │   Scanning      │
│ - Soak Tests    │                        │ - Penetration   │
│ - Spike Tests   │                        │   Testing       │
└─────────────────┘                        └─────────────────┘
```

### Code Quality
- **Static Analysis**: Linting and code style enforcement
- **Code Coverage**: Target 80%+ test coverage
- **Peer Review**: Mandatory code reviews
- **Security Scanning**: Automated vulnerability detection

This architecture ensures scalability, maintainability, and performance while adhering to the Zero-Backend-LLM principle for Phase 1 implementation.