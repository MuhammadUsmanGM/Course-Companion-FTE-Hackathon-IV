'use client';

import { useState, useEffect } from 'react';
import Header from '@/components/Header';

export default function QuizPage() {
  const [quizzes, setQuizzes] = useState([]);
  const [currentQuiz, setCurrentQuiz] = useState(null);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from the backend
    // For now, we'll simulate with sample data
    const sampleQuizzes = [
      {
        id: "quiz-python-basics",
        title: "Python Basics Quiz",
        description: "Test your knowledge of Python fundamentals",
        course_id: "course-python-intro",
        course_title: "Introduction to Modern Python",
        questions: [
          {
            id: "q1",
            question: "What is the correct way to declare a variable in Python?",
            options: ["int x = 5", "var x = 5", "x = 5", "declare x = 5"],
            correct_answer: "x = 5"
          },
          {
            id: "q2",
            question: "Which of these is a valid Python function declaration?",
            options: ["function my_func():", "def my_func():", "func my_func():", "void my_func():"],
            correct_answer: "def my_func():"
          }
        ],
        passing_score: 0.7
      }
    ];

    setQuizzes(sampleQuizzes);
    setLoading(false);
  }, []);

  const startQuiz = (quiz: any) => {
    setCurrentQuiz(quiz);
    setAnswers({});
    setSubmitted(false);
    setResult(null);
  };

  const handleAnswerChange = (questionId: string, answer: string) => {
    setAnswers({
      ...answers,
      [questionId]: answer
    });
  };

  const handleSubmitQuiz = async () => {
    if (!currentQuiz) return;

    // Prepare submission data
    const submission = {
      user_id: 'user-1',
      quiz_id: currentQuiz.id,
      answers
    };

    try {
      // In a real app, we would submit to the backend
      // For simulation, calculate score manually
      let correctAnswers = 0;
      currentQuiz.questions.forEach((question: any) => {
        if (answers[question.id] === question.correct_answer) {
          correctAnswers++;
        }
      });

      const score = correctAnswers / currentQuiz.questions.length;
      const passed = score >= currentQuiz.passing_score;

      setResult({
        score,
        passed,
        feedback: passed ? "Great job! You passed the quiz." : "Keep studying, you'll get it next time!",
        correctAnswers,
        totalQuestions: currentQuiz.questions.length
      });

      setSubmitted(true);
    } catch (error) {
      console.error('Error submitting quiz:', error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-emerald-600 dark:border-emerald-400"></div>
          <p className="mt-4 text-emerald-700 dark:text-emerald-300">Loading quizzes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-emerald-50 to-teal-100 dark:from-emerald-900 dark:to-teal-900">
      <Header />

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {!currentQuiz ? (
          <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6">
            <h1 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100 mb-6">Available Quizzes</h1>

            <div className="space-y-4">
              {quizzes.map((quiz: any) => (
                <div key={quiz.id} className="border border-emerald-200 dark:border-emerald-700 rounded-lg p-4 hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition">
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-medium text-emerald-900 dark:text-emerald-100">{quiz.title}</h3>
                      <p className="text-sm text-emerald-600 dark:text-emerald-300 mt-1">{quiz.description}</p>
                      <p className="text-sm text-emerald-600 dark:text-emerald-300 mt-1">
                        From: {quiz.course_title}
                      </p>
                    </div>
                    <button
                      className="bg-emerald-600 text-white px-4 py-2 rounded-lg text-sm hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800"
                      onClick={() => startQuiz(quiz)}
                    >
                      Start Quiz
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ) : submitted && result ? (
          <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6">
            <h1 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100 mb-6">Quiz Result</h1>

            <div className="text-center mb-8">
              <div className={`text-6xl font-bold mb-4 ${result.passed ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'}`}>
                {Math.round(result.score * 100)}%
              </div>
              <h2 className={`text-2xl font-semibold mb-2 ${result.passed ? 'text-emerald-700 dark:text-emerald-300' : 'text-red-700 dark:text-red-300'}`}>
                {result.passed ? 'Congratulations! You Passed!' : 'Keep Studying!'}
              </h2>
              <p className="text-emerald-600 dark:text-emerald-300 mb-4">{result.feedback}</p>
              <p className="text-emerald-600 dark:text-emerald-300">
                You got {result.correctAnswers} out of {result.totalQuestions} questions correct.
              </p>
            </div>

            <div className="flex justify-center gap-4">
              <button
                className="bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800"
                onClick={() => {
                  setCurrentQuiz(null);
                  setResult(null);
                }}
              >
                Back to Quizzes
              </button>
              <button
                className="border border-emerald-300 dark:border-emerald-600 text-emerald-700 dark:text-emerald-200 px-6 py-3 rounded-lg hover:bg-emerald-50 dark:hover:bg-emerald-700/50 transition"
                onClick={() => {
                  // Reset quiz to retake
                  setAnswers({});
                  setSubmitted(false);
                  setResult(null);
                }}
              >
                Retake Quiz
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-white dark:bg-emerald-800 rounded-xl shadow-lg p-6">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold text-emerald-800 dark:text-emerald-100">{currentQuiz.title}</h1>
              <button
                className="text-emerald-500 dark:text-emerald-300 hover:text-emerald-700 dark:hover:text-emerald-100"
                onClick={() => {
                  setCurrentQuiz(null);
                  setAnswers({});
                  setSubmitted(false);
                  setResult(null);
                }}
              >
                Back to Quizzes
              </button>
            </div>

            <p className="text-emerald-600 dark:text-emerald-300 mb-6">{currentQuiz.description}</p>

            <div className="space-y-8">
              {currentQuiz.questions.map((question: any, index: number) => (
                <div key={question.id} className="border-b border-emerald-100 dark:border-emerald-700 pb-6 last:border-b-0">
                  <h3 className="text-lg font-medium text-emerald-900 dark:text-emerald-100 mb-4">
                    Question {index + 1}: {question.question}
                  </h3>

                  <div className="space-y-3">
                    {question.options.map((option: string, optIndex: number) => (
                      <div key={optIndex} className="flex items-start">
                        <input
                          type="radio"
                          id={`${question.id}-${optIndex}`}
                          name={question.id}
                          value={option}
                          checked={answers[question.id] === option}
                          onChange={(e) => handleAnswerChange(question.id, e.target.value)}
                          className="mt-1 mr-3 text-emerald-600 dark:text-emerald-400 focus:ring-emerald-500"
                        />
                        <label
                          htmlFor={`${question.id}-${optIndex}`}
                          className="text-emerald-700 dark:text-emerald-200"
                        >
                          {option}
                        </label>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-8 flex justify-end">
              <button
                className="bg-emerald-600 text-white px-6 py-3 rounded-lg hover:bg-emerald-700 transition dark:bg-emerald-700 dark:hover:bg-emerald-800 disabled:opacity-50"
                onClick={handleSubmitQuiz}
                disabled={Object.keys(answers).length !== currentQuiz.questions.length}
              >
                Submit Quiz
              </button>
            </div>
          </div>
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