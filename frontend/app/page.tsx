import { useState, useEffect } from 'react';
import { Course } from '@/types/course';
import CourseCard from '@/components/CourseCard';
import Header from '@/components/Header';

export default function Home() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<Course | null>(null);
  const [user, setUser] = useState({ id: 'user-1', name: 'Student' });
  const [loading, setLoading] = useState(true);

  // Load courses from backend API
  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await fetch('http://localhost:8000/courses');
        const data = await response.json();
        setCourses(data.courses || []);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching courses:', error);
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  const handleCourseSelect = (course: Course) => {
    setSelectedCourse(course);
  };

  const handleChapterComplete = async (courseId: string, chapterId: string) => {
    try {
      await fetch(`http://localhost:8000/progress/${user.id}/courses/${courseId}/chapters/${chapterId}`, {
        method: 'POST',
      });

      // Refresh the selected course to show updated progress
      if (selectedCourse?.id === courseId) {
        setSelectedCourse({ ...selectedCourse });
      }
    } catch (error) {
      console.error('Error marking chapter as complete:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <section className="mb-12">
          <h2 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100 mb-6">Available Courses</h2>

          {loading ? (
            <div className="text-center py-10">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-600 dark:border-emerald-400"></div>
              <p className="mt-4 text-emerald-700 dark:text-emerald-300">Loading courses...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {courses.map((course) => (
                <CourseCard key={course.id} course={course} />
              ))}
            </div>
          )}
        </section>

        {selectedCourse && (
          <section className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100">{selectedCourse.title}</h2>
              <button
                className="text-emerald-500 dark:text-emerald-300 hover:text-emerald-700 dark:hover:text-emerald-100"
                onClick={() => setSelectedCourse(null)}
              >
                Close
              </button>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-medium text-emerald-700 dark:text-emerald-200 mb-4">Chapters</h3>
              <div className="space-y-4">
                {selectedCourse.chapters.map((chapter, index) => (
                  <div
                    key={chapter.id}
                    className="border border-emerald-200 dark:border-emerald-700 rounded-lg p-4 hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium text-emerald-900 dark:text-emerald-100">Chapter {index + 1}: {chapter.title}</h4>
                        <p className="text-emerald-600 dark:text-emerald-300 mt-1 line-clamp-2">{chapter.content.substring(0, 100)}...</p>
                      </div>
                      <button
                        className="bg-emerald-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800"
                        onClick={() => handleChapterComplete(selectedCourse.id, chapter.id)}
                      >
                        Mark Complete
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex space-x-4">
              <button className="bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800">
                Take Quiz
              </button>
              <button className="border border-emerald-300 dark:border-emerald-600 text-emerald-700 dark:text-emerald-200 px-6 py-3 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition">
                Search Content
              </button>
            </div>
          </section>
        )}
      </main>

      <footer className="bg-white dark:bg-emerald-900 border-t border-emerald-200 dark:border-emerald-800 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
          <p className="text-center text-emerald-600 dark:text-emerald-300">© 2026 Course Companion FTE. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}