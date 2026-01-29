import requests
import json

BASE_URL = "http://localhost:8000"

def test_api_endpoints():
    print("Testing Course Companion FTE API endpoints...\n")

    # Test getting all courses
    print("1. Testing GET /courses")
    response = requests.get(f"{BASE_URL}/courses")
    courses = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Number of courses: {len(courses['courses'])}")
    if courses['courses']:
        print(f"   First course: {courses['courses'][0]['title']}")
    print()

    # Test getting a specific course
    if courses['courses']:
        course_id = courses['courses'][0]['id']
        print(f"2. Testing GET /courses/{course_id}")
        response = requests.get(f"{BASE_URL}/courses/{course_id}")
        course = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Course title: {course['title']}")
        print()

        # Test getting chapters for the course
        print(f"3. Testing GET /courses/{course_id}/chapters")
        response = requests.get(f"{BASE_URL}/courses/{course_id}/chapters")
        chapters = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Number of chapters: {len(chapters['chapters'])}")
        print()

    # Test search functionality
    print("4. Testing GET /search?query=python")
    response = requests.get(f"{BASE_URL}/search?query=python")
    search_results = response.json()
    print(f"   Status: {response.status_code}")
    print(f"   Search results: {len(search_results['results'])}")
    print()

    # Test getting a specific chapter
    if courses['courses'] and courses['courses'][0]['chapters']:
        chapter_id = courses['courses'][0]['chapters'][0]['id']
        print(f"5. Testing GET /chapters/{chapter_id}")
        response = requests.get(f"{BASE_URL}/chapters/{chapter_id}")
        chapter = response.json()
        print(f"   Status: {response.status_code}")
        print(f"   Chapter title: {chapter['title']}")
        print()

        # Test getting next chapter
        if chapter.get('next_chapter_id'):
            print(f"6. Testing GET /chapters/{chapter_id}/next")
            response = requests.get(f"{BASE_URL}/chapters/{chapter_id}/next")
            next_chapter = response.json()
            print(f"   Status: {response.status_code}")
            if 'title' in next_chapter:
                print(f"   Next chapter: {next_chapter['title']}")
            else:
                print(f"   Message: {next_chapter.get('message', 'Unknown')}")
            print()

    # Test progress tracking
    user_id = "test-user-1"
    if courses['courses']:
        course_id = courses['courses'][0]['id']
        if courses['courses'][0]['chapters']:
            chapter_id = courses['courses'][0]['chapters'][0]['id']
            print(f"7. Testing POST /progress/{user_id}/courses/{course_id}/chapters/{chapter_id}")
            response = requests.post(f"{BASE_URL}/progress/{user_id}/courses/{course_id}/chapters/{chapter_id}")
            progress_result = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Message: {progress_result.get('message', 'N/A')}")
            print()

            # Test getting user progress
            print(f"8. Testing GET /progress/{user_id}/courses/{course_id}")
            response = requests.get(f"{BASE_URL}/progress/{user_id}/courses/{course_id}")
            user_progress = response.json()
            print(f"   Status: {response.status_code}")
            print(f"   Completed chapters: {len(user_progress.get('completed_chapters', []))}")
            print(f"   Completion percentage: {user_progress.get('completion_percentage', 0)}%")
            print()

    print("API testing completed successfully!")

if __name__ == "__main__":
    test_api_endpoints()