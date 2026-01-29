from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging
from datetime import datetime

from config.database import get_db
from models import UserProgress as UserProgressModel, Chapter as ChapterModel, Course as CourseModel
from schemas import UserProgress as UserProgressSchema, UserProgressCreate

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.post("/{user_id}/courses/{course_id}/chapters/{chapter_id}")
async def mark_chapter_completed(user_id: str, course_id: str, chapter_id: str, db: Session = Depends(get_db)):
    """Mark a chapter as completed for a user"""
    try:
        # Check if chapter exists
        chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        # Check if course exists
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Find or create user progress record
        user_progress = db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id,
            UserProgressModel.course_id == course_id
        ).first()

        if not user_progress:
            # Create new progress record if it doesn't exist
            user_progress = UserProgressModel(
                user_id=user_id,
                course_id=course_id,
                completed_chapters=[],
                quiz_scores={},
                streak_days=0
            )
            db.add(user_progress)
            db.commit()
            db.refresh(user_progress)

        # Add chapter to completed if not already there
        if chapter_id not in user_progress.completed_chapters:
            user_progress.completed_chapters.append(chapter_id)
            user_progress.last_accessed = datetime.utcnow()

        db.commit()

        logger.info(f"Chapter {chapter_id} marked as completed for user {user_id} in course {course_id}")
        return {
            "message": "Chapter marked as completed",
            "progress": {
                "user_id": user_progress.user_id,
                "course_id": user_progress.course_id,
                "completed_chapters": user_progress.completed_chapters,
                "quiz_scores": user_progress.quiz_scores,
                "last_accessed": user_progress.last_accessed,
                "streak_days": user_progress.streak_days
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error marking chapter as completed: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}/courses/{course_id}", response_model=UserProgressSchema)
async def get_user_progress(user_id: str, course_id: str, db: Session = Depends(get_db)):
    """Get a user's progress in a specific course"""
    try:
        # Check if course exists
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")

        # Get user progress
        user_progress = db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id,
            UserProgressModel.course_id == course_id
        ).first()

        if not user_progress:
            # Return default progress if no record exists
            return {
                "id": 0,
                "user_id": user_id,
                "course_id": course_id,
                "completed_chapters": [],
                "quiz_scores": {},
                "last_accessed": datetime.utcnow(),
                "streak_days": 0
            }

        # Calculate completion percentage
        total_chapters = db.query(ChapterModel).filter(ChapterModel.course_id == course_id).count()
        completed_count = len(user_progress.completed_chapters)
        completion_percentage = (completed_count / total_chapters) * 100 if total_chapters > 0 else 0

        logger.info(f"Retrieved progress for user {user_id} in course {course_id}")
        return {
            "id": user_progress.id,
            "user_id": user_progress.user_id,
            "course_id": user_progress.course_id,
            "completed_chapters": user_progress.completed_chapters,
            "quiz_scores": user_progress.quiz_scores,
            "last_accessed": user_progress.last_accessed,
            "streak_days": user_progress.streak_days,
            "completion_percentage": completion_percentage
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving user progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{user_id}/courses", response_model=List[dict])
async def get_user_courses_progress(user_id: str, db: Session = Depends(get_db)):
    """Get a user's progress across all courses"""
    try:
        # Get all progress records for the user
        user_progress_list = db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id
        ).all()

        progress_summary = []

        for progress in user_progress_list:
            # Get course info
            course = db.query(CourseModel).filter(CourseModel.id == progress.course_id).first()

            # Calculate completion percentage
            total_chapters = db.query(ChapterModel).filter(ChapterModel.course_id == progress.course_id).count()
            completed_count = len(progress.completed_chapters)
            completion_percentage = (completed_count / total_chapters) * 100 if total_chapters > 0 else 0

            progress_summary.append({
                "course_id": progress.course_id,
                "course_title": course.title if course else "Unknown Course",
                "completed_chapters": len(progress.completed_chapters),
                "total_chapters": total_chapters,
                "completion_percentage": completion_percentage,
                "quiz_scores": progress.quiz_scores,
                "streak_days": progress.streak_days,
                "last_accessed": progress.last_accessed
            })

        logger.info(f"Retrieved progress summary for user {user_id} across {len(progress_summary)} courses")
        return progress_summary
    except Exception as e:
        logger.error(f"Error retrieving user courses progress: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.put("/{user_id}/streak/reset")
async def reset_streak(user_id: str, db: Session = Depends(get_db)):
    """Reset a user's streak days to 0"""
    try:
        # Find all progress records for the user
        user_progress_list = db.query(UserProgressModel).filter(
            UserProgressModel.user_id == user_id
        ).all()

        for progress in user_progress_list:
            progress.streak_days = 0
            progress.last_accessed = datetime.utcnow()

        db.commit()

        logger.info(f"Reset streak for user {user_id}")
        return {"message": "Streak reset successfully", "user_id": user_id}
    except Exception as e:
        logger.error(f"Error resetting streak: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")