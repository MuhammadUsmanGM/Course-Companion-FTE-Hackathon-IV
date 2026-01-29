'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();

  const isActive = (path: string) => {
    if (path === '/') {
      return pathname === '/';
    }
    return pathname.startsWith(path);
  };

  return (
    <header className="bg-white dark:bg-emerald-900 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center">
          <div className="flex items-center space-x-8">
            <Link href="/" className="text-2xl font-bold text-emerald-800 dark:text-emerald-100">
              Course Companion FTE
            </Link>

            <nav className="hidden md:flex space-x-6">
              <Link
                href="/"
                className={`font-medium transition-colors ${
                  isActive('/')
                    ? 'text-emerald-700 dark:text-emerald-300'
                    : 'text-emerald-600 hover:text-emerald-800 dark:text-emerald-400 dark:hover:text-emerald-200'
                }`}
              >
                Courses
              </Link>
              <Link
                href="/progress"
                className={`font-medium transition-colors ${
                  isActive('/progress')
                    ? 'text-emerald-700 dark:text-emerald-300'
                    : 'text-emerald-600 hover:text-emerald-800 dark:text-emerald-400 dark:hover:text-emerald-200'
                }`}
              >
                My Progress
              </Link>
              <Link
                href="/quiz"
                className={`font-medium transition-colors ${
                  isActive('/quiz')
                    ? 'text-emerald-700 dark:text-emerald-300'
                    : 'text-emerald-600 hover:text-emerald-800 dark:text-emerald-400 dark:hover:text-emerald-200'
                }`}
              >
                Quizzes
              </Link>
              <Link
                href="/search"
                className={`font-medium transition-colors ${
                  isActive('/search')
                    ? 'text-emerald-700 dark:text-emerald-300'
                    : 'text-emerald-600 hover:text-emerald-800 dark:text-emerald-400 dark:hover:text-emerald-200'
                }`}
              >
                Search
              </Link>
            </nav>
          </div>

          <div className="flex items-center space-x-4">
            <span className="text-emerald-700 dark:text-emerald-200 hidden sm:block">Welcome, Student</span>
            <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800">
              Sign In
            </button>
          </div>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden mt-4 flex justify-around">
          <Link
            href="/"
            className={`font-medium py-2 px-3 rounded-lg transition-colors ${
              isActive('/')
                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100'
                : 'text-emerald-600 hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-800/50'
            }`}
          >
            Courses
          </Link>
          <Link
            href="/progress"
            className={`font-medium py-2 px-3 rounded-lg transition-colors ${
              isActive('/progress')
                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100'
                : 'text-emerald-600 hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-800/50'
            }`}
          >
            Progress
          </Link>
          <Link
            href="/quiz"
            className={`font-medium py-2 px-3 rounded-lg transition-colors ${
              isActive('/quiz')
                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100'
                : 'text-emerald-600 hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-800/50'
            }`}
          >
            Quizzes
          </Link>
          <Link
            href="/search"
            className={`font-medium py-2 px-3 rounded-lg transition-colors ${
              isActive('/search')
                ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-800 dark:text-emerald-100'
                : 'text-emerald-600 hover:bg-emerald-50 dark:text-emerald-400 dark:hover:bg-emerald-800/50'
            }`}
          >
            Search
          </Link>
        </div>
      </div>
    </header>
  );
}