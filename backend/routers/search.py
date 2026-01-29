from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import logging
from sqlalchemy import or_

from config.database import get_db
from models import Course as CourseModel, Chapter as ChapterModel
from schemas import SearchRequest, SearchResponse

router = APIRouter()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@router.get("/", response_model=SearchResponse)
async def search_content(query: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search for content across courses and chapters"""
    try:
        results = []

        # Search in courses
        course_results = db.query(CourseModel).filter(
            or_(
                CourseModel.title.ilike(f"%{query}%"),
                CourseModel.description.ilike(f"%{query}%")
            )
        ).limit(limit).all()

        for course in course_results:
            results.append({
                "type": "course",
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "relevance": 0.9
            })

        # Search in chapters
        chapter_results = db.query(ChapterModel).filter(
            or_(
                ChapterModel.title.ilike(f"%{query}%"),
                ChapterModel.content.ilike(f"%{query}%")
            )
        ).limit(limit).all()

        for chapter in chapter_results:
            # Find the associated course
            course = db.query(CourseModel).filter(CourseModel.id == chapter.course_id).first()

            relevance = 0.8 if query.lower() in chapter.title.lower() else 0.6

            results.append({
                "type": "chapter",
                "id": chapter.id,
                "title": chapter.title,
                "course_id": chapter.course_id,
                "course_title": course.title if course else "Unknown Course",
                "relevance": relevance
            })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)

        # Limit results
        limited_results = results[:limit]

        logger.info(f"Search query '{query}' returned {len(limited_results)} results")
        return SearchResponse(results=limited_results)
    except Exception as e:
        logger.error(f"Error performing search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/courses", response_model=SearchResponse)
async def search_courses(query: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search specifically for courses"""
    try:
        results = []

        # Search in courses only
        course_results = db.query(CourseModel).filter(
            or_(
                CourseModel.title.ilike(f"%{query}%"),
                CourseModel.description.ilike(f"%{query}%")
            )
        ).limit(limit).all()

        for course in course_results:
            results.append({
                "type": "course",
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "relevance": 0.9
            })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)

        logger.info(f"Course search query '{query}' returned {len(results)} results")
        return SearchResponse(results=results[:limit])
    except Exception as e:
        logger.error(f"Error performing course search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/chapters", response_model=SearchResponse)
async def search_chapters(query: str, limit: int = 10, db: Session = Depends(get_db)):
    """Search specifically for chapters"""
    try:
        results = []

        # Search in chapters only
        chapter_results = db.query(ChapterModel).filter(
            or_(
                ChapterModel.title.ilike(f"%{query}%"),
                ChapterModel.content.ilike(f"%{query}%")
            )
        ).limit(limit).all()

        for chapter in chapter_results:
            # Find the associated course
            course = db.query(CourseModel).filter(CourseModel.id == chapter.course_id).first()

            relevance = 0.8 if query.lower() in chapter.title.lower() else 0.6

            results.append({
                "type": "chapter",
                "id": chapter.id,
                "title": chapter.title,
                "course_id": chapter.course_id,
                "course_title": course.title if course else "Unknown Course",
                "relevance": relevance
            })

        # Sort by relevance
        results.sort(key=lambda x: x["relevance"], reverse=True)

        logger.info(f"Chapter search query '{query}' returned {len(results)} results")
        return SearchResponse(results=results[:limit])
    except Exception as e:
        logger.error(f"Error performing chapter search: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")