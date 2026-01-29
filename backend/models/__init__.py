from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func
from config.database import Base
from datetime import datetime


class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    prerequisites = Column(JSON, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.id"))
    title = Column(String, index=True)
    content = Column(Text)
    next_chapter_id = Column(String, nullable=True)
    prev_chapter_id = Column(String, nullable=True)
    order = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    course_id = Column(String, ForeignKey("courses.id"))
    completed_chapters = Column(JSON, default=[])
    quiz_scores = Column(JSON, default={})
    last_accessed = Column(DateTime(timezone=True), server_default=func.now())
    streak_days = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(String, primary_key=True, index=True)
    course_id = Column(String, ForeignKey("courses.id"))
    chapter_id = Column(String, ForeignKey("chapters.id"))
    title = Column(String)
    questions = Column(JSON)  # Stores questions in JSON format
    passing_score = Column(Float, default=0.7)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    quiz_id = Column(String, ForeignKey("quizzes.id"))
    answers = Column(JSON)  # Stores user answers in JSON format
    score = Column(Float)
    passed = Column(Boolean)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    plan_type = Column(String, default="free")  # free, premium, pro, team
    start_date = Column(DateTime(timezone=True), server_default=func.now())
    end_date = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class HybridUsage(Base):
    __tablename__ = "hybrid_usage"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    month_year = Column(String)  # Format: YYYY-MM
    adaptive_learning = Column(Integer, default=0)
    llm_assessment = Column(Integer, default=0)
    synthesis = Column(Integer, default=0)
    mentor_sessions = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())