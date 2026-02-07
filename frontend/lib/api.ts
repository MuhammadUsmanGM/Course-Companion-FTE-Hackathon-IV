// API utility functions for the Course Companion FTE frontend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

/**
 * Generic API request function
 */
export async function apiRequest(endpoint: string, options: RequestInit = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultOptions: RequestInit = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  try {
    const response = await fetch(url, {
      ...defaultOptions,
      ...options,
      headers: {
        ...defaultOptions.headers,
        ...options.headers,
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
}

/**
 * Course-related API functions
 */
export const courseApi = {
  getCourses: () => apiRequest('/api/v1/courses'),
  getCourse: (id: string) => apiRequest(`/api/v1/courses/${id}`),
  getCourseChapters: (courseId: string) => apiRequest(`/api/v1/courses/${courseId}/chapters`),
  getChapter: (chapterId: string) => apiRequest(`/api/v1/courses/chapters/${chapterId}`),
  getNextChapter: (chapterId: string) => apiRequest(`/api/v1/courses/chapters/${chapterId}/next`),
  getPrevChapter: (chapterId: string) => apiRequest(`/api/v1/courses/chapters/${chapterId}/previous`),
};

/**
 * Quiz-related API functions
 */
export const quizApi = {
  getQuiz: (quizId: string) => apiRequest(`/api/v1/quizzes/${quizId}`),
  submitQuiz: (submission: any) => apiRequest('/api/v1/quizzes/submit', {
    method: 'POST',
    body: JSON.stringify(submission),
  }),
  getUserQuizAttempts: (userId: string, quizId: string) =>
    apiRequest(`/api/v1/quizzes/attempts/${userId}/${quizId}`),
  getUserQuizzesForCourse: (userId: string, courseId: string) =>
    apiRequest(`/api/v1/quizzes/user/${userId}/course/${courseId}`),
};

/**
 * Progress-related API functions
 */
export const progressApi = {
  markChapterCompleted: (userId: string, courseId: string, chapterId: string) =>
    apiRequest(`/api/v1/progress/${userId}/courses/${courseId}/chapters/${chapterId}`, {
      method: 'POST',
    }),
  getUserProgress: (userId: string, courseId: string) =>
    apiRequest(`/api/v1/progress/${userId}/courses/${courseId}`),
  getUserCoursesProgress: (userId: string) =>
    apiRequest(`/api/v1/progress/${userId}/courses`),
  resetStreak: (userId: string) =>
    apiRequest(`/api/v1/progress/${userId}/streak/reset`, {
      method: 'PUT',
    }),
};

/**
 * Search-related API functions
 */
export const searchApi = {
  searchAll: (query: string, limit: number = 10) =>
    apiRequest(`/api/v1/search?query=${encodeURIComponent(query)}&limit=${limit}`),
  searchCourses: (query: string, limit: number = 10) =>
    apiRequest(`/api/v1/search/courses?query=${encodeURIComponent(query)}&limit=${limit}`),
  searchChapters: (query: string, limit: number = 10) =>
    apiRequest(`/api/v1/search/chapters?query=${encodeURIComponent(query)}&limit=${limit}`),
};