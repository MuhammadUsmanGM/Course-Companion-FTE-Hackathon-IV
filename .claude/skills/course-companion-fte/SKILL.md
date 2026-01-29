---
name: course-companion-fte
description: |-
  Comprehensive educational tutoring platform supporting content delivery, navigation, grounded Q&A, rule-based quizzes, progress tracking, and freemium gate features.
  Use when users ask for educational tutoring assistance, course content delivery, quiz generation, progress tracking, or educational content management for the Course Companion FTE platform.
---

# Course Companion FTE Educational Tutoring Platform

This skill provides comprehensive educational tutoring capabilities following the Agent Factory Architecture for digital full-time equivalent education.

## Core Capabilities

### 1. Content Delivery & Navigation
- Serve course content verbatim while enabling ChatGPT to explain concepts at learner's level
- Provide next/previous chapter navigation with intelligent path suggestions
- Support multiple course content types (AI Agent Development, Cloud-Native Python, Generative AI, Modern Python)

### 2. Grounded Q&A
- Return relevant sections from course content for question answering
- Enable ChatGPT to answer questions using only provided content
- Maintain factual accuracy and prevent hallucinations

### 3. Rule-Based Quizzes
- Generate and grade quizzes using predetermined answer keys
- Enable ChatGPT to present quizzes with encouragement and explanations
- Support various question types (multiple choice, true/false, fill-in-the-blank)

### 4. Progress Tracking
- Store completion status and streaks in backend
- Enable ChatGPT to celebrate achievements and maintain motivation
- Track learning patterns and engagement metrics

### 5. Freemium Gate Management
- Check user access rights in backend
- Enable ChatGPT to explain premium features gracefully
- Support tiered access (Free, Premium $9.99/mo, Pro $19.99/mo, Team $49.99/mo)

## Zero-Backend-LLM Architecture (Phase 1)

### Backend Responsibilities
- Serve content verbatim
- Return next/previous chapters
- Return relevant sections for Q&A
- Grade quizzes with answer key
- Store completion/streaks
- Check access rights

### ChatGPT Responsibilities
- Explain concepts at learner's level
- Suggest optimal learning path
- Answer questions using content only
- Present quizzes with encouragement
- Celebrate achievements and motivate
- Explain premium features gracefully

## Agent Skills Framework

### concept-explainer
- Explain concepts at various complexity levels
- Handle requests like "explain", "what is", "how does"
- Adapt explanations to learner's knowledge level

### quiz-master
- Guide students through quizzes with encouragement
- Handle requests like "quiz", "test me", "practice"
- Provide immediate feedback and explanations

### socratic-tutor
- Guide learning through questions, not answers
- Handle requests like "help me think", "I'm stuck"
- Encourage critical thinking and self-discovery

### progress-motivator
- Celebrate achievements and maintain motivation
- Handle requests like "my progress", "streak", "how am I doing"
- Provide personalized encouragement

## Implementation Guidelines

### Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing backend structure (FastAPI), frontend patterns (Next.js/React), storage systems (Cloudflare R2) |
| **Conversation** | User's specific educational needs, preferred course topics, learning objectives |
| **Skill References** | Domain patterns from `references/` (educational best practices, tutoring methodologies, course content structures) |
| **User Guidelines** | Project-specific conventions, team standards, cost efficiency requirements |

Ensure all required context is gathered before implementing.
Only ask user for THEIR specific requirements (domain expertise is in this skill).

### Required Clarifications

1. **Course Topic Selection**: Which course topic should be prioritized? (AI Agent Development, Cloud-Native Python, Generative AI, or Modern Python)
2. **User Role**: Are you a student seeking tutoring, an educator creating content, or a developer building the platform?
3. **Feature Priority**: Which features should be emphasized? (content delivery, quizzing, progress tracking, or premium features)
4. **Integration Context**: Is this for ChatGPT App, standalone Web App, or both?

### Optional Clarifications

5. **Learning Objectives**: Specific goals or outcomes the user hopes to achieve
6. **Technical Constraints**: Any specific platform or technology limitations
7. **Customization Needs**: Special requirements for content adaptation or personalization

## Educational Methodology

### Teaching Approach
- Adaptive explanations based on user comprehension
- Scaffolding: building from known to unknown concepts
- Active learning: encouraging questions and critical thinking
- Immediate feedback: correcting misconceptions promptly

### Content Structure
- Modular lessons that can stand alone or connect to others
- Progressive difficulty: concepts build upon previous knowledge
- Multiple representations: text, examples, analogies, diagrams
- Practice opportunities: quizzes, exercises, hands-on activities

## Technical Architecture

### Phase 1: Zero-Backend-LLM
- Backend: FastAPI serving content, tracking progress, enforcing rules
- ChatGPT: Explains, tutors, adapts, motivates
- Storage: Cloudflare R2 for course content and media
- Cost: ~$16-$41 monthly for 10K users ($0.002-$0.004 per user)

### Phase 2: Hybrid Features (Premium)
- Adaptive Learning Path: analyzes patterns, generates recommendations
- LLM-Graded Assessments: evaluates free-form answers with feedback
- Cross-Chapter Synthesis: connects concepts across chapters
- AI Mentor Agent: long-running agent for complex workflows

## Quality Standards

### Content Accuracy
- Verify all information against course materials
- Maintain factual integrity
- Attribute sources appropriately

### Educational Effectiveness
- Ensure explanations match learner's level
- Provide relevant examples and analogies
- Encourage active participation

### User Experience
- Respond promptly to queries
- Maintain consistent tone and personality
- Provide clear navigation options

## Cost Efficiency Considerations

- Prioritize Phase 1 features for maximum user reach at minimal cost
- Reserve Phase 2 features for premium users
- Monitor LLM usage to maintain cost targets
- Optimize for 85-90% cost savings compared to human tutors