'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import Header from '@/components/Header';

export default function CourseDetailPage() {
  const { id } = useParams();
  const [course, setCourse] = useState(null);
  const [chapters, setChapters] = useState([]);
  const [userProgress, setUserProgress] = useState({});
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState({ id: 'user-1', name: 'Student' });

  useEffect(() => {
    const fetchCourseData = async () => {
      try {
        // Fetch course details
        const courseResponse = await fetch(`http://localhost:8000/courses/${id}`);
        const courseData = await courseResponse.json();
        setCourse(courseData);

        // Fetch course chapters
        const chaptersResponse = await fetch(`http://localhost:8000/courses/${id}/chapters`);
        const chaptersData = await chaptersResponse.json();
        setChapters(chaptersData.chapters || []);

        // Fetch user progress
        const progressResponse = await fetch(`http://localhost:8000/progress/${user.id}/courses/${id}`);
        const progressData = await progressResponse.json();
        setUserProgress(progressData);

        setLoading(false);
      } catch (error) {
        console.error('Error fetching course data:', error);
        setLoading(false);
      }
    };

    if (id) {
      fetchCourseData();
    }
  }, [id]);

  const handleChapterComplete = async (chapterId) => {
    try {
      await fetch(`http://localhost:8000/progress/${user.id}/courses/${id}/chapters/${chapterId}`, {
        method: 'POST',
      });

      // Refresh progress
      const progressResponse = await fetch(`http://localhost:8000/progress/${user.id}/courses/${id}`);
      const progressData = await progressResponse.json();
      setUserProgress(progressData);
    } catch (error) {
      console.error('Error marking chapter as complete:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-600 dark:border-emerald-400"></div>
          <p className="mt-4 text-emerald-700 dark:text-emerald-300">Loading course...</p>
        </div>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100">Course not found</h2>
          <p className="text-emerald-600 dark:text-emerald-300">The requested course could not be found.</p>
        </div>
      </div>
    );
  }

  const completedCount = userProgress.completed_chapters ? userProgress.completed_chapters.length : 0;
  const totalCount = chapters.length;
  const progressPercentage = totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6 mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold text-emerald-800 dark:text-emerald-100">{course.title}</h1>
              <p className="text-emerald-600 dark:text-emerald-200 mt-2">{course.description}</p>
            </div>
            <button
              className="mt-4 md:mt-0 bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800"
              onClick={() => window.history.back()}
            >
              Back to Courses
            </button>
          </div>

          {/* Progress Bar */}
          <div className="mb-6">
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-emerald-700 dark:text-emerald-200">Your Progress</span>
              <span className="text-sm font-medium text-emerald-700 dark:text-emerald-200">{progressPercentage}%</span>
            </div>
            <div className="w-full bg-emerald-200 dark:bg-emerald-700 rounded-full h-4">
              <div
                className="bg-emerald-600 h-4 rounded-full dark:bg-emerald-500 transition-all duration-500"
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
            <p className="text-sm text-emerald-600 dark:text-emerald-300 mt-2">
              {completedCount} of {totalCount} chapters completed
            </p>
          </div>

          {/* Prerequisites */}
          {course.prerequisites && course.prerequisites.length > 0 && (
            <div className="mb-6 p-4 bg-emerald-50 dark:bg-emerald-700/30 rounded-lg">
              <h3 className="font-medium text-emerald-800 dark:text-emerald-100 mb-2">Prerequisites</h3>
              <ul className="list-disc pl-5 text-emerald-700 dark:text-emerald-200">
                {course.prerequisites.map((prereq, index) => (
                  <li key={index}>{prereq}</li>
                ))}
              </ul>
            </div>
          )}

          <div className="mt-8">
            <h2 className="text-xl font-semibold text-emerald-800 dark:text-emerald-100 mb-4">Course Content</h2>

            <div className="space-y-4">
              {chapters.map((chapter, index) => {
                const isCompleted = userProgress.completed_chapters &&
                                  userProgress.completed_chapters.includes(chapter.id);

                return (
                  <div
                    key={chapter.id}
                    className={`border rounded-lg p-4 transition-all ${
                      isCompleted
                        ? 'border-emerald-300 dark:border-emerald-600 bg-emerald-50 dark:bg-emerald-700/30'
                        : 'border-emerald-200 dark:border-emerald-700 bg-white dark:bg-emerald-800/50'
                    }`}
                  >
                    <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                      <div className="flex items-start gap-4">
                        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                          isCompleted
                            ? 'bg-emerald-500 text-white'
                            : 'bg-emerald-100 dark:bg-emerald-700 text-emerald-800 dark:text-emerald-200'
                        }`}>
                          {isCompleted ? '✓' : index + 1}
                        </div>
                        <div>
                          <h3 className="font-medium text-emerald-900 dark:text-emerald-100">
                            Chapter {index + 1}: {chapter.title}
                          </h3>
                          <p className="text-sm text-emerald-600 dark:text-emerald-300 mt-1 line-clamp-2">
                            {chapter.content.substring(0, 100)}...
                          </p>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <button
                          className="text-sm bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800"
                          onClick={() => handleChapterComplete(chapter.id)}
                        >
                          {isCompleted ? 'Completed' : 'Mark Complete'}
                        </button>

                        <button className="text-sm border border-emerald-300 dark:border-emerald-600 text-emerald-700 dark:text-emerald-200 px-4 py-2 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition">
                          Study
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* Course Actions */}
        <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6">
          <div className="flex flex-wrap gap-4">
            <button className="bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800">
              Take Quiz
            </button>
            <button className="border border-emerald-300 dark:border-emerald-600 text-emerald-700 dark:text-emerald-200 px-6 py-3 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition">
              Search Content
            </button>
            <button className="border border-emerald-300 dark:border-emerald-600 text-emerald-700 dark:text-emerald-200 px-6 py-3 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition">
              Download Materials
            </button>
          </div>
        </div>
      </main>

      <footer className="bg-white dark:bg-emerald-900 border-t border-emerald-200 dark:border-emerald-800 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-emerald-600 dark:text-emerald-300">© 2026 Course Companion FTE. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}