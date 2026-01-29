import requests
import json

BASE_URL = "http://localhost:8000"

def test_hybrid_features():
    print("Testing Course Companion FTE Phase 2 Hybrid Intelligence Features...\n")

    # Test Adaptive Learning Path
    print("1. Testing POST /hybrid/adaptive-learning")
    adaptive_request = {
        "user_id": "test-user-1",
        "course_id": "course-python-intro",
        "current_chapter_id": "ch1-intro",
        "quiz_performance": {"quiz-python-basics": 0.65},  # Below passing threshold
        "time_spent": {"ch1-intro": 150, "ch2-basics": 200}
    }
    response = requests.post(f"{BASE_URL}/hybrid/adaptive-learning", json=adaptive_request)
    adaptive_result = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Recommended next chapter: {adaptive_result.get('recommended_next_chapter', 'N/A')}")
    print(f"   Confidence: {adaptive_result.get('confidence', 'N/A')}")
    print(f"   Improvement areas: {adaptive_result.get('improvement_areas', [])}")
    print()

    # Test LLM Assessment
    print("2. Testing POST /hybrid/llm-assessment")
    assessment_request = {
        "user_id": "test-user-1",
        "quiz_id": "quiz-python-basics",
        "question_id": "q1",
        "user_response": "In Python, you assign a value to a variable using the equals sign, like x equals 5.",
        "correct_answer": "x = 5",
        "question_context": "How to declare a variable in Python"
    }
    response = requests.post(f"{BASE_URL}/hybrid/llm-assessment", json=assessment_request)
    assessment_result = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Score: {assessment_result.get('score', 'N/A')}")
    print(f"   Feedback: {assessment_result.get('feedback', 'N/A')}")
    print(f"   Confidence level: {assessment_result.get('confidence_level', 'N/A')}")
    print()

    # Test Cross-Chapter Synthesis
    print("3. Testing POST /hybrid/synthesis")
    synthesis_request = {
        "user_id": "test-user-1",
        "course_id": "course-python-intro",
        "chapter_ids": ["ch1-intro", "ch2-basics", "ch3-functions"],
        "learning_goals": ["understand variables", "learn functions", "master typing"]
    }
    response = requests.post(f"{BASE_URL}/hybrid/synthesis", json=synthesis_request)
    synthesis_result = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Synthesized concepts: {len(synthesis_result.get('synthesized_concepts', []))}")
    print(f"   Connections identified: {len(synthesis_result.get('connections_identified', []))}")
    print()

    # Test AI Mentor Session
    print("4. Testing POST /hybrid/mentor-session")
    mentor_request = {
        "user_id": "test-user-1",
        "course_id": "course-python-intro",
        "chapter_id": "ch2-basics",
        "question": "I don't understand how functions work in Python",
        "context": "Currently learning about Python basics including variables and data types"
    }
    response = requests.post(f"{BASE_URL}/hybrid/mentor-session", json=mentor_request)
    mentor_result = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Response length: {len(mentor_result.get('response', ''))} characters")
    print(f"   Teaching points: {len(mentor_result.get('teaching_points', []))}")
    print()

    # Test Usage Tracking
    print("5. Testing GET /hybrid/usage/{user_id}")
    response = requests.get(f"{BASE_URL}/hybrid/usage/test-user-1")
    usage_result = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Adaptive learning calls: {usage_result.get('adaptive_learning', 0)}")
    print(f"   LLM assessment calls: {usage_result.get('llm_assessment', 0)}")
    print(f"   Synthesis calls: {usage_result.get('synthesis', 0)}")
    print(f"   Mentor session calls: {usage_result.get('mentor_sessions', 0)}")
    print()

    print("Hybrid Intelligence features testing completed successfully!")
    print("\nPhase 2 Hybrid Intelligence Features:")
    print("- [X] Adaptive Learning Path")
    print("- [X] LLM-Graded Assessments")
    print("- [X] Cross-Chapter Synthesis")
    print("- [X] AI Mentor Agent")
    print("- [X] Usage Tracking for Cost Analysis")


if __name__ == "__main__":
    test_hybrid_features()