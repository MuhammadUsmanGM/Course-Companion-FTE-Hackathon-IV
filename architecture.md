# Course Companion FTE - Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              COURSE COMPANION FTE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐            │
│  │   USER AGENTS   │    │   CHATGPT APP   │    │    WEB APP      │            │
│  │                 │    │                 │    │                 │            │
│  │ • Students      │    │ • Conversational│    │ • Course Browse │            │
│  │ • Educators     │◄──►│ • Tutoring      │◄──►│ • Progress Track│            │
│  │ • Admins        │    │ • Interaction   │    │ • Quiz System   │            │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘            │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                        BACKEND SERVICES                               │    │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐       │    │
│  │  │  DETERMINISTIC  │  │ HYBRID INTEL-   │  │  CONTENT &      │       │    │
│  │  │     APIs        │  │   LIGENCE       │  │   STORAGE       │       │    │
│  │  │                 │  │  (Phase 2)      │  │                 │       │    │
│  │  │ • Content APIs  │  │ • Adaptive      │  │ • Cloudflare R2 │       │    │
│  │  │ • Navigation    │  │   Learning      │  │ • Course Data   │       │    │
│  │  │ • Quiz Grading  │  │ • LLM Assess-   │  │ • Media Assets  │       │    │
│  │  │ • Progress Track│  │   ments         │  │ • Quiz Banks    │       │    │
│  │  │ • Search        │  │ • Synthesis     │  │                 │       │    │
│  │  │ • Access Control│  │ • Mentor Agent  │  │                 │       │    │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘       │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │                       INFRASTRUCTURE                                  │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │    │
│  │  │DATABASE     │  │LOAD BALANCER│  │CACHE        │  │MONITORING   │  │    │
│  │  │• User Data  │  │• Traffic     │  │• API Caching│  │• Performance│  │    │
│  │  │• Progress   │  │• Scaling     │  │• CDN       │  │• Errors     │  │    │
│  │  │• Quiz Scores│  │              │  │            │  │• Usage      │  │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘  │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Phase 1: Zero-Backend-LLM Architecture

```
User Request
      ↓
   ChatGPT App
      ↓
   Backend Server (Deterministic)
      ↓
   Content Storage (Cloudflare R2)
      ↓
   Response to ChatGPT App
      ↓
   Response to User

KEY: No LLM calls in backend during Phase 1
```

## Phase 2: Hybrid Intelligence (Optional Features)

```
User Request
      ↓
   ChatGPT App
      ↓
   Backend Server
      ├─ Deterministic APIs (Phase 1 features)
      └─ Hybrid Intelligence APIs (Premium features)
             ↓
         LLM API Calls (OpenAI/Claude)
             ↓
         Processed Response
             ↓
         Backend Server
             ↓
         Response to ChatGPT App
             ↓
         Response to User

KEY: Hybrid features are premium-gated and user-initiated
```

## Phase 3: Web App Architecture

```
Browser/Device
      ↓
   Next.js Frontend
      ↓
   Backend Server
      ├─ All APIs (Free + Premium features)
      └─ LLM API Calls (where needed)
           ↓
       Response to Frontend
           ↓
       Rendered UI
```

## Security & Compliance

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AUTHENTICATION│    │  DATA SECURITY  │    │  PRIVACY        │
│                 │    │                 │    │                 │
│ • User Sessions │    │ • Encryption    │    │ • GDPR Compliant│
│ • OAuth 2.0     │    │ • Secure APIs   │    │ • Data Minim.   │
│ • Role-based    │    │ • Input Validation│   │ • Consent       │
│   Access        │    │ • Rate Limiting │    │   Management    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Scalability & Performance

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   LOAD BALANCING│    │   CACHING       │    │   MONITORING    │
│                 │    │                 │    │                 │
│ • Horizontal    │    │ • API Responses │    │ • Real-time     │
│   Scaling       │    │ • Static Assets │    │   Dashboard     │
│ • Auto-scaling  │    │ • CDN           │    │ • Error Tracking│
│ • Health Checks │    │ • Database Cache│    │ • Performance   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```