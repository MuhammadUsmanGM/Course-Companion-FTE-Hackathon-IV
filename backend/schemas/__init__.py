from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class CourseBase(BaseModel):
    title: str
    description: str
    prerequisites: List[str] = []


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: str

    class Config:
        from_attributes = True


class ChapterBase(BaseModel):
    course_id: str
    title: str
    content: str
    next_chapter_id: Optional[str] = None
    prev_chapter_id: Optional[str] = None
    order: int


class ChapterCreate(ChapterBase):
    pass


class Chapter(ChapterBase):
    id: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    is_active: bool

    class Config:
        from_attributes = True


class UserProgressBase(BaseModel):
    user_id: str
    course_id: str
    completed_chapters: List[str] = []
    quiz_scores: Dict[str, Any] = {}


class UserProgressCreate(UserProgressBase):
    pass


class UserProgress(UserProgressBase):
    id: int
    last_accessed: datetime
    streak_days: int

    class Config:
        from_attributes = True


class QuizQuestion(BaseModel):
    id: str
    question: str
    options: List[str]
    correct_answer: str


class QuizBase(BaseModel):
    course_id: str
    chapter_id: str
    title: str
    questions: List[QuizQuestion]
    passing_score: float = 0.7


class QuizCreate(QuizBase):
    pass


class Quiz(QuizBase):
    id: str

    class Config:
        from_attributes = True


class QuizSubmission(BaseModel):
    user_id: str
    quiz_id: str
    answers: Dict[str, str]


class QuizResult(BaseModel):
    quiz_id: str
    score: float
    passed: bool
    feedback: str


class QuizAttemptBase(BaseModel):
    user_id: str
    quiz_id: str
    answers: Dict[str, str]
    score: float
    passed: bool


class QuizAttemptCreate(QuizAttemptBase):
    pass


class QuizAttempt(QuizAttemptBase):
    id: int
    completed_at: datetime

    class Config:
        from_attributes = True


class SubscriptionType(str, Enum):
    FREE = "free"
    PREMIUM = "premium"
    PRO = "pro"
    TEAM = "team"


class SubscriptionBase(BaseModel):
    user_id: str
    plan_type: SubscriptionType
    is_active: bool = True


class SubscriptionCreate(SubscriptionBase):
    pass


class Subscription(SubscriptionBase):
    id: int
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class HybridUsageBase(BaseModel):
    user_id: str
    month_year: str
    adaptive_learning: int = 0
    llm_assessment: int = 0
    synthesis: int = 0
    mentor_sessions: int = 0


class HybridUsageCreate(HybridUsageBase):
    pass


class HybridUsage(HybridUsageBase):
    id: int

    class Config:
        from_attributes = True


class AdaptiveLearningRequest(BaseModel):
    user_id: str
    course_id: str
    current_chapter_id: str
    quiz_performance: Dict[str, float]
    time_spent: Dict[str, int]


class AdaptiveLearningResponse(BaseModel):
    recommended_next_chapter: str
    confidence: float
    learning_style: str
    improvement_areas: List[str]
    estimated_time_to_mastery: str


class LLMAssessmentRequest(BaseModel):
    user_id: str
    quiz_id: str
    question_id: str
    user_response: str
    correct_answer: str
    question_context: str


class LLMAssessmentResponse(BaseModel):
    score: float
    feedback: str
    misconceptions_identified: List[str]
    recommended_study_topics: List[str]
    confidence_level: str


class CrossChapterSynthesisRequest(BaseModel):
    user_id: str
    course_id: str
    chapter_ids: List[str]
    learning_goals: List[str]


class CrossChapterSynthesisResponse(BaseModel):
    synthesized_concepts: List[str]
    connections_identified: List[str]
    big_picture_insights: List[str]
    practical_applications: List[str]


class MentorSessionRequest(BaseModel):
    user_id: str
    course_id: str
    chapter_id: str
    question: str
    context: str


class MentorSessionResponse(BaseModel):
    response: str
    teaching_points: List[str]
    follow_up_questions: List[str]
    related_concepts: List[str]


class SearchRequest(BaseModel):
    query: str
    limit: int = 10


class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]