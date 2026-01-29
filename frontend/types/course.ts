export interface Course {
  id: string;
  title: string;
  description: string;
  chapters?: Chapter[];
  prerequisites?: string[];
}

export interface Chapter {
  id: string;
  title: string;
  content: string;
  next_chapter_id?: string | null;
  prev_chapter_id?: string | null;
}

export interface UserProgress {
  user_id: string;
  course_id: string;
  completed_chapters: string[];
  quiz_scores: Record<string, any>;
  last_accessed: string;
  streak_days: number;
  completion_percentage?: number;
}