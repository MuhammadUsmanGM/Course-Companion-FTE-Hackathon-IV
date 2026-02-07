from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging
from datetime import datetime

from config.database import get_db
from models import HybridUsage as HybridUsageModel, Course as CourseModel, Chapter as ChapterModel
from schemas import (
    AdaptiveLearningRequest, AdaptiveLearningResponse, 
    LLMAssessmentRequest, LLMAssessmentResponse,
    CrossChapterSynthesisRequest, CrossChapterSynthesisResponse,
    MentorSessionRequest, MentorSessionResponse,
    HybridUsage
)

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/adaptive-learning", response_model=AdaptiveLearningResponse)
async def adaptive_learning_path(request: AdaptiveLearningRequest, db: Session = Depends(get_db)):
    """
    Premium feature: Generate personalized learning path based on user performance
    Cost: $0.018 per request (Claude Sonnet, ~2K tokens)
    """
    try:
        # Track usage for cost analysis
        current_month = datetime.utcnow().strftime('%Y-%m')
        usage = db.query(HybridUsageModel).filter(
            HybridUsageModel.user_id == request.user_id,
            HybridUsageModel.month_year == current_month
        ).first()

        if not usage:
            usage = HybridUsageModel(user_id=request.user_id, month_year=current_month)
            db.add(usage)
        
        usage.adaptive_learning += 1
        db.commit()

        logger.info(f"Adaptive learning request for user {request.user_id}, course {request.course_id}")

        # Simulate LLM processing for adaptive learning
        # In a real implementation, this would call an LLM API
        course = db.query(CourseModel).filter(CourseModel.id == request.course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        chapters = db.query(ChapterModel).filter(ChapterModel.course_id == request.course_id).order_by(ChapterModel.order).all()
        
        current_chapter_idx = 0
        for idx, chapter in enumerate(chapters):
            if chapter.id == request.current_chapter_id:
                current_chapter_idx = idx
                break

        # Determine next chapter based on performance
        next_chapter_idx = min(current_chapter_idx + 1, len(chapters) - 1)
        next_chapter_id = chapters[next_chapter_idx].id if chapters else request.current_chapter_id

        # Analyze quiz performance to identify weak areas
        weak_areas = []
        for quiz_id, score in request.quiz_performance.items():
            if score < 0.7:  # Below passing threshold
                weak_areas.append(quiz_id)

        # Simulate learning style analysis
        learning_style = "visual" if sum(request.time_spent.values()) > 300 else "kinesthetic"

        response = AdaptiveLearningResponse(
            recommended_next_chapter=next_chapter_id,
            confidence=0.85,
            learning_style=learning_style,
            improvement_areas=weak_areas,
            estimated_time_to_mastery="2-3 weeks"
        )

        logger.info(f"Adaptive learning response generated for user {request.user_id}")
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in adaptive learning: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/llm-assessment", response_model=LLMAssessmentResponse)
async def llm_grade_assessment(request: LLMAssessmentRequest, db: Session = Depends(get_db)):
    """
    Premium feature: LLM-based assessment with detailed feedback
    Cost: $0.014 per request (Claude Sonnet, ~1.5K tokens)
    """
    try:
        # Track usage
        current_month = datetime.utcnow().strftime('%Y-%m')
        usage = db.query(HybridUsageModel).filter(
            HybridUsageModel.user_id == request.user_id,
            HybridUsageModel.month_year == current_month
        ).first()

        if not usage:
            usage = HybridUsageModel(user_id=request.user_id, month_year=current_month)
            db.add(usage)
        
        usage.llm_assessment += 1
        db.commit()

        logger.info(f"LLM assessment request for user {request.user_id}, question {request.question_id}")

        # Simulate LLM processing
        score = 0.8
        feedback_parts = []
        if len(request.user_response) < 50:
            feedback_parts.append("Your response is quite brief. Try to elaborate on your answer.")

        if request.correct_answer.lower() in request.user_response.lower():
            feedback_parts.append("Good job identifying the key concept!")
        else:
            feedback_parts.append(f"Consider reviewing: {request.correct_answer}")

        feedback = " ".join(feedback_parts) if feedback_parts else "Well done! Your answer demonstrates good understanding."
        misconceptions = ["Incomplete explanation"] if len(request.user_response) < 100 else []
        topics = ["Review fundamental concepts", "Practice with examples"]

        response = LLMAssessmentResponse(
            score=score,
            feedback=feedback,
            misconceptions_identified=misconceptions,
            recommended_study_topics=topics,
            confidence_level="high" if score >= 0.8 else "medium"
        )

        logger.info(f"LLM assessment response generated for user {request.user_id}")
        return response
    except Exception as e:
        logger.error(f"Error in LLM assessment: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/synthesis", response_model=CrossChapterSynthesisResponse)
async def cross_chapter_synthesis(request: CrossChapterSynthesisRequest, db: Session = Depends(get_db)):
    """
    Premium feature: Connect concepts across chapters and generate insights
    Cost: $0.027 per request (Claude Sonnet, ~3K tokens)
    """
    try:
        # Track usage
        current_month = datetime.utcnow().strftime('%Y-%m')
        usage = db.query(HybridUsageModel).filter(
            HybridUsageModel.user_id == request.user_id,
            HybridUsageModel.month_year == current_month
        ).first()

        if not usage:
            usage = HybridUsageModel(user_id=request.user_id, month_year=current_month)
            db.add(usage)
        
        usage.synthesis += 1
        db.commit()

        logger.info(f"Synthesis request for user {request.user_id}, course {request.course_id}")

        # Simulate LLM processing
        chapters = db.query(ChapterModel).filter(ChapterModel.id.in_(request.chapter_ids)).all()
        concepts = [ch.title for ch in chapters]

        connections = [
            f"The concept of '{concepts[0] if concepts else 'Unknown'}' builds upon previous units in important ways.",
            f"Understanding these core principles is crucial for mastering advanced topics."
        ]

        insights = [
            "These concepts form a foundational understanding of the subject.",
            "The progression from basic to advanced concepts demonstrates increasing complexity."
        ]

        applications = [
            "Apply these concepts in real-world scenarios to reinforce learning.",
            "Connect these ideas to other subjects for deeper understanding."
        ]

        response = CrossChapterSynthesisResponse(
            synthesized_concepts=concepts,
            connections_identified=connections,
            big_picture_insights=insights,
            practical_applications=applications
        )

        logger.info(f"Synthesis response generated for user {request.user_id}")
        return response
    except Exception as e:
        logger.error(f"Error in synthesis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/mentor-session", response_model=MentorSessionResponse)
async def ai_mentor_session(request: MentorSessionRequest, db: Session = Depends(get_db)):
    """
    Premium feature: Long-running AI mentor for complex tutoring workflows
    Cost: $0.090 per session (Claude Sonnet, ~10K tokens)
    """
    try:
        # Track usage
        current_month = datetime.utcnow().strftime('%Y-%m')
        usage = db.query(HybridUsageModel).filter(
            HybridUsageModel.user_id == request.user_id,
            HybridUsageModel.month_year == current_month
        ).first()

        if not usage:
            usage = HybridUsageModel(user_id=request.user_id, month_year=current_month)
            db.add(usage)
        
        usage.mentor_sessions += 1
        db.commit()

        logger.info(f"Mentor session request for user {request.user_id}, question: {request.question[:50]}...")

        # Simulate LLM processing
        response_text = f"I understand you're asking about '{request.question}'. Based on the context of '{request.context}', I'd suggest considering the following approach: "
        response_text += "First, let's break down the problem into smaller components. Then, we can address each part systematically. "
        response_text += "Would you like me to walk you through a specific example?"

        teaching_points = [
            "Break complex problems into smaller parts",
            "Apply concepts learned in previous chapters",
            "Practice with guided examples"
        ]

        follow_up_questions = [
            "Can you think of any real-world applications for this concept?",
            "How does this connect to what you learned in the previous chapter?",
            "Would you like to try a practice problem?"
        ]

        related_concepts = [
            "Foundational concepts from earlier chapters",
            "Advanced applications in later chapters"
        ]

        response = MentorSessionResponse(
            response=response_text,
            teaching_points=teaching_points,
            follow_up_questions=follow_up_questions,
            related_concepts=related_concepts
        )

        logger.info(f"Mentor session response generated for user {request.user_id}")
        return response
    except Exception as e:
        logger.error(f"Error in mentor session: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/usage/{user_id}", response_model=HybridUsage)
async def get_hybrid_usage(user_id: str, db: Session = Depends(get_db)):
    """
    Get usage statistics for hybrid intelligence features for cost tracking
    """
    current_month = datetime.utcnow().strftime('%Y-%m')
    usage = db.query(HybridUsageModel).filter(
        HybridUsageModel.user_id == user_id,
        HybridUsageModel.month_year == current_month
    ).first()

    if usage:
        return usage
    else:
        return HybridUsage(
            user_id=user_id,
            month_year=current_month,
            adaptive_learning=0,
            llm_assessment=0,
            synthesis=0,
            mentor_sessions=0
        )
