'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function ProgressPage() {
  const [user, setUser] = useState({ id: 'user-1', name: 'Student' });
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        // Fetch all courses to display progress
        const coursesResponse = await fetch('http://localhost:8000/courses');
        const coursesData = await coursesResponse.json();

        // For each course, fetch user progress
        const coursesWithProgress = await Promise.all(
          coursesData.courses.map(async (course: any) => {
            try {
              const progressResponse = await fetch(`http://localhost:8000/progress/${user.id}/courses/${course.id}`);
              const progressData = await progressResponse.json();

              return {
                ...course,
                progress: progressData
              };
            } catch (error) {
              return {
                ...course,
                progress: {
                  completed_chapters: [],
                  quiz_scores: {},
                  completion_percentage: 0
                }
              };
            }
          })
        );

        setCourses(coursesWithProgress);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching user data:', error);
        setLoading(false);
      }
    };

    fetchUserData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-600 dark:border-emerald-400"></div>
          <p className="mt-4 text-emerald-700 dark:text-emerald-300">Loading progress...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6 mb-8">
          <h1 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100 mb-6">My Learning Progress</h1>

          <div className="mb-8">
            <h2 className="text-xl font-semibold text-emerald-700 dark:text-emerald-200 mb-4">Overall Stats</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-emerald-50 dark:bg-emerald-700/30 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-emerald-800 dark:text-emerald-100">Total Courses</h3>
                <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-200">{courses.length}</p>
              </div>
              <div className="bg-emerald-50 dark:bg-emerald-700/30 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-emerald-800 dark:text-emerald-100">Courses Completed</h3>
                <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-200">
                  {courses.filter((course: any) => course.progress.completion_percentage === 100).length}
                </p>
              </div>
              <div className="bg-emerald-50 dark:bg-emerald-700/30 p-4 rounded-lg">
                <h3 className="text-lg font-medium text-emerald-800 dark:text-emerald-100">Avg. Completion</h3>
                <p className="text-2xl font-bold text-emerald-600 dark:text-emerald-200">
                  {Math.round(courses.reduce((acc, course: any) => acc + (course.progress.completion_percentage || 0), 0) / courses.length || 0)}%
                </p>
              </div>
            </div>
          </div>

          <div>
            <h2 className="text-xl font-semibold text-emerald-700 dark:text-emerald-200 mb-4">Course Progress</h2>

            {courses.length === 0 ? (
              <p className="text-emerald-600 dark:text-emerald-300">No courses enrolled yet.</p>
            ) : (
              <div className="space-y-6">
                {courses.map((course: any) => {
                  const progress = course.progress || {
                    completed_chapters: [],
                    quiz_scores: {},
                    completion_percentage: 0
                  };

                  const completedCount = progress.completed_chapters ? progress.completed_chapters.length : 0;
                  const totalCount = course.chapters ? course.chapters.length : 0;

                  return (
                    <div key={course.id} className="border border-emerald-200 dark:border-emerald-700 rounded-lg p-4">
                      <div className="flex justify-between items-center mb-3">
                        <h3 className="font-medium text-emerald-900 dark:text-emerald-100">{course.title}</h3>
                        <span className="text-sm font-medium text-emerald-700 dark:text-emerald-200">
                          {progress.completion_percentage || 0}%
                        </span>
                      </div>

                      <div className="mb-2">
                        <div className="w-full bg-emerald-200 dark:bg-emerald-700 rounded-full h-3">
                          <div
                            className="bg-emerald-600 h-3 rounded-full dark:bg-emerald-500 transition-all duration-500"
                            style={{ width: `${progress.completion_percentage || 0}%` }}
                          ></div>
                        </div>
                      </div>

                      <p className="text-sm text-emerald-600 dark:text-emerald-300">
                        {completedCount} of {totalCount} chapters completed
                      </p>

                      <div className="flex gap-2 mt-3">
                        <button className="text-sm bg-emerald-600 text-white px-3 py-1 rounded hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800">
                          Continue
                        </button>
                        <button className="text-sm border border-emerald-300 dark:border-emerald-600 text-emerald-700 dark:text-emerald-200 px-3 py-1 rounded hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition">
                          Review
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}