# Claude Code Guide for Course Companion FTE

## Project Overview
The Course Companion FTE is a Digital Full-Time Equivalent Educational Tutor designed to serve as a 24/7 educational companion, operating 168 hours per week with 85-90% cost savings compared to human tutors. This project implements the Agent Factory Architecture to create an AI-Native Course Companion that teaches, explains, quizzes, tracks, and adapts to learners.

## Project Goals
- Build a production-ready Digital FTE that can tutor thousands of students simultaneously
- Operate 24/7 without fatigue while maintaining 99%+ consistency in educational delivery
- Scale from 10 to 100,000 users without linear cost increase
- Support both ChatGPT App and standalone Web App frontends

## Architecture Principles

### Zero-Backend-LLM Architecture (Phase 1)
- Backend performs ZERO LLM inference
- ChatGPT handles ALL explanation, tutoring, and adaptation
- System is production-viable and can scale to 100k+ users cheaply
- Backend responsibilities: Serve content, track progress, enforce rules
- ChatGPT responsibilities: Explain concepts, provide analogies, answer questions, adapt tone

### Technical Stack
- **Frontend (Phase 1)**: ChatGPT App using OpenAI Apps SDK
- **Backend**: FastAPI (Python) for content APIs, quiz APIs, progress APIs
- **Storage**: Cloudflare R2 for course content, media assets, quiz banks
- **Phase 2**: Hybrid backend with FastAPI + LLM API Calls for premium features
- **Phase 3**: Web frontend with Next.js/React and consolidated backend

## Key Features

### Phase 1 Required Features
1. **Content Delivery**: Backend serves content verbatim, ChatGPT explains at learner's level
2. **Navigation**: Backend returns next/previous chapters, ChatGPT suggests optimal path
3. **Grounded Q&A**: Backend returns relevant sections, ChatGPT answers using content only
4. **Rule-Based Quizzes**: Backend grades with answer key, ChatGPT presents, encourages, explains
5. **Progress Tracking**: Backend stores completion/streaks, ChatGPT celebrates, motivates
6. **Freemium Gate**: Backend checks access rights, ChatGPT explains premium gracefully

### Phase 2 Hybrid Features (Choose Up to 2)
- Adaptive Learning Path: Analyzes patterns, generates personalized recommendations
- LLM-Graded Assessments: Evaluates free-form written answers with detailed feedback
- Cross-Chapter Synthesis: Connects concepts across chapters, generates "big picture"
- AI Mentor Agent: Long-running agent for complex tutoring workflows

## Agent Skills Design
Runtime skills that teach the Course Companion FTE how to perform educational tasks consistently:

- **concept-explainer**: Explain concepts at various complexity levels ("explain", "what is", "how does")
- **quiz-master**: Guide students through quizzes with encouragement ("quiz", "test me", "practice")
- **socratic-tutor**: Guide learning through questions, not answers ("help me think", "I'm stuck")
- **progress-motivator**: Celebrate achievements, maintain motivation ("my progress", "streak", "how am I doing")

## Course Content Options
Teams must choose ONE course topic:
- Option A: AI Agent Development (Claude Agent SDK concepts, MCP, Agent Skills)
- Option B: Cloud-Native Python (FastAPI, Containers, Kubernetes basics)
- Option C: Generative AI Fundamentals (LLMs, Prompting, RAG, Fine-tuning)
- Option D: Modern Python (Modern Python with Typing)

## Cost Considerations
- **Phase 1 (Zero-Backend-LLM)**: ~$16-$41 monthly for 10K users ($0.002-$0.004 per user)
- **Phase 2 (Hybrid)**: Additional LLM costs depending on feature usage
- **Monetization**: Free tier, Premium ($9.99/mo), Pro ($19.99/mo), Team ($49.99/mo)

## Implementation Guidelines
- Strictly avoid LLM API calls in Phase 1 backend (disqualification criterion)
- Implement clear separation between deterministic and hybrid features in Phase 2
- Ensure premium features are properly gated and user-initiated
- Follow the 8-layer Agent Factory architecture (L0-L7)
- Design with scalability and cost efficiency in mind

## Success Metrics
- Architecture correctness (zero backend LLM calls in Phase 1)
- Feature completeness (all required features implemented)
- User experience quality (UX testing and responsiveness)
- Cost efficiency (proper cost analysis and tracking)
- Clear separation between free and premium features