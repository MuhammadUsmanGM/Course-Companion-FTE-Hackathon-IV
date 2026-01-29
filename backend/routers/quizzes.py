from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from config.database import get_db
from models import Quiz as QuizModel, QuizAttempt as QuizAttemptModel, UserProgress as UserProgressModel
from schemas import Quiz as QuizSchema, QuizSubmission, QuizResult, QuizAttemptCreate, QuizAttempt

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/{quiz_id}", response_model=QuizSchema)
async def get_quiz(quiz_id: str, db: Session = Depends(get_db)):
    """Get a specific quiz by ID"""
    try:
        quiz = db.query(QuizModel).filter(QuizModel.id == quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")
        logger.info(f"Retrieved quiz: {quiz_id}")
        return quiz
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving quiz {quiz_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/submit", response_model=QuizResult)
async def submit_quiz(submission: QuizSubmission, db: Session = Depends(get_db)):
    """Submit quiz answers and get results"""
    try:
        # Get the quiz
        quiz = db.query(QuizModel).filter(QuizModel.id == submission.quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=404, detail="Quiz not found")

        # Calculate score
        correct_answers = 0
        total_questions = len(quiz.questions)

        for question in quiz.questions:
            question_id = question.id
            if question_id in submission.answers:
                if submission.answers[question_id] == question.correct_answer:
                    correct_answers += 1

        score = correct_answers / total_questions if total_questions > 0 else 0
        passed = score >= quiz.passing_score

        # Save quiz attempt
        quiz_attempt = QuizAttemptModel(
            user_id=submission.user_id,
            quiz_id=submission.quiz_id,
            answers=submission.answers,
            score=score,
            passed=passed
        )
        db.add(quiz_attempt)
        db.commit()
        db.refresh(quiz_attempt)

        # Update user progress
        user_progress = db.query(UserProgressModel).filter(
            UserProgressModel.user_id == submission.user_id,
            UserProgressModel.course_id == quiz.course_id
        ).first()

        if not user_progress:
            # Create new progress record if it doesn't exist
            user_progress = UserProgressModel(
                user_id=submission.user_id,
                course_id=quiz.course_id,
                completed_chapters=[],
                quiz_scores={},
                streak_days=0
            )
            db.add(user_progress)

        # Update quiz scores
        user_progress.quiz_scores[submission.quiz_id] = {
            "score": score,
            "passed": passed,
            "date": datetime.utcnow().isoformat()
        }
        db.commit()

        feedback = "Great job!" if passed else "Keep studying, you'll get it next time!"

        result = QuizResult(
            quiz_id=submission.quiz_id,
            score=score,
            passed=passed,
            feedback=feedback
        )

        logger.info(f"Quiz submitted by user {submission.user_id}, score: {score}, passed: {passed}")
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting quiz: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/attempts/{user_id}/{quiz_id}", response_model=List[QuizAttempt])
async def get_user_quiz_attempts(user_id: str, quiz_id: str, db: Session = Depends(get_db)):
    """Get all attempts by a user for a specific quiz"""
    try:
        attempts = db.query(QuizAttemptModel).filter(
            QuizAttemptModel.user_id == user_id,
            QuizAttemptModel.quiz_id == quiz_id
        ).order_by(QuizAttemptModel.completed_at.desc()).all()

        logger.info(f"Retrieved {len(attempts)} attempts for user {user_id} and quiz {quiz_id}")
        return attempts
    except Exception as e:
        logger.error(f"Error retrieving quiz attempts: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/user/{user_id}/course/{course_id}", response_model=List[QuizSchema])
async def get_user_quizzes_for_course(user_id: str, course_id: str, db: Session = Depends(get_db)):
    """Get all quizzes for a specific course that a user can access"""
    try:
        quizzes = db.query(QuizModel).filter(QuizModel.course_id == course_id).all()

        logger.info(f"Retrieved {len(quizzes)} quizzes for course {course_id} for user {user_id}")
        return quizzes
    except Exception as e:
        logger.error(f"Error retrieving quizzes for course {course_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")