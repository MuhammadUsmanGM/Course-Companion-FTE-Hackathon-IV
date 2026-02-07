from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from config.database import get_db
from models import Course as CourseModel, Chapter as ChapterModel
from schemas import Course as CourseSchema, Chapter as ChapterSchema, CourseCreate

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/")
async def get_courses(db: Session = Depends(get_db)):
    """Get all available courses"""
    try:
        courses = db.query(CourseModel).all()
        logger.info(f"Retrieved {len(courses)} courses")
        return {"courses": courses}
    except Exception as e:
        logger.error(f"Error retrieving courses: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{course_id}", response_model=CourseSchema)
async def get_course(course_id: str, db: Session = Depends(get_db)):
    """Get a specific course by ID"""
    try:
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        logger.info(f"Retrieved course: {course_id}")
        return course
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving course {course_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{course_id}/chapters")
async def get_course_chapters(course_id: str, db: Session = Depends(get_db)):
    """Get all chapters for a specific course"""
    try:
        chapters = db.query(ChapterModel).filter(ChapterModel.course_id == course_id).order_by(ChapterModel.order).all()
        if not chapters:
            # Check if course exists to return appropriate error
            course_exists = db.query(CourseModel).filter(CourseModel.id == course_id).first()
            if not course_exists:
                raise HTTPException(status_code=404, detail="Course not found")
        logger.info(f"Retrieved {len(chapters)} chapters for course: {course_id}")
        return {"chapters": chapters}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving chapters for course {course_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chapters/{chapter_id}", response_model=ChapterSchema)
async def get_chapter(chapter_id: str, db: Session = Depends(get_db)):
    """Get a specific chapter by ID"""
    try:
        chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
        if not chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")
        logger.info(f"Retrieved chapter: {chapter_id}")
        return chapter
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving chapter {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chapters/{chapter_id}/next", response_model=ChapterSchema)
async def get_next_chapter(chapter_id: str, db: Session = Depends(get_db)):
    """Get the next chapter after the specified one"""
    try:
        current_chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
        if not current_chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        if not current_chapter.next_chapter_id:
            raise HTTPException(status_code=404, detail="No next chapter available")

        next_chapter = db.query(ChapterModel).filter(ChapterModel.id == current_chapter.next_chapter_id).first()
        if not next_chapter:
            raise HTTPException(status_code=404, detail="Next chapter not found")

        logger.info(f"Retrieved next chapter: {next_chapter.id} for chapter: {chapter_id}")
        return next_chapter
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving next chapter for {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chapters/{chapter_id}/previous", response_model=ChapterSchema)
async def get_prev_chapter(chapter_id: str, db: Session = Depends(get_db)):
    """Get the previous chapter before the specified one"""
    try:
        current_chapter = db.query(ChapterModel).filter(ChapterModel.id == chapter_id).first()
        if not current_chapter:
            raise HTTPException(status_code=404, detail="Chapter not found")

        if not current_chapter.prev_chapter_id:
            raise HTTPException(status_code=404, detail="No previous chapter available")

        prev_chapter = db.query(ChapterModel).filter(ChapterModel.id == current_chapter.prev_chapter_id).first()
        if not prev_chapter:
            raise HTTPException(status_code=404, detail="Previous chapter not found")

        logger.info(f"Retrieved previous chapter: {prev_chapter.id} for chapter: {chapter_id}")
        return prev_chapter
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving previous chapter for {chapter_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")