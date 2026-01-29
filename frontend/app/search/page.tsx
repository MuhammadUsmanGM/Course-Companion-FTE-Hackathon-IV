'use client';

import { useState } from 'react';
import Header from '@/components/Header';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/search?query=${encodeURIComponent(query)}`);
      const data = await response.json();
      setResults(data.results || []);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6 mb-8">
          <h1 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100 mb-6">Search Content</h1>

          <form onSubmit={handleSearch} className="mb-8">
            <div className="relative">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search courses, chapters, concepts..."
                className="w-full px-4 py-3 pl-12 border border-emerald-300 dark:border-emerald-600 rounded-lg focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 dark:bg-emerald-700/30 dark:text-white"
              />
              <svg
                className="absolute left-4 top-1/2 transform -translate-y-1/2 h-5 w-5 text-emerald-400 dark:text-emerald-300"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
                />
              </svg>
            </div>
          </form>

          {loading && (
            <div className="text-center py-10">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-600 dark:border-emerald-400"></div>
              <p className="mt-4 text-emerald-700 dark:text-emerald-300">Searching...</p>
            </div>
          )}

          {!loading && results.length > 0 && (
            <div>
              <h2 className="text-lg font-semibold text-emerald-700 dark:text-emerald-200 mb-4">
                Search Results ({results.length})
              </h2>
              <div className="space-y-4">
                {results.map((result: any, index: number) => (
                  <div
                    key={index}
                    className="border border-emerald-200 dark:border-emerald-700 rounded-lg p-4 hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition cursor-pointer"
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h3 className="font-medium text-emerald-900 dark:text-emerald-100">
                          {result.title}
                        </h3>
                        {result.type === 'chapter' && (
                          <p className="text-sm text-emerald-600 dark:text-emerald-300">
                            From: {result.course_title}
                          </p>
                        )}
                        <p className="text-sm text-emerald-600 dark:text-emerald-300 mt-2">
                          Relevance: {(result.relevance * 100).toFixed(0)}%
                        </p>
                      </div>
                      <button className="bg-emerald-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800">
                        View
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!loading && results.length === 0 && query && (
            <div className="text-center py-10">
              <p className="text-emerald-700 dark:text-emerald-300">No results found for "{query}"</p>
            </div>
          )}

          {!loading && !query && (
            <div className="text-center py-10">
              <p className="text-emerald-700 dark:text-emerald-300">Enter a search term to find courses and content</p>
            </div>
          )}
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