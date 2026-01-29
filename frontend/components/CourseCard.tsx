import Link from 'next/link';
import { Course } from '@/types/course';

interface CourseCardProps {
  course: Course;
}

export default function CourseCard({ course }: CourseCardProps) {
  return (
    <Link href={`/courses/${course.id}`} className="block">
      <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-md overflow-hidden cursor-pointer transform transition-transform hover:scale-105 hover:shadow-lg">
        <div className="p-6">
          <h3 className="text-xl font-semibold text-emerald-800 dark:text-emerald-100 mb-2">{course.title}</h3>
          <p className="text-emerald-600 dark:text-emerald-200 mb-4">{course.description}</p>
          <div className="flex justify-between items-center">
            <span className="text-sm text-emerald-500 dark:text-emerald-300">{course.chapters?.length || 0} chapters</span>
            <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800">
              Start Learning
            </button>
          </div>
        </div>
      </div>
    </Link>
  );
}